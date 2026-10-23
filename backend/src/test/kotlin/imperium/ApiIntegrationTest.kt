package imperium

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.testing.*
import kotlinx.serialization.json.*
import kotlinx.coroutines.*
import org.testcontainers.containers.PostgreSQLContainer
import java.util.UUID
import kotlin.test.*

class ApiIntegrationTest {
    companion object {
        // A supplied database must be disposable and explicitly named with a _test suffix.
        private val database: Database by lazy {
            val url = System.getenv("TEST_DATABASE_URL")
            val db = if (url != null) {
                require(url.substringBefore('?').endsWith("_test")) { "Tests require a database ending in _test" }
                Database(url, System.getenv("TEST_DATABASE_USER") ?: "postgres", System.getenv("TEST_DATABASE_PASSWORD") ?: "")
            } else {
                val postgres = PostgreSQLContainer<Nothing>("postgres:17-alpine")
                postgres.start()
                Database(postgres.jdbcUrl, postgres.username, postgres.password)
            }
            db.migrate(); db
        }
    }
    private fun runApi(block: suspend ApplicationTestBuilder.() -> Unit) = testApplication {
        application { module(database, AppConfig("http://localhost:3000", false)) }
        block()
    }
    private suspend fun HttpClient.postJson(path: String, body: String, cookie: String? = null) = post(path) {
        header(HttpHeaders.Origin,"http://localhost:3000"); contentType(ContentType.Application.Json)
        if (cookie != null) header(HttpHeaders.Cookie,cookie)
        setBody(body)
    }
    private suspend fun HttpClient.account(): String {
        val credentials = """{"email":"${UUID.randomUUID()}@example.com","password":"a strong test passphrase"}"""
        assertEquals(HttpStatusCode.Created, postJson("/api/auth/register",credentials).status)
        val login = postJson("/api/auth/login",credentials)
        assertEquals(HttpStatusCode.OK,login.status)
        val cookie = login.headers[HttpHeaders.SetCookie]!!
        assertTrue(cookie.contains("HttpOnly",ignoreCase=true))
        assertTrue(cookie.contains("SameSite=Lax",ignoreCase=true))
        return cookie.substringBefore(';')
    }
    private suspend fun HttpClient.create(cookie:String, name:String="Test soldier"): HttpResponse {
        val draft=productionFixture().copy(name=name,requestId=UUID.randomUUID().toString())
        return postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),draft),cookie)
    }
    private suspend fun HttpResponse.json() = Json.parseToJsonElement(bodyAsText()).jsonObject

    @Test fun `registration login creation and persistent sheet retrieval`() = runApi {
        val cookie=client.account()
        val response=client.create(cookie)
        assertEquals(HttpStatusCode.Created,response.status)
        val created=response.json(); val id=created.getValue("id").jsonPrimitive.content
        assertEquals("Test soldier",created.getValue("name").jsonPrimitive.content)
        assertEquals(11,created.getValue("calculated").jsonObject.getValue("maximumWounds").jsonPrimitive.int)
        assertTrue(created.getValue("inventory").jsonArray.any { it.jsonObject.getValue("name").jsonPrimitive.content=="Lasgun" })
        // A fresh HTTP request and repository connection must see the committed row.
        val fetched=client.get("/api/characters/$id") {header(HttpHeaders.Cookie,cookie)}
        assertEquals(HttpStatusCode.OK,fetched.status); assertEquals(created,fetched.json())
        val stored=database.read {it.query("SELECT count(*) FROM player_characters WHERE id=?",uuid(id)){r->r.getInt(1)}.single()}
        assertEquals(1,stored)
        val list=client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}
        assertEquals(1,Json.parseToJsonElement(list.bodyAsText()).jsonArray.size)
    }
    @Test fun `ownership blocks reads updates deletes and list leakage`() = runApi {
        val owner=client.account();val stranger=client.account()
        val id=client.create(owner).json().getValue("id").jsonPrimitive.content
        assertEquals(HttpStatusCode.NotFound,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,stranger)}.status)
        assertEquals(HttpStatusCode.NotFound,client.patch("/api/characters/$id"){
            header(HttpHeaders.Cookie,stranger);header(HttpHeaders.Origin,"http://localhost:3000")
            contentType(ContentType.Application.Json);setBody("""{"name":"stolen"}""")
        }.status)
        assertEquals(HttpStatusCode.NotFound,client.delete("/api/characters/$id"){
            header(HttpHeaders.Cookie,stranger);header(HttpHeaders.Origin,"http://localhost:3000")
        }.status)
        val list=client.get("/api/characters"){header(HttpHeaders.Cookie,stranger)}
        assertEquals(0,Json.parseToJsonElement(list.bodyAsText()).jsonArray.size)
        assertEquals(HttpStatusCode.OK,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,owner)}.status)
    }
    @Test fun `seed species classes and weapons are available to authenticated users`() = runApi {
        val cookie=client.account()
        for ((path,name) in mapOf("species" to "Human","classes" to "Guardsman","weapons" to "Lasgun")) {
            val response=client.get("/api/$path"){header(HttpHeaders.Cookie,cookie)}
            assertEquals(HttpStatusCode.OK,response.status)
            assertEquals(name,Json.parseToJsonElement(response.bodyAsText()).jsonArray[0].jsonObject.getValue("name").jsonPrimitive.content)
        }
    }
    @Test fun `logout revokes cookie and unauthenticated requests fail`() = runApi {
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/characters").status)
        val cookie=client.account()
        assertEquals(HttpStatusCode.NoContent,client.postJson("/api/auth/logout","{}",cookie).status)
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/auth/me"){header(HttpHeaders.Cookie,cookie)}.status)
    }
    @Test fun `invalid credentials input and origin return structured errors`() = runApi {
        val invalid=client.postJson("/api/auth/register","""{"email":"bad","password":"short"}""")
        assertEquals(HttpStatusCode.BadRequest,invalid.status);assertTrue(invalid.json().containsKey("error"))
        assertEquals(HttpStatusCode.Unauthorized,client.postJson("/api/auth/login","""{"email":"absent@example.com","password":"not a valid password"}""").status)
        assertEquals(HttpStatusCode.Forbidden,client.post("/api/auth/register"){header(HttpHeaders.Origin,"https://evil.example")}.status)
        assertEquals(HttpStatusCode.Forbidden,client.post("/api/auth/logout").status)
        assertEquals(HttpStatusCode.BadRequest,client.postJson("/api/auth/login","{").status)
    }
    @Test fun `invalid content never creates a partial character`() = runApi {
        val cookie=client.account()
        val response=client.postJson("/api/characters","""{"name":"Invalid","speciesId":"10000000-0000-0000-0000-000000000001","classId":"20000000-0000-0000-0000-000000000001","weaponId":"${UUID.randomUUID()}"}""",cookie)
        assertEquals(HttpStatusCode.BadRequest,response.status)
        assertEquals("[]",client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}.bodyAsText())
        assertEquals(HttpStatusCode.UnprocessableEntity,client.create(cookie," ").status)
    }
    @Test fun `owner can rename and delete and equipment is removed`() = runApi {
        val cookie=client.account();val id=client.create(cookie).json().getValue("id").jsonPrimitive.content
        val renamed=client.patch("/api/characters/$id"){
            header(HttpHeaders.Cookie,cookie);header(HttpHeaders.Origin,"http://localhost:3000")
            contentType(ContentType.Application.Json);setBody("""{"name":"Renamed soldier"}""")
        }
        assertEquals(HttpStatusCode.OK,renamed.status);assertEquals("Renamed soldier",renamed.json().getValue("name").jsonPrimitive.content)
        assertEquals(HttpStatusCode.NoContent,client.delete("/api/characters/$id"){
            header(HttpHeaders.Cookie,cookie);header(HttpHeaders.Origin,"http://localhost:3000")
        }.status)
        assertEquals(HttpStatusCode.NotFound,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.status)
        assertEquals(0,database.read{it.query("SELECT count(*) FROM player_character_inventory WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single()})
    }
    @Test fun `validation is structured authenticated and has no persistence side effects`() = runApi {
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/character-builder/profile").status)
        val cookie=client.account()
        val profile=client.get("/api/character-builder/profile"){header(HttpHeaders.Cookie,cookie)}.json()
        assertEquals("di-phb-1.0-tier1-v6",profile.text("id"))
        assertEquals(listOf(JsonPrimitive(1)),profile.arr("levels").toList())
        assertFalse(profile.containsKey("records"))
        val invalid=productionFixture().copy(speciesId="di.species.ogryn",answers=emptyMap())
        val body=Json.encodeToString(NarrowDraft.serializer(),invalid)
        val validation=client.postJson("/api/characters/validate",body,cookie).json()
        assertEquals("INVALID",validation.text("status"))
        assertTrue(validation.objects("errors").any { it.text("code")=="CONTENT_NOT_SUPPORTED" && it.text("field")=="speciesId" })
        assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters",body,cookie).status)
        val forged=JsonObject(Json.encodeToJsonElement(NarrowDraft.serializer(),productionFixture()).jsonObject+mapOf("ownerId" to JsonPrimitive(UUID.randomUUID().toString())))
        assertEquals(HttpStatusCode.BadRequest,client.postJson("/api/characters",forged.toString(),cookie).status)
        assertEquals("[]",client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}.bodyAsText())
    }
    @Test fun `creation retries are owner scoped and cannot duplicate inventory`() = runApi {
        val cookie=client.account();val body=Json.encodeToString(NarrowDraft.serializer(),productionFixture().copy(requestId=UUID.randomUUID().toString()))
        val first=client.postJson("/api/characters",body,cookie).json()
        val second=client.postJson("/api/characters",body,cookie).json()
        assertEquals(first,second)
        val id=uuid(first.text("id"))
        assertEquals(6,database.read { it.query("SELECT count(*) FROM player_character_inventory WHERE character_id=?",id){r->r.getInt(1)}.single() })
        val changed=JsonObject(Json.parseToJsonElement(body).jsonObject+mapOf("name" to JsonPrimitive("Different draft")))
        assertEquals(HttpStatusCode.Conflict,client.postJson("/api/characters",changed.toString(),cookie).status)
        val stranger=client.account()
        assertNotEquals(first.text("id"),client.postJson("/api/characters",body,stranger).json().text("id"))
    }
    @Test fun `failed child insert rolls back character choices and inventory`() = runApi {
        val cookie=client.account();val draft=productionFixture().copy(requestId=UUID.randomUUID().toString())
        // A test-only trigger fails the final insert after character, choices and kit were written.
        database.transaction { con ->
            con.execute("CREATE OR REPLACE FUNCTION test_fail_runtime() RETURNS trigger LANGUAGE plpgsql AS 'BEGIN RAISE EXCEPTION ''forced rollback verification''; END'")
            con.execute("CREATE TRIGGER test_fail_runtime BEFORE INSERT ON player_character_runtime FOR EACH ROW EXECUTE FUNCTION test_fail_runtime()")
        }
        try {
            assertEquals(HttpStatusCode.InternalServerError,client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),draft),cookie).status)
            assertEquals(0,database.read { it.query("SELECT count(*) FROM player_characters WHERE request_id=?",uuid(draft.requestId)){r->r.getInt(1)}.single() })
            assertEquals("[]",client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}.bodyAsText())
        } finally {
            database.transaction { it.execute("DROP TRIGGER test_fail_runtime ON player_character_runtime");it.execute("DROP FUNCTION test_fail_runtime()") }
        }
        assertEquals(HttpStatusCode.Created,client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),draft),cookie).status)
    }
    @Test fun `saved ruleset snapshot remains locked when a new release is registered`() = runApi {
        val cookie=client.account();val saved=client.create(cookie).json()
        val rules=NarrowRules.bundled()
        val spec=JsonObject(rules.spec+mapOf("id" to JsonPrimitive("test-release-${UUID.randomUUID()}")))
        val payload=JsonObject(rules.payload+mapOf("spec" to spec))
        ProductionCharacters(database,NarrowRules(obj("digest" to sha(canonicalJson(payload)),"payload" to payload)))
        val fetched=client.get("/api/characters/${saved.text("id")}"){header(HttpHeaders.Cookie,cookie)}.json()
        assertEquals(saved,fetched);assertEquals(rules.digest,fetched.text("rulesetDigest"))
        val altered=JsonObject(rules.payload+mapOf("testChange" to JsonPrimitive(true)))
        assertFailsWith<IllegalStateException> { ProductionCharacters(database,NarrowRules(obj("digest" to sha(canonicalJson(altered)),"payload" to altered))) }
    }

    @Test fun `sheet retrieval never resets HP or consumes inventory`() = runApi {
        val cookie=client.account();val saved=client.create(cookie).json();val id=uuid(saved.text("id"))
        database.transaction { con ->
            con.execute("UPDATE player_character_runtime SET current_hp=4,state_version=1 WHERE character_id=?",id)
            con.execute("UPDATE player_character_inventory SET quantity=1 WHERE character_id=? AND definition_id='di.weapon.frag_grenade'",id)
        }
        repeat(2) {
            val sheet=client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json()
            assertEquals(4,sheet.getValue("runtime").jsonObject.num("currentHp"))
            assertEquals(11,sheet.getValue("calculated").jsonObject.num("maximumWounds"))
            assertEquals(1,sheet.objects("inventory").single { row->row.text("definitionId")=="di.weapon.frag_grenade" }.num("quantity"))
        }
    }


    @Test fun `tier1 saves reopens and rolls while old characters remain pinned`() = runApi {
        val cookie=client.account();val old=client.create(cookie).json()
        val draft=tier1Fixture().copy(requestId=UUID.randomUUID().toString())
        val createdResponse=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),draft),cookie)
        assertEquals(HttpStatusCode.Created,createdResponse.status)
        val created=createdResponse.json();val id=created.text("id")
        val reopened=client.get("/api/characters/$id") { header(HttpHeaders.Cookie,cookie) }.json()
        assertEquals(created,reopened);assertEquals(draft.profileDigest,reopened.text("rulesetDigest"))
        val options=client.get("/api/characters/$id/rolls/options") { header(HttpHeaders.Cookie,cookie) }.json()
        val roll=options.objects("options").first()
        val request=RollRequest(UUID.randomUUID().toString(),roll.text("id"),draft.profileId,draft.profileDigest,0)
        val rolled=client.postJson("/api/characters/$id/rolls",Json.encodeToString(RollRequest.serializer(),request),cookie)
        assertEquals(HttpStatusCode.OK,rolled.status)
        val oldAgain=client.get("/api/characters/${old.text("id")}") { header(HttpHeaders.Cookie,cookie) }.json()
        assertEquals(old,oldAgain)
        val invalid=draft.copy(requestId=UUID.randomUUID().toString(),speciesId="di.species.ogryn")
        assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),invalid),cookie).status)
    }
    @Test fun `v2 classes and doctrines persist reopen roll and retain history`() = runApi {
        val cookie=client.account()
        for(name in listOf("veteran-1","veteran-2","shock_trooper","marksman","sergeant","hive_scum-1")) {
            val draft=tier2Fixture(name).copy(requestId=UUID.randomUUID().toString())
            val response=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),draft),cookie)
            assertEquals(HttpStatusCode.Created,response.status,response.bodyAsText())
            val created=response.json();val id=created.text("id")
            val reopened=client.get("/api/characters/$id") { header(HttpHeaders.Cookie,cookie) }.json()
            assertEquals(created,reopened);assertEquals(draft.level,reopened.num("level"))
            val options=client.get("/api/characters/$id/rolls/options") { header(HttpHeaders.Cookie,cookie) }.json()
            val option=options.objects("options").first()
            val request=RollRequest(UUID.randomUUID().toString(),option.text("id"),draft.profileId,draft.profileDigest,0)
            assertEquals(HttpStatusCode.OK,client.postJson("/api/characters/$id/rolls",Json.encodeToString(RollRequest.serializer(),request),cookie).status)
            val history=client.get("/api/characters/$id/rolls") { header(HttpHeaders.Cookie,cookie) }
            assertEquals(HttpStatusCode.OK,history.status);assertTrue(history.bodyAsText().contains(draft.profileDigest))
        }
    }

    @Test fun `advancement preserves owned state and original retry response through level three`() = runApi {
        val cookie=client.account();val stranger=client.account()
        val d=tier2Fixture("veteran-1").copy(requestId=UUID.randomUUID().toString())
        val created=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=created.text("id")
        database.transaction { con ->
            con.execute("UPDATE player_character_runtime SET current_hp=4,resources=(SELECT jsonb_object_agg(key,value || jsonb_build_object('remaining',0)) FROM jsonb_each(resources)),conditions='[\"manual-condition\"]'::jsonb,temporary_effects='[\"manual-effect\"]'::jsonb WHERE character_id=?",uuid(id))
            con.execute("UPDATE player_character_inventory SET ammunition=jsonb_build_object('remaining',3) WHERE character_id=? AND definition_id='di.weapon.lasgun'",uuid(id))
            con.execute("UPDATE player_character_inventory SET quantity=0 WHERE character_id=? AND definition_id='di.weapon.frag_grenade'",uuid(id))
        }
        suspend fun sheet()=client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json()
        val before=sheet();val version=before.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long
        val request=AdvanceRequest(UUID.randomUUID().toString(),version,2)
        fun body(r:AdvanceRequest)=Json.encodeToString(AdvanceRequest.serializer(),r)
        assertEquals(HttpStatusCode.NotFound,client.postJson("/api/characters/$id/advance",body(request),stranger).status)
        assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body(request.copy(destinationLevel=3)),cookie).status)
        assertEquals(HttpStatusCode.OK,client.postJson("/api/characters/$id/advancement/preview",body(request),cookie).status)
        assertEquals(before,sheet())
        val response=client.postJson("/api/characters/$id/advance",body(request),cookie)
        assertEquals(HttpStatusCode.OK,response.status,response.bodyAsText());val result=response.json();val second=result.getValue("character").jsonObject
        assertEquals(2,second.num("level"));assertEquals(18,second.getValue("calculated").jsonObject.num("maximumWounds"))
        assertEquals(before["inventory"],second["inventory"]);assertEquals(4,second.getValue("runtime").jsonObject.num("currentHp"))
        assertEquals(before.getValue("runtime").jsonObject.filterKeys { it!="stateVersion" },second.getValue("runtime").jsonObject.filterKeys { it!="stateVersion" })
        assertEquals(result,client.postJson("/api/characters/$id/advance",body(request),cookie).json())
        assertEquals(HttpStatusCode.Conflict,client.postJson("/api/characters/$id/advance",body(request.copy(destinationLevel=3)),cookie).status)
        val third=AdvanceRequest(UUID.randomUUID().toString(),version+1,3,mapOf("di.choice.veteran.subclass" to listOf("marksman")))
        assertEquals(HttpStatusCode.Conflict,client.postJson("/api/characters/$id/advance",body(third.copy(expectedStateVersion=version)),cookie).status)
        assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body(third.copy(choices=emptyMap())),cookie).status)
        val end=client.postJson("/api/characters/$id/advance",body(third),cookie)
        assertEquals(HttpStatusCode.OK,end.status,end.bodyAsText())
        val saved=end.json().getValue("character").jsonObject
        assertEquals(3,saved.num("level"));assertEquals(25,saved.getValue("calculated").jsonObject.num("maximumWounds"));assertEquals(before["inventory"],saved["inventory"])
        assertEquals(result,client.postJson("/api/characters/$id/advance",body(request),cookie).json());assertEquals(created["rulesetDigest"],saved["rulesetDigest"])
    }

    @Test fun `concurrent advancement serializes duplicates and rejects stale competing requests`() = runApi {
        val cookie=client.account();val d=tier2Fixture("veteran-1").copy(requestId=UUID.randomUUID().toString())
        val sheet=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=uuid(sheet.text("id"))
        val owner=database.read { it.query("SELECT user_id FROM player_characters WHERE id=?",id){r->r.getObject(1,UUID::class.java)}.single() }
        val service=CharacterAdvancement(database,ProductionCharacters(database));val r=AdvanceRequest(UUID.randomUUID().toString(),sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long,2)
        val duplicates=coroutineScope { (1..2).map { async(Dispatchers.IO) { service.advance(owner,id,r) } }.awaitAll() }
        assertEquals(duplicates[0],duplicates[1])
        val next=r.copy(requestId=UUID.randomUUID().toString(),expectedStateVersion=r.expectedStateVersion+1,destinationLevel=3,choices=mapOf("di.choice.veteran.subclass" to listOf("sergeant")))
        val competing=coroutineScope { (1..2).map { async(Dispatchers.IO) { runCatching { service.advance(owner,id,next.copy(requestId=UUID.randomUUID().toString())) } } }.awaitAll() }
        assertEquals(1,competing.count { it.isSuccess });assertTrue(competing.single { it.isFailure }.exceptionOrNull() is ApiException)
        assertEquals(2,database.read { it.query("SELECT count(*) FROM character_advancements WHERE character_id=?",id){r->r.getInt(1)}.single() })
    }
    @Test fun `failed advancement final insert rolls back level choices and state`() = runApi {
        val cookie=client.account();val d=tier2Fixture("veteran-2").copy(requestId=UUID.randomUUID().toString())
        val sheet=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=sheet.text("id")
        val r=AdvanceRequest(UUID.randomUUID().toString(),sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long,3,mapOf("di.choice.veteran.subclass" to listOf("shock_trooper")))
        database.transaction { con ->
            con.execute("CREATE OR REPLACE FUNCTION test_fail_advance() RETURNS trigger LANGUAGE plpgsql AS 'BEGIN RAISE EXCEPTION ''forced advancement rollback''; END'")
            con.execute("CREATE TRIGGER test_fail_advance BEFORE INSERT ON character_advancements FOR EACH ROW EXECUTE FUNCTION test_fail_advance()")
        }
        try {
            assertEquals(HttpStatusCode.InternalServerError,client.postJson("/api/characters/$id/advance",Json.encodeToString(AdvanceRequest.serializer(),r),cookie).status)
            assertEquals(sheet,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json())
        } finally { database.transaction { con -> con.execute("DROP TRIGGER test_fail_advance ON character_advancements");con.execute("DROP FUNCTION test_fail_advance()") } }
    }

    @Test fun `level four upgrade preserves state history and retry result with authoritative new rolls`() = runApi {
        val cookie=client.account();val v4=NarrowRules.tier4();val d=tier2Fixture("marksman").copy(profileId=v4.id,profileDigest=v4.digest,requestId=UUID.randomUUID().toString())
        val created=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=created.text("id")
        database.transaction { it.execute("UPDATE player_character_runtime SET current_hp=11 WHERE character_id=?",uuid(id)) }
        suspend fun sheet()=client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json()
        val before=sheet();val owner=database.read { it.query("SELECT user_id FROM player_characters WHERE id=?",uuid(id)){r->r.getObject(1,UUID::class.java)}.single() }
        val characters=ProductionCharacters(database);val rolls=CharacterRolls(database,characters)
        val oldOptions=rolls.options(owner,uuid(id));val oldRoll=oldOptions.objects("options").first { it.text("label")=="Initiative" }
        rolls.execute(owner,uuid(id),RollRequest(UUID.randomUUID().toString(),oldRoll.text("id"),v4.id,v4.digest,0))
        val request=AdvanceRequest(UUID.randomUUID().toString(),0,4,mapOf("di.choice.veteran.level4_improvement" to listOf("plus_two_constitution")),true)
        fun body(r:AdvanceRequest)=Json.encodeToString(AdvanceRequest.serializer(),r)
        assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body(request.copy(confirmProfileUpgrade=false)),cookie).status)
        assertEquals(before,sheet())
        val response=client.postJson("/api/characters/$id/advance",body(request),cookie);assertEquals(HttpStatusCode.OK,response.status,response.bodyAsText())
        val result=response.json();val saved=sheet();assertEquals(4,saved.num("level"));assertEquals(NarrowRules.tier5().id,saved.text("rulesetProfileId"));assertEquals(36,saved.getValue("calculated").jsonObject.num("maximumWounds"));assertEquals(11,saved.getValue("runtime").jsonObject.num("currentHp"));assertEquals(before["inventory"],saved["inventory"])
        assertEquals(result,client.postJson("/api/characters/$id/advance",body(request),cookie).json())
        assertEquals(1,database.read { it.query("SELECT count(*) FROM character_profile_upgrades WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single() })
        assertEquals(v4.digest,database.read { it.query("SELECT profile_digest FROM character_rolls WHERE character_id=? ORDER BY created_at LIMIT 1",uuid(id)){r->r.getString(1)}.single() })
        val newOptions=rolls.options(owner,uuid(id));val con=newOptions.objects("options").first { it.text("label")=="constitution check" };assertEquals(2,con.num("modifier"))
        val rolled=rolls.execute(owner,uuid(id),RollRequest(UUID.randomUUID().toString(),con.text("id"),newOptions.text("profileId"),newOptions.text("profileDigest"),1));assertTrue(rolled.isNotEmpty())
        assertEquals(HttpStatusCode.Conflict,client.postJson("/api/characters/$id/advance",body(request.copy(requestId=UUID.randomUUID().toString())),cookie).status)
    }
    @Test fun `failed level four final insert rolls back upgrade choices resources and history`() = runApi {
        val cookie=client.account();val v4=NarrowRules.tier4();val d=tier2Fixture("marksman").copy(profileId=v4.id,profileDigest=v4.digest,requestId=UUID.randomUUID().toString())
        val before=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=before.text("id")
        val request=AdvanceRequest(UUID.randomUUID().toString(),0,4,mapOf("di.choice.veteran.level4_improvement" to listOf("combat_medic")),true)
        database.transaction { con -> con.execute("CREATE OR REPLACE FUNCTION test_fail_level4() RETURNS trigger LANGUAGE plpgsql AS 'BEGIN RAISE EXCEPTION ''forced rollback''; END'");con.execute("CREATE TRIGGER test_fail_level4 BEFORE INSERT ON character_advancements FOR EACH ROW EXECUTE FUNCTION test_fail_level4()") }
        try {
            assertEquals(HttpStatusCode.InternalServerError,client.postJson("/api/characters/$id/advance",Json.encodeToString(AdvanceRequest.serializer(),request),cookie).status)
            assertEquals(before,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json())
            assertEquals(0,database.read { it.query("SELECT count(*) FROM character_profile_upgrades WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single() })
        } finally {database.transaction { it.execute("DROP TRIGGER test_fail_level4 ON character_advancements");it.execute("DROP FUNCTION test_fail_level4()") }}
    }

    @Test fun `level four rejects forged profile HP and old profiles without contract`() = runApi {
        val cookie=client.account();val v4=NarrowRules.tier4()
        for(profile in listOf(NarrowRules.tier3(),v4)) {
            val d=tier2Fixture("marksman").copy(profileId=profile.id,profileDigest=profile.digest,requestId=UUID.randomUUID().toString())
            val before=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=before.text("id")
            val request=AdvanceRequest(UUID.randomUUID().toString(),0,4,mapOf("di.choice.veteran.level4_improvement" to listOf("rapid_reload")),true)
            val body=Json.encodeToJsonElement(AdvanceRequest.serializer(),request).jsonObject
            if(profile.id!=v4.id) assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body.toString(),cookie).status)
            else for(extra in listOf("profileId" to JsonPrimitive(NarrowRules.tier5().id),"calculated" to obj("maximumWounds" to 999))) assertEquals(HttpStatusCode.BadRequest,client.postJson("/api/characters/$id/advance",JsonObject(body+extra).toString(),cookie).status)
            assertEquals(before,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json())
        }
    }
    @Test fun `v4 upgrade rejects incompatible runtime resources without any write`() = runApi {
        val cookie=client.account();val r=NarrowRules.tier4();val d=tier2Fixture("marksman").copy(profileId=r.id,profileDigest=r.digest,requestId=UUID.randomUUID().toString())
        val created=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=created.text("id")
        database.transaction { it.execute("UPDATE player_character_runtime SET resources=resources || ?::jsonb WHERE character_id=?",obj("unknown" to obj("maximum" to 1,"remaining" to 1)).toString(),uuid(id)) }
        val request=AdvanceRequest(UUID.randomUUID().toString(),0,4,mapOf("di.choice.veteran.level4_improvement" to listOf("rapid_reload")),true)
        val response=client.postJson("/api/characters/$id/advance",Json.encodeToString(AdvanceRequest.serializer(),request),cookie)
        assertEquals(HttpStatusCode.UnprocessableEntity,response.status);assertTrue(response.bodyAsText().contains("UPGRADE_INCOMPATIBLE"))
        assertEquals(r.id,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json().text("rulesetProfileId"))
    }

    @Test fun `nonhuman upgrades advance every class sequentially preserving spent kit and runtime`() = runApi {
        val cookie=client.account();val rules=NarrowRules.tier6()
        val fixtures=tier6Fixtures().filter { it.level==1 && it.speciesId!="di.species.human" }.distinctBy { it.classId }
        assertEquals(8,fixtures.size)
        for(base in fixtures) {
            val old=if(base.classId=="di.class.ratling_sharpshooter")rules else NarrowRules.tier4()
            val d=base.copy(profileId=old.id,profileDigest=old.digest,requestId=UUID.randomUUID().toString())
            val created=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie);assertEquals(HttpStatusCode.Created,created.status,created.bodyAsText())
            val id=created.json().text("id")
            database.transaction { con ->
                con.execute("UPDATE player_character_runtime SET current_hp=3,conditions='[\"test-context\"]'::jsonb,temporary_effects='[{\"id\":\"retained\"}]'::jsonb WHERE character_id=?",uuid(id))
                con.execute("UPDATE player_character_inventory SET quantity=0 WHERE character_id=? AND definition_id IN ('di.weapon.frag_grenade','di.weapon.frag_bomb')",uuid(id))
                con.execute("UPDATE player_character_runtime SET resources=(SELECT coalesce(jsonb_object_agg(key,value || '{\"remaining\":0}'::jsonb),'{}'::jsonb) FROM jsonb_each(resources)) WHERE character_id=?",uuid(id))
            }
            suspend fun sheet()=client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json()
            val before=sheet();val oldRuntime=before.getValue("runtime").jsonObject
            val owner=database.read { it.query("SELECT user_id FROM player_characters WHERE id=?",uuid(id)){r->r.getObject(1,UUID::class.java)}.single() }
            database.transaction { it.execute("UPDATE player_character_runtime SET conditions='[]'::jsonb,temporary_effects='[]'::jsonb WHERE character_id=?",uuid(id)) }
            val rollService=CharacterRolls(database,ProductionCharacters(database));val ro=rollService.options(owner,uuid(id));val roll=ro.objects("options").first { it.text("label")=="Initiative" }
            rollService.execute(owner,uuid(id),RollRequest(UUID.randomUUID().toString(),roll.text("id"),old.id,old.digest,0))
            database.transaction { it.execute("UPDATE player_character_runtime SET conditions=?::jsonb,temporary_effects=?::jsonb WHERE character_id=?",oldRuntime.getValue("conditions").toString(),oldRuntime.getValue("temporaryEffects").toString(),uuid(id)) }
            for(level in 2..4) {
                val expected=tier6Fixtures().first { it.speciesId==base.speciesId && it.originId==base.originId && it.classId==base.classId && it.level==level }
                val current=sheet();val answers=Json.decodeFromJsonElement(NarrowDraft.serializer(),current.getValue("selections")).answers
                val request=AdvanceRequest(UUID.randomUUID().toString(),(level-2).toLong(),level,expected.answers.filterKeys { it !in answers },true)
                fun body(q:AdvanceRequest)=Json.encodeToString(AdvanceRequest.serializer(),q)
                if(level==2 && old.id!=rules.id) {
                    val ready=client.get("/api/characters/$id/advancement"){header(HttpHeaders.Cookie,cookie)}.json();assertTrue(ready.getValue("requiresProfileUpgrade").jsonPrimitive.boolean)
                    assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body(request.copy(confirmProfileUpgrade=false)),cookie).status)
                }
                assertEquals(HttpStatusCode.UnprocessableEntity,client.postJson("/api/characters/$id/advance",body(request.copy(destinationLevel=level+1)),cookie).status)
                val response=client.postJson("/api/characters/$id/advance",body(request),cookie);assertEquals(HttpStatusCode.OK,response.status,response.bodyAsText())
                assertEquals(response.json(),client.postJson("/api/characters/$id/advance",body(request),cookie).json())
                assertEquals(HttpStatusCode.Conflict,client.postJson("/api/characters/$id/advance",body(request.copy(requestId=UUID.randomUUID().toString())),cookie).status)
                val saved=sheet();assertEquals(rules.id,saved.text("rulesetProfileId"));assertEquals(level,saved.num("level"));assertEquals(before["inventory"],saved["inventory"])
                val runtime=saved.getValue("runtime").jsonObject;assertEquals(3,runtime.num("currentHp"));assertEquals(oldRuntime["conditions"],runtime["conditions"]);assertEquals(oldRuntime["temporaryEffects"],runtime["temporaryEffects"])
                for((key,value) in oldRuntime.getValue("resources").jsonObject)assertEquals(value,runtime.getValue("resources").jsonObject[key])
            }
            // Unknown runtime conditions remain preserved and correctly prevent baseline roll authorization.
            assertFailsWith<ApiException> { val opts=rollService.options(owner,uuid(id));rollService.execute(owner,uuid(id),RollRequest(UUID.randomUUID().toString(),opts.objects("options").first().text("id"),rules.id,rules.digest,3)) }
            database.transaction { it.execute("UPDATE player_character_runtime SET conditions='[]'::jsonb,temporary_effects='[]'::jsonb WHERE character_id=?",uuid(id)) }
            val ro4=rollService.options(owner,uuid(id));val initiative=ro4.objects("options").first { it.text("label")=="Initiative" }
            rollService.execute(owner,uuid(id),RollRequest(UUID.randomUUID().toString(),initiative.text("id"),rules.id,rules.digest,3))
            assertEquals(old.digest,database.read { it.query("SELECT profile_digest FROM character_rolls WHERE character_id=? ORDER BY created_at LIMIT 1",uuid(id)){r->r.getString(1)}.single() })
            assertEquals(if(old.id==rules.id)0 else 1,database.read { it.query("SELECT count(*) FROM character_profile_upgrades WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single() })
        }
    }
    @Test fun `nonhuman upgrade failure rolls back profile level and resources`() = runApi {
        val cookie=client.account();val r=NarrowRules.tier4();val d=nonhumanFixtures().first().copy(requestId=UUID.randomUUID().toString())
        val before=client.postJson("/api/characters",Json.encodeToString(NarrowDraft.serializer(),d),cookie).json();val id=before.text("id")
        database.transaction { con->con.execute("CREATE FUNCTION test_fail_v6() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'forced v6 rollback'; END $$");con.execute("CREATE TRIGGER test_fail_v6 BEFORE INSERT ON character_profile_upgrades FOR EACH ROW EXECUTE FUNCTION test_fail_v6()") }
        try {
            val request=AdvanceRequest(UUID.randomUUID().toString(),0,2,confirmProfileUpgrade=true)
            assertEquals(HttpStatusCode.InternalServerError,client.postJson("/api/characters/$id/advance",Json.encodeToString(AdvanceRequest.serializer(),request),cookie).status)
            assertEquals(before,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.json())
            assertEquals(0,database.read { it.query("SELECT count(*) FROM character_profile_upgrades WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single() })
        } finally {database.transaction { it.execute("DROP TRIGGER test_fail_v6 ON character_profile_upgrades");it.execute("DROP FUNCTION test_fail_v6()") }}
    }

}

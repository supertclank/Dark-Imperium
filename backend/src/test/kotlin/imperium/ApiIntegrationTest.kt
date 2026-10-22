package imperium

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.testing.*
import kotlinx.serialization.json.*
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
        assertEquals("di-phb-1.0-tier1-v2",profile.text("id"))
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

}

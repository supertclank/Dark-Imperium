package imperium

import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.server.testing.*
import kotlinx.serialization.json.*
import org.testcontainers.containers.PostgreSQLContainer
import java.util.UUID
import java.util.concurrent.CompletableFuture
import java.util.concurrent.atomic.AtomicInteger
import kotlin.test.*

class CharacterRollsTest {
    companion object {
        private val db: Database by lazy {
            val url=System.getenv("TEST_DATABASE_URL")
            val database=if(url!=null) {
                require(url.substringBefore('?').endsWith("_test"))
                Database(url,System.getenv("TEST_DATABASE_USER")?:"postgres",System.getenv("TEST_DATABASE_PASSWORD")?:"")
            } else {
                val pg=PostgreSQLContainer<Nothing>("postgres:17-alpine");pg.start();Database(pg.jdbcUrl,pg.username,pg.password)
            }
            database.migrate();database
        }
    }
    private data class Rig(val owner:UUID,val id:UUID,val characters:ProductionCharacters,val rolls:CharacterRolls) {
        fun sheet()=characters.get(owner,id)
        fun request(label:String):RollRequest {
            val options=rolls.options(owner,id)
            val roll=options.objects("options").single { it.text("label")==label }
            return RollRequest(UUID.randomUUID().toString(),roll.text("id"),options.text("profileId"),options.text("profileDigest"),options.getValue("stateVersion").jsonPrimitive.long,
                confirmConsumption=roll.getValue("consumes").jsonPrimitive.boolean)
        }
        fun execute(label:String)=rolls.execute(owner,id,request(label))
        fun quantity()=sheet().objects("inventory").single { it.text("definitionId")=="di.weapon.frag_grenade" }.num("quantity")
    }
    private fun rig(source:DieSource=DieSource { 1 }, draft:NarrowDraft=productionFixture()):Rig {
        val user=AuthService(db).register(Credentials("${UUID.randomUUID()}@example.com","roll test passphrase"))
        val characters=ProductionCharacters(db);val owner=uuid(user.id)
        val sheet=characters.create(owner,draft.copy(requestId=UUID.randomUUID().toString()))
        return Rig(owner,uuid(sheet.text("id")),characters,CharacterRolls(db,characters,DiceEngine(source)))
    }
    private fun error(code:String,block:()->Unit) { assertEquals(code,assertFailsWith<ApiException>(block=block).code) }


    @Test fun `all historical profile generations reopen without migration`() {
        val generations=listOf(
            productionFixture(),tier1Fixture(),tier2Fixture(),
            tier2Fixture("veteran-1").let { it.copy(profileId=NarrowRules.tier3().id,profileDigest=NarrowRules.tier3().digest) },
            nonhumanFixtures().first(),
            tier6Fixtures().first(),
            tier6Fixtures().first().let { it.copy(profileId=NarrowRules.tier7().id,profileDigest=NarrowRules.tier7().digest) })
        for(draft in generations){
            val r=rig(draft=draft);val result=r.execute("Initiative")
            assertEquals(draft.profileId,r.sheet().text("rulesetProfileId"))
            assertEquals(draft.profileDigest,r.sheet().text("rulesetDigest"))
            assertEquals(draft.profileDigest,result.text("rulesetDigest"))
        }
        val r=rig(draft=tier2Fixture("marksman").copy(profileId=NarrowRules.tier4().id,profileDigest=NarrowRules.tier4().digest))
        CharacterAdvancement(db,r.characters).advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,4,mapOf("di.choice.veteran.level4_improvement" to listOf("plus_two_constitution")),true))
        assertEquals(NarrowRules.tier5().id,r.sheet().text("rulesetProfileId"))
        assertEquals(NarrowRules.tier5().digest,r.execute("Initiative").text("rulesetDigest"))
    }
    @Test fun `inspector covers owned entity categories without using the global draft catalogue`() {
        val rules=NarrowRules.tier7()
        val base=tier6Fixtures().first { it.classId=="di.class.ratling_sharpshooter" && it.level==4 }
        val draft=base.copy(profileId=rules.id,profileDigest=rules.digest,answers=base.answers+mapOf("di.choice.veteran.level4_improvement" to listOf("armour_familiarity")))
        val one=rules.spec.objects("pathConfigurations").first { it.text("speciesId")==draft.speciesId && it.text("originId")==draft.originId && it.text("classId")==draft.classId && it.num("level")==1 }.strings("choices").toSet()
        val r=rig(draft=draft.copy(level=1,answers=draft.answers.filterKeys { it in one }))
        val advance=CharacterAdvancement(db,r.characters)
        for(level in 2..4){val config=rules.spec.objects("pathConfigurations").first { it.text("speciesId")==draft.speciesId && it.text("originId")==draft.originId && it.text("classId")==draft.classId && it.num("level")==level };val choices=draft.answers.filterKeys { it in config.strings("choices") && it !in r.sheet().getValue("selections").jsonObject.getValue("answers").jsonObject.keys };advance.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),(level-2).toLong(),level,choices))}
        val sheet=r.sheet();val calc=sheet.getValue("calculated").jsonObject
        val details=SheetDetails(db,r.characters)
        val keys=listOf(draft.speciesId,draft.originId,draft.classId,draft.traitId)+
            draft.inventory.map{it.definitionId}+calc.objects("features").map{it.text("id")}+
            calc.objects("proficiencies").map{it.text("id")}+calc.getValue("skills").jsonObject.keys+
            listOf(calc.getValue("subclass").jsonObject.text("id"))
        for(key in keys.distinct()) {
            val entity=details.entity(r.owner,r.id,key)
            assertEquals(key,entity.text("id"));assertEquals(rules.digest,entity.text("profileDigest"))
        }
        assertEquals("Armour Familiarity",details.entity(r.owner,r.id,"di.feature.talent.armour_familiarity").text("name"))
        assertFailsWith<ApiException>{details.entity(UUID.randomUUID(),r.id,draft.classId)}
    }
    @Test fun `fixed Knife rejects forged ability and notes remain private versioned and independent`() {
        val rules=NarrowRules.tier7()
        val draft=tier6Fixtures().first { it.classId=="di.class.ratling_sharpshooter" && it.level==1 }.copy(profileId=rules.id,profileDigest=rules.digest)
        val r=rig(DieSource { minOf(10,it) },draft)
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Knife attack").copy(ability="strength")) }
        val attack=r.execute("Knife attack")
        assertEquals("dexterity",attack.getValue("context").jsonObject.text("ability"))
        val damage=r.rolls.execute(r.owner,r.id,r.request("Knife damage").copy(parentResultId=attack.text("id")))
        assertEquals("dexterity",damage.getValue("context").jsonObject.text("ability"))
        val details=SheetDetails(db,r.characters)
        assertEquals(rules.id,details.entity(r.owner,r.id,"di.weapon.knife").text("profileId"))
        error("DETAIL_NOT_AVAILABLE") { details.entity(r.owner,r.id,"di.weapon.thunder_hammer") }
        val before=r.sheet().getValue("runtime")
        assertEquals("",details.notes(r.owner,r.id).text("text"))
        details.saveNotes(r.owner,r.id,NotesUpdate("Private session journal",0))
        assertEquals("Private session journal",details.notes(r.owner,r.id).text("text"))
        error("NOTES_CONFLICT") { details.saveNotes(r.owner,r.id,NotesUpdate("stale",0)) }
        error("NOTES_TOO_LONG") { details.saveNotes(r.owner,r.id,NotesUpdate("x".repeat(20001),1)) }
        error("NOT_FOUND") { details.notes(UUID.randomUUID(),r.id) }
        error("NOT_FOUND") { details.saveNotes(UUID.randomUUID(),r.id,NotesUpdate("intrusion",1)) }
        assertEquals(before,r.sheet().getValue("runtime"))
        assertEquals(rules.digest,r.sheet().text("rulesetDigest"))
    }
    @Test fun `v4 retains existing Human advancement and pinned original HP inventory and history`() {
        val rules=NarrowRules.tier4();val d=tier2Fixture("veteran-1").copy(profileId=rules.id,profileDigest=rules.digest)
        val r=rig(DieSource { 10 },d);val rolled=r.execute("Initiative");val before=r.sheet()
        val advance=CharacterAdvancement(db,r.characters)
        advance.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,2))
        advance.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),1,3,mapOf("di.choice.veteran.subclass" to listOf("marksman"))))
        val after=r.sheet();assertEquals(3,after.num("level"));assertEquals(before["inventory"],after["inventory"])
        assertEquals(before.getValue("runtime").jsonObject.num("currentHp"),after.getValue("runtime").jsonObject.num("currentHp"))
        assertEquals(25,after.getValue("calculated").jsonObject.num("maximumWounds"));assertEquals(rules.digest,after.text("rulesetDigest"))
        assertEquals(rolled.text("id"),r.rolls.history(r.owner,r.id).objects("items").single().text("id"))
    }
    @Test fun `new species persist reopen roll and retain pinned history`() {
        for(d in nonhumanFixtures()) {
            val r=rig(DieSource { 10 },d);val result=r.execute("Initiative")
            assertEquals(d.profileId,r.sheet().text("rulesetProfileId"))
            assertEquals(d.profileDigest,r.sheet().text("rulesetDigest"))
            assertEquals(r.sheet().getValue("calculated").jsonObject.num("initiative")+10,result.num("total"))
            assertEquals(result.text("id"),r.rolls.history(r.owner,r.id).objects("items").first().text("id"))
        }
    }
    @Test fun `Frag Bomb consumes once uses own exact half policy and leaves prone manual`() {
        val count=AtomicInteger(0);val r=rig(DieSource { if(count.getAndIncrement()==0) 2 else 1 },nonhumanFixtures().first())
        val request=r.request("Frag Bomb damage");val result=r.rolls.execute(r.owner,r.id,request)
        assertEquals(5,result.num("total"));val grenade=result.getValue("grenade").jsonObject
        assertEquals("5/2",grenade.getValue("outcomes").jsonObject.text("success"))
        assertTrue(grenade.text("application").contains("not knocked prone"))
        assertEquals(0,r.sheet().objects("inventory").single { it.text("definitionId")=="di.weapon.frag_bomb" }.num("quantity"))
        assertEquals(result,r.rolls.execute(r.owner,r.id,request));assertEquals(4,count.get())
        error("RESOURCE_EXHAUSTED") { r.execute("Frag Bomb damage") }
        assertTrue(r.sheet().getValue("runtime").jsonObject.arr("conditions").isEmpty())
    }
    @Test fun `checks skills saves and initiative use saved calculated modifiers without mutation`() {
        val r=rig(DieSource { 10 })
        for((label,total) in mapOf("strength check" to 13,"Athletics" to 15,"wisdom save" to 12,"Initiative" to 14)) {
            val result=r.execute(label);assertEquals(total,result.num("total"));assertEquals(0,result.num("stateVersionAfter"))
        }
        assertEquals(2,r.quantity());assertEquals(11,r.sheet().getValue("runtime").jsonObject.num("currentHp"))
    }
    @Test fun `weapon attack and damage derive canonical dice and mark natural outcomes`() {
        val r=rig(DieSource { it })
        for(label in listOf("Lasgun attack","Laspistol attack","Combat Blade attack")) {
            val result=r.execute(label);assertEquals(20,result.num("naturalResult"));assertTrue(result.getValue("criticalCandidate").jsonPrimitive.boolean)
        }
        for((label,total) in mapOf("Lasgun damage" to 10,"Laspistol damage" to 8,"Combat Blade damage" to 9)) assertEquals(total,r.execute(label).num("total"))
        val low=rig().execute("Lasgun attack")
        assertTrue(low.getValue("naturalOne").jsonPrimitive.boolean);assertFalse(low.getValue("criticalCandidate").jsonPrimitive.boolean)
    }
    @Test fun `finesse chooses strength or dexterity but never arbitrary substitution`() {
        val r=rig();val attack=r.request("Combat Blade attack")
        assertEquals(6,r.rolls.execute(r.owner,r.id,attack.copy(ability="strength")).num("total"))
        val option=r.rolls.options(r.owner,r.id).objects("options").single { it.text("label")=="Combat Blade attack" }
        assertEquals(4,option.getValue("modifierChoices").jsonObject.num("dexterity"))
        assertEquals(5,r.rolls.execute(r.owner,r.id,attack.copy(requestId=UUID.randomUUID().toString(),ability="dexterity")).num("total"))
        assertEquals(3,r.rolls.execute(r.owner,r.id,r.request("Combat Blade damage").copy(ability="dexterity")).num("total"))
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Combat Blade attack").copy(ability="wisdom")) }
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Lasgun attack").copy(ability="dexterity")) }
    }
    @Test fun `damage parent must match character action and ability without asserting a hit`() {
        val r=rig(DieSource { it });val attack=r.rolls.execute(r.owner,r.id,r.request("Combat Blade attack").copy(ability="dexterity"))
        val damage=r.rolls.execute(r.owner,r.id,r.request("Combat Blade damage").copy(ability="dexterity",parentResultId=attack.text("id")))
        assertEquals(8,damage.num("total"));assertEquals("NOT_APPLIED",damage.getValue("context").jsonObject.text("criticalDamage"))
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Lasgun damage").copy(parentResultId=attack.text("id"))) }
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Combat Blade damage").copy(parentResultId=attack.text("id"))) }
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("strength check").copy(parentResultId=attack.text("id"))) }
    }
    @Test fun `grenade commits once replay survives stale version and exhaustion is enforced`() {
        val r=rig(DieSource { 3 });val request=r.request("Frag Grenade damage")
        val result=r.rolls.execute(r.owner,r.id,request)
        assertEquals(9,result.num("total"));assertEquals(4,result.getValue("grenade").jsonObject.getValue("outcomes").jsonObject.num("success"))
        assertEquals(1,r.quantity());assertEquals(1,result.num("stateVersionAfter"))
        assertEquals(result,r.rolls.execute(r.owner,r.id,request));assertEquals(1,r.quantity())
        error("STATE_CONFLICT") { r.rolls.execute(r.owner,r.id,request.copy(requestId=UUID.randomUUID().toString())) }
        r.execute("Frag Grenade damage");assertEquals(0,r.quantity())
        error("RESOURCE_EXHAUSTED") { r.execute("Frag Grenade damage") }
        assertEquals(result,r.rolls.execute(r.owner,r.id,request))
        assertFalse(r.rolls.options(r.owner,r.id).objects("options").single { it.text("label")=="Frag Grenade damage" }.getValue("available").jsonPrimitive.boolean)
    }
    @Test fun `invalid IDs context and ruleset never produce history`() {
        val r=rig();val request=r.request("Frag Grenade damage")
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,request.copy(confirmConsumption=false)) }
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,request.copy(visibility="PUBLIC")) }
        error("RULESET_MISMATCH") { r.rolls.execute(r.owner,r.id,request.copy(profileDigest="stale")) }
        error("ROLL_NOT_AVAILABLE") { r.rolls.execute(r.owner,r.id,request.copy(rollId=UUID.randomUUID().toString())) }
        assertEquals(0,r.rolls.history(r.owner,r.id).objects("items").size);assertEquals(2,r.quantity())
    }
    @Test fun `idempotency conflicts are scoped to owner and include character`() {
        val r=rig();val request=r.request("strength check");r.rolls.execute(r.owner,r.id,request)
        error("IDEMPOTENCY_CONFLICT") { r.rolls.execute(r.owner,r.id,request.copy(rollId=r.request("Initiative").rollId)) }
        val other=r.characters.create(r.owner,productionFixture().copy(requestId=UUID.randomUUID().toString()))
        error("IDEMPOTENCY_CONFLICT") { r.rolls.execute(r.owner,uuid(other.text("id")),request) }
    }
    @Test fun `parallel retries consume once and only sample committed roll once`() {
        val calls=AtomicInteger();val r=rig(DieSource { calls.incrementAndGet();3 });val request=r.request("Frag Grenade damage")
        val tasks=List(2) { CompletableFuture.supplyAsync { r.rolls.execute(r.owner,r.id,request) } }
        assertEquals(tasks[0].get(),tasks[1].get());assertEquals(3,calls.get());assertEquals(1,r.quantity())
        assertEquals(1,r.rolls.history(r.owner,r.id).objects("items").size)
    }
    @Test fun `parallel distinct grenade requests with same state permit one commit`() {
        val r=rig();val request=r.request("Frag Grenade damage")
        val tasks=List(2) { CompletableFuture.supplyAsync { try { r.rolls.execute(r.owner,r.id,request.copy(requestId=UUID.randomUUID().toString()));"OK" } catch(e:ApiException) { e.code } } }
        assertEquals(setOf("OK","STATE_CONFLICT"),tasks.map { it.get() }.toSet());assertEquals(1,r.quantity())
    }
    @Test fun `roll insert failure rolls back inventory and version then same request can retry`() {
        val r=rig();val request=r.request("Frag Grenade damage")
        db.transaction { con ->
            con.execute("CREATE FUNCTION test_fail_roll() RETURNS trigger LANGUAGE plpgsql AS 'BEGIN RAISE EXCEPTION ''forced roll failure''; END'")
            con.execute("CREATE TRIGGER test_fail_roll BEFORE INSERT ON character_rolls FOR EACH ROW EXECUTE FUNCTION test_fail_roll()")
        }
        try {
            assertFails { r.rolls.execute(r.owner,r.id,request) }
            assertEquals(2,r.quantity());assertEquals(0,r.sheet().getValue("runtime").jsonObject.num("stateVersion"));assertEquals(0,r.rolls.history(r.owner,r.id).objects("items").size)
        } finally { db.transaction { it.execute("DROP TRIGGER test_fail_roll ON character_rolls");it.execute("DROP FUNCTION test_fail_roll()") } }
        r.rolls.execute(r.owner,r.id,request);assertEquals(1,r.quantity())
    }
    @Test fun `history is private bounded and stores immutable results and ruleset context`() {
        val r=rig();val first=r.execute("Lasgun attack");r.execute("Athletics");r.execute("Initiative")
        val history=r.rolls.history(r.owner,r.id,2);assertEquals(2,history.objects("items").size);assertTrue(history.getValue("hasMore").jsonPrimitive.boolean)
        error("INVALID_CONTEXT") { r.rolls.history(r.owner,r.id,51) }
        val stranger=UUID.randomUUID()
        error("CHARACTER_NOT_FOUND") { r.rolls.history(stranger,r.id) }
        error("CHARACTER_NOT_FOUND") { r.rolls.execute(stranger,r.id,r.request("Athletics")) }
        r.characters.rename(r.owner,r.id,"Changed name")
        val stored=r.rolls.history(r.owner,r.id).objects("items").single { it.text("id")==first.text("id") }
        assertEquals(first,stored);assertEquals(r.sheet().text("rulesetDigest"),stored.text("rulesetDigest"))
        assertNotEquals("Changed name",stored.text("characterName"))
    }
    @Test fun `unsupported runtime effects fail closed and unavailable weapon cannot roll`() {
        val r=rig();val request=r.request("Lasgun attack")
        db.transaction { it.execute("UPDATE player_character_inventory SET quantity=0 WHERE character_id=? AND definition_id='di.weapon.lasgun'",r.id) }
        error("ACTION_NOT_AVAILABLE") { r.rolls.execute(r.owner,r.id,request) }
        db.transaction { it.execute("UPDATE player_character_runtime SET conditions='[\"unmapped\"]'::jsonb WHERE character_id=?",r.id) }
        error("ACTION_NOT_AVAILABLE") { r.execute("Athletics") }
    }
    @Test fun `HTTP requires authentication rejects client dice and validates owner`() = testApplication {
        application { module(db,AppConfig("http://localhost:3000",false),DiceEngine { 10 }) }
        val r=rig()
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/characters/${r.id}/rolls").status)
        val credentials=Credentials("${UUID.randomUUID()}@example.com","http roll test passphrase")
        AuthService(db).register(credentials)
        val login=client.post("/api/auth/login") { header(HttpHeaders.Origin,"http://localhost:3000");contentType(ContentType.Application.Json);setBody(Json.encodeToString(Credentials.serializer(),credentials)) }
        val cookie=login.headers[HttpHeaders.SetCookie]!!.substringBefore(';')
        assertEquals(HttpStatusCode.NotFound,client.get("/api/characters/${r.id}/rolls"){header(HttpHeaders.Cookie,cookie)}.status)
        val forged=JsonObject(Json.encodeToJsonElement(RollRequest.serializer(),r.request("Athletics")).jsonObject+mapOf("modifier" to JsonPrimitive(999)))
        assertEquals(HttpStatusCode.BadRequest,client.post("/api/characters/${r.id}/rolls") { header(HttpHeaders.Cookie,cookie);header(HttpHeaders.Origin,"http://localhost:3000");contentType(ContentType.Application.Json);setBody(forged.toString()) }.status)
    }
    @Test fun `advancement keeps history immutable and old attacks cannot authorize new level damage`() {
        val r=rig(draft=tier2Fixture("veteran-1"));val old=r.execute("Lasgun attack");val history=r.rolls.history(r.owner,r.id)
        val advance=CharacterAdvancement(db,r.characters)
        advance.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,2))
        assertEquals(history,r.rolls.history(r.owner,r.id));assertEquals(1,old.getValue("context").jsonObject.num("characterLevel"))
        error("INVALID_CONTEXT") { r.rolls.execute(r.owner,r.id,r.request("Lasgun damage").copy(parentResultId=old.text("id"))) }
        val fresh=r.execute("Lasgun attack");assertEquals(2,fresh.getValue("context").jsonObject.num("characterLevel"));assertNotEquals(old["requestedRollId"],fresh["requestedRollId"])
    }
    @Test fun `old profiles scum illegal transitions and respec inputs are rejected`() {
        for(d in listOf(productionFixture(),tier2Fixture())) {
            val r=rig(draft=d);val service=CharacterAdvancement(db,r.characters)
            assertFalse(service.readiness(r.owner,r.id).getValue("available").jsonPrimitive.boolean)
            error("PATH_NOT_CERTIFIED") { service.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,2)) }
        }
        val r=rig(draft=tier2Fixture("veteran-1"));val service=CharacterAdvancement(db,r.characters)
        for(level in listOf(0,1,3,4)) error("INVALID_TRANSITION") { service.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,level)) }
        error("INVALID_ADVANCEMENT_CHOICE") { service.advance(r.owner,r.id,AdvanceRequest(UUID.randomUUID().toString(),0,2,mapOf("di.choice.veteran.subclass" to listOf("marksman")))) }
    }

}

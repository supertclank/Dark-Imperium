package imperium
import kotlinx.serialization.json.*
import java.util.UUID
import kotlin.test.*

class PsychicRuntimeTest {
 companion object {
  private val db:Database by lazy { val url=requireNotNull(System.getenv("TEST_DATABASE_URL"));require(url.substringBefore('?').endsWith("_test"));Database(url,System.getenv("TEST_DATABASE_USER")?:"postgres",System.getenv("TEST_DATABASE_PASSWORD")?:"").also{it.migrate()} }
 }
 private data class Rig(val owner:UUID,val id:UUID,val chars:ProductionCharacters,val rolls:CharacterRolls,val sessions:PhysicalRollSessions,val commands:CharacterActions) {
  fun sheet()=chars.get(owner,id)
  fun version()=sheet().getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long
  fun command(action:String,power:String?=null,empowered:String?=null,free:Boolean=false)=commands.execute(owner,id,CharacterActionRequest(UUID.randomUUID().toString(),version(),action,power,empowered,free))
  fun roll(value:Int):JsonObject {
   val o=rolls.options(owner,id);val roll=o.objects("options").single{it.text("id").startsWith("psychic:")}
   val request=RollRequest(UUID.randomUUID().toString(),roll.text("id"),o.text("profileId"),o.text("profileDigest"),version())
   val session=sessions.character(owner,id,request);val submitted=PhysicalSubmission(session.objects("groups").map{group->List(group.num("count")){value.coerceAtMost(group.num("sides"))}})
   val result=sessions.finalize(owner,uuid(session.text("rollSessionId")),submitted)
   assertEquals(result,sessions.finalize(owner,uuid(session.text("rollSessionId")),submitted));return result
  }
 }
 private fun rig(cl:String="psyker",sub:String?=null):Rig {
  val rules=tier10Rules();val chars=ProductionCharacters(db,rules);val owner=uuid(AuthService(db).register(Credentials("${UUID.randomUUID()}@example.com","psychic acceptance passphrase")).id)
  db.transaction{c->for(scope in listOf("blank_null_bound","warlock_pyromancy"))c.execute("INSERT INTO character_creation_approvals(user_id,profile_id,scope,approved_by,evidence) VALUES (?,?,?,?,?)",owner,rules.id,scope,"Test GM","Explicit test fixture approval")}
  val full=tier10Fixtures().first{it.classId=="di.class.$cl"&&it.level==5&&(sub==null||it.answers["di.choice.$cl.subclass"]?.single()==sub)}
  fun keys(l:Int)=rules.spec.objects("pathConfigurations").single{it.text("classId")==full.classId&&it.text("speciesId")==full.speciesId&&it.text("originId")==full.originId&&it.num("level")==l}.strings("choices").toSet()
  val initial=full.copy(level=1,requestId=UUID.randomUUID().toString(),answers=full.answers.filterKeys{it in keys(1)})
  val sheet=chars.create(owner,initial);val id=uuid(sheet.text("id"));val advancement=CharacterAdvancement(db,chars)
  val initialHp=sheet.getValue("runtime").jsonObject.num("currentHp")
  for(level in 2..5){val version=chars.get(owner,id).getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long;val input=AdvanceRequest(UUID.randomUUID().toString(),version,level,full.answers.filterKeys{it in keys(level)&&it !in keys(level-1)});val result=advancement.advance(owner,id,input);assertEquals(result,advancement.advance(owner,id,input))}
  assertEquals(initialHp,chars.get(owner,id).getValue("runtime").jsonObject.num("currentHp"))
  val rolls=CharacterRolls(db,chars);return Rig(owner,id,chars,rolls,PhysicalRollSessions(db,rolls,FreeRolls(db)),CharacterActions(db,chars))
 }
 @Test fun `four new classes actually advance continuously and preserve state`() {
  for(cl in listOf("zealot","arbites_enforcer","psyker","aeldari_warlock")) {
   val r=rig(cl);assertEquals(5,r.sheet().num("level"));val count=r.sheet().getValue("calculated").jsonObject.getValue("attackAction").jsonObject.num("attacksPerAttackAction");assertEquals(if(cl in listOf("zealot","arbites_enforcer"))2 else 1,count)
  }
 }
 @Test fun `physical cast pressure Perils and rests persist without duplicate effects`() {
  val r=rig();val request=CharacterActionRequest(UUID.randomUUID().toString(),r.version(),"manifest","di.power.warp_spark","overcharged_damage",true)
  val started=r.commands.execute(r.owner,r.id,request);assertEquals(started,r.commands.execute(r.owner,r.id,request))
  r.roll(15);val damage=r.roll(4);assertEquals(2,damage.getValue("dice").jsonObject.objects("groups").single().arr("dice").size)
  r.command("resolve_power");assertEquals(1,r.sheet().getValue("runtime").jsonObject.num("currentWarpPressure"))
  r.roll(1);r.roll(1);r.roll(1);assertEquals("resolve_perils",r.sheet().getValue("runtime").jsonObject.getValue("pendingAction").jsonObject.text("stage"))
  r.command("resolve_perils");assertEquals(0,r.sheet().getValue("runtime").jsonObject.num("currentWarpPressure"))
  assertEquals(0,r.sheet().getValue("runtime").jsonObject.getValue("resources").jsonObject.getValue("empowered_manifestation").jsonObject.num("remaining"))
  r.command("short_rest");assertEquals(1,r.sheet().getValue("runtime").jsonObject.getValue("resources").jsonObject.getValue("empowered_manifestation").jsonObject.num("remaining"))
  assertEquals(5,r.rolls.history(r.owner,r.id).objects("items").size)
 }
 @Test fun `Ward and Vent use authorised dice and zero floor`() {
  val r=rig("aeldari_warlock");r.command("ward");r.roll(4);assertEquals(1,r.sheet().getValue("runtime").jsonObject.num("currentWarpPressure"))
  r.command("vent");r.roll(20);r.roll(4);assertEquals(0,r.sheet().getValue("runtime").jsonObject.num("currentWarpPressure"))
  r.command("vent");r.roll(1);r.roll(1);assertEquals(0,r.sheet().getValue("runtime").jsonObject.num("currentWarpPressure"))
 }
 @Test fun `unknown power and stale state fail before spending and pending cast prevents resting`() {
  val r=rig();val before=r.sheet();assertFailsWith<ApiException>{r.command("manifest","di.power.warp_bite")};assertEquals(before,r.sheet())
  r.command("manifest","di.power.warp_spark");assertFailsWith<ApiException>{r.command("short_rest")};assertFailsWith<ApiException>{r.commands.execute(r.owner,r.id,CharacterActionRequest(UUID.randomUUID().toString(),0,"ward"))}
 }
}


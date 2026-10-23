package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
fun tier8Fixtures():List<NarrowDraft> = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier8/all-paths.json")).readText())
class Tier8RulesTest {
 private val rules=NarrowRules.tier8()
 private fun calc(d:NarrowDraft):JsonObject {val v=rules.validate(d);assertEquals(emptyList(),v.errors,d.name+" "+d.answers);return v.calculated!!}
 @Test fun `all 297 family tuples validate with correct level five attack capacity`() {
  val fixtures=tier8Fixtures();assertEquals(297,fixtures.size);assertEquals(77,fixtures.count{it.level==5})
  val extra=setOf("veteran","ogryn_skullbreaker","skitarii_veteran","kin_armsman","hernkyn_prospector","aeldari_outcast")
  for(d in fixtures){val c=calc(d);val attack=c.getValue("attackAction").jsonObject
   assertEquals(if(d.level==5 && d.classId.removePrefix("di.class.") in extra)2 else 1,attack.num("attacksPerAttackAction"))
   if(d.level==5)assertEquals(3,c.num("proficiencyBonus"))
   val eligible=attack.strings("actionIds");assertTrue(c.objects("actions").filter{it["saveDc"]!=JsonNull}.none{it.text("id") in eligible})
  }
 }
 @Test fun `level four choices retained and Constitution HP applies through five including Ogryn`() {
  for(d in tier8Fixtures().filter{it.level==5}) {
   val before=calc(d.copy(level=4));val after=calc(d)
   assertEquals(before["attributes"],after["attributes"]);assertEquals(before["advancementSelection"],after["advancementSelection"])
   val die=rules.payload.getValue("classTraining").jsonObject.getValue(d.classId).jsonObject.num("hitDie")
   val con=after.getValue("attributeModifiers").jsonObject.num("constitution")
   assertEquals(maxOf(1,die/2+1+con)+(if(d.speciesId=="di.species.ogryn")3 else 0),after.num("maximumWounds")-before.num("maximumWounds"))
  }
  val ogryn=calc(tier8Fixtures().first{it.level==5 && it.speciesId=="di.species.ogryn"});assertEquals(70,ogryn.num("maximumWounds"))
  assertEquals(9,Level4Rules.currentHp(9,70));assertEquals(7,Level4Rules.currentHp(9,7))
 }
 @Test fun `Killshot and Backstabber are manual and do not duplicate attacks or damage`() {
  for(cl in listOf("ratling_sharpshooter","hive_scum")) {
   val d=tier8Fixtures().first{it.level==5 && it.classId=="di.class.$cl"};val c=calc(d)
   assertEquals(1,c.getValue("attackAction").jsonObject.num("attacksPerAttackAction"))
   val before=calc(d.copy(level=4));assertEquals(before.objects("actions").map{it["damageExpression"]},c.objects("actions").map{it["damageExpression"]})
   assertEquals("MANUAL",c.objects("features").single{it.text("id").contains(".level_5.")}.text("classification"))
   if(cl=="ratling_sharpshooter")assertEquals(1,c.objects("resources").single{it.text("key")=="killshot"}.num("maximum"))
  }
 }
 @Test fun `all level four Talents and split ASIs persist through level five`() {
  for(base in tier8Fixtures().filter{it.level==5}.distinctBy{it.speciesId to it.classId}) {
   val policy=rules.spec.getValue("level4Advancement").jsonObject;val key=policy.text("choiceId")
   for(o in policy.objects("options")) {
    val talent=o["talentId"]?.jsonPrimitive?.content
    if(talent!=null && !Level4Rules.eligible(rules.data(talent)["requirements"] as? JsonObject,setOf(base.speciesId,base.classId,base.originId)))continue
    val d=base.copy(answers=base.answers+mapOf(key to listOf(o.text("id"))))
    assertEquals(calc(d.copy(level=4))["advancementSelection"],calc(d)["advancementSelection"])
   }
  }
 }
 @Test fun `historical v7 calculations and digest remain unchanged and level six is rejected`() {
  val old=NarrowRules.tier7();assertEquals("af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5",old.digest)
  for(d in tier8Fixtures().filter{it.level<=4}) {
   val previous=old.validate(d.copy(profileId=old.id,profileDigest=old.digest));assertEquals(emptyList(),previous.errors)
   assertFalse(previous.calculated!!.containsKey("attackAction"))
   val current=calc(d)
   for(key in listOf("attributes","maximumWounds","defence","movement","initiative","skills","features","resources"))assertEquals(previous.calculated!![key],current[key],key)
  }
  assertTrue(rules.validate(tier8Fixtures().first{it.level==5}.copy(level=6)).errors.isNotEmpty())
 }
}

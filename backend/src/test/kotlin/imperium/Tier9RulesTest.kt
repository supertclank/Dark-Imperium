package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
fun tier9Fixtures():List<NarrowDraft> = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier9/all-paths.json")).readText())
class Tier9RulesTest {
 private val rules=NarrowRules.tier9()
 @Test fun `all families and newly completed Human Scum paths validate`() {
  val all=tier9Fixtures();assertEquals(329,all.size)
  val added=all.filter{it.speciesId=="di.species.human" && it.classId=="di.class.hive_scum"};assertEquals(40,added.size)
  for(d in all)assertEquals(emptyList(),rules.validate(d).errors,d.originId+" "+d.level)
  for(d in added) {
   val c=rules.validate(d).calculated!!;assertEquals(1,c.getValue("attackAction").jsonObject.num("attacksPerAttackAction"))
   if(d.level>=3)assertEquals("di.subclass.hive_scum.gunslinger",c.getValue("subclass").jsonObject.text("id"))
   if(d.level==5){val f=c.objects("features").single{it.text("id").contains(".level_5.")};assertEquals("MANUAL",f.text("classification"));assertTrue(f.text("playerNote").contains("+3d6"))}
   assertEquals("dexterity",c.objects("actions").single{it.text("itemId")=="di.weapon.knife"}.text("attackAbilityId"))
  }
 }
 @Test fun `new Human families retain every eligible improvement at level five`() {
  val policy=rules.spec.getValue("level4Advancement").jsonObject
  for(d in tier9Fixtures().filter{it.level==5 && it.speciesId=="di.species.human" && it.classId=="di.class.hive_scum"})for(o in policy.objects("options")) {
   val talent=o["talentId"]?.jsonPrimitive?.content
   if(talent!=null && !Level4Rules.eligible(rules.data(talent)["requirements"] as? JsonObject,setOf(d.speciesId,d.classId,d.originId)))continue
   val selected=d.copy(answers=d.answers+mapOf(policy.text("choiceId") to listOf(o.text("id"))))
   val four=rules.validate(selected.copy(level=4));val five=rules.validate(selected)
   assertEquals(emptyList(),four.errors);assertEquals(emptyList(),five.errors)
   assertEquals(four.calculated!!["attributes"],five.calculated!!["attributes"]);assertEquals(four.calculated!!["advancementSelection"],five.calculated!!["advancementSelection"])
  }
 }
 @Test fun `v8 calculations preserved and unsupported combinations fail closed`() {
  val old=NarrowRules.tier8();assertEquals("ebb729c9d8953afbe5053085374279053f446551181ec7ea1e409d8c711ec4b5",old.digest)
  for(d in tier8Fixtures()) {
   val a=old.validate(d).calculated!!;val b=rules.validate(d.copy(profileId=rules.id,profileDigest=rules.digest)).calculated!!
   for(key in listOf("attributes","maximumWounds","defence","movement","initiative","skills","features","resources","attackAction"))assertEquals(a[key],b[key],key)
  }
  val d=tier9Fixtures().first{it.classId=="di.class.hive_scum" && it.speciesId=="di.species.human" && it.level==5}
  assertTrue(rules.validate(d.copy(level=6)).errors.isNotEmpty())
  for(cl in listOf("zealot","arbites_enforcer","psyker","aeldari_warlock"))assertTrue(rules.validate(d.copy(classId="di.class.$cl")).errors.isNotEmpty())
  assertTrue(rules.validate(d.copy(speciesId="di.species.ogryn")).errors.isNotEmpty())
 }
}

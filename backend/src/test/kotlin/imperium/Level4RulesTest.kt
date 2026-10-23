package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
class Level4RulesTest {
 private val rules=NarrowRules.tier5()
 private val key=rules.spec.getValue("level4Advancement").jsonObject.text("choiceId")
 private fun draft(option:String)=tier2Fixture("marksman").copy(profileId=rules.id,profileDigest=rules.digest,level=4,answers=tier2Fixture("marksman").answers+mapOf(key to listOf(option)))
 private fun calculated(option:String):JsonObject {val v=rules.validate(draft(option));assertEquals(emptyList(),v.errors);return v.calculated!!}
 @Test fun `dexterity ASI recalculates independent golden values`() {
  val c=calculated("plus_two_dexterity");assertEquals(17,c.getValue("attributes").jsonObject.num("dexterity"));assertEquals(3,c.getValue("attributeModifiers").jsonObject.num("dexterity"))
  assertEquals(32,c.num("maximumWounds"));assertEquals(15,c.num("defence"));assertEquals(5,c.num("initiative"));assertEquals(5,c.getValue("saves").jsonObject.getValue("dexterity").jsonObject.num("modifier"))
  val gun=c.objects("actions").single { it.text("itemId")=="di.weapon.lasgun" };assertEquals(5,gun.num("attackBonus"));assertEquals("1d8 + 3",gun.text("damageExpression"))
  assertEquals(13,c.objects("actions").single { it.text("itemId")=="di.weapon.frag_grenade" }.num("saveDc"))
 }
 @Test fun `Constitution and split increases use final modifier once for every level`() {
  val con=calculated("plus_two_constitution");assertEquals(15,con.getValue("attributes").jsonObject.num("constitution"));assertEquals(36,con.num("maximumWounds")) // 10+2 + 3*(6+2), not 40
  val split=calculated("split_strength_constitution");assertEquals(18,split.getValue("attributes").jsonObject.num("strength"));assertEquals(14,split.getValue("attributes").jsonObject.num("constitution"));assertEquals(36,split.num("maximumWounds"))
  assertEquals(11,Level4Rules.currentHp(11,36));assertEquals(20,Level4Rules.currentHp(25,20));assertEquals(4,Level4Rules.hp(6,4,-10));assertEquals(36,Level4Rules.hp(10,4,2))
 }
 @Test fun `Talents and exact subchoices grant persistent canonical ownership`() {
  for(o in listOf("rapid_reload","weapon_specialist_basic_firearm","cybernetic_implant_optical_implant")) {val c=calculated(o);assertEquals(32,c.num("maximumWounds"));assertTrue(c.objects("features").any { it.text("id").startsWith("di.feature.talent.") });assertEquals(o,c.getValue("advancementSelection").jsonObject.text("id"))}
  assertEquals("1d8 + 3",calculated("weapon_specialist_basic_firearm").objects("actions").single { it.text("itemId")=="di.weapon.lasgun" }.text("damageExpression"))
  assertEquals(2,calculated("combat_medic").objects("resources").single { it.text("key")=="combat_medic" }.num("maximum"))
 }
 @Test fun `ASI limits apply only to this event and reject wasted or duplicate points`() {
  val p=rules.spec.getValue("level4Advancement").jsonObject;val base=rules.attributes.associateWith { 19 }
  fun check(branch:String,attrs:List<String>,scores:Map<String,Int> = base)=Level4Rules.validate(p,obj("branch" to branch,"abilities" to attrs),scores,emptySet(),true)
  assertEquals("ASI_MAXIMUM_EXCEEDED",check("ASI_PLUS_TWO",listOf("strength")))
  assertNull(check("ASI_PLUS_TWO",listOf("strength"),base+mapOf("strength" to 18)))
  assertNull(check("ASI_SPLIT",listOf("strength","dexterity")))
  assertEquals("ASI_MAXIMUM_EXCEEDED",check("ASI_SPLIT",listOf("strength","dexterity"),base+mapOf("dexterity" to 20)))
  for(a in listOf(emptyList(),listOf("strength"),listOf("strength","strength"),listOf("strength","unknown"))) assertEquals("INVALID_ASI_SELECTION",check("ASI_SPLIT",a))
 }
 @Test fun `invalid talent repeated talent and simultaneous branches fail closed`() {
  val p=rules.spec.getValue("level4Advancement").jsonObject;val o=p.objects("options").first { it.text("id")=="rapid_reload" }
  assertEquals("TALENT_ALREADY_OWNED",Level4Rules.validate(p,o,emptyMap(),setOf(o.text("talentId")),true))
  assertEquals("TALENT_INELIGIBLE",Level4Rules.validate(p,o,emptyMap(),emptySet(),false))
  for(option in listOf("unknown","bigger_gun","weapon_specialist_unknown","cybernetic_implant_unknown","split_strength_strength")) assertTrue(rules.validate(draft(option)).errors.isNotEmpty())
  assertTrue(rules.validate(draft("rapid_reload").copy(answers=draft("rapid_reload").answers+mapOf(key to listOf("rapid_reload","plus_two_strength")))).errors.isNotEmpty())
 }
 @Test fun `only 24 existing Human Veteran families gain level four`() {
  val families=rules.spec.objects("certifiedPaths").filter { it.num("level")==4 };assertEquals(24,families.size);assertTrue(families.all { it.text("speciesId")=="di.species.human"&&it.text("classId")=="di.class.veteran" })
  for(d in nonhumanFixtures()) assertTrue(rules.validate(d.copy(profileId=rules.id,profileDigest=rules.digest,level=4)).errors.any { it.code=="PATH_NOT_CERTIFIED" })
 }
 @Test fun `all existing Human Veteran families and every published option execute`() {
  val ds=Json.decodeFromString<List<NarrowDraft>>(requireNotNull(javaClass.getResource("/tier2/all-paths.json")).readText()).filter { it.level==3 }
  assertEquals(24,ds.size)
  for(d in ds) {
   val next=d.copy(profileId=rules.id,profileDigest=rules.digest,level=4,answers=d.answers+mapOf(key to listOf("plus_two_dexterity")))
   val v=rules.validate(next);assertEquals(emptyList(),v.errors,d.name);assertEquals(32,v.calculated!!.num("maximumWounds"))
  }
  for(o in rules.spec.getValue("level4Advancement").jsonObject.objects("options")) assertEquals(emptyList(),rules.validate(draft(o.text("id"))).errors,o.text("id"))
 }

}

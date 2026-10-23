package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
fun tier6Fixtures():List<NarrowDraft> = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier6/all-paths.json")).readText())
class Tier6RulesTest {
 private val r=NarrowRules.tier6()
 private val key=r.spec.getValue("level4Advancement").jsonObject.text("choiceId")
 private fun fixture(cl:String,level:Int=4)=tier6Fixtures().first { it.classId=="di.class.$cl" && it.level==level && it.speciesId!="di.species.human" }
 private fun calc(d:NarrowDraft):JsonObject {val v=r.validate(d);assertEquals(emptyList(),v.errors,d.name+" "+d.answers);return v.calculated!!}
 @Test fun `every certified tuple closes and produces authoritative definitions`() {
  val fixtures=tier6Fixtures();assertEquals(220,fixtures.size)
  for(d in fixtures) {val c=calc(d);assertTrue(c.objects("rollDefinitions").isNotEmpty());assertEquals(d.inventory.size,c.objects("inventory").size);assertEquals(d.level>=3,c["subclass"]!=JsonNull)}
 }
 @Test fun `each eligible Talent and ASI is valid only in its selected species context`() {
  for(cl in listOf("veteran","hive_scum","ratling_sharpshooter","ogryn_skullbreaker","skitarii_veteran","kin_armsman","hernkyn_prospector","aeldari_outcast")) {
   val d=fixture(cl)
   for(o in r.spec.getValue("level4Advancement").jsonObject.objects("options")) {
    val fid=o["talentId"]?.jsonPrimitive?.content;val eligible=fid==null||Level4Rules.eligible(r.data(fid)["requirements"] as? JsonObject,setOf(d.speciesId,d.classId))
    val v=r.validate(d.copy(answers=d.answers+mapOf(key to listOf(o.text("id")))))
    if(eligible) assertEquals(emptyList(),v.errors,cl+" "+o.text("id")) else assertTrue(v.errors.any { it.code=="TALENT_INELIGIBLE" })
   }
  }
 }
 @Test fun `Ogryn floor ASI and Massive Build compose once with current Constitution`() {
  val d=fixture("ogryn_skullbreaker");val c=calc(d)
  assertEquals(16,c.getValue("attributes").jsonObject.num("constitution"));assertEquals(57,c.num("maximumWounds")) // d12 + 3, three times (7+3), then 3 HP per level
  val a=d.attributes+mapOf("dexterity" to 8,"charisma" to 14)
  val dex=calc(d.copy(attributes=a,answers=d.answers+mapOf(key to listOf("plus_two_dexterity"))))
  assertEquals(8,dex.getValue("attributes").jsonObject.num("dexterity")) // floor 6 then +2
  assertEquals(53,dex.num("maximumWounds"));assertEquals(11,Level4Rules.currentHp(11,c.num("maximumWounds")))
 }
 @Test fun `Skitarii initiative and Hernkyn movement are source calculations not baseline condition bonuses`() {
  val d=fixture("skitarii_veteran",2);val c=calc(d);val m=c.getValue("attributeModifiers").jsonObject
  assertEquals(m.num("dexterity")+m.num("intelligence")+2,c.num("initiative"))
  val h=fixture("hernkyn_prospector",3);assertEquals(30,calc(h).num("movement"))
  val a=calc(fixture("aeldari_outcast"));assertEquals(35,a.num("movement"));assertEquals(90,a.num("darkvisionFeet"))
 }
 @Test fun `all Sharpshooter package and tool training combinations remain separate and executable`() {
  val base=fixture("ratling_sharpshooter",1);val pack=r.payload.getValue("packages").jsonObject.getValue(base.classId).jsonObject.getValue("display").jsonObject
  val fields=pack.objects("choices")
  fun visit(index:Int,choices:Map<String,String>) {
   if(index<fields.size) {for(o in fields[index].objects("options"))visit(index+1,choices+mapOf(fields[index].text("id") to o.text("id")));return}
   val inv=StartingPackages.compile(r.payload.getValue("packages").jsonObject.getValue(base.classId).jsonObject.getValue("executable").jsonObject,choices.mapValues { listOf(it.value) },r.records,r.spec.strings("equipment").toSet()).inventory
   for(tool in listOf("cooks_utensils","thieves_tools")) {
    val d=base.copy(packageChoices=choices,inventory=inv,answers=base.answers+mapOf("di.choice.ratling_sharpshooter.training_tool" to listOf(tool)));val c=calc(d)
    assertTrue(c.objects("proficiencies").any { it.text("id")=="di.proficiency.tool.$tool" })
    val dex=c.getValue("attributeModifiers").jsonObject.num("dexterity")
    assertEquals((if(choices["armour"]=="di.armour.heavy_clothing")11 else 12)+dex,c.num("defence"))
    if(choices["primary"]=="di.weapon.long_las")assertEquals("1d10 + $dex",c.objects("actions").single { it.text("itemId")=="di.weapon.long_las" }.text("damageExpression"))
   }
  }
  visit(0,emptyMap())
  for(v in listOf(emptyList(),listOf("cooks_utensils","thieves_tools"),listOf("unknown"))) assertTrue(r.validate(base.copy(answers=base.answers+mapOf("di.choice.ratling_sharpshooter.training_tool" to v))).errors.isNotEmpty())
 }
 @Test fun `blocked subclass choices cannot hide behind a supported parent progression`() {
  val blocked=mapOf("ratling_sharpshooter" to "underhive_rat","skitarii_veteran" to "data_hunter","hernkyn_prospector" to "claim_staker","aeldari_outcast" to "shadow_guide","hive_scum" to "sump_ghost")
  for((cl,sub) in blocked) {val d=fixture(cl,3);assertTrue(r.validate(d.copy(answers=d.answers+mapOf("di.choice.$cl.subclass" to listOf(sub)))).errors.any { it.code=="PATH_NOT_CERTIFIED" })}
  assertFalse(r.spec.strings("classes").any { it in setOf("di.class.psyker","di.class.aeldari_warlock") })
  assertTrue(r.validate(fixture("ogryn_skullbreaker").copy(level=5)).errors.isNotEmpty())
 }
 @Test fun `Bone ead and Black Market Gremlin grant their mandatory training`() {
  val o=calc(fixture("ogryn_skullbreaker",3));assertTrue(o.getValue("saves").jsonObject.getValue("wisdom").jsonObject.getValue("proficient").jsonPrimitive.boolean)
  val d=tier6Fixtures().first { it.classId=="di.class.ratling_sharpshooter" && it.level==3 && it.answers["di.choice.ratling_sharpshooter.subclass"]==listOf("black_market_gremlin") }
  val c=calc(d);assertTrue(c.objects("proficiencies").any { it.text("id")=="di.proficiency.tool.thieves_tools" })
 }
}

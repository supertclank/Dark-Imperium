package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
fun tier10Rules()=NarrowRules(Json.parseToJsonElement(requireNotNull(NarrowRules::class.java.getResource("/tier10/candidate.json")).readText()).jsonObject)
fun tier10Fixtures():List<NarrowDraft> = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier10/all-paths.json")).readText())
class Tier10RulesTest {
 private val rules=tier10Rules()
 private val approvals=setOf("blank_null_bound","warlock_pyromancy")
 @Test fun `all twelve classes cover every level with legal complete selections`() {
  assertEquals(setOf("veteran","zealot","psyker","ogryn_skullbreaker","arbites_enforcer","hive_scum","ratling_sharpshooter","skitarii_veteran","kin_armsman","hernkyn_prospector","aeldari_outcast","aeldari_warlock"),rules.spec.strings("classes").map{it.removePrefix("di.class.")}.toSet())
  for(cl in rules.spec.strings("classes"))assertEquals((1..5).toSet(),tier10Fixtures().filter{it.classId==cl}.map{it.level}.toSet())
  for(d in tier10Fixtures())assertEquals(emptyList(),rules.validate(d,trustedApprovals=approvals).errors,"${d.classId} ${d.originId} ${d.level} ${d.answers}")
 }
 @Test fun `psychic maths and explicit Warlock weapon overrides`() {
  for(d in tier10Fixtures().filter{it.classId in setOf("di.class.psyker","di.class.aeldari_warlock")}) {
   val c=rules.validate(d,trustedApprovals=approvals).calculated!!;val p=c.getValue("psychic").jsonObject;val modifier=c.getValue("attributeModifiers").jsonObject.num("intelligence")
   assertEquals(modifier+c.num("proficiencyBonus"),p.num("attackModifier"));assertEquals(8+modifier+c.num("proficiencyBonus"),p.num("saveDc"))
   if(d.classId=="di.class.aeldari_warlock")assertEquals("intelligence",c.objects("actions").single{it.text("itemId")=="di.weapon.witchblade"}.text("attackAbilityId"))
  }
 }
 @Test fun `approval and discipline gates do not accept client substitutions`() {
  val d=tier10Fixtures().first{it.classId=="di.class.psyker"&&it.level==1&&it.answers["di.choice.psyker.subclass"]==listOf("blank_null_bound")}
  assertTrue(rules.validate(d).errors.any{it.code=="GM_APPROVAL_REQUIRED"})
  assertTrue(rules.validate(d.copy(answers=d.answers+mapOf("di.choice.psychic.minor_level_1" to listOf("warp_bite","warp_bite"))),trustedApprovals=approvals).errors.any{it.code=="DUPLICATE_POWER"})
  val w=tier10Fixtures().first{it.classId=="di.class.aeldari_warlock"&&it.level==1}
  assertTrue(rules.validate(w.copy(answers=w.answers+mapOf("di.choice.psychic.minor_level_1" to listOf("warp_bite","warp_spark"))),trustedApprovals=approvals).errors.any{it.code=="POWER_NOT_ELIGIBLE"})
  assertTrue(rules.validate(w.copy(level=6),trustedApprovals=approvals).errors.isNotEmpty())
 }
 @Test fun `pressure bounds and Perils boundary arithmetic follow approved ruling`() {
  assertEquals(0,PsychicRules.reduce(3,6));assertEquals(0,PsychicRules.reduce(1,1));assertEquals(0,PsychicRules.reduce(0,1));assertEquals(3,PsychicRules.afterPerils(7))
  assertTrue(PsychicRules.triggers(7,7));assertFalse(PsychicRules.triggers(7,8));assertFalse(PsychicRules.triggers(0,1))
  assertEquals("Warp Static",PsychicRules.severity(rules,1,1).text("name"));assertEquals("Catastrophic Perils",PsychicRules.severity(rules,20,20).text("name"))
 }
}

package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
class BuilderPresentationTest {
 private val rules=NarrowRules.tier4()
 @Test fun `server rejects incomplete duplicate extra and non array values`() {
  val d=nonhumanFixtures().first()
  for(a in listOf(emptyMap(),d.attributes-"charisma",d.attributes.mapValues { 15 },d.attributes+mapOf("strength" to 16),d.attributes+mapOf("luck" to 8))) {
   val v=rules.validate(d.copy(attributes=a));assertTrue(v.errors.any { it.field=="attributes" });assertNull(v.calculated);assertNull(v.abilityPreview)
  }
  assertEquals("VALID",rules.validate(d).status)
 }
 @Test fun `backend supplies floor breakdown for preview and review`() {
  val d=nonhumanFixtures().first();val attrs=d.attributes+mapOf("dexterity" to 8,"charisma" to 14)
  val v=rules.validate(d.copy(attributes=attrs));assertEquals(emptyList(),v.errors)
  val row=v.abilityPreview!!.getValue("breakdown").jsonObject.getValue("dexterity").jsonObject
  val adjustment=row.objects("adjustments").single();assertEquals(8,adjustment.num("before"));assertEquals(6,adjustment.num("after"));assertEquals(6,adjustment.num("minimum"))
  assertEquals(adjustment,v.calculated!!.objects("abilityAdjustments").single())
 }
 @Test fun `presentation exposes species traits origin rarity and exact doctrine features`() {
  val p=rules.profile();val human=p.objects("species").first { it.text("name")=="Human" }.getValue("presentation").jsonObject
  assertTrue(human.objects("stats").any { it.text("label")=="Size" });assertTrue(human.objects("features").isNotEmpty())
  val states=p.objects("origins").flatMap { it.getValue("presentation").jsonObject.objects("groups") }.flatMap { it.objects("items") }.mapNotNull { it["state"]?.jsonPrimitive?.content }.toSet()
  assertTrue(states.containsAll(setOf("NORMAL","RARE","LIMITED")))
  val doctrines=p.objects("choices").filter { it.text("purpose")=="subclass" }.flatMap { it.objects("options") }
  assertTrue(doctrines.size>=3)
  for(option in doctrines) for(level in option.getValue("detail").jsonObject.objects("levels")) for(f in level.objects("features")) {
   assertEquals(rules.record(f.text("id")).text("descriptionMarkdown").replace(Regex("\\s+")," ").trim(),f.text("text"))
  }
  assertEquals("2ef85cd454999670ee61f51eebcc9b23e6805d5220b518d2c5643001831c5119",rules.digest)
 }
}

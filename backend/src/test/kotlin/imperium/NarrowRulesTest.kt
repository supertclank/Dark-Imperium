package imperium

import kotlinx.serialization.json.*
import kotlin.test.*

fun productionFixture():NarrowDraft = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/production-draft.json")).readText())

class NarrowRulesTest {
    private val rules=NarrowRules.bundled()
    private fun errors(d:NarrowDraft)=rules.validate(d).errors
    @Test fun `profile exposes only runtime allowlisted selectors`() {
        val p=rules.profile()
        for((group,id) in mapOf("species" to "di.species.human","origins" to "di.background.schola_progenium","classes" to "di.class.veteran","traits" to "di.feature.universal.twitchy")) assertEquals(listOf(id),p.objects(group).map { it.text("id") })
        assertFalse(p.containsKey("records"));assertFalse(p.objects("equipment").any { it.text("name")=="Auspex" })
    }
    @Test fun `golden calculated mechanics match independent Python fixture`() {
        val result=rules.validate(productionFixture());assertEquals(emptyList(),result.errors)
        val actual=result.calculated!!;val golden=Json.parseToJsonElement(requireNotNull(javaClass.getResource("/golden-mechanics.json")).readText()).jsonObject
        for(key in listOf("attributes","attributeModifiers","proficiencyBonus","maximumWounds","defence","initiative","saves")) assertEquals(golden.getValue(key),actual.getValue(key),key)
        assertEquals(30,actual.num("movement"))
        for((id,value) in golden.getValue("skills").jsonObject) assertEquals(value.jsonObject.num("modifier"),actual.getValue("skills").jsonObject.getValue(id).jsonObject.num("modifier"))
        assertEquals(setOf("Lasgun","Laspistol","Combat Blade","Frag Grenade"),actual.objects("actions").map { it.text("name") }.toSet())
        val grenade=actual.objects("actions").single { it.text("name")=="Frag Grenade" }
        assertEquals("3d6",grenade.text("damageExpression"));assertEquals(12,grenade.num("saveDc"))
        assertEquals(2,actual.objects("inventory").single { it.text("name")=="Frag Grenade" }.num("quantity"))
    }
    @Test fun `unsupported selectors and eligibility cannot be forged`() {
        val d=productionFixture()
        for(bad in listOf(d.copy(speciesId="di.species.ogryn"),d.copy(originId="di.background.hiveborn"),d.copy(classId="di.class.psyker"),d.copy(traitId="di.feature.universal.jaded"),d.copy(level=2))) assertTrue(errors(bad).any { it.code=="CONTENT_NOT_SUPPORTED" })
        assertTrue(errors(d.copy(speciesId="di.species.ogryn")).any { it.code=="INVALID_ELIGIBILITY" })
    }
    @Test fun `standard array and canonical species bonuses are validated`() {
        val d=productionFixture();assertTrue(errors(d.copy(attributes=d.attributes+mapOf("strength" to 20))).any { it.code=="INVALID_ABILITY_ALLOCATION" })
        val key="di.choice.human.ability_scores"
        val alternate=d.copy(answers=d.answers+mapOf(key to listOf("dexterity_constitution")))
        val output=rules.validate(alternate).calculated!!
        assertEquals(16,output.getValue("attributes").jsonObject.num("dexterity"));assertEquals(14,output.getValue("attributes").jsonObject.num("constitution"));assertEquals(12,output.num("maximumWounds"))
        assertTrue(errors(d.copy(answers=d.answers+mapOf(key to listOf("illegal")))).isNotEmpty())
    }
    @Test fun `required skill proficiency and broad training choices validated`() {
        val d=productionFixture()
        for(key in d.answers.keys) assertTrue(errors(d.copy(answers=d.answers-key)).any { it.code=="MISSING_CHOICE" })
        val key="di.choice.veteran.starting_skills"
        assertTrue(errors(d.copy(answers=d.answers+mapOf(key to listOf("athletics","athletics")))).any { it.code=="INVALID_SKILL_SELECTION" })
        assertTrue(errors(d.copy(answers=d.answers+mapOf("di.choice.unapproved" to listOf("yes")))).any { it.code=="CONTENT_NOT_SUPPORTED" })
    }
    @Test fun `exact starting equipment quantities armour and profile required`() {
        val d=productionFixture()
        assertTrue(errors(d.copy(packageChoices=d.packageChoices+mapOf("utility" to "di.equipment.auspex"))).any { it.code=="INVALID_EQUIPMENT_SELECTION" })
        assertTrue(errors(d.copy(inventory=d.inventory.map { it.copy(quantity=1) })).any { it.code=="INVALID_QUANTITY" })
        assertTrue(errors(d.copy(inventory=d.inventory+d.inventory[0])).any { it.code=="INVALID_EQUIPMENT_SELECTION" })
        assertTrue(errors(d.copy(inventory=d.inventory.map { it.copy(equipped=false) })).any { it.code=="INVALID_EQUIPMENT_SELECTION" })
        assertTrue(errors(d.copy(profileId="latest")).any { it.code=="RULESET_MISMATCH" })
        assertTrue(errors(d.copy(profileDigest="stale")).any { it.code=="STALE_PROFILE" })
    }
    @Test fun `tampered content cannot retain profile digest`() {
        val bundle=JsonObject(rules.bundle+mapOf("digest" to JsonPrimitive("0".repeat(64))))
        assertFailsWith<IllegalArgumentException> { NarrowRules(bundle) }
    }
    @Test fun `calculation has no state side effects and rolls carry no authority`() {
        val d=productionFixture();val first=rules.validate(d).calculated!!;assertEquals(first,rules.validate(d).calculated)
        assertEquals("DISPLAY_ONLY_NOT_AUTHORIZATION",first.text("rollAuthority"));assertEquals(2,d.inventory.single { it.definitionId=="di.weapon.frag_grenade" }.quantity)
        assertTrue(first.objects("rollDefinitions").all { it.getValue("snapshot").jsonObject.text("rulesetLockDigest")==rules.digest })
    }
    @Test fun `ability preview works before later skill choices are completed`() {
        val d=productionFixture()
        val preview=rules.validate(d.copy(answers=d.answers.filterKeys { it=="di.choice.human.ability_scores" }))
        assertEquals("INVALID",preview.status)
        assertEquals(17,preview.abilityPreview!!.getValue("scores").jsonObject.num("strength"))
        assertNull(preview.calculated)
    }

}

package imperium

import kotlinx.serialization.json.*
import kotlin.test.*

fun tier1Fixture():NarrowDraft=Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier1-draft.json")).readText())

class Tier1RulesTest {
    private val rules=NarrowRules.tier1()
    @Test fun `new Hiveborn golden projection inventory actions and baseline rolls`() {
        val result=rules.validate(tier1Fixture());assertEquals(emptyList(),result.errors)
        val actual=result.calculated!!
        val golden=Json.parseToJsonElement(requireNotNull(javaClass.getResource("/tier1-golden.json")).readText()).jsonObject
        for(key in listOf("attributes","attributeModifiers","proficiencyBonus","maximumWounds","defence","initiative","saves")) assertEquals(golden[key],actual[key],key)
        for((id,v) in golden.getValue("skills").jsonObject) {
            val skill=actual.getValue("skills").jsonObject.getValue(id).jsonObject
            assertEquals(v.jsonObject.num("modifier"),skill.num("modifier"),id)
            assertEquals(v.jsonObject["proficient"],skill["proficient"],id)
        }
        assertEquals(tier1Fixture().inventory.map { it.definitionId to it.quantity }.toMap(),actual.objects("inventory").associate { it.text("definitionId") to it.num("quantity") })
        for((id,expected) in golden.getValue("expectedActions").jsonObject) {
            val action=actual.objects("actions").single { it.text("itemId")==id }
            for((key,value) in expected.jsonObject) assertEquals(value,action[key],"$id.$key")
        }
        for(expected in golden.objects("expectedBaselineRolls")) {
            val roll=actual.objects("rollDefinitions").single { it.text("label")==expected.text("label") && it.text("category")==expected.text("category") }
            val component=roll.objects("components").single();val dice=component.objects("groups").single()
            assertEquals(expected.num("count"),dice.num("count"));assertEquals(expected.num("sides"),dice.num("sides"));assertEquals(expected.num("modifier"),component.objects("modifiers").single().num("value"))
        }
        val stealth=actual.objects("rollDefinitions").single { it.text("category")=="skill" && it.text("label")=="Stealth" }
        assertEquals(4,stealth.objects("components").single().objects("modifiers").single().num("value"))
        assertEquals("phb-tier1-kotlin-v1",stealth.getValue("snapshot").jsonObject.text("engineVersion"))
        assertTrue(actual.objects("features").any { it.text("id")=="di.feature.origin.hiveborn" && it["manual"]==JsonPrimitive(true) })
    }
    @Test fun `rare limited invalid and uncertified levels fail closed`() {
        val d=tier1Fixture()
        for(bad in listOf(d.copy(speciesId="di.species.ogryn"),d.copy(speciesId="di.species.skitarii",originId="di.background.militarum_regiment")))
            assertTrue(rules.validate(bad).errors.any { it.code=="APPROVAL_REQUIRED" })
        for(bad in listOf(d.copy(level=2),d.copy(level=3),d.copy(level=4),d.copy(speciesId="di.species.kin"),d.copy(originId="di.background.forge_world")))
            assertTrue(rules.validate(bad).errors.any { it.code=="PATH_NOT_CERTIFIED" })
        assertTrue(rules.validate(d.copy(answers=d.answers+mapOf("gmApproval" to listOf("true")))).errors.isNotEmpty())
    }
    @Test fun `shared level calculations do not publish levels or invent minimum HP`() {
        for((die,expected) in mapOf(6 to listOf(7,12,17),8 to listOf(9,15,21),10 to listOf(11,18,25),12 to listOf(13,21,29)))
            for(level in 1..3) assertEquals(expected[level-1],Tier1Calculations.hp(die,level,1))
        assertFailsWith<IllegalArgumentException> { Tier1Calculations.hp(6,2,-5) }
        assertEquals(14,Tier1Calculations.armour(12,3,2));assertEquals(11,Tier1Calculations.armour(12,-1,2))
    }
    @Test fun `package compiler supports nested optional grants equip proficiency and narrative`() {
        val item="di.weapon.lasgun";val armour="di.armour.flak_armour"
        val steps=listOf(obj("kind" to "item","itemId" to armour,"quantity" to 1),obj("kind" to "equip","itemId" to armour),
            obj("kind" to "choice","id" to "branch","min" to 1,"max" to 1,"options" to listOf(obj("id" to "a","steps" to listOf(obj("kind" to "item","itemId" to item,"quantity" to 2),obj("kind" to "proficiency","proficiencyId" to "di.proficiency.skill.stealth"),obj("kind" to "narrative","text" to "Reviewed contact"))))),
            obj("kind" to "choice","id" to "optional","min" to 0,"max" to 1,"options" to listOf(obj("id" to "kit","steps" to listOf(obj("kind" to "item","itemId" to item,"quantity" to 1))))))
        val definition=obj("steps" to steps)
        fun compile(a:Map<String,List<String>>)=StartingPackages.compile(definition,a,rules.records,rules.spec.strings("equipment").toSet())
        val result=compile(mapOf("branch" to listOf("a")))
        assertEquals(2,result.inventory.single { it.definitionId==item }.quantity)
        assertTrue(result.inventory.single { it.definitionId==armour }.equipped)
        assertEquals(setOf("di.proficiency.skill.stealth"),result.proficiencies);assertEquals(listOf("Reviewed contact"),result.narratives)
        assertEquals(3,compile(mapOf("branch" to listOf("a"),"optional" to listOf("kit"))).inventory.single { it.definitionId==item }.quantity)
        for(a in listOf(emptyMap(),mapOf("branch" to listOf("bad")),mapOf("branch" to listOf("a","a")),mapOf("branch" to listOf("a"),"fake" to listOf("yes")))) assertFailsWith<IllegalArgumentException> { compile(a) }
    }
    @Test fun `package rejects unknown candidates quantities and forged inventory`() {
        for((id,n) in listOf("di.weapon.lasgun" to 0,"di.weapon.lasgun" to -1,"di.equipment.auspex" to 1,"unknown" to 1)) {
            assertFailsWith<IllegalArgumentException> { StartingPackages.compile(obj("steps" to listOf(obj("kind" to "item","itemId" to id,"quantity" to n))),emptyMap(),rules.records,rules.spec.strings("equipment").toSet()) }
        }
        val d=tier1Fixture();assertTrue(rules.validate(d.copy(inventory=d.inventory.dropLast(1))).errors.isNotEmpty())
        assertTrue(rules.validate(d.copy(packageChoices=d.packageChoices+mapOf("primary" to "di.weapon.autogun"))).errors.isNotEmpty())
    }
    @Test fun `old snapshot remains pinned and independently valid`() {
        val old=NarrowRules.bundled();assertEquals("3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af",old.digest)
        assertEquals(emptyList(),old.validate(productionFixture()).errors)
        assertNotEquals(old.digest,rules.digest)
    }
}

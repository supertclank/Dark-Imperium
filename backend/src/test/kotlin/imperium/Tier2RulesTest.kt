package imperium

import kotlinx.serialization.json.*
import kotlin.test.*

fun tier2Fixture(name:String="hive_scum-1"):NarrowDraft=Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier2/$name.json")).readText())

class Tier2RulesTest {
    private val rules=NarrowRules.tier2()
    @Test fun `all 48 families calculate source HP skills inventory and valid baseline rolls`() {
        val drafts=Json.decodeFromString<List<NarrowDraft>>(requireNotNull(javaClass.getResource("/tier2/all-paths.json")).readText())
        assertEquals(48,drafts.size)
        for(draft in drafts) {
            val v=rules.validate(draft);assertEquals(emptyList(),v.errors,draft.name)
            val c=v.calculated!!
            assertEquals(if(draft.classId=="di.class.hive_scum") 9 else listOf(11,18,25)[draft.level-1],c.num("maximumWounds"))
            assertEquals(14,c.num("defence"));assertEquals(2,c.num("proficiencyBonus"));assertEquals(4,c.num("initiative"))
            assertEquals(30,c.num("movement"));assertEquals(35,c.objects("rollDefinitions").size)
            assertEquals(draft.inventory.map { it.definitionId }.toSet(),c.objects("inventory").map { it.text("definitionId") }.toSet())
            for(roll in c.objects("rollDefinitions")) assertEquals(rules.digest,roll.getValue("snapshot").jsonObject.text("rulesetLockDigest"))
            if(draft.level>=2) {
                val blocked=c.objects("features").single { it.text("id").endsWith("suppressing_fire") }
                assertEquals("BLOCKED",blocked.text("classification"));assertEquals(listOf("PHB-RULE-022"),blocked.strings("rulingIds"))
                assertFalse(c.objects("rollDefinitions").any { "Suppress" in it.text("label") })
            }
            if(draft.originId=="di.background.voidborn") assertEquals(5,c.arr("proceduralProficiencies").size)
        }
    }
    @Test fun `each doctrine includes only its reached feature and no contextual attack bonus`() {
        for(sub in listOf("shock_trooper","marksman","sergeant")) {
            val c=rules.validate(tier2Fixture(sub)).calculated!!
            assertEquals("di.subclass.veteran.$sub",c.getValue("subclass").jsonObject.text("id"))
            val features=c.objects("features").filter { it.text("id").startsWith("di.feature.subclass.") }
            assertEquals(listOf("di.feature.subclass.veteran.$sub.level_3"),features.map { it.text("id") })
            assertEquals("MANUAL",features.single().text("classification"))
            val golden=Json.parseToJsonElement(requireNotNull(javaClass.getResource("/tier2/$sub-golden.json")).readText()).jsonObject
            assertEquals(golden.strings("expectedFeatures").toSet(),c.objects("features").map { it.text("id") }.toSet())
            for(key in listOf("attributes","attributeModifiers","proficiencyBonus","maximumWounds","defence","initiative","saves")) assertEquals(golden[key],c[key],key)
            assertEquals(golden.objects("expectedInventory").associate { it.text("definitionId") to it.num("quantity") },c.objects("inventory").associate { it.text("definitionId") to it.num("quantity") })
            for((id,expected) in golden.getValue("expectedActions").jsonObject) {
                val action=c.objects("actions").single { it.text("itemId")==id }
                for((key,value) in expected.jsonObject) assertEquals(value,action[key],"$sub $id.$key")
            }
            for(expected in golden.objects("expectedBaselineRolls")) {
                val roll=c.objects("rollDefinitions").single { it.text("label")==expected.text("label") && it.text("category")==expected.text("category") }
                val component=roll.objects("components").single();val dice=component.objects("groups").single()
                assertEquals(expected.num("count"),dice.num("count"));assertEquals(expected.num("sides"),dice.num("sides"));assertEquals(expected.num("modifier"),component.objects("modifiers").single().num("value"))
            }

            val gun=c.objects("actions").single { it.text("itemId")=="di.weapon.lasgun" }
            assertEquals(4,gun.num("attackBonus"));assertEquals("1d8 + 2",gun.text("damageExpression"))
        }
    }
    @Test fun `subclass and level tampering fails closed`() {
        assertTrue(rules.validate(tier2Fixture("invalid-subclass")).errors.isNotEmpty())
        val d=tier2Fixture("marksman")
        for(bad in listOf(d.copy(level=1),d.copy(level=2),d.copy(level=4),d.copy(classId="di.class.hive_scum"),d.copy(answers=d.answers-"di.choice.veteran.subclass"),d.copy(answers=d.answers+mapOf("di.choice.veteran.subclass" to listOf("medic"))),d.copy(answers=d.answers+mapOf("di.choice.veteran.subclass" to listOf("marksman","sergeant"))))) assertTrue(rules.validate(bad).errors.isNotEmpty())
        assertTrue(rules.validate(tier2Fixture().copy(level=2)).errors.isNotEmpty())
    }
    @Test fun `Hive Scum contacts are not inventory and both pistol branches are safe`() {
        for(pistol in listOf("autopistol","stub_pistol")) {
            val d=tier2Fixture();val selected="di.weapon.$pistol"
            val changed=d.copy(packageChoices=d.packageChoices+mapOf("pistol" to selected),inventory=d.inventory.map { if(it.definitionId=="di.weapon.autopistol") it.copy(definitionId=selected) else it })
            val v=rules.validate(changed);assertEquals(emptyList(),v.errors)
            val c=v.calculated!!;assertEquals(1,c.arr("contacts").size);assertEquals(5,c.arr("inventory").size)
            assertEquals(4,c.getValue("saves").jsonObject.getValue("dexterity").jsonObject.num("modifier"))
            assertEquals(1,c.getValue("saves").jsonObject.getValue("charisma").jsonObject.num("modifier"))
            assertEquals("1d4 + 3",c.objects("actions").single { it.text("itemId")=="di.weapon.knife" }.text("damageExpression"))
            assertEquals("PARTIAL",c.objects("features").single { it.text("id").endsWith("streetwise") }.text("classification"))
        }
    }
    @Test fun `resources follow selected Origin and previous profiles remain frozen`() {
        val all=Json.decodeFromString<List<NarrowDraft>>(requireNotNull(javaClass.getResource("/tier2/all-paths.json")).readText())
        val penal=rules.validate(all.first { it.originId=="di.background.penal_worlder" }).calculated!!
        assertEquals(setOf("failed_save_reroll","dirty_survival"),penal.objects("resources").map { it.text("key") }.toSet())
        assertEquals("d75739125210dd704ca0b3362a2c864a0fdd32b6b2765b0bbc137f5792971f32",NarrowRules.tier1().digest)
        assertEquals(emptyList(),NarrowRules.tier1().validate(tier1Fixture()).errors)
        assertEquals(emptyList(),NarrowRules.bundled().validate(productionFixture()).errors)
    }
    @Test fun `real Zealot and Arbites packages reject unpromoted mandatory equipment`() {
        for(name in listOf("zealot","arbites_enforcer")) {
            val definition=Json.parseToJsonElement(requireNotNull(javaClass.getResource("/tier2/$name-package.json")).readText()).jsonObject
            val choices=definition.getValue("display").jsonObject.objects("choices").associate { it.text("id") to listOf(it.objects("options").first().text("id")) }
            assertFailsWith<IllegalArgumentException> { StartingPackages.compile(definition.getValue("executable").jsonObject,choices,rules.records,rules.records.keys) }
        }
    }
    @Test fun `compiler grants canonical shield and consumables without inventing execution`() {
        val definition=obj("steps" to listOf(obj("kind" to "item","itemId" to "di.shield.shield","quantity" to 1),obj("kind" to "equip","itemId" to "di.shield.shield"),obj("kind" to "item","itemId" to "di.weapon.frag_grenade","quantity" to 2),obj("kind" to "contact","id" to "friend","text" to "Source-defined contact")))
        val result=StartingPackages.compile(definition,emptyMap(),rules.records,rules.records.keys)
        assertTrue(result.inventory.single { it.definitionId=="di.shield.shield" }.equipped)
        assertEquals(2,result.inventory.single { it.definitionId=="di.weapon.frag_grenade" }.quantity)
        assertEquals(1,result.contacts.size)
    }

}

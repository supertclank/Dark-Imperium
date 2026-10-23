package imperium

import kotlinx.serialization.json.*
import kotlin.test.*

fun nonhumanFixtures():List<NarrowDraft> = Json.decodeFromString(requireNotNull(NarrowRules::class.java.getResource("/tier4/all-paths.json")).readText())
class Tier4RulesTest {
    private val rules=NarrowRules.tier4()
    @Test fun `six new families have independently checked source baselines`() {
        assertEquals(64,rules.spec.objects("certifiedPaths").size)
        val expected=mapOf(
            "di.class.ogryn_skullbreaker" to listOf(17,12,14,17,16,30,0),
            "di.class.skitarii_veteran" to listOf(15,16,14,12,15,30,0),
            "di.class.kin_armsman" to listOf(15,14,15,12,16,25,60),
            "di.class.hernkyn_prospector" to listOf(15,14,15,10,16,25,60),
            "di.class.aeldari_outcast" to listOf(15,16,13,9,15,35,90))
        for(d in nonhumanFixtures()) {
            val result=rules.validate(d);assertEquals(emptyList(),result.errors,d.classId)
            val c=result.calculated!!;val a=c.getValue("attributes").jsonObject
            assertEquals(expected.getValue(d.classId),listOf(a.num("strength"),a.num("dexterity"),a.num("constitution"),c.num("maximumWounds"),c.num("defence"),c.num("movement"),c.num("darkvisionFeet")),d.classId)
            assertEquals(d.inventory.size,c.objects("inventory").size)
            assertTrue(c.objects("rollDefinitions").isNotEmpty())
            assertTrue(rules.validate(d.copy(level=2)).errors.any { it.code=="PATH_NOT_CERTIFIED" })
        }
    }
    @Test fun `specific perception duplicate bonus is one point not expertise`() {
        val d=nonhumanFixtures().last();val c=rules.validate(d).calculated!!
        assertEquals(3,c.getValue("skills").jsonObject.getValue("di.skill.perception").jsonObject.num("modifier"))
        val triple=d.copy(answers=d.answers+mapOf("di.choice.craftworld_outcast.skills" to listOf("perception","insight")))
        assertEquals(3,rules.validate(triple).calculated!!.getValue("skills").jsonObject.getValue("di.skill.perception").jsonObject.num("modifier"))
    }
    @Test fun `Ogryn floor composes after species and innate damage has no inventory item`() {
        val d=nonhumanFixtures().first();val attrs=d.attributes.toMutableMap();attrs["dexterity"]=8;attrs["charisma"]=14
        val c=rules.validate(d.copy(attributes=attrs)).calculated!!
        assertEquals(6,c.getValue("attributes").jsonObject.num("dexterity"))
        val innate=c.objects("rollDefinitions").single { it.text("label")=="Brute Strength unarmed damage" }
        val component=innate.objects("components").single();assertEquals(6,component.objects("groups").single().num("sides"));assertEquals(3,component.objects("modifiers").single().num("value"))
        assertTrue(c.objects("inventory").none { it.text("definitionId").contains("unarmed") })
    }
    @Test fun `approval psychic fit choice and species gates reject forged selections`() {
        val ogryn=nonhumanFixtures().first();val skitarii=nonhumanFixtures()[2];val kin=nonhumanFixtures()[4]
        assertTrue(rules.validate(ogryn.copy(originId="di.background.hiveborn")).errors.any { it.code=="APPROVAL_REQUIRED" })
        assertTrue(rules.validate(skitarii.copy(originId="di.background.militarum_regiment")).errors.any { it.code=="APPROVAL_REQUIRED" })
        assertTrue(rules.validate(skitarii.copy(classId="di.class.psyker")).errors.any { it.code=="PSYCHIC_PROHIBITED" })
        assertTrue(rules.validate(skitarii.copy(traitId="di.feature.universal.touched_by_the_warp")).errors.any { it.code=="PSYCHIC_PROHIBITED" })
        assertTrue(rules.validate(skitarii.copy(answers=skitarii.answers-"di.choice.skitarii.noospheric_focus")).errors.any { it.code=="MISSING_CHOICE" })
        assertTrue(rules.validate(kin.copy(packageChoices=kin.packageChoices+mapOf("primary" to "di.weapon.magna_rail_rifle"))).errors.any { it.code=="GM_APPROVAL_REQUIRED" })
        assertTrue(rules.validate(ogryn.copy(inventory=ogryn.inventory+InventorySelection("di.weapon.laspistol",1))).errors.any { it.code=="EQUIPMENT_FIT_NOT_CERTIFIED" })
    }
    @Test fun `each published kit branch compiles and has the reviewed base damage`() {
        val damage=mapOf("ripper_gun" to (1 to 12),"ogryn_club" to (1 to 12),"taser_goad" to (1 to 8),"ion_blaster" to (1 to 10),"autoch_pattern_pistol" to (1 to 8),"kin_power_axe" to (1 to 10),"concussion_hammer" to (1 to 10),"shuriken_pistol" to (1 to 6),"shuriken_catapult" to (1 to 8),"ranger_long_rifle" to (1 to 10),"monomolecular_blade" to (1 to 6))
        for(d in nonhumanFixtures()) {
            val pack=rules.payload.getValue("packages").jsonObject.getValue(d.classId).jsonObject
            for(choice in pack.getValue("display").jsonObject.objects("choices")) for(option in choice.objects("options")) {
                val selected=d.packageChoices+mapOf(choice.text("id") to option.text("id"))
                val inventory=StartingPackages.compile(pack.getValue("executable").jsonObject,selected.mapValues { listOf(it.value) },rules.records,rules.spec.strings("equipment").toSet()).inventory
                val result=rules.validate(d.copy(packageChoices=selected,inventory=inventory));assertEquals(emptyList(),result.errors)
                for(item in inventory.filter { it.definitionId.removePrefix("di.weapon.") in damage }) {
                    val definition=result.calculated!!.objects("rollDefinitions").single { it.text("category")=="damage" && it.getValue("source").jsonObject.getValue("ref").jsonObject.text("id")==item.definitionId }
                    val group=definition.objects("components").single().objects("groups").single()
                    assertEquals(damage.getValue(item.definitionId.removePrefix("di.weapon.")),group.num("count") to group.num("sides"),item.definitionId)
                }
            }
        }
    }
    @Test fun `package compiler rejects GM-only branch even for a listed canonical item`() {
        val pack=obj("steps" to listOf(obj("kind" to "choice","id" to "special","min" to 1,"max" to 1,"options" to listOf(obj("id" to "approved_item","approvalRequired" to true,"steps" to listOf(obj("kind" to "item","itemId" to "di.weapon.lasgun","quantity" to 1)))))))
        val e=assertFailsWith<IllegalArgumentException> { StartingPackages.compile(pack,mapOf("special" to listOf("approved_item")),rules.records,rules.spec.strings("equipment").toSet()) }
        assertEquals("GM_APPROVAL_REQUIRED",e.message)
    }
    @Test fun `historical profiles retain exact digests`() {
        assertEquals("5c4d81d1cf9a55be138d5e73a58acfccd96fb2dcb0eeadb157fbcfde08b2a795",NarrowRules.tier3().digest)
        assertEquals("2882f86ce5f26e0806be49ad8fc6d3068b9573f376222fc6b0b835b32cdeabf8",NarrowRules.tier2().digest)
        assertEquals("d75739125210dd704ca0b3362a2c864a0fdd32b6b2765b0bbc137f5792971f32",NarrowRules.tier1().digest)
        assertEquals("3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af",NarrowRules.bundled().digest)
    }
}

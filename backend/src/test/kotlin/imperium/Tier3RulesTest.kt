package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
class Tier3RulesTest {
    @Test fun `Ratling normal families have mandatory attributes senses skills and manual traits`() {
        val rules=NarrowRules.tier3();val configs=rules.spec.objects("pathConfigurations").filter { it.text("speciesId")=="di.species.ratling" }
        assertEquals(10,configs.size)
        for(config in configs) {
            val fixture=Json.decodeFromString<List<NarrowDraft>>(requireNotNull(javaClass.getResource("/tier2/all-paths.json")).readText()).single { it.classId==config.text("classId") && it.originId==config.text("originId") && it.level==1 }
            val d=fixture.copy(profileId=rules.id,profileDigest=rules.digest,speciesId="di.species.ratling",originId=config.text("originId"),answers=fixture.answers.filterKeys { it in config.strings("choices") })
            val result=rules.validate(d);assertEquals(emptyList(),result.errors,d.originId)
            val c=result.calculated!!;assertEquals(16,c.getValue("attributes").jsonObject.num("dexterity"));assertEquals(11,c.getValue("attributes").jsonObject.num("wisdom"))
            assertEquals(25,c.num("movement"));assertEquals(60,c.num("darkvisionFeet"));assertEquals("small",c.text("size"))
            assertEquals(5,c.getValue("skills").jsonObject.getValue("di.skill.stealth").jsonObject.num("modifier"))
            assertTrue(c.objects("resources").any { it.text("key")=="lucky_shot" });assertFalse(c.objects("resources").any { it.text("sourceId").contains("human") })
            assertTrue(rules.validate(d.copy(originId="di.background.shrine_worlder")).errors.any { it.code=="APPROVAL_REQUIRED" })
            assertTrue(rules.validate(d.copy(level=2)).errors.any { it.code=="PATH_NOT_CERTIFIED" })
        }
    }
}

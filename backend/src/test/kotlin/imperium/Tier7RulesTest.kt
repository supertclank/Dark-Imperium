package imperium
import kotlinx.serialization.json.*
import kotlin.test.*
class Tier7RulesTest {
 @Test fun `existing families remain valid and Knife has fixed Dexterity`() {
  val r=NarrowRules.tier7()
  for(old in tier6Fixtures()) {
   val v=r.validate(old.copy(profileId=r.id,profileDigest=r.digest))
   assertEquals(emptyList(),v.errors,old.name)
   for(a in v.calculated!!.objects("actions")) {
    if(a.text("itemId")=="di.weapon.knife") {
     assertEquals("dexterity",a.text("attackAbilityId"))
     assertEquals("dexterity",a.text("damageAbilityId"))
    }
   }
  }
  assertFalse("di.weapon.thunder_hammer" in r.records)
  assertFalse(r.spec.containsKey("upgradeContracts"))
 }
 @Test fun `historical policy and canonical overrides remain distinct`() {
  assertEquals("strength",WeaponAbilities.resolve("finesse",false))
  assertEquals("dexterity",WeaponAbilities.resolve("finesse",true))
  assertEquals("strength",WeaponAbilities.resolve("strength",true))
  assertEquals("intelligence",WeaponAbilities.resolve("intelligence",true))
  assertNull(WeaponAbilities.resolve("none",true))
  assertEquals("fc78eebe9eab846b96aecf4823f88185e6d9818a1cde59bf255368be37db7769",NarrowRules.tier6().digest)
 }
}

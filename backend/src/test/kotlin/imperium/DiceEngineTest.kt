package imperium

import kotlinx.serialization.json.Json
import kotlin.test.*

class DiceEngineTest {
    @Test fun `all supported dice respect bounds using secure production source`() {
        val engine=DiceEngine()
        for(sides in listOf(4,6,8,10,12,20,100)) {
            val result=engine.resolve(listOf(DiceGroup(100,sides)),0)
            assertEquals(100,result.groups.single().dice.size)
            assertTrue(result.groups.single().dice.all { it in 1..sides })
        }
    }
    @Test fun `injected results retain individual dice and add modifier once`() {
        val values=ArrayDeque(listOf(4,3,5))
        val result=DiceEngine { values.removeFirst() }.resolve(listOf(DiceGroup(3,6)),2)
        assertEquals(listOf(4,3,5),result.groups.single().dice)
        assertEquals(14,result.total);assertEquals(2,result.modifier)
        assertEquals(emptyList(),result.groups.single().discarded)
    }
    @Test fun `keep highest and lowest track discarded dice and stable ties`() {
        for((mode,kept,total) in listOf(Triple(Keep.HIGHEST,listOf(0,2),40),Triple(Keep.LOWEST,listOf(0,1),21))) {
            val values=ArrayDeque(listOf(20,1,20))
            val result=DiceEngine { values.removeFirst() }.resolve(listOf(DiceGroup(3,20,mode,2)),0)
            assertEquals(kept,result.groups.single().keptIndices);assertEquals(total,result.total)
            assertEquals(1,result.groups.single().discarded.size)
        }
    }
    @Test fun `invalid dice budgets and bad injected RNG fail closed`() {
        val engine=DiceEngine { 1 }
        for(group in listOf(DiceGroup(0,6),DiceGroup(101,6),DiceGroup(1,7),DiceGroup(2,6,Keep.ALL,1),DiceGroup(2,6,Keep.LOWEST,3)))
            assertFailsWith<IllegalArgumentException> { engine.resolve(listOf(group),0) }
        assertFailsWith<IllegalArgumentException> { DiceEngine { 0 }.resolve(listOf(DiceGroup(1,6)),0) }
    }
    @Test fun `structured resolution round trips without changing totals`() {
        val result=DiceEngine { it }.resolve(listOf(DiceGroup(2,8,Keep.HIGHEST,1)),-2)
        assertEquals(result,Json.decodeFromString<DiceResolution>(Json.encodeToString(DiceResolution.serializer(),result)))
    }
}

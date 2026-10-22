package imperium

import kotlinx.serialization.Serializable
import java.security.SecureRandom

fun interface DieSource { fun roll(sides: Int): Int }

/** SecureRandom.nextInt(bound) uses unbiased bounded sampling, not remainder reduction. */
class SecureDice : DieSource {
    private val random = SecureRandom()
    override fun roll(sides: Int) = random.nextInt(sides) + 1
}

@Serializable enum class Keep { ALL, HIGHEST, LOWEST }
@Serializable data class DiceGroup(val count: Int, val sides: Int, val keep: Keep = Keep.ALL, val keepCount: Int = count)
@Serializable data class ResolvedGroup(
    val sides: Int, val dice: List<Int>, val keptIndices: List<Int>, val discardedIndices: List<Int>,
    val kept: List<Int>, val discarded: List<Int>, val keep: Keep
)
@Serializable data class DiceResolution(val groups: List<ResolvedGroup>, val modifier: Int, val total: Int)

class DiceEngine(private val source: DieSource = SecureDice()) {
    fun resolve(groups: List<DiceGroup>, modifier: Int): DiceResolution {
        require(groups.isNotEmpty() && groups.size <= 16 && groups.sumOf { it.count } in 1..100)
        require(modifier in -1000000..1000000)
        val results = groups.map { group ->
            require(group.sides in setOf(4,6,8,10,12,20,100))
            require(group.count in 1..100 && group.keepCount in 1..group.count)
            require(group.keep != Keep.ALL || group.keepCount == group.count)
            val dice = List(group.count) { source.roll(group.sides).also { require(it in 1..group.sides) } }
            val ranked = when(group.keep) {
                Keep.ALL -> dice.indices.toList()
                Keep.HIGHEST -> dice.indices.sortedByDescending { dice[it] }
                Keep.LOWEST -> dice.indices.sortedBy { dice[it] }
            }
            val kept = ranked.take(group.keepCount).sorted()
            val discarded = dice.indices.filter { it !in kept }
            ResolvedGroup(group.sides,dice,kept,discarded,kept.map(dice::get),discarded.map(dice::get),group.keep)
        }
        return DiceResolution(results,modifier,results.sumOf { it.kept.sum() } + modifier)
    }
}

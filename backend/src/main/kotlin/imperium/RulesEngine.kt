package imperium

/** Interprets a deliberately narrow, versioned effect vocabulary, never content names. */
object RulesEngine {
    val startingAttributes = linkedMapOf("Strength" to 30, "Agility" to 30, "Toughness" to 30,
        "Intellect" to 30, "Willpower" to 30, "Presence" to 30)

    fun calculate(vararg sources: Rules): CalculatedValues {
        val values = mutableMapOf("movement" to 0, "maxWounds" to 0)
        sources.forEach { rules ->
            require(rules.schemaVersion == 1) { "Unsupported rules schema" }
            rules.effects.forEach { effect ->
                require(effect.operation == "add" && effect.target in values) { "Unsupported effect" }
                values[effect.target] = Math.addExact(values.getValue(effect.target), effect.value)
            }
        }
        return CalculatedValues(values.getValue("movement").coerceAtLeast(0), values.getValue("maxWounds").coerceAtLeast(1))
    }
}

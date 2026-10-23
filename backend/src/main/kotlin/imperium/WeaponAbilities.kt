package imperium

/** Declarative bindings are compiled into each immutable profile; explicit abilities win. */
object WeaponAbilities {
    fun resolve(binding:String, fixedPolicy:Boolean):String? = when(binding) {
        "none" -> null
        "finesse" -> if(fixedPolicy) "dexterity" else "strength"
        in setOf("strength","dexterity","constitution","intelligence","wisdom","charisma") -> binding
        else -> throw IllegalArgumentException("Unsupported weapon ability binding: $binding")
    }
}

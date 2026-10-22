package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonObject

@Serializable data class Credentials(val email: String, val password: String)
@Serializable data class UserView(val id: String, val email: String)
@Serializable data class ApiError(val error: ErrorDetail)
@Serializable data class ErrorDetail(val code: String, val message: String)
class ApiException(val status: Int, val code: String, override val message: String) : RuntimeException(message)
@Serializable data class Effect(val operation: String, val target: String, val value: Int)
@Serializable data class Rules(val schemaVersion: Int = 1, val effects: List<Effect> = emptyList())
@Serializable data class Content(val id: String, val name: String, val description: String, val rules: Rules)
@Serializable data class WeaponProperty(val key: String, val label: String, val parameters: JsonObject)
@Serializable data class Weapon(
    val id: String, val name: String, val description: String, val category: String,
    val damageDice: String, val damageType: String, val normalRange: Int, val longRange: Int,
    val properties: List<WeaponProperty>
)
@Serializable data class CreateCharacter(val name: String, val speciesId: String, val classId: String, val weaponId: String)
@Serializable data class RenameCharacter(val name: String)
@Serializable data class CalculatedValues(val movement: Int, val maxWounds: Int)
@Serializable data class CharacterSheet(
    val id: String, val name: String, val species: Content, val characterClass: Content,
    val level: Int, val attributes: Map<String, Int>, val currentWounds: Int,
    val calculated: CalculatedValues, val equipment: List<Weapon>
)

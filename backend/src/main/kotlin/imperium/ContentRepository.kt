package imperium

import java.sql.Connection
import java.sql.ResultSet
import java.util.UUID
import kotlinx.serialization.json.Json

enum class ContentKind(val table: String) { SPECIES("species"), CLASS("classes") }
class ContentRepository(private val db: Database) {
    private fun content(row: ResultSet) = Content(row.getString("id"), row.getString("name"), row.getString("description"), Json.decodeFromString<Rules>(row.getString("rules")))
    fun list(kind: ContentKind): List<Content> = db.read { it.query("SELECT * FROM ${kind.table} ORDER BY name", map = ::content) }
    fun get(connection: Connection, kind: ContentKind, id: UUID): Content = connection.query("SELECT * FROM ${kind.table} WHERE id=?", id, map = ::content).singleOrNull()
        ?: throw ApiException(400, "INVALID_CONTENT", "The selected ${kind.table} entry does not exist.")
    fun weapon(row: ResultSet) = Weapon(row.getString("id"), row.getString("name"), row.getString("description"),
        row.getString("category"), row.getString("damage_dice"), row.getString("damage_type"),
        row.getInt("normal_range"), row.getInt("long_range"), Json.decodeFromString<List<WeaponProperty>>(row.getString("properties")))
    fun weapons(): List<Weapon> = db.read { it.query("SELECT * FROM weapons ORDER BY name", map = ::weapon) }
    fun weapon(connection: Connection, id: UUID): Weapon = connection.query("SELECT * FROM weapons WHERE id=?", id, map = ::weapon).singleOrNull()
        ?: throw ApiException(400, "INVALID_CONTENT", "The selected weapon does not exist.")
}

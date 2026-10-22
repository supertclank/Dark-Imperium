package imperium

import java.sql.Connection
import java.util.UUID
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class CharacterService(private val db: Database, private val content: ContentRepository) {
    private fun name(raw: String): String = raw.trim().also {
        if (it.isEmpty() || it.length > 80 || it.any(Char::isISOControl))
            throw ApiException(400, "INVALID_NAME", "Use 1 to 80 printable characters for the name.")
    }
    fun create(owner: UUID, input: CreateCharacter): CharacterSheet {
        val name = name(input.name)
        val speciesId = uuid(input.speciesId); val classId = uuid(input.classId); val weaponId = uuid(input.weaponId)
        return db.transaction { connection ->
            val species = content.get(connection, ContentKind.SPECIES, speciesId)
            val characterClass = content.get(connection, ContentKind.CLASS, classId)
            content.weapon(connection, weaponId)
            val values = RulesEngine.calculate(species.rules, characterClass.rules)
            val id = UUID.randomUUID()
            connection.execute("INSERT INTO characters(id,user_id,name,species_id,class_id,attributes,current_wounds) VALUES (?,?,?,?,?,?::jsonb,?)",
                id, owner, name, speciesId, classId, Json.encodeToString(RulesEngine.startingAttributes), values.maxWounds)
            connection.execute("INSERT INTO character_equipment(id,character_id,item_id) VALUES (?,?,?)", UUID.randomUUID(), id, weaponId)
            get(connection, owner, id)
        }
    }
    fun list(owner: UUID): List<CharacterSheet> = db.read { connection ->
        connection.query("SELECT id FROM characters WHERE user_id=? ORDER BY created_at DESC", owner) { it.getObject("id", UUID::class.java) }
            .map { get(connection, owner, it) }
    }
    fun get(owner: UUID, id: UUID): CharacterSheet = db.read { get(it, owner, id) }
    private fun get(connection: Connection, owner: UUID, id: UUID): CharacterSheet {
        return connection.query("SELECT * FROM characters WHERE id=? AND user_id=?", id, owner) { row ->
            val species = content.get(connection, ContentKind.SPECIES, row.getObject("species_id", UUID::class.java))
            val characterClass = content.get(connection, ContentKind.CLASS, row.getObject("class_id", UUID::class.java))
            val equipment = connection.query("SELECT w.* FROM weapons w JOIN character_equipment e ON e.item_id=w.id WHERE e.character_id=? ORDER BY w.name", id, map = content::weapon)
            CharacterSheet(id.toString(), row.getString("name"), species, characterClass, row.getInt("level"),
                Json.decodeFromString<Map<String, Int>>(row.getString("attributes")), row.getInt("current_wounds"),
                RulesEngine.calculate(species.rules, characterClass.rules), equipment)
        }.singleOrNull() ?: throw ApiException(404, "NOT_FOUND", "Character not found.")
    }
    fun rename(owner: UUID, id: UUID, input: RenameCharacter): CharacterSheet = db.transaction { connection ->
        val updated = connection.execute("UPDATE characters SET name=?,updated_at=now() WHERE id=? AND user_id=?", name(input.name), id, owner)
        if (updated == 0) throw ApiException(404, "NOT_FOUND", "Character not found.")
        get(connection, owner, id)
    }
    fun delete(owner: UUID, id: UUID) {
        if (db.read { it.execute("DELETE FROM characters WHERE id=? AND user_id=?", id, owner) } == 0)
            throw ApiException(404, "NOT_FOUND", "Character not found.")
    }
}

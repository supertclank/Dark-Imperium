package imperium

import java.sql.Connection
import java.util.UUID
import kotlinx.serialization.json.*

/** Selections and owned state are persisted separately; derived values are never stored. */
class ProductionCharacters(private val db: Database, val rules: NarrowRules = NarrowRules.tier7()) {
    private val profiles=listOf(NarrowRules.bundled(),NarrowRules.tier1(),NarrowRules.tier2(),NarrowRules.tier3(),NarrowRules.tier4(),NarrowRules.tier5(),NarrowRules.tier6(),NarrowRules.tier7(),rules).associateBy { it.id }
    fun rulesFor(profileId:String)=profiles[profileId] ?: rules
    init { db.transaction { connection ->
      for(rules in profiles.values) {
        connection.execute("INSERT INTO ruleset_profiles(id,digest,engine_version,snapshot) VALUES (?,?,?,?::jsonb) ON CONFLICT(id) DO NOTHING",rules.id,rules.digest,rules.spec.text("engineVersion"),rules.bundle.toString())
        val pinned=connection.query("SELECT digest FROM ruleset_profiles WHERE id=?",rules.id) { it.getString(1) }.single()
        check(pinned==rules.digest) { "Immutable profile ID reused with changed content; publish a new profile ID" }
      }
    } }
    fun create(owner:UUID,draft:NarrowDraft):JsonObject {
        val rules=rulesFor(draft.profileId)
        if(Level4Rules.policy(rules)!=null && draft.level !in (rules.spec["creationLevels"] as? JsonArray).orEmpty().map { it.jsonPrimitive.int }) throw ApiException(422,"ADVANCEMENT_REQUIRED","This profile is entered only through explicit certified advancement.")
        val requestId=try { UUID.fromString(draft.requestId) } catch(_:IllegalArgumentException) { throw InvalidDraft(listOf(DraftIssue("INVALID_REQUEST_ID","requestId","A creation request UUID is required."))) }
        val id=UUID.randomUUID();val validation=rules.validate(draft,id.toString())
        if(validation.errors.isNotEmpty()) throw InvalidDraft(validation.errors)
        val requestDigest=sha(canonicalJson(Json.encodeToJsonElement(NarrowDraft.serializer(),draft)))
        return db.transaction { con ->
            val inserted=con.execute("""INSERT INTO player_characters(id,user_id,profile_id,profile_digest,name,species_id,origin_id,class_id,trait_id,level,base_attributes,package_choices,request_id,request_digest)
                VALUES (?,?,?,?,?,?,?,?,?,?,?::jsonb,?::jsonb,?,?) ON CONFLICT(user_id,request_id) DO NOTHING""",
                id,owner,rules.id,rules.digest,draft.name.trim(),draft.speciesId,draft.originId,draft.classId,draft.traitId,draft.level,json(draft.attributes).toString(),json(draft.packageChoices).toString(),requestId,requestDigest)
            if(inserted==0) {
                val existing=con.query("SELECT id,request_digest FROM player_characters WHERE user_id=? AND request_id=?",owner,requestId) { it.getObject(1,UUID::class.java) to it.getString(2) }.single()
                if(existing.second!=requestDigest) throw ApiException(409,"IDEMPOTENCY_CONFLICT","This request ID already belongs to a different character draft.")
                return@transaction get(con,owner,existing.first)
            }
            for((choice,options) in draft.answers) con.execute("INSERT INTO player_character_choices(character_id,choice_id,option_ids) VALUES (?,?,?::jsonb)",id,choice,json(options).toString())
            for(item in draft.inventory) con.execute("INSERT INTO player_character_inventory(id,character_id,definition_id,initial_quantity,quantity,equipped) VALUES (?,?,?,?,?,?)",UUID.randomUUID(),id,item.definitionId,item.quantity,item.quantity,item.equipped)
            val resources=(if(rules.expanded) validation.calculated!!.objects("resources") else rules.spec.objects("runtimeResources")).associate { it.text("key") to obj("sourceId" to it.text("sourceId"),"remaining" to it.num("maximum"),"maximum" to it.num("maximum"),"recovery" to it.text("recovery"),"automation" to it.text("automation")) }
            con.execute("INSERT INTO player_character_runtime(character_id,current_hp,resources) VALUES (?,?,?::jsonb)",id,validation.calculated!!.num("maximumWounds"),json(resources).toString())
            get(con,owner,id)
        }
    }
    fun get(owner:UUID,id:UUID):JsonObject=db.read { get(it,owner,id) }
    internal fun get(con:Connection,owner:UUID,id:UUID):JsonObject {
        val base=con.query("SELECT c.*,p.snapshot FROM player_characters c JOIN ruleset_profiles p ON p.id=c.profile_id AND p.digest=c.profile_digest WHERE c.id=? AND c.user_id=?",id,owner) { row ->
            Triple(obj("id" to id.toString(),"name" to row.getString("name"),"createdAt" to row.getTimestamp("created_at").toInstant().toString(),"updatedAt" to row.getTimestamp("updated_at").toInstant().toString()),
                NarrowDraft(profileId=row.getString("profile_id"),profileDigest=row.getString("profile_digest"),requestId=row.getString("request_id"),name=row.getString("name"),speciesId=row.getString("species_id"),originId=row.getString("origin_id"),classId=row.getString("class_id"),traitId=row.getString("trait_id"),level=row.getInt("level"),attributes=Json.decodeFromString(row.getString("base_attributes")),packageChoices=Json.decodeFromString(row.getString("package_choices"))),
                NarrowRules(Json.parseToJsonElement(row.getString("snapshot")).jsonObject))
        }.singleOrNull() ?: throw ApiException(404,"NOT_FOUND","Character not found.")
        val choices=con.query("SELECT choice_id,option_ids FROM player_character_choices WHERE character_id=? ORDER BY choice_id",id) { it.getString(1) to Json.decodeFromString<List<String>>(it.getString(2)) }.toMap()
        val inventory=con.query("SELECT * FROM player_character_inventory WHERE character_id=? ORDER BY definition_id",id) { row -> obj("id" to row.getString("id"),"definitionId" to row.getString("definition_id"),"name" to base.third.label(row.getString("definition_id")),"initialQuantity" to row.getInt("initial_quantity"),"quantity" to row.getInt("quantity"),"equipped" to row.getBoolean("equipped"),"ammunition" to row.getString("ammunition")?.let(Json::parseToJsonElement)) }
        val draft=base.second.copy(answers=choices,inventory=inventory.map { InventorySelection(it.text("definitionId"),it.num("initialQuantity"),it.getValue("equipped").jsonPrimitive.boolean) })
        val calculation=base.third.validate(draft,id.toString())
        check(calculation.errors.isEmpty()) { "Persisted selections violate their pinned profile" }
        val runtime=con.query("SELECT * FROM player_character_runtime WHERE character_id=?",id) { row -> obj("currentHp" to row.getInt("current_hp"),"stateVersion" to row.getLong("state_version"),"resources" to Json.parseToJsonElement(row.getString("resources")),"conditions" to Json.parseToJsonElement(row.getString("conditions")),"temporaryEffects" to Json.parseToJsonElement(row.getString("temporary_effects"))) }.single()
        return JsonObject(base.first+mapOf("rulesetProfileId" to JsonPrimitive(draft.profileId),"rulesetDigest" to JsonPrimitive(draft.profileDigest),"selections" to Json { encodeDefaults = true }.encodeToJsonElement(NarrowDraft.serializer(),draft),"species" to obj("id" to draft.speciesId,"name" to base.third.label(draft.speciesId)),"origin" to obj("id" to draft.originId,"name" to base.third.label(draft.originId)),"characterClass" to obj("id" to draft.classId,"name" to base.third.label(draft.classId)),"trait" to obj("id" to draft.traitId,"name" to base.third.label(draft.traitId)),"level" to JsonPrimitive(draft.level),"calculated" to calculation.calculated!!,"runtime" to runtime,"inventory" to json(inventory)))
    }
    fun list(owner:UUID):List<JsonObject> = db.read { con ->
        con.query("SELECT id FROM player_characters WHERE user_id=? ORDER BY created_at DESC",owner) { it.getObject(1,UUID::class.java) }.map { id ->
            val sheet=get(con,owner,id)
            JsonObject(sheet.filterKeys { it in setOf("id","name","species","origin","characterClass","level","updatedAt","rulesetProfileId") })
        }
    }
    fun rename(owner:UUID,id:UUID,name:String):JsonObject = db.transaction { con ->
        if(name.trim().isEmpty() || name.length>80 || name.any(Char::isISOControl)) throw InvalidDraft(listOf(DraftIssue("INVALID_NAME","name","Use 1 to 80 printable characters.")))
        if(con.execute("UPDATE player_characters SET name=?,updated_at=now() WHERE id=? AND user_id=?",name.trim(),id,owner)==0) throw ApiException(404,"NOT_FOUND","Character not found.")
        con.execute("UPDATE player_character_runtime SET state_version=state_version+1 WHERE character_id=?",id)
        get(con,owner,id)
    }
    fun delete(owner:UUID,id:UUID) { db.transaction { con ->
        if(con.execute("DELETE FROM player_characters WHERE id=? AND user_id=?",id,owner)==0) throw ApiException(404,"NOT_FOUND","Character not found.")
    } }
}

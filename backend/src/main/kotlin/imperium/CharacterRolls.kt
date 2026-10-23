package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.sql.Connection
import java.time.Instant
import java.util.UUID

@Serializable data class RollRequest(
    val requestId: String, val rollId: String, val profileId: String, val profileDigest: String,
    val expectedStateVersion: Long, val ability: String? = null, val parentResultId: String? = null,
    val visibility: String = "PRIVATE", val confirmConsumption: Boolean = false
)

/** Runtime authorization is independent of the display-only character projection. */
class CharacterRolls(
    private val db: Database, private val characters: ProductionCharacters,
    private val dice: DiceEngine = DiceEngine()
) {
    private fun fail(code: String, message: String, status: Int = 422): Nothing = throw ApiException(status,code,message)
    private fun requestUuid(value: String): UUID = try { UUID.fromString(value) }
        catch (_: IllegalArgumentException) { fail("INVALID_CONTEXT","A valid request/result UUID is required.") }
    private fun own(con: Connection, owner: UUID, character: UUID, lock: Boolean = false) {
        val suffix = if(lock) " FOR UPDATE OF c,r" else ""
        if(con.query("SELECT c.id FROM player_characters c JOIN player_character_runtime r ON r.character_id=c.id WHERE c.id=? AND c.user_id=?$suffix",character,owner) { it.getString(1) }.isEmpty())
            fail("CHARACTER_NOT_FOUND","Character not found.",404)
    }
    private fun load(con: Connection, owner: UUID, character: UUID): Pair<JsonObject,NarrowRules> {
        val sheet = characters.get(con,owner,character)
        val snapshot = con.query("SELECT snapshot FROM ruleset_profiles WHERE id=? AND digest=?",sheet.text("rulesetProfileId"),sheet.text("rulesetDigest")) { Json.parseToJsonElement(it.getString(1)).jsonObject }.single()
        val rules = NarrowRules(snapshot)
        if(mapOf("di-phb-1.0-narrow-v1" to "narrow-kotlin-v1", "di-phb-1.0-tier1-v1" to "phb-tier1-kotlin-v1", "di-phb-1.0-tier1-v2" to "phb-tier1-kotlin-v1", "di-phb-1.0-tier1-v3" to "phb-tier1-kotlin-v1", "di-phb-1.0-tier1-v4" to "phb-tier1-kotlin-v1", "di-phb-1.0-tier1-v5" to "phb-tier1-kotlin-v1", "di-phb-1.0-tier1-v6" to "phb-tier1-kotlin-v1")[rules.id] != rules.spec.text("engineVersion"))
            fail("RULESET_MISMATCH","Runtime rolling is not supported for this ruleset.",409)
        return sheet to rules
    }
    private fun blockedState(sheet: JsonObject): Boolean {
        val runtime = sheet.getValue("runtime").jsonObject
        return runtime.arr("conditions").isNotEmpty() || runtime.arr("temporaryEffects").isNotEmpty()
    }
    private fun item(definition: JsonObject, rules: NarrowRules): String? {
        val source = definition.getValue("source").jsonObject.getValue("ref").jsonObject.text("id")
        return source.takeIf { rules.record(it).text("kind") == "weapon" }
    }
    private fun consumes(item: String?, rules: NarrowRules) = item != null && rules.data(item).objects("modes").singleOrNull()?.containsKey("consumption") == true
    private fun finesse(item: String?, rules: NarrowRules) = item != null && rules.data(item).getValue("abilityBinding").jsonObject.text("attack") == "finesse"
    private fun quantity(sheet: JsonObject, item: String) = sheet.objects("inventory").singleOrNull { it.text("definitionId") == item }?.num("quantity") ?: 0
    private fun actionId(definition: JsonObject) = (definition["action"] as? JsonObject)?.getValue("ref")?.jsonObject?.text("id")

    fun options(owner: UUID, character: UUID): JsonObject = db.read { con ->
        own(con,owner,character)
        val (sheet,rules) = load(con,owner,character)
        val options = sheet.getValue("calculated").jsonObject.objects("rollDefinitions").map { definition ->
            val item = item(definition,rules)
            val count = item?.let { quantity(sheet,it) }
            val component = definition.objects("components").single()
            val unavailable = when {
                blockedState(sheet) -> "Current conditions or temporary effects require unsupported runtime adjudication."
                count != null && count < 1 -> if(consumes(item,rules)) "You have no ${rules.label(item!!)} remaining." else "This item is not available."
                else -> null
            }
            obj("id" to definition.text("id"),"label" to definition.text("label"),"category" to definition.text("category"),
                "actionId" to actionId(definition),"itemId" to item,"available" to (unavailable == null),"reason" to unavailable,
                "consumes" to consumes(item,rules),"quantity" to count,"abilities" to if(finesse(item,rules)) listOf("strength","dexterity") else emptyList<String>(),
                "groups" to component.arr("groups"),"modifier" to component.objects("modifiers").sumOf { it.num("value") })
        }
        obj("profileId" to rules.id,"profileDigest" to rules.digest,"stateVersion" to sheet.getValue("runtime").jsonObject.getValue("stateVersion"),"options" to options)
    }

    fun execute(owner: UUID, character: UUID, request: RollRequest): JsonObject {
        val requestId = requestUuid(request.requestId)
        val requestDigest = sha(canonicalJson(obj("characterId" to character.toString(),"request" to Json.encodeToJsonElement(RollRequest.serializer(),request))))
        return db.transaction { con ->
            // Serialize the owner/request key even when competing requests target different characters.
            con.query("SELECT pg_advisory_xact_lock(hashtextextended(?,0))","$owner:$requestId") { 0 }
            own(con,owner,character,lock=true)
            val previous = con.query("SELECT request_digest,result FROM character_rolls WHERE user_id=? AND request_id=?",owner,requestId) { it.getString(1) to Json.parseToJsonElement(it.getString(2)).jsonObject }.singleOrNull()
            if(previous != null) {
                if(previous.first != requestDigest) fail("IDEMPOTENCY_CONFLICT","This request ID was already used with different roll choices.",409)
                return@transaction previous.second // replay precedes state/resource checks
            }
            val (sheet,rules) = load(con,owner,character)
            if(request.profileId != rules.id || request.profileDigest != rules.digest)
                fail("RULESET_MISMATCH","Refresh the character's pinned ruleset before rolling.",409)
            val before = sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long
            if(request.expectedStateVersion != before) fail("STATE_CONFLICT","Character state changed. Refresh before rolling.",409)
            if(request.visibility != "PRIVATE") fail("INVALID_CONTEXT","Only private owner-visible rolls are supported.")
            if(blockedState(sheet)) fail("ACTION_NOT_AVAILABLE","Current conditions or temporary effects are not supported by this runtime adapter.")
            val calculation = sheet.getValue("calculated").jsonObject
            val baseline = calculation.objects("rollDefinitions").singleOrNull { it.text("id") == request.rollId }
                ?: fail("ROLL_NOT_AVAILABLE","This roll is not available for the current character.")
            val item = item(baseline,rules)
            val action = actionId(baseline)
            val category = baseline.text("category")
            if(item != null && quantity(sheet,item) < 1)
                fail(if(consumes(item,rules)) "RESOURCE_EXHAUSTED" else "ACTION_NOT_AVAILABLE",if(consumes(item,rules)) "You have no ${rules.label(item!!)} remaining." else "The required weapon is unavailable.")
            val mutates = consumes(item,rules)
            if(mutates && (!request.confirmConsumption || category != "damage")) fail("INVALID_CONTEXT","Confirm consuming one ${rules.label(item!!)} to execute its base damage roll.")
            if(!mutates && request.confirmConsumption) fail("INVALID_CONTEXT","This roll does not consume an item.")
            val actionView = calculation.objects("actions").singleOrNull { it.text("id") == action }
            val defaultAbility = (actionView?.get("ability") as? JsonPrimitive)?.contentOrNull
            if(request.ability != null && (!finesse(item,rules) || request.ability !in listOf("strength","dexterity")))
                fail("INVALID_CONTEXT","Ability substitution is permitted only for this weapon's Finesse choices.")
            val ability = request.ability ?: defaultAbility
            val parent = request.parentResultId?.let { value ->
                if(category != "damage" || mutates) fail("INVALID_CONTEXT","Only weapon damage may reference an attack result.")
                con.query("SELECT result FROM character_rolls WHERE id=? AND character_id=? AND user_id=?",requestUuid(value),character,owner) { Json.parseToJsonElement(it.getString(1)).jsonObject }.singleOrNull()
                    ?: fail("INVALID_CONTEXT","The parent attack is not available for this character.")
            }
            if(parent != null && (parent.text("rollType") != "attack" || parent.text("rulesetDigest") != rules.digest || parent["actionId"] != json(action) || parent.getValue("context").jsonObject["ability"] != json(ability)))
                fail("INVALID_CONTEXT","Damage must use the same weapon and ability as its parent attack.")
            if(parent != null && calculation.objects("rollDefinitions").none { it.text("category")=="attack" && it.text("id")==parent.text("requestedRollId") })
                fail("INVALID_CONTEXT","The parent attack belongs to an earlier character level; roll a new attack.")
            val baseComponent = baseline.objects("components").single()
            val baseModifier = baseComponent.objects("modifiers").sumOf { it.num("value") }
            val modifiers = calculation.getValue("attributeModifiers").jsonObject
            val modifier = baseModifier + if(finesse(item,rules)) modifiers.num(ability!!) - modifiers.num(defaultAbility!!) else 0
            val groups = baseComponent.objects("groups").map { DiceGroup(it.num("count"),it.num("sides")) }
            val resolved = dice.resolve(groups,modifier)
            val natural = if(category != "damage") resolved.groups.single().kept.single() else null
            val resultId = UUID.randomUUID()
            val after = before + if(mutates) 1 else 0
            val context = obj("characterLevel" to sheet.num("level"),"ability" to ability,"parentResultId" to request.parentResultId,"mode" to "baseline",
                "targetResolution" to "MANUAL","criticalDamage" to "NOT_APPLIED","consumptionConfirmed" to request.confirmConsumption)
            val definitionId = UUID.nameUUIDFromBytes("${baseline.text("id")}:$before:${canonicalJson(context)}".toByteArray()).toString()
            val component = JsonObject(baseComponent + mapOf("modifiers" to json(listOf(obj("id" to "resolved","value" to modifier,
                "source" to baseline.getValue("source"),"label" to "Server-calculated modifier","contextual" to (request.ability != null))))))
            val snapshot = JsonObject(baseline.getValue("snapshot").jsonObject + mapOf("stateVersion" to json(before),"contextDigest" to json(sha(canonicalJson(context)))))
            val runtimeAction = (baseline["action"] as? JsonObject)?.let {
                val execution = parent?.getValue("definition")?.jsonObject?.get("action")?.jsonObject?.get("executionId") ?: json(resultId.toString())
                JsonObject(it + mapOf("executionId" to execution))
            }
            val definition = JsonObject(baseline + mapOf("id" to json(definitionId),"components" to json(listOf(component)),"snapshot" to snapshot) +
                (runtimeAction?.let { mapOf("action" to it) } ?: emptyMap()))
            val damageTypeId = (component["damageType"] as? JsonObject)?.text("id")
            val grenade = if(mutates) {
                val save = actionView!!.getValue("save").jsonObject
                val outcomes = save.getValue("outcomes").jsonObject.mapValues { (_,value) ->
                    val outcome = value.jsonObject
                    val fraction = outcome.getValue("damageMultiplier").jsonObject
                    val numerator=resolved.total*fraction.num("numerator");val denominator=fraction.num("denominator")
                    when(outcome.text("rounding")) {
                        "floor" -> json(Math.floorDiv(numerator,denominator))
                        "exact_fraction" -> if(numerator%denominator==0) json(numerator/denominator) else json("$numerator/$denominator")
                        else -> error("Unsupported damage rounding policy")
                    }
                }
                obj("saveAttribute" to save.text("attribute"),"saveDc" to actionView.num("saveDc"),"area" to actionView.getValue("area"),"outcomes" to outcomes,
                    "rule" to save,"application" to (rules.data(item!!).objects("modes").single().objects("manualRules").joinToString(" ") { it.text("text") }+" Target-by-target application currently requires manual adjudication."))
            } else null
            val now = Instant.now()
            val result = obj("request" to Json { encodeDefaults = true }.encodeToJsonElement(RollRequest.serializer(),request),"id" to resultId.toString(),"requestId" to requestId.toString(),"userId" to owner.toString(),"characterId" to character.toString(),"characterName" to sheet.text("name"),
                "rulesetProfileId" to rules.id,"rulesetDigest" to rules.digest,"engineVersion" to "production-dice-v1",
                "actionId" to action,"requestedRollId" to request.rollId,"rollDefinitionId" to definitionId,"definition" to definition,
                "label" to baseline.text("label"),"rollType" to category,"dice" to Json.encodeToJsonElement(DiceResolution.serializer(),resolved),"total" to resolved.total,
                "naturalResult" to natural,"criticalCandidate" to (category == "attack" && natural == baseline.getValue("critical").jsonObject.num("threshold")),
                "naturalOne" to (category == "attack" && natural == 1),"damageType" to damageTypeId?.let { obj("id" to it,"name" to rules.label(it)) },
                "visibility" to request.visibility,"timestamp" to now.toString(),"parentResultId" to request.parentResultId,"context" to context,
                "stateVersionBefore" to before,"stateVersionAfter" to after,"grenade" to grenade,
                "consumption" to if(mutates) obj("itemId" to item,"quantity" to 1,"remaining" to quantity(sheet,item!!)-1) else null)
            if(mutates) {
                check(con.execute("UPDATE player_character_inventory SET quantity=quantity-1 WHERE character_id=? AND definition_id=? AND quantity>=1",character,item)==1)
                if(con.execute("UPDATE player_character_runtime SET state_version=state_version+1 WHERE character_id=? AND state_version=?",character,before)!=1)
                    fail("STATE_CONFLICT","Character state changed. Refresh before rolling.",409)
                con.execute("UPDATE player_characters SET updated_at=now() WHERE id=?",character)
            }
            con.execute("""INSERT INTO character_rolls(id,user_id,character_id,request_id,request_digest,profile_id,profile_digest,roll_definition_id,action_id,roll_type,visibility,parent_result_id,state_version_before,state_version_after,result,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?::jsonb,?)""",resultId,owner,character,requestId,requestDigest,rules.id,rules.digest,uuid(definitionId),action,category,request.visibility,request.parentResultId?.let(::requestUuid),before,after,result.toString(),java.sql.Timestamp.from(now))
            result
        }
    }

    /** Bounded newest-first snapshot history; never recalculates historical totals. */
    fun history(owner: UUID, character: UUID, limit: Int = 25): JsonObject = db.read { con ->
        if(limit !in 1..50) fail("INVALID_CONTEXT","History limit must be between 1 and 50.",400)
        own(con,owner,character)
        val rows = con.query("SELECT result FROM character_rolls WHERE character_id=? AND user_id=? ORDER BY created_at DESC,id DESC LIMIT ?",character,owner,limit+1) { Json.parseToJsonElement(it.getString(1)).jsonObject }
        obj("items" to rows.take(limit),"limit" to limit,"hasMore" to (rows.size > limit))
    }
}

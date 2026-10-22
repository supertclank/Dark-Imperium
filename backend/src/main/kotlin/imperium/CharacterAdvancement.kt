package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.sql.Connection
import java.util.UUID

@Serializable data class AdvanceRequest(val requestId:String, val expectedStateVersion:Long, val destinationLevel:Int, val choices:Map<String,List<String>> = emptyMap())

/** Creation packages are validated from initial selections, but never reissued on advancement. */
class CharacterAdvancement(private val db:Database,private val characters:ProductionCharacters) {
    private fun own(con:Connection,owner:UUID,id:UUID,write:Boolean) {
        val lock=if(write) "UPDATE" else "SHARE"
        if(con.query("SELECT c.id FROM player_characters c JOIN player_character_runtime r ON r.character_id=c.id WHERE c.id=? AND c.user_id=? FOR $lock OF c,r",id,owner) { it.getString(1) }.isEmpty()) throw ApiException(404,"NOT_FOUND","Character not found.")
    }
    private fun pinned(con:Connection,sheet:JsonObject)=NarrowRules(con.query("SELECT snapshot FROM ruleset_profiles WHERE id=? AND digest=?",sheet.text("rulesetProfileId"),sheet.text("rulesetDigest")) { Json.parseToJsonElement(it.getString(1)).jsonObject }.single())
    private fun draft(sheet:JsonObject)=Json.decodeFromJsonElement(NarrowDraft.serializer(),sheet.getValue("selections"))
    private fun config(rules:NarrowRules,d:NarrowDraft)=rules.spec.objects("pathConfigurations").singleOrNull { it.text("speciesId")==d.speciesId && it.text("originId")==d.originId && it.text("classId")==d.classId && it.num("level")==d.level }
    private fun required(rules:NarrowRules,d:NarrowDraft):List<String> = config(rules,d.copy(level=d.level+1))?.strings("choices").orEmpty()-config(rules,d)?.strings("choices").orEmpty().toSet()
    private fun blockers(rules:NarrowRules,d:NarrowDraft):List<JsonObject> {
        if(d.level>=3) return listOf(obj("code" to "LEVEL_CAP","message" to "Advancement beyond level 3 is unavailable."))
        if(rules.id !in setOf("di-phb-1.0-tier1-v2","di-phb-1.0-tier1-v3") || config(rules,d.copy(level=d.level+1))==null) return listOf(obj("code" to "PATH_NOT_CERTIFIED","message" to "The pinned ruleset does not certify the next level for this path. No profile migration is performed."))
        return emptyList()
    }
    private fun destination(sheet:JsonObject,rules:NarrowRules,request:AdvanceRequest):Pair<NarrowDraft,JsonObject> {
        val current=draft(sheet)
        if(request.expectedStateVersion!=sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long) throw ApiException(409,"STATE_CONFLICT","Character changed. Refresh the preview.")
        if(request.destinationLevel!=current.level+1 || request.destinationLevel !in 2..3) throw ApiException(422,"INVALID_TRANSITION","Advance exactly one level, through level 3 only.")
        val blocked=blockers(rules,current)
        if(blocked.isNotEmpty()) throw ApiException(422,blocked.first().text("code"),blocked.first().text("message"))
        val allowed=required(rules,current)
        if(request.choices.keys.any { it !in allowed }) throw ApiException(422,"INVALID_ADVANCEMENT_CHOICE","Only newly required level choices may be supplied; existing choices cannot be changed.")
        val next=current.copy(level=request.destinationLevel,answers=current.answers+request.choices)
        val validation=rules.validate(next,sheet.text("id"))
        if(validation.errors.isNotEmpty()) throw InvalidDraft(validation.errors)
        val calculated=validation.calculated!!;val old=sheet.getValue("calculated").jsonObject
        if(calculated.getValue("attributes").jsonObject["constitution"]!=old.getValue("attributes").jsonObject["constitution"]) throw ApiException(422,"PHB_RULE_014","Constitution changes during advancement require an approved HP policy.")
        val oldResources=old.objects("resources").associateBy { it.text("key") }
        // No currently certified transition grants a new resource. Do not invent initial uses
        // or reconcile changed maxima for a future feature without a pinned approved policy.
        if(calculated.objects("resources").any { oldResources[it.text("key")]!=it }) throw ApiException(422,"RESOURCE_POLICY_REQUIRED","New or changed resources require a certified initial-use policy.")
        return next to calculated
    }
    private fun previewView(sheet:JsonObject,next:NarrowDraft,calculated:JsonObject):JsonObject {
        val old=sheet.getValue("calculated").jsonObject
        val prior=old.objects("features").map { it.text("id") }.toSet()
        return obj("fromLevel" to sheet.num("level"),"toLevel" to next.level,"maximumHpBefore" to old.num("maximumWounds"),"maximumHpAfter" to calculated.num("maximumWounds"),"currentHp" to sheet.getValue("runtime").jsonObject.num("currentHp"),"newFeatures" to calculated.objects("features").filter { it.text("id") !in prior },"subclass" to calculated["subclass"],"proficiencyBonus" to calculated.num("proficiencyBonus"),"profileId" to sheet.text("rulesetProfileId"),"profileDigest" to sheet.text("rulesetDigest"))
    }
    fun readiness(owner:UUID,id:UUID):JsonObject=db.transaction { con ->
        own(con,owner,id,false);val sheet=characters.get(con,owner,id);val rules=pinned(con,sheet);val d=draft(sheet)
        val blocked=blockers(rules,d);val keys=required(rules,d);val version=sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long
        val preview=if(blocked.isEmpty() && keys.isEmpty()) { val (next,c)=destination(sheet,rules,AdvanceRequest(UUID.randomUUID().toString(),version,d.level+1));previewView(sheet,next,c) } else null
        obj("available" to blocked.isEmpty(),"currentLevel" to d.level,"nextLevel" to if(blocked.isEmpty()) d.level+1 else null,"stateVersion" to version,"requiredChoices" to rules.profile().objects("choices").filter { it.text("id") in keys },"blockers" to blocked,"preview" to preview)
    }
    fun preview(owner:UUID,id:UUID,request:AdvanceRequest):JsonObject=db.transaction { con ->
        own(con,owner,id,false);val sheet=characters.get(con,owner,id);val (next,c)=destination(sheet,pinned(con,sheet),request);previewView(sheet,next,c)
    }
    fun advance(owner:UUID,id:UUID,request:AdvanceRequest):JsonObject {
        val requestId=uuid(request.requestId)
        val digest=sha(canonicalJson(obj("characterId" to id.toString(),"request" to Json.encodeToJsonElement(AdvanceRequest.serializer(),request))))
        return db.transaction { con ->
            con.query("SELECT pg_advisory_xact_lock(hashtextextended(?,0))","advance:$owner:$requestId") { 0 }
            own(con,owner,id,true)
            val prior=con.query("SELECT request_digest,result FROM character_advancements WHERE user_id=? AND request_id=?",owner,requestId) { it.getString(1) to Json.parseToJsonElement(it.getString(2)).jsonObject }.singleOrNull()
            if(prior!=null) {
                if(prior.first!=digest) throw ApiException(409,"IDEMPOTENCY_CONFLICT","Request ID already used with different advancement choices.")
                return@transaction prior.second
            }
            val sheet=characters.get(con,owner,id);val (next,c)=destination(sheet,pinned(con,sheet),request)
            for((key,options) in request.choices) con.execute("INSERT INTO player_character_choices(character_id,choice_id,option_ids) VALUES (?,?,?::jsonb)",id,key,json(options).toString())
            con.execute("UPDATE player_characters SET level=?,updated_at=now() WHERE id=?",next.level,id)
            check(con.execute("UPDATE player_character_runtime SET state_version=state_version+1 WHERE character_id=? AND state_version=?",id,request.expectedStateVersion)==1)
            val result=obj("advancementId" to UUID.randomUUID().toString(),"preview" to previewView(sheet,next,c),"character" to characters.get(con,owner,id))
            con.execute("INSERT INTO character_advancements(id,user_id,character_id,request_id,request_digest,from_level,to_level,state_version_before,state_version_after,result) VALUES (?,?,?,?,?,?,?,?,?,?::jsonb)",uuid(result.text("advancementId")),owner,id,requestId,digest,sheet.num("level"),next.level,request.expectedStateVersion,request.expectedStateVersion+1,result.toString())
            result
        }
    }
}

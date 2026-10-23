package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.sql.Connection
import java.util.UUID

@Serializable data class AdvanceRequest(val requestId:String, val expectedStateVersion:Long, val destinationLevel:Int, val choices:Map<String,List<String>> = emptyMap(),val confirmProfileUpgrade:Boolean=false)

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
    private fun contract(source:NarrowRules,destination:NarrowRules,d:NarrowDraft):JsonObject? {
        val contracts=destination.spec.objects("upgradeContracts")+listOfNotNull(destination.spec["upgradeContract"] as? JsonObject)
        return contracts.singleOrNull { c -> source.id==c.text("fromProfile") && source.digest==c.text("fromDigest") && destination.id==c.text("toProfile") && d.level==c.num("fromLevel") && d.level+1==c.num("toLevel") &&
            (if(c.containsKey("speciesIds")) d.speciesId in c.strings("speciesIds") else d.speciesId==c.text("speciesId")) &&
            (if(c.containsKey("classIds")) d.classId in c.strings("classIds") else d.classId==c.text("classId")) && config(destination,d.copy(level=d.level+1))!=null }
    }
    private fun target(rules:NarrowRules,d:NarrowDraft):NarrowRules = listOf(NarrowRules.tier5(),NarrowRules.tier6(),NarrowRules.tier8()).firstOrNull { contract(rules,it,d)!=null } ?: rules
    private fun blockers(rules:NarrowRules,d:NarrowDraft):List<JsonObject> {
        val next=target(rules,d)
        if(d.level>=5 || (d.level>=4 && next.spec.arr("levels").none { it.jsonPrimitive.int==5 }) || (d.level>=3 && next.id==rules.id && Level4Rules.policy(rules)==null)) return listOf(obj("code" to "LEVEL_CAP","message" to "No further level is certified for this pinned profile."))
        if(config(next,d.copy(level=d.level+1))==null) return listOf(obj("code" to "PATH_NOT_CERTIFIED","message" to "The next level is not certified for this path."))
        return emptyList()
    }
    private fun compatible(sheet:JsonObject,source:NarrowRules,destination:NarrowRules) {
        val d=draft(sheet)
        if(contract(source,destination,d)==null) throw ApiException(422,"UPGRADE_NOT_CERTIFIED","No matching upgrade contract exists.")
        val check=destination.validate(d.copy(profileId=destination.id,profileDigest=destination.digest),sheet.text("id"))
        if(check.errors.isNotEmpty()) throw ApiException(422,"UPGRADE_INCOMPATIBLE","Existing selections are incompatible with the destination profile.")
        val before=sheet.getValue("calculated").jsonObject;val after=check.calculated!!
        for(key in listOf("attributes","attributeModifiers","maximumWounds","defence","movement","initiative","saves","skills","inventory","resources","subclass","features")) if(before[key]!=after[key]) throw ApiException(422,"UPGRADE_INCOMPATIBLE","Existing $key would change before advancement.")
        fun actionValues(c:JsonObject)=c.objects("actions").map { JsonObject(it.filterKeys { k->k!="damageRollId" }) }
        if(actionValues(before)!=actionValues(after)) throw ApiException(422,"UPGRADE_INCOMPATIBLE","Existing actions would change before advancement.")
        val known=before.objects("resources").associateBy { it.text("key") }
        for((key,value) in sheet.getValue("runtime").jsonObject.getValue("resources").jsonObject) {
            val definition=known[key] ?: throw ApiException(422,"UPGRADE_INCOMPATIBLE","Unknown runtime resource.")
            if(value.jsonObject.num("maximum")!=definition.num("maximum")) throw ApiException(422,"UPGRADE_INCOMPATIBLE","Resource maximum changed.")
        }
    }
    private fun destination(sheet:JsonObject,source:NarrowRules,request:AdvanceRequest):Pair<NarrowDraft,JsonObject> {
        val current=draft(sheet);val rules=target(source,current)
        if(rules.id!=source.id) { if(!request.confirmProfileUpgrade) throw ApiException(422,"PROFILE_UPGRADE_CONFIRMATION_REQUIRED","Confirm the validated profile upgrade before advancing.");compatible(sheet,source,rules) }
        if(request.expectedStateVersion!=sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long) throw ApiException(409,"STATE_CONFLICT","Character changed. Refresh the preview.")
        if(request.destinationLevel!=current.level+1 || request.destinationLevel !in 2..5) throw ApiException(422,"INVALID_TRANSITION","Advance exactly one level, through certified level 5 only.")
        val blocked=blockers(source,current)
        if(blocked.isNotEmpty()) throw ApiException(422,blocked.first().text("code"),blocked.first().text("message"))
        val allowed=required(rules,current)
        if(request.choices.keys.any { it !in allowed }) throw ApiException(422,"INVALID_ADVANCEMENT_CHOICE","Only newly required level choices may be supplied; existing choices cannot be changed.")
        val next=current.copy(profileId=rules.id,profileDigest=rules.digest,level=request.destinationLevel,answers=current.answers+request.choices)
        val validation=rules.validate(next,sheet.text("id"))
        if(validation.errors.isNotEmpty()) throw InvalidDraft(validation.errors)
        val calculated=validation.calculated!!;val old=sheet.getValue("calculated").jsonObject
        if(Level4Rules.policy(rules)==null && calculated.getValue("attributes").jsonObject["constitution"]!=old.getValue("attributes").jsonObject["constitution"]) throw ApiException(422,"PHB_RULE_014","Constitution changes during advancement require an approved HP policy.")
        val oldResources=old.objects("resources").associateBy { it.text("key") }
        // v5 initialises new source-defined resources at full uses; existing maxima cannot change.
        if(calculated.objects("resources").any { val prior=oldResources[it.text("key")]; (prior!=null && prior!=it) || (prior==null && Level4Rules.policy(rules)==null) }) throw ApiException(422,"RESOURCE_POLICY_REQUIRED","New or changed resources require a certified initial-use policy.")
        return next to calculated
    }
    private fun previewView(sheet:JsonObject,next:NarrowDraft,calculated:JsonObject):JsonObject {
        val old=sheet.getValue("calculated").jsonObject
        val prior=old.objects("features").map { it.text("id") }.toSet()
        return obj("fromLevel" to sheet.num("level"),"toLevel" to next.level,"maximumHpBefore" to old.num("maximumWounds"),"maximumHpAfter" to calculated.num("maximumWounds"),"currentHpBefore" to sheet.getValue("runtime").jsonObject.num("currentHp"),"currentHp" to Level4Rules.currentHp(sheet.getValue("runtime").jsonObject.num("currentHp"),calculated.num("maximumWounds")),"newFeatures" to calculated.objects("features").filter { it.text("id") !in prior },"subclass" to calculated["subclass"],"proficiencyBonus" to calculated.num("proficiencyBonus"),"profileId" to next.profileId,"profileDigest" to next.profileDigest,"before" to old,"after" to calculated,"selection" to calculated["advancementSelection"],"newResources" to calculated.objects("resources").filter { r -> old.objects("resources").none { it.text("key")==r.text("key") } })
    }
    fun readiness(owner:UUID,id:UUID):JsonObject=db.transaction { con ->
        own(con,owner,id,false);val sheet=characters.get(con,owner,id);val rules=pinned(con,sheet);val d=draft(sheet)
        val targetRules=target(rules,d);val blocked=blockers(rules,d);val keys=required(targetRules,d);val version=sheet.getValue("runtime").jsonObject.getValue("stateVersion").jsonPrimitive.long
        val preview=if(blocked.isEmpty() && keys.isEmpty() && targetRules.id==rules.id) { val (next,c)=destination(sheet,rules,AdvanceRequest(UUID.randomUUID().toString(),version,d.level+1));previewView(sheet,next,c) } else null
        obj("available" to blocked.isEmpty(),"currentLevel" to d.level,"nextLevel" to if(blocked.isEmpty()) d.level+1 else null,"stateVersion" to version,"requiresProfileUpgrade" to (targetRules.id!=rules.id),"upgradeContract" to (if(targetRules.id!=rules.id) contract(rules,targetRules,d) else null),"level4Choice" to (if(d.level==3 && blocked.isEmpty()) Level4Rules.policy(targetRules)?.let { policy -> JsonObject(policy+mapOf("options" to json(policy.objects("options").filter { option -> val talent=option["talentId"]?.jsonPrimitive?.content;talent==null || Level4Rules.eligible(targetRules.data(talent)["requirements"] as? JsonObject,setOf(d.speciesId,d.originId,d.classId,d.traitId)) }))) } else null),"ownedTalentIds" to sheet.getValue("calculated").jsonObject.objects("features").filter { it.text("id").startsWith("di.feature.talent.") }.map { it.text("id") },"requiredChoices" to targetRules.profile().objects("choices").filter { it.text("id") in keys },"blockers" to blocked,"preview" to preview)
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
            con.execute("UPDATE player_characters SET level=?,profile_id=?,profile_digest=?,updated_at=now() WHERE id=?",next.level,next.profileId,next.profileDigest,id)
            val runtime=sheet.getValue("runtime").jsonObject;val resources=runtime.getValue("resources").jsonObject.toMutableMap()
            for(r in c.objects("resources")) if(r.text("key") !in resources) resources[r.text("key")]=obj("sourceId" to r.text("sourceId"),"remaining" to r.num("maximum"),"maximum" to r.num("maximum"),"recovery" to r.text("recovery"),"automation" to r.text("automation"))
            con.execute("UPDATE player_character_runtime SET current_hp=?,resources=?::jsonb WHERE character_id=?",Level4Rules.currentHp(runtime.num("currentHp"),c.num("maximumWounds")),JsonObject(resources).toString(),id)
            if(next.profileId!=sheet.text("rulesetProfileId")) con.execute("INSERT INTO character_profile_upgrades(character_id,from_profile,from_digest,to_profile,to_digest,request_id,contract_version) VALUES (?,?,?,?,?,?,?)",id,sheet.text("rulesetProfileId"),sheet.text("rulesetDigest"),next.profileId,next.profileDigest,requestId,contract(pinned(con,sheet),characters.rulesFor(next.profileId),draft(sheet))!!.text("version"))
            check(con.execute("UPDATE player_character_runtime SET state_version=state_version+1 WHERE character_id=? AND state_version=?",id,request.expectedStateVersion)==1)
            val result=obj("advancementId" to UUID.randomUUID().toString(),"preview" to previewView(sheet,next,c),"character" to characters.get(con,owner,id))
            con.execute("INSERT INTO character_advancements(id,user_id,character_id,request_id,request_digest,from_level,to_level,state_version_before,state_version_after,result) VALUES (?,?,?,?,?,?,?,?,?,?::jsonb)",uuid(result.text("advancementId")),owner,id,requestId,digest,sheet.num("level"),next.level,request.expectedStateVersion,request.expectedStateVersion+1,result.toString())
            result
        }
    }
}

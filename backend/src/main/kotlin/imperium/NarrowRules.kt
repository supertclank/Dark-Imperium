package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.security.MessageDigest
import java.util.UUID

@Serializable data class InventorySelection(val definitionId: String, val quantity: Int, val equipped: Boolean = false)
@Serializable data class NarrowDraft(
    val profileId: String = "", val profileDigest: String = "", val requestId: String = "",
    val name: String = "", val speciesId: String = "", val originId: String = "", val classId: String = "",
    val level: Int = 1, val traitId: String = "", val attributes: Map<String,Int> = emptyMap(),
    val answers: Map<String,List<String>> = emptyMap(), val packageChoices: Map<String,String> = emptyMap(),
    val inventory: List<InventorySelection> = emptyList()
)
@Serializable data class DraftIssue(val code: String, val field: String, val message: String)
@Serializable data class DraftValidation(val status: String, val errors: List<DraftIssue>, val abilityPreview: JsonObject? = null, val calculated: JsonObject? = null)
class InvalidDraft(val issues: List<DraftIssue>) : RuntimeException("Character validation failed")

internal fun json(value: Any?): JsonElement = when(value) {
    null -> JsonNull
    is JsonElement -> value
    is String -> JsonPrimitive(value)
    is Number -> JsonPrimitive(value)
    is Boolean -> JsonPrimitive(value)
    is Map<*,*> -> JsonObject(value.entries.associate { it.key.toString() to json(it.value) })
    is Iterable<*> -> JsonArray(value.map(::json))
    else -> error("Unsupported JSON value: ${value::class}")
}
internal fun obj(vararg pairs: Pair<String,Any?>) = json(mapOf(*pairs)).jsonObject
internal fun JsonObject.text(key: String) = getValue(key).jsonPrimitive.content
internal fun JsonObject.num(key: String) = getValue(key).jsonPrimitive.int
internal fun JsonObject.arr(key: String) = getValue(key).jsonArray
internal fun JsonObject.objects(key: String) = (get(key) as? JsonArray)?.map { it.jsonObject } ?: emptyList()
internal fun JsonObject.strings(key: String) = arr(key).map { it.jsonPrimitive.content }
internal fun canonicalJson(e: JsonElement): String = when(e) {
    is JsonObject -> e.toSortedMap().entries.joinToString(",","{","}") { JsonPrimitive(it.key).toString()+":"+canonicalJson(it.value) }
    is JsonArray -> e.joinToString(",","[","]", transform=::canonicalJson)
    else -> e.toString()
}
internal fun sha(value: String) = MessageDigest.getInstance("SHA-256").digest(value.toByteArray(Charsets.UTF_8)).joinToString("") { "%02x".format(it) }

/** The immutable snapshot supplies all exposed choices and mechanical inputs. */
class NarrowRules(val bundle: JsonObject) {
    val digest = bundle.text("digest")
    val payload = bundle.getValue("payload").jsonObject
    val spec = payload.getValue("spec").jsonObject
    val id = spec.text("id")
    val records = payload.getValue("records").jsonObject
    val kit = payload.getValue("package").jsonObject
    val attributes = spec.strings("attributes")
    private val tier1 = spec.text("engineVersion")=="phb-tier1-kotlin-v1"
    val expanded = spec["compositionVersion"]?.jsonPrimitive?.int == 2
    private val speciesComposition = spec["speciesComposition"]?.jsonPrimitive?.boolean == true
    private val policy = spec.getValue("calculations").jsonObject
    init {
        require(sha(canonicalJson(payload)) == digest) { "Profile digest mismatch" }
        require(spec.text("engineVersion") in setOf("narrow-kotlin-v1","phb-tier1-kotlin-v1")) { "Unsupported calculation engine" }
    }
    fun record(id: String) = records.getValue(id).jsonObject
    fun data(id: String) = record(id).getValue("data").jsonObject
    private fun ref(e: JsonObject, key: String) = e.getValue(key).jsonObject.text("id")
    fun label(id: String) = record(id).text("name")
    private fun view(id: String) = obj("id" to id,"name" to label(id),"description" to record(id).text("descriptionMarkdown"))
    fun profile(): JsonObject = obj(
        "id" to id,"digest" to digest,"name" to spec.text("name"),"attributes" to attributes,"standardArray" to spec.arr("standardArray"),"levels" to spec.arr("levels"),
        "species" to spec.strings("species").map(::view),"origins" to spec.strings("origins").map(::view),"classes" to spec.strings("classes").map(::view),"traits" to spec.strings("traits").map(::view),
        "choices" to spec.strings("choices").map { key -> val d=data(key);obj("id" to key,"name" to label(key),"purpose" to d.text("purpose"),"cardinality" to d.getValue("cardinality"),"options" to d.objects("options").map { obj("id" to it.text("id"),"label" to it.text("label")) }) },
        "levelFeatures" to spec.strings("classes").flatMap { classId -> data(ref(data(classId),"progression")).objects("entries").filter { it.num("level") == 1 }.flatMap { it.objects("grants") }.filter { it.text("kind")=="feature" }.map { view(ref(it,"feature")) } },
        "package" to kit,"equipment" to spec.strings("equipment").map(::view),"armour" to spec.arr("armour"),"training" to payload.getValue("training"),"availability" to spec.arr("availability")
    ).let { base -> if(!expanded) base else JsonObject(base+mapOf("pathConfigurations" to spec.getValue("pathConfigurations"),"packages" to JsonObject(payload.getValue("packages").jsonObject.mapValues { it.value.jsonObject.getValue("display") }),"classTraining" to payload.getValue("classTraining"),"featureCatalogue" to json(records.keys.filter { record(it).text("kind")=="feature" }.map(::view)))) }
    private fun configuration(d: NarrowDraft) = spec.objects("pathConfigurations").singleOrNull { it.text("speciesId")==d.speciesId && it.text("originId")==d.originId && it.text("classId")==d.classId && it.num("level")==d.level }
    private fun choicesFor(d: NarrowDraft) = if(expanded) configuration(d)?.strings("choices").orEmpty() else spec.strings("choices")
    private fun packageFor(d: NarrowDraft) = (payload["packages"] as? JsonObject)?.get(d.classId)?.jsonObject
    private fun kitFor(d: NarrowDraft) = if(expanded) packageFor(d)?.get("display")?.jsonObject ?: obj() else kit
    private fun executableFor(d: NarrowDraft) = if(expanded) packageFor(d)?.get("executable")?.jsonObject ?: obj("steps" to emptyList<String>()) else payload.getValue("executablePackage").jsonObject
    private fun subclassFor(d: NarrowDraft): String? = choicesFor(d).filter { data(it).text("purpose")=="subclass" }.flatMap { key -> data(key).objects("options").filter { it.text("id") in d.answers[key].orEmpty() }.flatMap { it.objects("grants") }.filter { it.text("kind")=="select" }.map { ref(it,"content") } }.singleOrNull()
    private fun featureView(key: String): JsonObject {
        val basic=obj("id" to key,"name" to label(key),"text" to record(key).text("descriptionMarkdown"),"sources" to record(key).arr("sources"),"manual" to data(key).objects("manualRules").isNotEmpty())
        if(!expanded) return basic
        val support=(payload["featureSupport"] as? JsonObject)?.get(key)?.jsonObject
        return JsonObject(basic + (support ?: obj("classification" to if(data(key).objects("manualRules").isNotEmpty()) "MANUAL" else "AUTOMATED")))
    }
    private fun eligible(predicate: JsonObject, selected: Set<String>): Boolean = when(predicate.text("kind")) {
        "selected" -> ref(predicate,"content") in selected
        "all" -> predicate.objects("predicates").all { eligible(it,selected) }
        "any" -> predicate.objects("predicates").any { eligible(it,selected) }
        else -> false // no unapproved facts or unknown predicates may grant eligibility
    }
    private fun scores(draft: NarrowDraft): Map<String,Int> {
        val result=attributes.associateWith { draft.attributes.getValue(it) }.toMutableMap()
        for ((choice,options) in draft.answers.filterKeys { it in choicesFor(draft) && data(it).text("purpose")=="attribute" }) for(option in data(choice).objects("options").filter { it.text("id") in options }) {
            for(g in option.objects("grants")) if(g.text("kind")=="attribute_increase") result[g.text("attributeKey")]=result.getValue(g.text("attributeKey"))+g.num("amount")
        }
        if(speciesComposition) for(key in configuration(draft)?.strings("features").orEmpty()) for(e in data(key).objects("effects")) {
            val target=e.getValue("target").jsonObject.text("key")
            if(e.text("automation")=="automatic" && e.text("operation")=="add" && target.startsWith("attribute.") && target.endsWith(".score")) {
                val attribute=target.removePrefix("attribute.").removeSuffix(".score")
                result[attribute]=result.getValue(attribute)+e.getValue("value").jsonObject.num("value")
            }
        }
        return result
    }
    private fun modifiers(scores: Map<String,Int>) = scores.mapValues { (_,value) -> Math.floorDiv(value-policy.num("abilityOffset"),policy.num("abilityDivisor")) }
    fun validate(draft: NarrowDraft, actorId: String = "00000000-0000-0000-0000-000000000000"): DraftValidation {
        val errors=mutableListOf<DraftIssue>()
        fun issue(code:String,field:String,message:String) { errors+=DraftIssue(code,field,message) }
        if(draft.profileId!=id) issue("RULESET_MISMATCH","profileId","Select the supported ruleset.")
        if(draft.profileDigest!=digest) issue("STALE_PROFILE","profileDigest","The ruleset snapshot has changed. Reload the builder.")
        if(draft.name.trim().isEmpty() || draft.name.length>80 || draft.name.any(Char::isISOControl)) issue("INVALID_NAME","name","Use 1 to 80 printable characters.")
        for((field,value,group) in listOf(Triple("speciesId",draft.speciesId,"species"),Triple("originId",draft.originId,"origins"),Triple("classId",draft.classId,"classes"),Triple("traitId",draft.traitId,"traits"))) {
            if(value !in spec.strings(group)) issue(if(value.isEmpty()) "MISSING_CHOICE" else "CONTENT_NOT_SUPPORTED",field,"Choose a supported ${field.removeSuffix("Id")}.")
        }
        if(draft.level !in spec.arr("levels").map { it.jsonPrimitive.int }) issue("CONTENT_NOT_SUPPORTED","level","This level is not supported.")
        if(tier1) {
            val origin=(records[draft.originId] as? JsonObject)?.get("data") as? JsonObject
            val state=origin?.objects("originAvailability")?.singleOrNull { ref(it,"species")==draft.speciesId }?.text("state")
            if(state in setOf("RARE","LIMITED")) issue("APPROVAL_REQUIRED","originId","$state Origin requires trusted GM/campaign approval; self-service approval is unavailable.")
            if(spec.objects("certifiedPaths").none { it.text("speciesId")==draft.speciesId && it.text("originId")==draft.originId && it.text("classId")==draft.classId && it.num("level")==draft.level && it.text("traitId")==draft.traitId && (!expanded || (it["subclassId"]?.jsonPrimitive?.contentOrNull == subclassFor(draft))) }) issue("PATH_NOT_CERTIFIED","level","This complete path has not been certified.")
        }
        val selected=setOf(draft.speciesId,draft.originId,draft.classId,draft.traitId)
        for((field,key) in listOf("originId" to draft.originId,"classId" to draft.classId)) if(key in records) {
            val req=data(key)["requirements"] as? JsonObject
            if(req!=null && !eligible(req,selected)) issue("INVALID_ELIGIBILITY",field,"This choice does not meet its prerequisite.")
        }
        val baseValid=draft.attributes.keys==attributes.toSet() && draft.attributes.values.sorted()==spec.arr("standardArray").map { it.jsonPrimitive.int }.sorted()
        if(!baseValid) issue("INVALID_ABILITY_ALLOCATION","attributes","Assign every standard-array score exactly once.")
        val allowed=choicesFor(draft)
        val kit=kitFor(draft)
        if(expanded) subclassFor(draft)?.let { sub ->
            val d=data(sub);val req=d.getValue("requirements").jsonObject
            if(record(sub).text("kind")!="subclass" || ref(d,"parentClass")!=draft.classId || req.text("kind")!="level" || req.text("operator")!="gte" || req.getValue("axis").jsonObject.text("kind")!="class_level" || ref(req.getValue("axis").jsonObject,"class")!=draft.classId || draft.level<req.num("value")) issue("INVALID_SUBCLASS","answers","Subclass is not available for this class and level.")
        }
        for(key in draft.answers.keys-allowed.toSet()) issue("CONTENT_NOT_SUPPORTED","answers.$key","This choice is not in the supported profile.")
        for(key in allowed) {
            val answer=draft.answers[key].orEmpty();val d=data(key);val card=d.getValue("cardinality").jsonObject
            val code=if(d.text("purpose")=="skill") "INVALID_SKILL_SELECTION" else "INVALID_CHOICE"
            if(answer.size !in card.num("min")..card.num("max") || answer.distinct().size!=answer.size) issue(if(answer.isEmpty()) "MISSING_CHOICE" else code,"answers.$key","Choose ${card.num("min")} distinct option(s) for ${label(key)}.")
            if(answer.any { opt -> d.objects("options").none { it.text("id")==opt } }) issue(code,"answers.$key","Select only listed options.")
        }
        val expected=linkedMapOf<String,Int>()
        kit.objects("fixed").forEach { expected[ref(it,"item")]=it.num("quantity") }
        for(choice in kit.objects("choices")) {
            val key=choice.text("id");val chosen=draft.packageChoices[key]
            if(chosen==null || choice.objects("options").none { it.text("id")==chosen }) issue("INVALID_EQUIPMENT_SELECTION","packageChoices.$key","Choose a supported package option.")
            else expected[chosen]=choice.num("quantity")
        }
        if(draft.packageChoices.keys.any { key -> kit.objects("choices").none { it.text("id")==key } }) issue("INVALID_EQUIPMENT_SELECTION","packageChoices","Unknown package choice.")
        if(draft.inventory.map { it.definitionId }.toSet()!=expected.keys || draft.inventory.map { it.definitionId }.distinct().size!=draft.inventory.size) issue("INVALID_EQUIPMENT_SELECTION","inventory","Supply exactly the selected starting kit; no duplicate entries.")
        for(item in draft.inventory) {
            if(item.quantity!=expected[item.definitionId] || item.quantity<=0) issue("INVALID_QUANTITY","inventory.${item.definitionId}","Starting quantity must match the package.")
            if(item.definitionId !in spec.strings("equipment")) issue("CONTENT_NOT_SUPPORTED","inventory.${item.definitionId}","Item is unavailable in this profile.")
            if(item.equipped != (item.definitionId in spec.strings("armour"))) issue("INVALID_EQUIPMENT_SELECTION","inventory.${item.definitionId}.equipped","Equip the supported armour; other starting items are carried.")
        }
        if(tier1) {
            try {
                val compiled=StartingPackages.compile(executableFor(draft),draft.packageChoices.mapValues { listOf(it.value) },records,spec.strings("equipment").toSet())
                if(compiled.inventory.sortedBy { it.definitionId }!=draft.inventory.sortedBy { it.definitionId }) issue("INVALID_EQUIPMENT_SELECTION","inventory","Inventory must equal the compiled canonical package.")
            } catch(e:IllegalArgumentException) { issue("INVALID_EQUIPMENT_SELECTION","packageChoices",e.message ?: "Invalid package") }
        }
        val preview=if(baseValid && errors.none { it.field in allowed.filter { key -> data(key).text("purpose")=="attribute" }.map { key -> "answers.$key" } }) { val values=scores(draft);obj("scores" to values,"modifiers" to modifiers(values)) } else null
        return DraftValidation(if(errors.isEmpty()) "VALID" else "INVALID",errors,preview,if(errors.isEmpty()) calculate(draft,actorId) else null)
    }

    /** Called only after validation. All mechanics are read from this pinned snapshot. */
    private fun calculate(draft: NarrowDraft, actorId: String): JsonObject {
        val final=scores(draft);val mods=modifiers(final);val features=linkedSetOf<String>();val profs=linkedSetOf<String>();val visited=mutableSetOf<String>()
        fun applyGrant(g:JsonObject) { if(g.text("kind")=="proficiency") profs+=ref(g,"proficiency") }
        fun visit(key:String) {
            if(!visited.add(key)) return
            val e=record(key);val d=data(key)
            if(e.text("kind")=="feature") features+=key
            d.objects("features").forEach { visit(it.text("id")) }
            d.objects("grants").forEach { if(it.text("kind")=="feature") visit(ref(it,"feature")) else applyGrant(it) }
        }
        listOf(draft.speciesId,draft.originId,draft.classId,draft.traitId).forEach(::visit)
        val progression=data(ref(data(draft.classId),"progression"))
        progression.objects("entries").filter { it.num("level")<=draft.level }.forEach { row -> row.objects("grants").forEach { if(it.text("kind")=="feature") visit(ref(it,"feature")) else applyGrant(it) } }
        draft.answers.forEach { (key,options) -> data(key).objects("options").filter { it.text("id") in options }.forEach { it.objects("grants").forEach(::applyGrant) } }
        val subclass=if(expanded) subclassFor(draft) else null
        if(subclass!=null) {
            visit(subclass)
            data(ref(data(subclass),"progression")).objects("entries").filter { it.num("level")<=draft.level }.flatMap { it.objects("grants") }.forEach { if(it.text("kind")=="feature") visit(ref(it,"feature")) else applyGrant(it) }
        }
        if(tier1) profs+=StartingPackages.compile(executableFor(draft),draft.packageChoices.mapValues { listOf(it.value) },records,spec.strings("equipment").toSet()).proficiencies
        val effects=features.flatMap { data(it).objects("effects") }.filter { it.text("automation")=="automatic" }
        fun effectSum(key:String)=effects.filter { it.getValue("target").jsonObject.text("key")==key }.sumOf { it.getValue("value").jsonObject.num("value") }
        val pb=payload.objects("proficiencyBands").first { draft.level<=it.num("maximumLevel") }.num("bonus")
        val training=if(expanded) payload.getValue("classTraining").jsonObject.getValue(draft.classId).jsonObject else payload.getValue("training").jsonObject
        val hp=if(tier1) Tier1Calculations.hp(training.num("hitDie"),draft.level,mods.getValue("constitution")) else training.num("hitDie")+mods.getValue("constitution")
        val armour=draft.inventory.single { it.equipped };val armourData=data(armour.definitionId)
        val baseAc=armourData.getValue("defence").jsonObject.getValue("value").jsonObject.num("value")
        val dex=armourData["dexterityBonus"]?.jsonObject
        val ac=if(tier1) Tier1Calculations.armour(baseAc,if(dex?.get("enabled")?.jsonPrimitive?.boolean==true) mods.getValue("dexterity") else 0,dex?.get("cap")?.jsonPrimitive?.int) else baseAc+mods.getValue("dexterity")
        val saves=attributes.associateWith { attr -> val proficient=attr in training.strings("savingThrows");obj("modifier" to mods.getValue(attr)+(if(proficient) pb else 0),"proficient" to proficient) }
        val skillIds=profs.filter { data(it).text("category")=="skill" }.flatMap { data(it).getValue("appliesTo").jsonObject.objects("ids").map { x -> x.text("id") } }.toSet()
        val skills=records.values.map { it.jsonObject }.filter { it.text("kind")=="skill" }.sortedBy { it.text("name") }.associate { e -> val key=e.text("id");val attr=data(key).text("attributeKey");key to obj("name" to e.text("name"),"attribute" to attr,"proficient" to (key in skillIds),"modifier" to mods.getValue(attr)+(if(key in skillIds) pb else 0)) }
        val groups=profs.filter { data(it).text("category")=="weapon_group" }.flatMap { data(it).getValue("appliesTo").jsonObject.strings("groups") }.toSet()
        val direct=profs.filter { data(it).text("category")=="weapon" }.flatMap { data(it).getValue("appliesTo").jsonObject.objects("ids").map { x->x.text("id") } }.toSet()
        val starting=draft.inventory.map { it.definitionId }.filter { record(it).text("kind") in listOf("weapon","shield") }
        val inventory=draft.inventory.map { obj("definitionId" to it.definitionId,"name" to label(it.definitionId),"quantity" to it.quantity,"equipped" to it.equipped) }
        val rolls=mutableListOf<JsonObject>();val actions=mutableListOf<JsonObject>()
        val snapshot=obj("rulesetLockDigest" to digest,"engineVersion" to spec.text("engineVersion"),"stateVersion" to 0,"contextDigest" to sha(canonicalJson(obj("draft" to Json.encodeToJsonElement(NarrowDraft.serializer(),draft),"context" to "display-only baseline"))))
        fun roll(key:String,category:String,label:String,sourceId:String,count:Int,sides:Int,bonus:Int,damageType:JsonElement?=null,actionId:String?=null):JsonObject {
            val component=linkedMapOf<String,Any?>("id" to "base","groups" to listOf(obj("id" to "base","count" to count,"sides" to sides)),"modifiers" to listOf(obj("id" to "resolved","value" to bonus,"source" to obj("kind" to "content","ref" to obj("id" to sourceId)),"label" to "Resolved baseline modifier","contextual" to false)))
            if(damageType!=null) component["damageType"]=damageType
            val body=linkedMapOf<String,Any?>("schemaVersion" to 1,"id" to UUID.nameUUIDFromBytes("$actorId:$digest:$key:${snapshot.text("contextDigest")}".toByteArray()).toString(),"category" to category,"label" to label,"source" to obj("kind" to "content","ref" to obj("id" to sourceId)),"actor" to obj("kind" to "character","instanceId" to actorId),"snapshot" to snapshot,"components" to listOf(json(component)),"advantage" to obj("state" to "normal","policyId" to "phb.advantage.v1","appliedGroupIds" to emptyList<String>()),"critical" to if(category=="attack") obj("policyId" to "phb.critical.v1","status" to "enabled","threshold" to 20,"comparison" to "at_least") else obj("policyId" to "phb.critical.v1","status" to "disabled"))
            if(category!="damage") body["natural"]=obj("componentId" to "base","groupId" to "base")
            if(actionId!=null) body["action"]=obj("ref" to obj("id" to actionId),"executionId" to UUID.nameUUIDFromBytes("$actorId:$digest:$actionId:${snapshot.text("contextDigest")}".toByteArray()).toString(),"stageId" to category,"modeId" to "base")
            return json(body).jsonObject.also { rolls+=it }
        }
        for(attr in attributes) roll("ability.$attr","attribute","$attr check",draft.speciesId,1,20,mods.getValue(attr))
        for((key,value) in skills) roll("skill.$key","skill",label(key),key,1,20,value.num("modifier"))
        for(attr in attributes) roll("save.$attr","save","$attr save",draft.classId,1,20,saves.getValue(attr).num("modifier"))
        val initiative=mods.getValue("dexterity")+effectSum("initiative")
        roll("initiative","ability","Initiative",draft.traitId,1,20,initiative)
        for(item in starting) {
            val d=data(item);val mode=d.objects("modes").single();val binding=d.getValue("abilityBinding").jsonObject
            val ability=when(binding.text("attack")) { "finesse"->"strength";"none"->null;else->binding.text("attack") }
            val proficient=item in starting || item in direct || d.strings("proficiencyGroups").any { it in groups }
            val attack=ability?.let { mods.getValue(it)+(if(proficient) pb else 0) };val actionId=ref(mode,"action")
            if(attack!=null) roll("$item.attack","attack","${label(item)} attack",item,1,20,attack,actionId=actionId)
            val component=mode.objects("damage").single();val dice=component.getValue("dice").jsonObject
            val damageBonus=dice.num("bonus")+component.getValue("bonus").jsonObject.num("value")+(if(binding.text("damage")=="none") 0 else mods.getValue(ability!!))
            val damageRoll=roll("$item.damage","damage","${label(item)} damage",item,dice.num("count"),dice.num("sides"),damageBonus,component.getValue("damageType"),actionId)
            val expression="${dice.num("count")}d${dice.num("sides")}"+(if(damageBonus==0) "" else if(damageBonus>0) " + $damageBonus" else " - ${-damageBonus}")
            actions+=obj("id" to actionId,"itemId" to item,"name" to label(item),"attackBonus" to attack,"ability" to ability,"damageExpression" to expression,"damageType" to label(ref(component,"damageType")),"range" to mode.getValue("range"),"properties" to d.objects("properties").map { property -> label(ref(property,"property")) + ((property["arguments"] as? JsonObject)?.entries?.takeIf { it.isNotEmpty() }?.joinToString(", ", " (", ")") { (key,value) -> "$key: ${value.jsonPrimitive.content}" } ?: "") },"save" to mode["save"],"saveDc" to if(mode.containsKey("save")) policy.num("grenadeDcBase")+pb+mods.getValue("dexterity") else null,"area" to mode["area"],"consumption" to mode["consumption"],"damageRollId" to damageRoll.text("id"),"manual" to true)
        }
        return obj("attributes" to final,"attributeModifiers" to mods,"proficiencyBonus" to pb,"maximumWounds" to hp,"defence" to ac,"movement" to effectSum("movement.walk"),"initiative" to initiative,"saves" to saves,"skills" to skills,"proficiencies" to profs.map(::view),"weaponProficiencies" to obj("groups" to groups.sorted(),"specificWeapons" to direct.sorted(),"startingPackageWeapons" to starting),"features" to features.map(::featureView),"inventory" to inventory,"actions" to actions,"rollDefinitions" to rolls,"readiness" to "PLAYABLE_WITH_MANUAL_RULES","rollAuthority" to "DISPLAY_ONLY_NOT_AUTHORIZATION","profileDigest" to digest).let { base ->
            if(!expanded) base else {
                val supports=features.map(::featureView)
                val resources=spec.objects("runtimeResources").filter { !speciesComposition || it.text("sourceId") in features }+supports.flatMap { f -> f.objects("resources").map { JsonObject(it+mapOf("sourceId" to JsonPrimitive(f.text("id")))) } }
                JsonObject(base+(if(speciesComposition) mapOf("size" to data(draft.speciesId).getValue("size"),"darkvisionFeet" to json(effects.filter { it.getValue("target").jsonObject.text("key")=="sense.darkvision" }.maxOfOrNull { it.getValue("value").jsonObject.num("value") } ?: 0)) else emptyMap())+mapOf("subclass" to (subclass?.let(::view) ?: JsonNull),"resources" to json(resources),"contacts" to json(StartingPackages.compile(executableFor(draft),draft.packageChoices.mapValues { listOf(it.value) },records,spec.strings("equipment").toSet()).contacts),"proceduralProficiencies" to json(supports.flatMap { (it["proceduralProficiencies"] as? JsonArray)?.toList().orEmpty() }),"equipmentNotes" to JsonObject(payload.getValue("equipmentSupport").jsonObject.filterKeys { it in starting })))
            }
        }
    }
    companion object {
        fun tier3(): NarrowRules = NarrowRules(Json.parseToJsonElement(requireNotNull(NarrowRules::class.java.getResource("/profiles/di-phb-1.0-tier1-v3.json")).readText()).jsonObject)
        fun tier2(): NarrowRules = NarrowRules(Json.parseToJsonElement(requireNotNull(NarrowRules::class.java.getResource("/profiles/di-phb-1.0-tier1-v2.json")).readText()).jsonObject)
        fun tier1(): NarrowRules = NarrowRules(Json.parseToJsonElement(requireNotNull(NarrowRules::class.java.getResource("/profiles/di-phb-1.0-tier1-v1.json")).readText()).jsonObject)
        fun bundled(): NarrowRules = NarrowRules(Json.parseToJsonElement(requireNotNull(NarrowRules::class.java.getResource("/profiles/di-phb-1.0-narrow-v1.json")).readText()).jsonObject)
    }
}

package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.util.UUID

@Serializable data class NotesUpdate(val text:String,val expectedVersion:Long)
/** Details are read from the owned character's pinned snapshot, never a global draft catalogue. */
class SheetDetails(private val db:Database,private val characters:ProductionCharacters) {
    fun notes(owner:UUID,id:UUID):JsonObject=db.read { con ->
        con.query("SELECT notes,notes_version FROM player_characters WHERE id=? AND user_id=?",id,owner){obj("text" to it.getString(1),"version" to it.getLong(2))}.singleOrNull() ?: throw ApiException(404,"NOT_FOUND","Character not found.")
    }
    fun saveNotes(owner:UUID,id:UUID,input:NotesUpdate):JsonObject=db.transaction { con ->
        if(input.text.length>20000)throw ApiException(422,"NOTES_TOO_LONG","Notes must be 20,000 characters or fewer.")
        val version=con.query("SELECT notes_version FROM player_characters WHERE id=? AND user_id=? FOR UPDATE",id,owner){it.getLong(1)}.singleOrNull() ?: throw ApiException(404,"NOT_FOUND","Character not found.")
        if(version!=input.expectedVersion)throw ApiException(409,"NOTES_CONFLICT","Notes changed elsewhere. Copy your draft before reloading notes.")
        con.execute("UPDATE player_characters SET notes=?,notes_version=notes_version+1,updated_at=now() WHERE id=?",input.text,id)
        obj("text" to input.text,"version" to version+1)
    }
    fun entity(owner:UUID,id:UUID,key:String):JsonObject=db.read { con ->
        val sheet=characters.get(con,owner,id);val calc=sheet.getValue("calculated").jsonObject
        val rules=NarrowRules(con.query("SELECT snapshot FROM ruleset_profiles WHERE id=? AND digest=?",sheet.text("rulesetProfileId"),sheet.text("rulesetDigest")){Json.parseToJsonElement(it.getString(1)).jsonObject}.single())
        val allowed=mutableSetOf<String>()
        for(field in listOf("species","origin","characterClass","trait"))allowed+=sheet.getValue(field).jsonObject.text("id")
        for(field in listOf("features","proficiencies"))allowed+=calc.objects(field).map { it.text("id") }
        allowed+=sheet.objects("inventory").map { it.text("definitionId") }
        allowed+=calc.getValue("skills").jsonObject.keys
        (calc["subclass"] as? JsonObject)?.let { allowed+=it.text("id") }
        allowed+=calc.objects("actions").map { it.text("id") }
        val properties=allowed.filter { it in rules.records && rules.record(it).text("kind")=="weapon" }.flatMap { rules.data(it).objects("properties").map { p->p.getValue("property").jsonObject.text("id") } }
        allowed+=properties
        if(key !in allowed || key !in rules.records)throw ApiException(404,"DETAIL_NOT_AVAILABLE","This entity is not available in this character's pinned ruleset.")
        val record=rules.record(key);val data=rules.data(key);val fields=mutableListOf<JsonObject>()
        fun field(label:String,value:String?){if(!value.isNullOrBlank())fields+=obj("label" to label,"value" to if(label.endsWith("ability"))value.replaceFirstChar { it.uppercase() } else value)}
        fun readable(e:JsonElement?):String?=when(e){null,JsonNull->null;is JsonPrimitive->e.content;is JsonArray->e.mapNotNull(::readable).joinToString(" · ");is JsonObject->if(e.containsKey("unit") && e.containsKey("value")) "${readable(e["value"])} ${readable(e["unit"])}" else if(e.containsKey("id"))e.text("id").let { if(it in rules.records)rules.label(it) else it } else e.entries.mapNotNull { (k,v)->readable(v)?.let { "$k: $it" } }.joinToString("; ");else->null}
        for((label,name) in listOf("Category" to "category","Level" to "level","Prerequisites" to "requirements","Action type" to "actionType","Duration" to "duration","Uses" to "uses","Recovery" to "recovery","Tags" to "functionalTags"))field(label,readable(data[name]))
        val action=calc.objects("actions").singleOrNull { it.text("itemId")==key || it.text("id")==key }
        if(action!=null){
            field("Attack ability",action["attackAbilityId"]?.jsonPrimitive?.contentOrNull ?: action["ability"]?.jsonPrimitive?.contentOrNull)
            field("Damage ability",action["damageAbilityId"]?.jsonPrimitive?.contentOrNull)
            field("Attack modifier",action["attackBonus"]?.jsonPrimitive?.contentOrNull)
            field("Damage",action.text("damageExpression")+" "+action.text("damageType"))
            val range=action.getValue("range").jsonObject
            field("Range",if(range.text("kind")=="reach")readable(range["distance"]) else listOfNotNull(readable(range["normal"]),readable(range["long"])).joinToString(" / "))
            field("Save DC",action["saveDc"]?.jsonPrimitive?.contentOrNull)
            field("Properties",action.strings("properties").joinToString(" · "))
        }
        val inventory=sheet.objects("inventory").singleOrNull { it.text("definitionId")==key }
        inventory?.let { field("Quantity",it.num("quantity").toString());field("Equipped",if(it["equipped"]?.jsonPrimitive?.boolean==true) "Yes" else "No") }
        val feature=calc.objects("features").singleOrNull { it.text("id")==key }
        val capacity=data.objects("effects").filter { it.text("automation")=="automatic" && it.getValue("target").jsonObject.text("key")=="action.attack.capacity" }.maxOfOrNull { it.getValue("value").jsonObject.num("value") }
        if(capacity!=null) {field("Level","5");field("Attacks per Attack action",capacity.toString());field("Scope","Attack action on your turn; not bonus actions or reactions")}
        val status=feature?.get("classification")?.jsonPrimitive?.content ?: if(action!=null) "Baseline rolls available; conditional effects are manual" else "Reference information"
        val rulesText=data.objects("manualRules").mapNotNull { it["text"]?.jsonPrimitive?.content } + data.objects("properties").map { val prop=it.getValue("property").jsonObject.text("id");rules.label(prop)+": "+rules.record(prop).text("descriptionMarkdown") }
        obj("id" to key,"name" to record.text("name"),"kind" to record.text("kind"),"description" to record.text("descriptionMarkdown"),"fields" to fields,"sources" to record.arr("sources"),"rules" to rulesText.distinct(),"status" to status,"note" to feature?.get("playerNote"),"actionItemId" to action?.get("itemId"),"profileId" to rules.id,"profileDigest" to rules.digest)
    }
}

package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.sql.Connection
import java.util.UUID

@Serializable data class CharacterActionRequest(val requestId:String,val expectedStateVersion:Long,val action:String,val powerId:String?=null,val empoweredOption:String?=null,val useFreeEmpowerment:Boolean=false,val resourceKey:String?=null,val dieIndex:Int?=null)

/** Commands reserve a canonical action; individual dice stay in the existing physical sessions. */
class CharacterActions(private val db:Database,private val characters:ProductionCharacters) {
    fun execute(owner:UUID,id:UUID,input:CharacterActionRequest):JsonObject=db.transaction { con ->
        val requestId=uuid(input.requestId);val digest=sha(canonicalJson(obj("character" to id.toString(),"request" to Json.encodeToJsonElement(CharacterActionRequest.serializer(),input))))
        con.query("SELECT pg_advisory_xact_lock(hashtextextended(?,0))","action:$owner:$requestId"){0}
        con.query("SELECT request_digest,result FROM character_action_requests WHERE user_id=? AND request_id=?",owner,requestId){it.getString(1) to Json.parseToJsonElement(it.getString(2)).jsonObject}.singleOrNull()?.let {
            if(it.first!=digest)throw ApiException(409,"IDEMPOTENCY_CONFLICT","Request already used for a different action.")
            return@transaction it.second
        }
        if(con.query("SELECT c.id FROM player_characters c JOIN player_character_runtime r ON r.character_id=c.id WHERE c.id=? AND c.user_id=? FOR UPDATE OF c,r",id,owner){it.getString(1)}.isEmpty())throw ApiException(404,"NOT_FOUND","Character not found.")
        val sheet=characters.get(con,owner,id);val runtime=sheet.getValue("runtime").jsonObject
        if(runtime.getValue("stateVersion").jsonPrimitive.long!=input.expectedStateVersion)throw ApiException(409,"STATE_CONFLICT","Character changed. Refresh before acting.")
        val rules=NarrowRules(con.query("SELECT snapshot FROM ruleset_profiles WHERE id=?",sheet.text("rulesetProfileId")){Json.parseToJsonElement(it.getString(1)).jsonObject}.single())
        if(rules.spec["psychicMechanicsVersion"]==null)throw ApiException(422,"ACTION_NOT_AVAILABLE","This action is not part of this historical profile.")
        val d=Json.decodeFromJsonElement(NarrowDraft.serializer(),sheet.getValue("selections"));val calc=sheet.getValue("calculated").jsonObject
        var pending=runtime["pendingAction"] as? JsonObject;var pressure=runtime.num("currentWarpPressure")
        val resources=runtime.getValue("resources").jsonObject.toMutableMap()
        fun fail(message:String):Nothing=throw ApiException(422,"ACTION_NOT_AVAILABLE",message)
        fun spend(key:String) {
            val resource=resources[key]?.jsonObject ?: fail("This resource is not granted to this character.")
            if(resource.num("remaining")<1)fail("No uses remaining; recover with the source-defined rest.")
            resources[key]=JsonObject(resource+mapOf("remaining" to json(resource.num("remaining")-1)))
        }
        fun free(){if(pending!=null)fail("Finish the pending action before starting another action or resting.")}
        fun psychic(){if(!PsychicRules.enabled(rules,d))fail("This character has no psychic capability.")}
        when(input.action) {
            "manifest" -> {
                free();psychic()
                val power=PsychicRules.powers(rules,d).singleOrNull { it.text("id")==input.powerId } ?: fail("This character does not know that power.")
                if(!PsychicRules.eligible(rules,d,power,characters.approvals(con,owner,rules.id)))fail("Power not eligible for this character.")
                val empowered=input.empoweredOption
                if(empowered!=null && empowered !in power.strings("empoweredOptions"))fail("That Empowered option is not legal for this power.")
                if(empowered=="discipline_mastery") {
                    val tag=rules.payload.getValue("psychic").jsonObject.getValue("disciplineTags").jsonObject[PsychicRules.discipline(d) ?: ""]?.jsonPrimitive?.content
                    if(tag==null || tag !in power.strings("tags"))fail("Discipline Mastery requires your chosen discipline and a damage/healing die.")
                }
                if(input.useFreeEmpowerment) {
                    if(empowered==null || d.level<5)fail("A level-5 Empowered feature and option are required.")
                    if(d.classId=="di.class.aeldari_warlock" && power.strings("tags").none { it in setOf("Warlock","Divination","Telekinesis") })fail("Empowered Rune applies only to Warlock, Divination or Telekinesis powers.")
                    spend(if(d.classId=="di.class.psyker")"empowered_manifestation" else "empowered_rune")
                }
                pending=obj("id" to input.requestId,"kind" to "power","powerId" to power.text("id"),"name" to power.text("name"),"empoweredOption" to empowered,"freeEmpowerment" to input.useFreeEmpowerment,"pressureCost" to power.num("warpPressureCost")+power.num("extraWarpPressure")+(if(empowered!=null&&!input.useFreeEmpowerment)1 else 0),"saveDc" to (calc.getValue("psychic").jsonObject.num("saveDc")+(if(empowered=="brutal_manifestation")1 else 0)),"range" to power.text("range"),"empoweredInstruction" to (if(empowered!=null) rules.payload.getValue("psychic").jsonObject.objects("empoweredOptions").single { it.text("id")==empowered }.text("description") else null),"targetNumber" to 1,"stage" to if(power["attack"]?.jsonPrimitive?.boolean==true)"attack" else if(power["roll"]!=null)"effect" else "resolve_power")
            }
            "next_target" -> {
                val action=pending ?: fail("No power is pending.")
                if(action["powerId"]?.jsonPrimitive?.content!="di.power.assail" || action.text("stage")!="resolve_power" || action.num("targetNumber")>=3)fail("Assail permits up to three separately resolved targets.")
                pending=JsonObject(action+mapOf("stage" to json("attack"),"targetNumber" to json(action.num("targetNumber")+1)))
            }
            "reroll_die" -> {
                val action=pending ?: fail("No power is pending.")
                if(action["empoweredOption"]?.jsonPrimitive?.content!="discipline_mastery" || action.text("stage")!="resolve_power" || action["rerolled"]?.jsonPrimitive?.boolean==true)fail("No unused Discipline Mastery reroll is available.")
                val die=input.dieIndex ?: fail("Select one damage or healing die to reroll.")
                val effect=action["effectDice"]?.jsonObject ?: fail("Roll the base effect first.")
                val group=effect.objects("groups").single()
                if(die !in group.arr("dice").indices)fail("Select an existing die.")
                pending=JsonObject(action+mapOf("stage" to json("reroll"),"rerollIndex" to json(die),"rerolled" to json(true)))
            }
            "resolve_power" -> {
                val action=pending ?: fail("No power is pending.")
                if(action.text("kind")!="power" || action.text("stage") !in setOf("effect","resolve_power"))fail("Resolve the pending power roll first.")
                pressure=Math.addExact(pressure,action.num("pressureCost"))
                pending=JsonObject(action+mapOf("stage" to json("perils_check"),"pressureBefore" to json(runtime.num("currentWarpPressure")),"pressureAfter" to json(pressure)))
            }
            "resolve_perils" -> {
                if(pending?.text("stage")!="resolve_perils")fail("No resolved Perils effect awaits acknowledgement.")
                pressure=PsychicRules.afterPerils(pressure);pending=null
            }
            "vent" -> {free();psychic();pending=obj("id" to input.requestId,"kind" to "vent","name" to "Vent","stage" to "vent_save")}
            "ward" -> {free();psychic();if(d.level<2)fail("Ward is granted at level 2.");pending=obj("id" to input.requestId,"kind" to "ward","name" to if(d.classId=="di.class.psyker")"Psychic Ward" else "Rune Ward","stage" to "ward")}
            "mercy" -> {free();if(d.classId!="di.class.zealot")fail("Martyr’s Mercy is not granted.");spend("martyrs_mercy");pending=obj("id" to input.requestId,"kind" to "mercy","name" to "Martyr’s Mercy","stage" to "mercy")}
            "resource" -> {free();val key=input.resourceKey ?: fail("Select a granted resource.");if(key in setOf("empowered_manifestation","empowered_rune","martyrs_mercy"))fail("Use the corresponding action to spend this resource.");spend(key)}
            "short_rest","long_rest" -> {free();pressure=0;for((key,value) in resources.toMap()){val v=value.jsonObject;if(v.text("recovery")==input.action || (input.action=="long_rest"&&v.text("recovery")=="short_rest"))resources[key]=JsonObject(v+mapOf("remaining" to v.getValue("maximum")))}}
            else -> fail("Unknown action.")
        }
        con.execute("UPDATE player_character_runtime SET warp_pressure=?,pending_action=?::jsonb,resources=?::jsonb,state_version=state_version+1 WHERE character_id=?",pressure,pending?.toString(),JsonObject(resources).toString(),id)
        val result=characters.get(con,owner,id)
        con.execute("INSERT INTO character_action_requests(user_id,request_id,character_id,request_digest,result) VALUES (?,?,?,?,?::jsonb)",owner,requestId,id,digest,result.toString())
        result
    }
}

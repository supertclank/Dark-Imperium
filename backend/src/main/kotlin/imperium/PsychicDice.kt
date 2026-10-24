package imperium

import kotlinx.serialization.json.*
import java.sql.Connection
import java.time.Instant
import java.util.UUID

/** One authorised physical roll per step; state changes and history commit together. */
object PsychicDice {
    fun option(sheet:JsonObject,rules:NarrowRules):JsonObject? {
        val runtime=sheet.getValue("runtime").jsonObject;val pending=runtime["pendingAction"] as? JsonObject ?: return null
        val stage=pending.text("stage");if(stage in setOf("resolve_power","resolve_perils"))return null
        val calc=sheet.getValue("calculated").jsonObject;val psychic=calc["psychic"] as? JsonObject
        val d=Json.decodeFromJsonElement(NarrowDraft.serializer(),sheet.getValue("selections"))
        val power=PsychicRules.powers(rules,d).singleOrNull { it.text("id")==pending["powerId"]?.jsonPrimitive?.content }
        var count=1;var sides=20;var modifier=0
        val pb=calc.num("proficiencyBonus");val ability=psychic?.num("abilityModifier") ?: 0
        when(stage) {
            "attack" -> modifier=psychic!!.num("attackModifier")
            "effect" -> {
                val roll=power!!.getValue("roll").jsonObject;count=roll.num("count");sides=roll.num("sides")
                if(pending["empoweredOption"]?.jsonPrimitive?.content=="overcharged_damage")count++
                modifier=roll.num("abilityMultiplier")*ability+roll.num("proficiencyMultiplier")*pb
                if(pending["empoweredOption"]?.jsonPrimitive?.content=="sustained_focus")modifier+=pb
                val sub=calc["subclass"] as? JsonObject;val damage=roll["damageType"]?.jsonPrimitive?.contentOrNull.orEmpty()
                if(sub?.text("id")=="di.subclass.psyker.pyromancer" && "fire" in damage)modifier+=count
                if(sub?.text("id")=="di.subclass.aeldari_warlock.storm_warlock" && damage.split('/').any { it in setOf("force","lightning","fire","radiant") })modifier+=count
            }
            "reroll" -> sides=pending.getValue("effectDice").jsonObject.objects("groups").single().num("sides")
            "perils_check" -> Unit
            "perils_severity" -> modifier=runtime.num("currentWarpPressure")
            "perils_damage" -> {count=when(pending.text("peril")){"Warp Static"->1;"Catastrophic Perils"->4;else->2};sides=6}
            "vent_save" -> modifier=calc.getValue("saves").jsonObject.getValue("wisdom").jsonObject.num("modifier")
            "vent_reduction" -> {sides=4;modifier=pb}
            "vent_damage" -> sides=6
            "ward" -> {sides=8;modifier=ability}
            "mercy" -> {sides=6;modifier=calc.getValue("attributeModifiers").jsonObject.num(d.answers["di.choice.zealot.mercy_ability"]!!.single())}
            else -> return null
        }
        return obj("id" to "psychic:${pending.text("id")}:$stage","label" to "${pending.text("name")} · ${stage.replace('_',' ')}","category" to "psychic","actionId" to pending.text("id"),"itemId" to null,"available" to true,"reason" to null,"consumes" to false,"quantity" to null,"abilities" to emptyList<String>(),"groups" to listOf(obj("count" to count,"sides" to sides)),"modifier" to modifier)
    }
    fun execute(con:Connection,owner:UUID,id:UUID,request:RollRequest,requestDigest:String,sheet:JsonObject,rules:NarrowRules,dice:DiceEngine,raw:List<List<Int>>?,validateOnly:Boolean):JsonObject {
        fun fail(message:String):Nothing=throw ApiException(422,"ROLL_NOT_AVAILABLE",message)
        val option=option(sheet,rules) ?: fail("No psychic/action roll is pending.")
        if(request.rollId!=option.text("id") || request.parentResultId!=null || request.ability!=null || request.confirmConsumption)fail("Use the server-authorised pending action without overrides.")
        val groups=option.objects("groups").map { DiceGroup(it.num("count"),it.num("sides")) }
        if(validateOnly)return obj("label" to option.text("label"),"groups" to groups.map { obj("count" to it.count,"sides" to it.sides,"keep" to "ALL","keepCount" to it.count) },"modifier" to option.num("modifier"))
        val resolved=if(raw==null)dice.resolve(groups,option.num("modifier")) else dice.resolveRaw(groups,option.num("modifier"),raw)
        val runtime=sheet.getValue("runtime").jsonObject;val initial=runtime.getValue("pendingAction").jsonObject;var pending:JsonObject?=initial
        var pressure=runtime.num("currentWarpPressure");var hp=runtime.num("currentHp");val stage=initial.text("stage")
        val natural=resolved.groups.single().kept.singleOrNull()
        fun stage(next:String){pending=JsonObject(pending!!+mapOf("stage" to json(next)))}
        when(stage) {
            "attack" -> {
                if(initial["powerId"]?.jsonPrimitive?.content=="di.power.warp_bite" && natural==1)pressure++
                stage("effect")
            }
            "effect" -> {stage("resolve_power");pending=JsonObject(pending!!+mapOf("effectResultId" to json(request.requestId),"effectDice" to Json.encodeToJsonElement(DiceResolution.serializer(),resolved)))}
            "reroll" -> {
                val prior=initial.getValue("effectDice").jsonObject
                val old=prior.objects("groups").single();val values=old.arr("dice").map{it.jsonPrimitive.int}.toMutableList();values[initial.num("rerollIndex")]=natural!!
                val updated=JsonObject(prior+mapOf("total" to json(values.sum()+prior.num("modifier")),"groups" to json(listOf(JsonObject(old+mapOf("dice" to json(values),"kept" to json(values)))))))
                pending=JsonObject(pending!!+mapOf("effectDice" to updated));stage("resolve_power")
            }
            "perils_check" -> if(PsychicRules.triggers(pressure,natural!!))stage("perils_severity") else pending=null
            "perils_severity" -> {
                val band=PsychicRules.severity(rules,pressure,natural!!);val peril=band.text("name")
                pending=JsonObject(pending!!+mapOf("peril" to json(peril),"perilDescription" to band.getValue("description")))
                if(peril=="Catastrophic Perils")hp=0
                stage(if(peril in setOf("Warp Static","Bleeding Eyes","Soul Echo","Catastrophic Perils"))"perils_damage" else "resolve_perils")
            }
            "perils_damage" -> {if(initial.text("peril")!="Catastrophic Perils")hp=maxOf(0,hp-resolved.total);stage("resolve_perils")}
            "vent_save" -> if(resolved.total>=12)stage("vent_reduction") else {pressure=PsychicRules.reduce(pressure,1);stage("vent_damage")}
            "vent_reduction" -> {pressure=PsychicRules.reduce(pressure,maxOf(0,resolved.total));pending=null}
            "vent_damage" -> {hp=maxOf(0,hp-resolved.total);pending=null}
            "ward" -> {pressure++;pending=null} // A ward is not a power; no inferred extra Perils check.
            "mercy" -> pending=null // Recipient HP application is explicit/manual, never an invented target.
        }
        val before=runtime.getValue("stateVersion").jsonPrimitive.long;val after=before+1;val resultId=UUID.randomUUID();val now=Instant.now()
        val result=obj("id" to resultId.toString(),"request" to Json.encodeToJsonElement(RollRequest.serializer(),request),"requestId" to request.requestId,"userId" to owner.toString(),"characterId" to id.toString(),"characterName" to sheet.text("name"),"rulesetProfileId" to rules.id,"rulesetDigest" to rules.digest,"engineVersion" to "production-dice-v1","actionId" to initial.text("id"),"requestedRollId" to request.rollId,"rollDefinitionId" to resultId.toString(),"definition" to option,"label" to option.text("label"),"rollType" to "psychic","dice" to Json.encodeToJsonElement(DiceResolution.serializer(),resolved),"total" to resolved.total,"naturalResult" to natural,"criticalCandidate" to false,"naturalOne" to (stage=="attack"&&natural==1),"damageType" to null,"visibility" to "PRIVATE","timestamp" to now.toString(),"parentResultId" to null,"context" to obj("ability" to (sheet.getValue("calculated").jsonObject["psychic"] as? JsonObject)?.get("ability"),"targetResolution" to "MANUAL","criticalDamage" to "NOT_APPLIED","action" to initial,"warpPressureBefore" to runtime.num("currentWarpPressure"),"warpPressureAfter" to pressure,"perilsTriggered" to (stage=="perils_check"&&pending!=null),"peril" to pending?.get("peril")),"stateVersionBefore" to before,"stateVersionAfter" to after,"grenade" to null,"consumption" to null)
        check(con.execute("UPDATE player_character_runtime SET warp_pressure=?,pending_action=?::jsonb,current_hp=?,state_version=state_version+1 WHERE character_id=? AND state_version=?",pressure,pending?.toString(),hp,id,before)==1)
        con.execute("INSERT INTO character_rolls(id,user_id,character_id,request_id,request_digest,profile_id,profile_digest,roll_definition_id,action_id,roll_type,visibility,state_version_before,state_version_after,result,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?::jsonb,?)",resultId,owner,id,uuid(request.requestId),requestDigest,rules.id,rules.digest,resultId,initial.text("id"),"psychic","PRIVATE",before,after,result.toString(),java.sql.Timestamp.from(now))
        return result
    }
}

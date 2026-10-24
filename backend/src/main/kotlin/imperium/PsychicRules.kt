package imperium

import kotlinx.serialization.json.*

/** Shared psychic selection and arithmetic policies, driven by the pinned profile. */
object PsychicRules {
    fun policy(rules:NarrowRules)=rules.payload["psychic"] as? JsonObject
    fun enabled(rules:NarrowRules,d:NarrowDraft)=d.classId in policy(rules)?.strings("classes").orEmpty()
    fun ability(d:NarrowDraft)=d.answers["di.choice.psychic.ability"]?.singleOrNull()
    fun discipline(d:NarrowDraft)=d.answers["di.choice.psyker.subclass"]?.singleOrNull()
    fun knownIds(d:NarrowDraft)=d.answers.filterKeys { it.startsWith("di.choice.psychic.") && "_level_" in it }.values.flatten().map { "di.power.$it" }
    fun powers(rules:NarrowRules,d:NarrowDraft)=policy(rules)?.objects("powers").orEmpty().filter { it.text("id") in knownIds(d) }
    fun eligible(rules:NarrowRules,d:NarrowDraft,power:JsonObject,approvals:Set<String> = emptySet()):Boolean {
        if(!enabled(rules,d) || power.text("tier") !in setOf("minor","standard"))return false
        val tags=power.strings("tags").toSet()
        // Warlock rune powers are locked even when they have a second discipline tag.
        if(d.classId=="di.class.psyker") {
            if("Warlock" in tags)return false
            if(discipline(d)=="blank_null_bound" && "blank_null_bound" !in approvals)return false
            val tag=policy(rules)?.get("disciplineTags")?.jsonObject?.get(discipline(d) ?: "")?.jsonPrimitive?.content
            return "Universal" in tags || tag in tags
        }
        if("Malefic" in tags)return false
        return tags.any { it in setOf("Universal","Divination","Telekinesis","Warlock") } || ("Pyromancy" in tags && "warlock_pyromancy" in approvals)
    }
    fun validate(rules:NarrowRules,d:NarrowDraft,approvals:Set<String> = emptySet()):List<DraftIssue> {
        if(!enabled(rules,d))return emptyList()
        val errors=mutableListOf<DraftIssue>()
        fun issue(code:String,message:String)=errors.add(DraftIssue(code,"answers",message))
        if(ability(d) !in setOf("intelligence","wisdom"))issue("PSYCHIC_ABILITY_REQUIRED","Choose Intelligence or Wisdom as psychic ability.")
        if(d.classId=="di.class.psyker" && discipline(d)=="blank_null_bound" && "blank_null_bound" !in approvals)issue("GM_APPROVAL_REQUIRED","Blank / Null-Bound requires a trusted GM approval.")
        val ids=knownIds(d);val selected=powers(rules,d)
        if(ids.distinct().size!=ids.size)issue("DUPLICATE_POWER","A power cannot be learned twice.")
        if(selected.size!=ids.size)issue("UNKNOWN_POWER","Choose only powers in this pinned profile.")
        if(selected.any { !eligible(rules,d,it,approvals) })issue("POWER_NOT_ELIGIBLE","Power tier or discipline/list is not legal for this character.")
        val expected=policy(rules)?.get("knownByLevel")?.jsonObject?.get(d.level.toString())?.jsonObject
        if(expected!=null && listOf("minor","standard").any { tier->selected.count { it.text("tier")==tier }!=expected.num(tier) })issue("POWERS_KNOWN_COUNT","Select the exact Minor and Standard power counts for this level.")
        return errors
    }
    fun projection(rules:NarrowRules,d:NarrowDraft,mods:Map<String,Int>,pb:Int):JsonObject? {
        if(!enabled(rules,d))return null
        val ability=ability(d) ?: return null
        return obj("ability" to ability,"abilityModifier" to mods.getValue(ability),"attackModifier" to pb+mods.getValue(ability),"saveDc" to 8+pb+mods.getValue(ability),"powers" to powers(rules,d),"knownCounts" to policy(rules)!!.getValue("knownByLevel").jsonObject.getValue(d.level.toString()),"empoweredOptions" to policy(rules)!!.getValue("empoweredOptions"))
    }
    fun reduce(pressure:Int,amount:Int):Int {require(pressure>=0 && amount>=0);return maxOf(0,pressure-amount)}
    fun afterPerils(pressure:Int):Int {require(pressure>=0);return pressure/2}
    fun triggers(pressure:Int,natural:Int):Boolean {require(pressure>=0 && natural in 1..20);return natural<=pressure}
    fun severity(rules:NarrowRules,pressure:Int,natural:Int):JsonObject {
        require(pressure>=0 && natural in 1..20)
        val total=Math.addExact(pressure,natural)
        return policy(rules)!!.objects("perilsBands").single { total>=it.num("minimum") && (it["maximum"]==JsonNull || total<=it.num("maximum")) }
    }
}

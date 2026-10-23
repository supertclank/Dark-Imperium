package imperium

import kotlinx.serialization.json.*

/** Read-only presentation of a pinned snapshot. Text segmentation never drives calculations. */
class BuilderPresentation(private val rules:NarrowRules) {
    private fun data(id:String)=rules.data(id)
    private fun ref(o:JsonObject,key:String)=o.getValue(key).jsonObject.text("id")
    private fun plain(text:String)=text.replace(Regex("\\s+")," ").trim()
    private val fields=setOf("Ability Scores","Size","Speed","Available Classes","Allowed Species","Skill Proficiency","Hit Die","Primary Abilities","Saving Throws","Armour","Weapons")
    private fun sections(id:String):List<Pair<String,String>> {
        val text=rules.record(id).text("descriptionMarkdown").replace(Regex("(?m)^\\d+(?:\\.\\d+)*[ \\t]+[^\\n]+\\n?"),"")
        val matches=Regex("(?m)^([A-Z][^:\\n]{1,65}):[ \\t]*").findAll(text).toList()
        val firstField=matches.indexOfFirst { it.groupValues[1] in fields }.let { if(it<0) 0 else it }
        return matches.drop(firstField).mapIndexed { offset,m -> val i=offset+firstField; m.groupValues[1] to plain(text.substring(m.range.last+1,matches.getOrNull(i+1)?.range?.first ?: text.length)) }
    }
    private fun intro(id:String):String {
        val text=rules.record(id).text("descriptionMarkdown").replace(Regex("^\\d+(?:\\.\\d+)*[ \\t]+[^\\n]+\\n?"),"")
        val firstField=Regex("(?m)^([A-Z][^:\\n]{1,65}):").findAll(text).firstOrNull { it.groupValues[1] in fields }
        return plain(text.substring(0,firstField?.range?.first ?: text.length))
    }
    private fun features(id:String)=data(id).objects("features").map { it.text("id") }
    private fun choices(id:String):List<String> = (listOf(id)+features(id)).flatMap { key -> data(key).objects("choices").map { it.text("id") }+data(key).objects("grants").filter { it.text("kind")=="choice" }.map { ref(it,"choice") } }.distinct()
    private fun selectedSpecies(p:JsonObject):Set<String> = when(p.text("kind")) {
        "selected" -> setOf(ref(p,"content"))
        "all","any" -> p.objects("predicates").flatMap { selectedSpecies(it) }.toSet()
        else -> emptySet()
    }
    private fun feature(id:String)=JsonObject(rules.featureView(id)+mapOf("text" to JsonPrimitive(plain(rules.record(id).text("descriptionMarkdown")))))
    private fun progression(id:String):List<JsonObject> {
        val progression=data(id)["progression"] as? JsonObject ?: return emptyList()
        return data(progression.text("id")).objects("entries").filter { it.num("level") in rules.spec.arr("levels").map { v->v.jsonPrimitive.int } }.map { row ->
            obj("level" to row.num("level"),"features" to row.objects("grants").mapNotNull { g -> when(g.text("kind")) { "feature" -> feature(ref(g,"feature"));"choice" -> obj("id" to ref(g,"choice"),"name" to rules.label(ref(g,"choice")),"text" to "Choose from the supported options at this level.","manual" to false);else -> null } })
        }
    }
    fun subclass(id:String)=obj("id" to id,"name" to rules.label(id),"levels" to progression(id))
    fun choiceOption(option:JsonObject):JsonObject {
        val sub=option.objects("grants").firstOrNull { it.text("kind")=="select" && rules.record(ref(it,"content")).text("kind")=="subclass" }
        return if(sub==null) obj("id" to option.text("id"),"label" to option.text("label")) else obj("id" to option.text("id"),"label" to option.text("label"),"detail" to subclass(ref(sub,"content")))
    }
    fun view(id:String):JsonObject {
        val kind=rules.record(id).text("kind");val d=data(id);val parsed=sections(id).toMap()
        val stats=mutableListOf<JsonObject>();val groups=mutableListOf<JsonObject>()
        if(kind=="species") {
            val effects=features(id).flatMap { data(it).objects("effects") }.filter { it.text("automation")=="automatic" }
            val increases=effects.filter { it.getValue("target").jsonObject.text("key").startsWith("attribute.") }.map { obj("label" to "Ability adjustment","value" to "+${it.getValue("value").jsonObject.num("value")} ${it.getValue("target").jsonObject.text("key").split('.')[1].take(3).uppercase()}") }
            stats+=increases
            for(choice in choices(id).filter { data(it).text("purpose")=="attribute" }) {
                val grants=data(choice).objects("options").flatMap { it.objects("grants") }.filter { it.text("kind")=="attribute_increase" }
                val distinctPair=data(choice).objects("options").all { o -> val a=o.objects("grants").filter { it.text("kind")=="attribute_increase" };a.size>1 && a.map { it.text("attributeKey") }.distinct().size==a.size }
                for((amount,items) in grants.groupBy { it.num("amount") }) {
                    val attrs=items.map { it.text("attributeKey") }.distinct()
                    val label=if(attrs.toSet()==rules.attributes.toSet()) "Any ability" else attrs.joinToString(" or ") { it.take(3).uppercase() }
                    stats+=obj("label" to "Ability choice","value" to "+$amount $label${if(distinctPair && amount!=grants.maxOf { it.num("amount") }) " (different ability)" else ""}")
                }
            }
            stats+=obj("label" to "Size","value" to d.text("size"))
            stats+=obj("label" to "Speed","value" to "${effects.filter { it.getValue("target").jsonObject.text("key")=="movement.walk" }.sumOf { it.getValue("value").jsonObject.num("value") }} ft")
            val vision=effects.filter { it.getValue("target").jsonObject.text("key")=="sense.darkvision" }.maxOfOrNull { it.getValue("value").jsonObject.num("value") } ?: 0
            stats+=obj("label" to "Vision","value" to if(vision>0) "Darkvision $vision ft" else "No darkvision granted")
            val classes=rules.records.keys.filter { rules.record(it).text("kind")=="class" && (data(it)["requirements"] as? JsonObject)?.let(::selectedSpecies)?.contains(id)==true }
            groups+=obj("label" to "Canonical class access","items" to classes.map { obj("name" to rules.label(it),"state" to if(rules.spec.objects("certifiedPaths").any { p->p.text("speciesId")==id && p.text("classId")==it }) "Supported paths" else "Coming later") })
        }
        if(kind=="background") {
            groups+=obj("label" to "Allowed species","items" to d.objects("originAvailability").map { obj("name" to rules.label(ref(it,"species")),"state" to it.text("state")) })
            val grants=(listOf(id)+features(id)).flatMap { data(it).objects("grants") }.filter { it.text("kind")=="proficiency" }.map { ref(it,"proficiency") }.filter { data(it).text("category")=="skill" }
            if(grants.isNotEmpty()) groups+=obj("label" to "Also gain","items" to grants.distinct().map { obj("name" to rules.label(it)) })
            for(key in choices(id).filter { data(it).text("purpose")=="skill" }) groups+=obj("label" to "Choose ${data(key).getValue("cardinality").jsonObject.num("min")} skill${if(data(key).getValue("cardinality").jsonObject.num("min")==1) "" else "s"}","items" to data(key).objects("options").map { obj("name" to it.text("label")) })
        }
        if(kind=="class") {
            val training=(rules.payload["classTraining"] as? JsonObject)?.get(id)?.jsonObject
            if(training!=null) {
                stats+=obj("label" to "Hit die","value" to "d${training.num("hitDie")}")
                stats+=obj("label" to "Saving throws","value" to training.strings("savingThrows").joinToString(" · ") { it.take(3).uppercase() })
            }
            parsed["Primary Abilities"]?.let { stats+=obj("label" to "Primary abilities","value" to it.removeSuffix(".")) }
            for((field,label) in listOf("Armour" to "Armour training","Weapons" to "Weapon training")) parsed[field]?.let { text->groups+=obj("label" to label,"items" to text.removeSuffix(".").split(",").map { obj("name" to it.trim()) }) }
        }
        val blocks=if(kind in setOf("species","background")) sections(id).filter { it.first !in fields }.map { obj("name" to it.first,"text" to it.second) } else emptyList()
        return obj("summary" to intro(id),"stats" to stats,"groups" to groups,"features" to blocks,"levels" to if(kind=="class") progression(id) else emptyList<JsonObject>())
    }
}

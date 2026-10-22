package imperium

import kotlinx.serialization.json.*

data class CompiledPackage(val inventory: List<InventorySelection>, val proficiencies: Set<String>, val narratives: List<String>)

/** Structured grants only: no display-text parsing and no candidate promotion. */
object StartingPackages {
    fun compile(definition: JsonObject, answers: Map<String,List<String>>, records: JsonObject, allowedItems: Set<String>): CompiledPackage {
        val quantities=linkedMapOf<String,Int>();val equipped=mutableSetOf<String>();val profs=linkedSetOf<String>();val notes=mutableListOf<String>();val consumed=mutableSetOf<String>()
        fun item(id:String) {
            require(id in allowedItems && id in records) { "UNSUPPORTED_PACKAGE_ITEM" }
            require(records.getValue(id).jsonObject.text("kind") in setOf("weapon","armour","shield","equipment","tool","ammunition","consumable","augmetic")) { "PACKAGE_ITEM_KIND" }
        }
        fun visit(steps: List<JsonObject>,depth:Int) {
            require(depth<=8) { "PACKAGE_DEPTH" }
            for(step in steps) when(step.text("kind")) {
                "item" -> { val id=step.text("itemId");item(id);val n=step.num("quantity");require(n in 1..1000) { "INVALID_PACKAGE_QUANTITY" };quantities[id]=Math.addExact(quantities[id]?:0,n) }
                "equip" -> { val id=step.text("itemId");item(id);require(records.getValue(id).jsonObject.text("kind") in setOf("armour","shield")) { "PACKAGE_EQUIP_KIND" };equipped+=id }
                "proficiency" -> { val id=step.text("proficiencyId");require(records[id]?.jsonObject?.text("kind")=="proficiency") { "UNKNOWN_PACKAGE_PROFICIENCY" };profs+=id }
                "narrative" -> { val text=step.text("text");require(text.isNotBlank() && text.length<=4000);notes+=text }
                "choice" -> {
                    val id=step.text("id");require(consumed.add(id)) { "DUPLICATE_PACKAGE_CHOICE" }
                    val selected=answers[id].orEmpty();val min=step.num("min");val max=step.num("max");val options=step.objects("options")
                    require(min in 0..1 && max==1 && options.isNotEmpty() && options.map { it.text("id") }.distinct().size==options.size) { "PACKAGE_CHOICE_SCHEMA" }
                    require(selected.size in min..max && selected.distinct().size==selected.size) { "PACKAGE_CHOICE_CARDINALITY" }
                    for(option in selected) { val branch=options.singleOrNull { it.text("id")==option };require(branch!=null) { "INVALID_PACKAGE_BRANCH" };visit(branch.objects("steps"),depth+1) }
                }
                else -> error("UNKNOWN_PACKAGE_OPERATION")
            }
        }
        visit(definition.objects("steps"),0)
        require(answers.keys.all { it in consumed }) { "UNEXPECTED_PACKAGE_CHOICE" }
        require(equipped.all { it in quantities }) { "EQUIP_REQUIRES_GRANT" }
        return CompiledPackage(quantities.map { InventorySelection(it.key,it.value,it.key in equipped) },profs,notes)
    }
}

/** Shared approved numeric policies; eligibility/certification remains a separate gate. */
object Tier1Calculations {
    fun hp(hitDie:Int,level:Int,constitution:Int):Int {
        require(hitDie in setOf(6,8,10,12) && level in 1..3)
        val later=hitDie/2+1+constitution
        require(hitDie+constitution>0 && (level==1 || later>0)) { "PHB-RULE-014: minimum HP gain unresolved" }
        return hitDie+constitution+(level-1)*later
    }
    fun armour(base:Int,dexterity:Int,cap:Int?):Int = base + if(cap==null) dexterity else minOf(dexterity,cap)
}

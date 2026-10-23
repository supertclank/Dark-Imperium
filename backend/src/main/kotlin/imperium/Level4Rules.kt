package imperium

import kotlinx.serialization.json.*

/** Pinned v5 choices and approved policies. Never derives eligibility from prose. */
object Level4Rules {
 fun policy(r:NarrowRules)=r.spec["level4Advancement"] as? JsonObject
 fun selected(r:NarrowRules,d:NarrowDraft):JsonObject? {
  val p=policy(r) ?: return null
  val ids=d.answers[p.text("choiceId")].orEmpty()
  return if(ids.size==1) p.objects("options").singleOrNull { it.text("id")==ids.single() } else null
 }
 fun eligible(p:JsonObject?,selected:Set<String>):Boolean=when(p?.text("kind")) {
  null->true
  "selected"->p.getValue("content").jsonObject.text("id") in selected
  "all"->p.objects("predicates").all { eligible(it,selected) }
  "any"->p.objects("predicates").any { eligible(it,selected) }
  else->false
 }
 fun validate(p:JsonObject,selection:JsonObject,base:Map<String,Int>,owned:Set<String>,eligible:Boolean):String? {
  return when(selection.text("branch")) {
   "ASI_PLUS_TWO","ASI_SPLIT" -> {
    val a=selection.strings("abilities");val plus=selection.text("branch")=="ASI_PLUS_TWO"
    when { a.size!=(if(plus)1 else 2) || a.distinct().size!=a.size || a.any { it !in base } -> "INVALID_ASI_SELECTION"
     a.any { base.getValue(it)+(if(plus)2 else 1)>p.num("asiMaximum") } -> "ASI_MAXIMUM_EXCEEDED"
     else -> null }
   }
   "TALENT" -> when {selection.text("talentId") in owned -> "TALENT_ALREADY_OWNED";!eligible -> "TALENT_INELIGIBLE";else->null}
   else -> "INVALID_ADVANCEMENT_CHOICE"
  }
 }
 fun apply(r:NarrowRules,d:NarrowDraft,scores:MutableMap<String,Int>) {
  val option=selected(r,d) ?: return
  if(option.text("branch") in setOf("ASI_PLUS_TWO","ASI_SPLIT")) for(a in option.strings("abilities")) scores[a]=scores.getValue(a)+(if(option.text("branch")=="ASI_PLUS_TWO")2 else 1)
 }
 fun currentHp(current:Int,maximum:Int)=minOf(current,maximum)
 fun hp(hitDie:Int,level:Int,constitution:Int):Int {
  require(hitDie in setOf(6,8,10,12) && level in 1..4)
  return maxOf(1,hitDie+constitution)+(level-1)*maxOf(1,hitDie/2+1+constitution)
 }
 fun weaponBonus(r:NarrowRules,d:NarrowDraft,item:String):Int {
  val o=selected(r,d) ?: return 0
  return if(o["talentId"]?.jsonPrimitive?.content=="di.feature.talent.weapon_specialist" && o.text("subchoiceId") in r.data(item).strings("proficiencyGroups")) 1 else 0
 }
}

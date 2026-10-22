"""Review-only composition of already-approved shared calculations.

Inputs are resolved values, not character grants. This is not a new production
adapter and cannot establish eligibility or make manual core effects executable.
"""
import phb_policies as p
from content_import import require

def fixed_core(hit_die,level,scores,constitution_at_acquisition,save_attributes,skill_attributes,proficient_skills,armour_base,armour_dex_cap,walk,initiative_bonus=0):
    require(type(level) is int and 1<=level<=3,'TIER1_LEVEL_REQUIRED')
    require(set(scores)=={'strength','dexterity','constitution','intelligence','wisdom','charisma'},'ALL_ATTRIBUTES_REQUIRED')
    modifiers={key:p.ability_modifier(value) for key,value in scores.items()}
    require(len(constitution_at_acquisition)==level and all(type(v) is int for v in constitution_at_acquisition),'CONSTITUTION_HISTORY_REQUIRED')
    require(all(v==modifiers['constitution'] for v in constitution_at_acquisition),'PHB-RULE-014: changed Constitution remains blocked')
    gains=[p.hp_gain(hit_die,con,first=index==0) for index,con in enumerate(constitution_at_acquisition)]
    require(all(v>0 for v in gains),'PHB-RULE-014: no minimum HP gain invented')
    require(set(save_attributes)<=set(scores),'SAVE_ATTRIBUTE_UNKNOWN')
    require(set(skill_attributes.values())<=set(scores) and set(proficient_skills)<=set(skill_attributes),'SKILL_INPUT_UNKNOWN')
    require(type(walk) is int and walk>=0 and type(initiative_bonus) is int,'RESOLVED_MOVEMENT_INITIATIVE_REQUIRED')
    return {'scope':'CALCULATION_PROOF_NOT_PLAYABLE_CHARACTER','level':level,'attributeModifiers':modifiers,'proficiencyBonus':p.proficiency(level),
      'hpGains':gains,'maximumHp':sum(gains),'armourClass':p.armour_ac(armour_base,modifiers['dexterity'],armour_dex_cap),
      'walk':walk,'initiative':modifiers['dexterity']+initiative_bonus,
      'saves':{key:p.check_modifier(value,level,key in save_attributes) for key,value in modifiers.items()},
      'skills':{key:p.check_modifier(modifiers[attribute],level,key in proficient_skills) for key,attribute in skill_attributes.items()}}

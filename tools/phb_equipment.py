"""Strict, finite PHB equipment import capability; no executable formulas."""
import content_import as c
from phb_policies import WEAPON_GROUPS

def validate_equipment(entity, records):
    d=entity['data'];kind=entity['kind']
    if 'availability' in d:
        c.require(d['availability'] in ['Issued','Controlled','Scarce','Rare','Exceptional','Improvised'], 'AVAILABILITY')
    if 'aliases' in d:
        c.require(isinstance(d['aliases'],list) and all(isinstance(x,str) and x for x in d['aliases']), 'ALIASES')
    if 'proficiencyGroups' in d:
        g=d['proficiencyGroups'];c.require(isinstance(g,list) and g and len(g)==len(set(g)) and set(g)<=WEAPON_GROUPS,'WEAPON_GROUP')
    if kind=='armour' and 'dexterityBonus' in d:
        c.shape(d['dexterityBonus'],['enabled'],['cap']);c.require(type(d['dexterityBonus']['enabled']) is bool,'DEXTERITY_BONUS')
        if 'cap' in d['dexterityBonus']:c.integer(d['dexterityBonus']['cap'],0,1000000)
    if kind in ['equipment','tool','augmetic']:
        c.require(isinstance(d['functionalTags'],list) and all(isinstance(t,str) and c.LOCAL.fullmatch(t) for t in d['functionalTags']),'FUNCTIONAL_TAGS')
    if kind!='weapon':return
    c.require(d['category'] in ['melee','ranged','grenade'],'WEAPON_CATEGORY');c.local(d['subcategory']);c.integer(d['hands'],1,2)
    c.shape(d['abilityBinding'],['attack','damage'])
    for value in d['abilityBinding'].values():c.require(value in ['strength','dexterity','finesse','none'],'WEAPON_ABILITY')
    if 'deployment' in d:c.require(d['deployment']=='emplaced','DEPLOYMENT')
    for prop in d['properties']:
        c.shape(prop,['property','arguments']);c.ref(prop['property'],records,'property')
        params=records[prop['property']['id']]['data']['parameters']
        c.require(set(prop['arguments'])=={p['name'] for p in params},'PROPERTY_ARGUMENTS')
        for p in params:c.integer(prop['arguments'][p['name']],p['min'],p.get('max',1000))
    c.require(isinstance(d['modes'],list) and d['modes'],'WEAPON_MODES')
    c.require(len({m['id'] for m in d['modes']})==len(d['modes']),'DUPLICATE_MODE')
    for m in d['modes']:
        c.shape(m,['id','name','attackKind','delivery','damage','range','costs','action'],['save','manualRules','area','consumption'])
        c.local(m['id']);c.ref(m['action'],records,'action')
        c.require(m['attackKind'] in ['melee','ranged','area'] and m['delivery'] in ['attack_roll','target_test'],'WEAPON_MODE')
        c.require(m['costs']==[],'MANUAL_RESOURCE_COSTS_ONLY')
        if 'manualRules' in m:c.manuals(m['manualRules'])
        if 'save' in m:
            c.shape(m['save'],['attribute','dcPolicy'],['successOutcome','outcomes'])
            c.require(m['save']['attribute']=='dexterity' and m['save']['dcPolicy']=='phb.grenade_dc.v1','GRENADE_SAVE_SUBSET')
            c.require(('successOutcome' in m['save']) != ('outcomes' in m['save']),'SAVE_OUTCOME_REPRESENTATION')
            if 'outcomes' in m['save']:
                validate_save_outcomes(m['save']['outcomes'])
            else:c.require(m['save']['successOutcome']=='unresolved','UNRESOLVED_SAVE_OUTCOME')
        if 'area' in m:
            c.shape(m['area'],['shape','radius']);c.require(m['area']['shape']=='sphere','AREA_SHAPE');c.shape(m['area']['radius'],['value','unit']);c.integer(m['area']['radius']['value'],1,1000000);c.require(m['area']['radius']['unit']=='ft','AREA_UNIT')
        if 'consumption' in m:
            c.shape(m['consumption'],['resource','quantity','on']);c.require(m['consumption']=={'resource':'item_quantity','quantity':1,'on':'committed_use'},'ITEM_CONSUMPTION')
        c.require(m['damage'],'DAMAGE_REQUIRED')
        for component in m['damage']:
            c.shape(component,['id','dice','bonus','damageType']);c.local(component['id']);c.ref(component['damageType'],records,'damage_type');c.number(component['bonus'])
            dice=component['dice'];c.shape(dice,['count','sides','bonus']);c.integer(dice['count'],1,100);c.integer(dice['sides'],2,1000);c.integer(dice['bonus'],-1000000,1000000)
        r=m['range']
        if r['kind']=='reach':c.shape(r,['kind','distance']);distances=[r['distance']]
        else:c.shape(r,['kind','normal','long']);c.require(r['kind']=='distance','RANGE_KIND');distances=[r['normal'],r['long']];c.require(r['long']['value']>=r['normal']['value'],'RANGE_ORDER')
        for distance in distances:c.shape(distance,['value','unit']);c.require(distance['unit']=='ft','RANGE_UNIT');c.integer(distance['value'],1,1000000)

def validate_save_outcomes(outcomes):
    """Explicit rational scaling only. Absence never supplies a default."""
    c.shape(outcomes,['failure','success'])
    for outcome in outcomes.values():
        c.shape(outcome,['damageMultiplier','rounding'])
        c.shape(outcome['damageMultiplier'],['numerator','denominator'])
        c.integer(outcome['damageMultiplier']['numerator'],0,10)
        c.integer(outcome['damageMultiplier']['denominator'],1,10)
        c.require(outcome['rounding']=='floor','DAMAGE_ROUNDING')

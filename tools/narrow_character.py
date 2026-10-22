"""Deterministic level-1 Human/Schola/Veteran conformance projection.

This is an offline rules proof, not application authorization or a dice executor.
Approved item-specific save outcomes support the narrow manual-play gate.
"""
import copy
import uuid
import content_import as c
import character_creation as creation
import phb_policies as p

ENGINE='phb-narrow-proof.2'

def source(id):return {'kind':'content','ref':{'id':id}}
def modifier(id,value,owner,label,contextual=False):
    return {'id':id,'value':value,'source':source(owner),'label':label,'contextual':contextual}

def project(draft, records=None):
    records=records if records is not None else c.load()[1]
    out=creation.validate_character_selection(draft,records)
    if 'projection' not in out or out['errors']:return out
    s=draft.get('selections',{});v=out['projection']['values'];proj=out['projection']
    def block(code,field,message):out['unresolved'].append({'code':code,'field':field,'message':message,'rulingIds':[]})
    def invalid(code,field,message):out['errors'].append({'code':code,'field':field,'message':message,'rulingIds':[]})
    scope=(s.get('species')=={'id':'di.species.human'} and s.get('background')=={'id':'di.background.schola_progenium'} and s.get('classes')==[{'class':{'id':'di.class.veteran'},'level':1}])
    trait=next((a.get('optionIds') for a in s.get('answers',[]) if a.get('choice',{}).get('id')=='di.choice.creation.universal_trait'),[])
    if not scope or trait!=['universal_twitchy']:
        block('OUTSIDE_NARROW_PROFILE','selections','This reviewed profile supports Human/Schola/Veteran level 1 with Twitchy only.');return out
    # Scope is checked against selections, never a caller's claim of readiness.
    package=c.read(c.PACKAGE/'review/veteran-starting-package.json')
    choices=draft.get('startingPackageChoices',{})
    if not isinstance(choices,dict):choices={};invalid('PACKAGE_CHOICES','startingPackageChoices','Expected selected package option IDs.')
    inventory=draft.get('inventory',[]);actual={};expected={x['item']['id']:x['quantity'] for x in package['fixed']}
    for row in package['choices']:
        pick=choices.get(row['id'])
        if pick not in [x['id'] for x in row['options']]:block('PACKAGE_CHOICE_REQUIRED','startingPackageChoices.'+row['id'],'Select a reviewed package option.')
        else:expected[pick]=row['quantity']
    if set(choices)-{x['id'] for x in package['choices']}:invalid('UNKNOWN_PACKAGE_CHOICE','startingPackageChoices','Unknown package choice.')
    for item in inventory if isinstance(inventory,list) else []:
        if not isinstance(item,dict):continue
        id=item.get('definition',{}).get('id')
        if not isinstance(id,str):continue
        if id in actual:invalid('DUPLICATE_ITEM','inventory','Duplicate inventory definition.')
        actual[id]=item.get('quantity')
    if actual!=expected:block('STARTING_PACKAGE_MISMATCH','inventory','Inventory must contain the complete selected level-1 kit with exact quantities; no extras are certified by this scope.')
    if out['errors']:
        out['status']='INVALID';return out
    if any(x['code'] not in ['STARTING_EQUIPMENT_CONTENT_BLOCKED','PLAYABLE_PROFILE_MISSING'] for x in out['unresolved']):
        out['status']='INCOMPLETE';return out
    out['unresolved']=[]
    mods=v['attributeModifiers'];pb=v['proficiencyBonus']
    # One source armour, no competing protection or stack-policy assumption.
    armour=[i for i in inventory if i['definition']['id'].startswith('di.armour.') and i.get('equipped')]
    if len(armour)!=1 or armour[0]['definition']['id']!='di.armour.flak_armour':
        block('NARROW_ARMOUR_REQUIRED','inventory','Equip exactly the selected Flak Armour.');out['status']='INCOMPLETE';return out
    v['maximumWounds']=p.hp_gain(proj['classTraining']['hitDie'],mods['constitution'],first=True)
    armourdata=records['di.armour.flak_armour']['data']
    v['defence']=p.armour_ac(armourdata['defence']['value']['value'],mods['dexterity'])
    v['initiative']=mods['dexterity']+sum(e['value']['value'] for f in proj['features'] for e in records[f['id']]['data']['effects'] if e['target']['key']=='initiative' and e['automation']=='automatic')
    saveattrs=proj['classTraining']['savingThrowAttributes']
    v['saves']={a:{'modifier':mods[a]+(pb if a in saveattrs else 0),'proficient':a in saveattrs} for a in creation.ATTRIBUTES}
    skills=set();groups=set();direct=set()
    for prof in proj['proficiencies']:
        d=records[prof['id']]['data']
        if d['category']=='skill':skills.update(x['id'] for x in d['appliesTo']['ids'])
        elif d['category']=='weapon_group':groups.update(d['appliesTo']['groups'])
        elif d['category']=='weapon':direct.update(x['id'] for x in d['appliesTo']['ids'])
    v['skills']={id:{'attribute':e['data']['attributeKey'],'proficient':id in skills,'modifier':mods[e['data']['attributeKey']]+(pb if id in skills else 0)} for id,e in records.items() if e['kind']=='skill'}
    starting={id for id in expected if records[id]['kind'] in ['weapon','shield']}
    proj['weaponProficiencies']={'groups':sorted(groups),'specificWeapons':sorted(direct),'startingPackageWeapons':sorted(starting)}
    proj['inventory']=copy.deepcopy(inventory)
    frag=records['di.weapon.frag_grenade']['data']['modes'][0]
    if 'outcomes' not in frag.get('save',{}) or 'area' not in frag or 'consumption' not in frag:
        block('FRAG_SAVE_STRUCTURE_REQUIRED','inventory.di.weapon.frag_grenade','Explicit approved save outcomes, area and consumption are required.');out['status']='INCOMPLETE';return out
    from phb_equipment import validate_save_outcomes
    validate_save_outcomes(frag['save']['outcomes'])
    proj['grenadeSaveIntent']={'item':{'id':'di.weapon.frag_grenade'},'saveAttribute':frag['save']['attribute'],'dc':p.grenade_dc(1,mods['dexterity']),'area':copy.deepcopy(frag['area']),'damage':copy.deepcopy(frag['damage']),'abilityDamageBonus':p.save_weapon_damage_bonus(mods['dexterity']),'outcomes':copy.deepcopy(frag['save']['outcomes']),'consumption':copy.deepcopy(frag['consumption']),'resolution':'STRUCTURED','multiTargetDamageRollPolicy':'DEFERRED'}
    proj['features']=copy.deepcopy(proj['features'])
    proj['actions']=[{'ref':records[id]['data']['modes'][0]['action'],'item':{'id':id},'modeId':'base','resolution':'context_required'} for id in sorted(starting)]
    for f in proj['features']:
        if f['id']=='di.feature.class.veteran.level_1.tactical_aim':proj['actions'].append({'feature':f,'label':'Tactical Aim','resolution':'manual_context','economy':'bonus_action','effect':'Next ranged weapon attack against the chosen visible target this turn deals proficiency bonus extra damage.'})
    proj['actions'] += [{'label':'Faith, Fear, or Discipline','resolution':'manual','source':{'id':'di.feature.species.human.traits'},'uses':'Once per long rest; reroll failed save; must use new result.'},{'label':'Use Med-Pack','resolution':'manual','source':{'id':'di.equipment.med_pack'}}]
    # This snapshot pins every canonical record plus the approved policy document and kit.
    decisions=c.read(c.PACKAGE/'review/decisions.json')
    pin={'records':{id:c.digest(e) for id,e in sorted(records.items())},'approvals':c.digest({'human':decisions['humanRulings'],'item':decisions.get('itemRulings',[])}),'package':package,'engine':ENGINE}
    proj['lockDigest']=c.digest(pin);proj['engineVersion']=ENGINE
    proj['snapshotScope']='Offline content proof pin; not a published ruleset lock or runtime authorization.'
    proj['unresolvedFields']=[]
    proj['runtimeDeferred']=['multiTargetDamageRollPolicy','runtimeActionTransactions','authoritativeContextAndOwnership','publishedRulesetLock']
    proj['note']='Playable with source-defined manual procedures within the reviewed narrow scope; offline conformance is not runtime authorization.'
    out['status']='VALID';out['playability']='PLAYABLE_WITH_MANUAL_RULES';proj['readiness']='READY_WITH_MANUAL_RULES'
    out['dependencyAnalysis']={'creationBlockers':[],'resolvedItemRulings':['PHB-RULE-059'],'outsideScopeRulings':[x['id'] for x in c.read(c.PACKAGE/'review/human-rulings-integration.json') if x['status']=='UNRESOLVED'],'manualProcedures':['Human failed-save reroll','Schola conditional fear advantage and education','Tactical Aim target/turn tracking','Med-Pack use','Reload/ammunition and ordinary action adjudication'],'runtimeDeferred':proj['runtimeDeferred']}
    return out

def compile_rolls(projection, context, records=None, weapon_ids=None):
    """Compile baseline conformance intents from explicit, bounded test context.

    These definitions don't spend ammo, authorize attacks, or apply damage. A
    production caller must revalidate context and record accepted hit outcomes.
    """
    records=records if records is not None else c.load()[1]
    c.require(projection.get('engineVersion')==ENGINE and projection.get('lockDigest'),'NARROW_PROJECTION_REQUIRED')
    c.require(projection['values']['maximumWounds'] is not None,'INCOMPLETE_PROJECTION')
    c.shape(context,['stateVersion','mode','rangeBand','advantage','targetId','executionNonce','finesseAbility','tacticalAim','critical'])
    c.integer(context['stateVersion'],0,2147483647)
    c.require(context['mode']=='baseline_conformance' and context['rangeBand']=='normal' and context['advantage']=='normal' and context['tacticalAim'] is False and context['critical'] is False,'CONTEXT_UNSUPPORTED')
    c.require(context['finesseAbility'] in ['strength','dexterity'],'FINESSE_SELECTION_REQUIRED')
    c.require(all(isinstance(context[k],str) and context[k] for k in ['targetId','executionNonce']),'CONTEXT_ID_REQUIRED')
    values=projection['values'];mods=values['attributeModifiers'];pb=values['proficiencyBonus'];owner='di.class.veteran'
    c.require(values['skills']['di.skill.athletics']['proficient'], 'PROOF_ATHLETICS_PROFICIENCY_REQUIRED')
    snapshot={'rulesetLockDigest':projection['lockDigest'],'engineVersion':ENGINE,'stateVersion':context['stateVersion'],'contextDigest':c.digest({'context':context,'inventory':projection['inventory']})}
    def roll(key,label,category,groups,modifiers,owner=owner,damage=None,action=None):
        component={'id':'base','groups':groups,'modifiers':modifiers}
        if damage:component['damageType']=damage
        result={'schemaVersion':1,'id':str(uuid.uuid5(uuid.NAMESPACE_URL,c.digest({'snapshot':snapshot,'actor':projection['actorId'],'key':key,'component':component}))), 'category':category,'label':label,'source':source(owner),'actor':{'kind':'character','instanceId':projection['actorId']},'snapshot':snapshot,'components':[component],'advantage':{'state':'normal','policyId':'phb.advantage.v1','appliedGroupIds':[]},'critical':{'policyId':'phb.critical.v1','status':'disabled'}}
        if category!='damage':result['natural']={'componentId':'base','groupId':'base'}
        if category=='attack':result['critical'].update(status='enabled',threshold=20,comparison='at_least')
        if action:result['action']=action
        return result
    d20=[{'id':'base','count':1,'sides':20}]
    rolls=[roll('ability.strength','Strength check','attribute',d20,[modifier('ability',mods['strength'],owner,'Strength')]),roll('skill.athletics','Athletics','skill',d20,[modifier('ability',mods['strength'],owner,'Strength'),modifier('proficiency',pb,'di.skill.athletics','Proficiency')]),roll('save.dexterity','Dexterity save','save',d20,[modifier('ability',mods['dexterity'],owner,'Dexterity'),modifier('proficiency',pb,owner,'Save proficiency')]),roll('initiative','Initiative','ability',d20,[modifier('ability',mods['dexterity'],owner,'Dexterity'),modifier('twitchy',values['initiative']-mods['dexterity'],'di.feature.universal.twitchy','Twitchy')])]
    wp=projection['weaponProficiencies']
    for id in (weapon_ids if weapon_ids is not None else ['di.weapon.lasgun','di.weapon.combat_blade']):
        c.require(any(i['definition']['id']==id for i in projection['inventory']),'WEAPON_NOT_OWNED')
        weapon=records[id];d=weapon['data'];m=d['modes'][0]
        ability=p.weapon_ability(d['category'],finesse=d['abilityBinding']['attack']=='finesse',selected=context['finesseAbility'])
        proficient=p.weapon_proficient(id,d['proficiencyGroups'],wp['groups'],wp['specificWeapons'],wp['startingPackageWeapons'])
        attackmods=[modifier('ability',mods[ability],id,ability.title())]
        if proficient:attackmods.append(modifier('proficiency',pb,owner,'Weapon proficiency'))
        execution=str(uuid.uuid5(uuid.NAMESPACE_URL,c.digest({'actor':projection['actorId'],'snapshot':snapshot,'weapon':id})))
        action={'ref':m['action'],'executionId':execution,'stageId':'attack','modeId':m['id']}
        rolls.append(roll(id+'.attack',weapon['name']+' attack','attack',d20,attackmods,id,action=action))
        component=m['damage'][0];dice=component['dice'];action=dict(action,stageId='damage')
        rolls.append(roll(id+'.damage',weapon['name']+' damage','damage',[{'id':'base','count':dice['count'],'sides':dice['sides']}],[modifier('ability',mods[ability],id,ability.title()),modifier('printed',dice['bonus']+component['bonus']['value'],id,'Printed bonus')],id,component['damageType'],action))
    for r in rolls:validate_roll(r,records)
    return rolls

def compile_grenade_intent(projection, context, records=None):
    """Separate base damage definition from per-target save outcomes.

    No damage-sharing policy, target save bonus or resource mutation is inferred.
    """
    records=records if records is not None else c.load()[1]
    baseline=compile_rolls(projection,context,records)
    c.require(any(i['definition']['id']=='di.weapon.frag_grenade' and i['quantity']>0 for i in projection['inventory']),'GRENADE_NOT_OWNED')
    mode=records['di.weapon.frag_grenade']['data']['modes'][0]
    from phb_equipment import validate_save_outcomes
    validate_save_outcomes(mode['save'].get('outcomes'))
    c.require(records['di.weapon.frag_grenade']['data']['abilityBinding']['damage']=='none','GRENADE_ABILITY_EXCLUDED')
    snapshot=copy.deepcopy(baseline[0]['snapshot']);components=[]
    for damage in mode['damage']:
        dice=damage['dice'];printed=dice['bonus']+damage['bonus']['value']
        components.append({'id':damage['id'],'groups':[{'id':'base','count':dice['count'],'sides':dice['sides']}],'modifiers':[] if printed==0 else [modifier('printed',printed,'di.weapon.frag_grenade','Printed bonus')],'damageType':damage['damageType']})
    execution=str(uuid.uuid5(uuid.NAMESPACE_URL,c.digest({'actor':projection['actorId'],'snapshot':snapshot,'weapon':'di.weapon.frag_grenade'})))
    roll={'schemaVersion':1,'id':str(uuid.uuid5(uuid.NAMESPACE_URL,c.digest({'execution':execution,'components':components,'stage':'damage'}))),'category':'damage','label':'Frag Grenade base damage','source':source('di.weapon.frag_grenade'),'actor':{'kind':'character','instanceId':projection['actorId']},'snapshot':snapshot,'components':components,'advantage':{'state':'normal','policyId':'phb.advantage.v1','appliedGroupIds':[]},'critical':{'policyId':'phb.critical.v1','status':'disabled'},'action':{'ref':mode['action'],'executionId':execution,'stageId':'damage','modeId':'base'}}
    validate_roll(roll,records)
    values=projection['values']
    intent={'item':{'id':'di.weapon.frag_grenade'},'saveAttribute':mode['save']['attribute'],'dc':p.grenade_dc(values['level'],values['attributeModifiers']['dexterity']),'area':copy.deepcopy(mode['area']),'damage':copy.deepcopy(mode['damage']),'abilityDamageBonus':0,'outcomes':copy.deepcopy(mode['save']['outcomes']),'consumption':copy.deepcopy(mode['consumption']),'resolution':'STRUCTURED','multiTargetDamageRollPolicy':'DEFERRED','damageRoll':roll}
    intent['application']='Apply the explicit outcome to an accepted base roll separately for each accepted target save; target mitigation/HP application is outside this function.'
    return intent

def validate_roll(roll,records):
    c.shape(roll,['schemaVersion','id','category','label','source','actor','snapshot','components','advantage','critical'],['natural','action'])
    c.require(roll['schemaVersion']==1 and roll['category'] in ['attribute','skill','save','attack','damage','ability'],'ROLL_CATEGORY')
    uuid.UUID(roll['id']);c.shape(roll['source'],['kind','ref']);c.require(roll['source']['kind']=='content','ROLL_SOURCE');c.ref(roll['source']['ref'],records)
    c.shape(roll['actor'],['kind','instanceId']);c.require(roll['actor']['kind']=='character','ROLL_ACTOR');uuid.UUID(roll['actor']['instanceId'])
    s=roll['snapshot'];c.shape(s,['rulesetLockDigest','engineVersion','stateVersion','contextDigest'])
    c.require(s['engineVersion']==ENGINE and all(isinstance(s[k],str) and len(s[k])==64 for k in ['rulesetLockDigest','contextDigest']),'ROLL_SNAPSHOT');c.integer(s['stateVersion'],0,2147483647)
    c.require(roll['components'] and len(roll['components'])<=16,'ROLL_COMPONENTS')
    c.require(roll['advantage']=={'state':'normal','policyId':'phb.advantage.v1','appliedGroupIds':[]},'ROLL_ADVANTAGE_SUBSET')
    expectedcritical={'policyId':'phb.critical.v1','status':'disabled'}
    if roll['category']=='attack':expectedcritical.update(status='enabled',threshold=20,comparison='at_least')
    c.require(roll['critical']==expectedcritical,'ROLL_CRITICAL_POLICY')
    c.require(len({x['id'] for x in roll['components']})==len(roll['components']),'DUPLICATE_COMPONENT')
    dice_count=0
    for comp in roll['components']:
        c.shape(comp,['id','groups','modifiers'],['damageType']);c.local(comp['id'])
        c.require(('damageType' in comp)==(roll['category']=='damage'),'DAMAGE_TYPE_REQUIRED')
        if 'damageType' in comp:c.ref(comp['damageType'],records,'damage_type')
        c.require(len({m['id'] for m in comp['modifiers']})==len(comp['modifiers']),'DUPLICATE_MODIFIER')
        c.require(len(comp['modifiers'])<=32 and len({g['id'] for g in comp['groups']})==len(comp['groups']),'ROLL_GROUP_BOUNDS')
        for g in comp['groups']:
            c.shape(g,['id','count','sides']);c.local(g['id']);c.integer(g['count'],1,100);c.integer(g['sides'],2,1000);dice_count+=g['count']
        for m in comp['modifiers']:
            c.shape(m,['id','value','source','label','contextual']);c.integer(m['value'],-1000000,1000000);c.ref(m['source']['ref'],records);c.require(type(m['contextual']) is bool,'CONTEXTUAL_BOOLEAN')
    c.require(dice_count<=100,'ROLL_DICE_BUDGET')
    if 'natural' in roll:
        c.shape(roll['natural'],['componentId','groupId'])
        matches=[g for comp in roll['components'] if comp['id']==roll['natural']['componentId'] for g in comp['groups'] if g['id']==roll['natural']['groupId']]
        c.require(len(matches)==1 and matches[0]['count']==1,'ROLL_NATURAL')
    if 'action' in roll:
        c.shape(roll['action'],['ref','executionId','stageId','modeId']);c.ref(roll['action']['ref'],records,'action');uuid.UUID(roll['action']['executionId'])
        c.require(roll['action']['stageId']==roll['category'] and roll['action']['modeId']=='base','ROLL_STAGE')
    return True

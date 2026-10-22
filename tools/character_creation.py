"""Offline draft validation/projection for the existing CharacterModel selections.

This is a conformance adapter, not a runtime API or a playable ruleset. All
unresolved PHB rules stay unresolved. No user-supplied fact can approve a ruling.
"""
import copy
from collections import Counter
import content_import as ci
import phb_policies as policy

ATTRIBUTES=('strength','dexterity','constitution','intelligence','wisdom','charisma')
STANDARD_ARRAY=[8,10,12,13,14,15]

def validate_character_selection(draft, records=None):
    records=records if records is not None else ci.load()[1]
    errors=[];unresolved=[];selected=[];features={};proficiencies=set();pending={};increases=Counter()
    def problem(code,field,message,rulings=(),invalid=False):
        (errors if invalid else unresolved).append({'code':code,'field':field,'message':message,'rulingIds':list(rulings)})
    if not isinstance(draft,dict):return {'status':'INVALID','eligibilityStatus':'INVALID','errors':[{'code':'DRAFT_OBJECT_REQUIRED','field':'','message':'Expected a draft object.','rulingIds':[]}],'unresolved':[]}
    s=draft.get('selections',{})
    if not isinstance(s,dict):return validate_character_selection(None,records)
    def resolve(ref,kind,field):
        if ref is None:problem('SELECTION_REQUIRED',field,'Choose '+kind+'.');return None
        if not isinstance(ref,dict) or set(ref)!={'id'} or not isinstance(ref['id'],str):problem('REFERENCE_INVALID',field,'Expected one content ID.',invalid=True);return None
        e=records.get(ref['id'])
        if e is None:problem('CONTENT_NOT_CANONICAL',field,'Content is missing or still an incomplete candidate.');return None
        if e['kind']!=kind:problem('REFERENCE_KIND',field,'Expected '+kind+'.',invalid=True);return None
        return e
    species=resolve(s.get('species'),'species','selections.species')
    origin=resolve(s.get('background'),'background','selections.background')
    classes=s.get('classes',[])
    if not isinstance(classes,list):problem('CLASSES_ARRAY','selections.classes','Classes must be an array.',invalid=True);classes=[]
    if len(classes)!=1:problem('SINGLE_CLASS_REQUIRED','selections.classes','No reviewed multiclass policy exists; this adapter supports one class.',invalid=len(classes)>1)
    if any(not isinstance(c,dict) for c in classes):problem('CLASS_ENTRY_OBJECT','selections.classes','Each class entry must be an object.',invalid=True)
    entry=classes[0] if len(classes)==1 and isinstance(classes[0],dict) else {}
    klass=resolve(entry.get('class'),'class','selections.classes.0.class')
    level=entry.get('level')
    if type(level) is not int or not 1<=level<=20:problem('LEVEL_INVALID','selections.classes.0.level','Level must be an integer from1 to20.',invalid=level is not None);level=None
    subclass=resolve(entry['subclass'],'subclass','selections.classes.0.subclass') if 'subclass' in entry else None
    selected=[e['id'] for e in (species,origin,klass) if e]
    snapshot={'selected':selected,'classLevels':{klass['id']:level} if klass and level else {},'totalLevel':level,'facts':{}}
    # Facts are intentionally empty: no human rulings have been approved.
    def eligible(e,field,code):
        if e and 'requirements' in e['data']:
            answer=policy.evaluate(e['data']['requirements'],snapshot)
            if answer is False:problem(code,field,'Selected '+e['name']+' does not meet its canonical prerequisite.',invalid=True)
            elif answer is None:
                ids=ci.read(ci.PACKAGE/'review/creation-readiness.json').get('originRulings',{}).get(e['id'],[]) if e['kind']=='background' else []
                problem('ELIGIBILITY_UNRESOLVED',field,'Prerequisite requires missing information or an unapproved ruling.',ids)
    eligible(origin,'selections.background','ORIGIN_NOT_ELIGIBLE')
    eligible(klass,'selections.classes.0.class','CLASS_NOT_ELIGIBLE')
    if subclass:
        if not klass or subclass['data']['parentClass']['id']!=klass['id']:
            problem('SUBCLASS_PARENT_MISMATCH','selections.classes.0.subclass','Subclass belongs to a different class.',invalid=True)
        else:eligible(subclass,'selections.classes.0.subclass','SUBCLASS_NOT_ELIGIBLE')
    eligibility_status='INVALID' if errors else ('INCOMPLETE' if unresolved else 'VALID')
    if subclass and eligibility_status!='INVALID':selected.append(subclass['id'])
    base=s.get('attributes',{})
    if not isinstance(base,dict):problem('ATTRIBUTES_OBJECT','selections.attributes','Attributes must be an object.',invalid=True);base={}
    if set(base)-set(ATTRIBUTES):problem('ATTRIBUTE_KEY_UNKNOWN','selections.attributes','Unknown attribute key.',invalid=True)
    if set(base)!=set(ATTRIBUTES):problem('ATTRIBUTES_REQUIRED','selections.attributes','Assign the standard array to all six attributes.')
    elif any(type(v) is not int for v in base.values()) or sorted(base.values())!=STANDARD_ARRAY:
        problem('STANDARD_ARRAY_REQUIRED','selections.attributes','Expected exactly15,14,13,12,10,8 before species bonuses. Alternate methods are unresolved.',['PHB-RULE-012'],invalid=True)
    answers=s.get('answers',[])
    if not isinstance(answers,list):problem('ANSWERS_ARRAY','selections.answers','Answers must be an array.',invalid=True);answers=[]
    answer_map={};occurrences=set()
    for n,a in enumerate(answers):
        if not isinstance(a,dict) or not isinstance(a.get('choice'),dict) or set(a['choice'])!={'id'} or not isinstance(a['choice']['id'],str) or not isinstance(a.get('occurrenceId'),str):
            problem('ANSWER_SHAPE',f'selections.answers.{n}','Answer needs a choice reference.',invalid=True);continue
        key=a['choice']['id']
        if key in answer_map or a.get('occurrenceId') in occurrences:problem('DUPLICATE_ANSWER',f'selections.answers.{n}','Duplicate choice or occurrence.',invalid=True)
        answer_map[key]=a;occurrences.add(a.get('occurrenceId'))
        if a.get('status')!='valid':problem('STALE_ANSWER',f'selections.answers.{n}','Stale answers must be revalidated.')
    visiting=set();visited=set();consumed=set()
    def grant(g):
        k=g['kind']
        if k=='feature':visit(g['feature']['id'])
        elif k=='proficiency':proficiencies.add(g['proficiency']['id'])
        elif k=='choice':choice(g['choice']['id'])
        elif k=='attribute_increase':increases[g['attributeKey']]+=g['amount']
        elif k=='select':
            target=records[g['content']['id']];eligible(target,'selections.answers','OPTION_NOT_ELIGIBLE')
            if target['kind']=='subclass' and (not subclass or target['id']!=subclass['id']):problem('SUBCLASS_ANSWER_MISMATCH','selections.answers','Subclass answer disagrees with selected subclass.',invalid=True)
        else:problem('GRANT_NOT_IMPLEMENTED','selections.answers','Grant needs a reviewed implementation: '+k)
    def choice(key):
        if key in pending:return
        e=records[key];d=e['data'];pending[key]={'choice':{'id':key},'status':'INCOMPLETE'}
        a=answer_map.get(key)
        if a is None and d['purpose']=='subclass' and subclass:
            matching=[o['id'] for o in d['options'] if any(g.get('content',{}).get('id')==subclass['id'] for g in o['grants'])]
            a={'optionIds':matching}
        if a is None:problem('CHOICE_REQUIRED','selections.answers',f'Answer required: {e["name"]}.');return
        consumed.add(key);options=a.get('optionIds');card=d['cardinality']
        if not isinstance(options,list) or any(not isinstance(o,str) for o in options) or len(set(options))!=len(options) or not card['min']<=len(options)<=card['max']:
            problem('CHOICE_CARDINALITY','selections.answers','Invalid number or duplicate options for '+key,invalid=True);return
        byid={o['id']:o for o in d['options']}
        if any(o not in byid for o in options):problem('CHOICE_OPTION_UNKNOWN','selections.answers','Unknown option in '+key,invalid=True);return
        pending[key]['status']='VALID'
        for option in options:
            for g in byid[option]['grants']:grant(g)
    def visit(key):
        if key in visiting:problem('CHOICE_CYCLE','selections.answers','Cyclic unlock graph.',invalid=True);return
        if key in visited:return
        visiting.add(key);e=records[key];d=e['data']
        if e['kind']=='feature':
            eligible(e,'selections.answers','FEATURE_NOT_ELIGIBLE');features[key]=e
            for g in d['grants']:grant(g)
        for f in d.get('features',[]):visit(f['id'])
        for ch in d.get('choices',[]):choice(ch['id'])
        visiting.remove(key);visited.add(key)
    for e in (species,origin,klass):
        if e:visit(e['id'])
    if klass and level:
        for row in records[klass['data']['progression']['id']]['data']['entries']:
            if row['level']<=level:
                for g in row['grants']:grant(g)
    if subclass and klass and level and subclass['data']['parentClass']['id']==klass['id'] and eligibility_status!='INVALID':
        visit(subclass['id'])
        for row in records[subclass['data']['progression']['id']]['data']['entries']:
            if row['level']<=level:
                for g in row['grants']:grant(g)
    choice('di.choice.creation.universal_trait')
    for key in answer_map.keys()-consumed:problem('UNGRANTED_CHOICE','selections.answers','Answer was not granted: '+key,invalid=True)
    # Derive only unconditional, source-defined baselines. Conditional context and
    # arbitrary manual text never contribute to a numeric result.
    attributes=copy.deepcopy(base);speed=None;manual=[]
    for e in features.values():
        for effect in e['data']['effects']:
            if effect['automation']!='automatic' or effect['value']['kind']!='constant':continue
            target=effect['target']['key'];value=effect['value']['value']
            if target=='movement.walk' and effect['operation']=='base':speed=value
            if target.startswith('attribute.') and target.endswith('.score') and effect['operation']=='add':increases[target.split('.')[1]]+=value
        for rule in e['data']['manualRules']:manual.append({'source':{'id':e['id']},'localId':rule['id'],'text':rule['text'],'reason':rule['reason']})
    for key,amount in increases.items():
        if type(attributes.get(key)) is int:attributes[key]+=amount
    problem('ATTRIBUTE_MODIFIER_POLICY_BLOCKED','calculated.attributeModifiers','No approved score-to-modifier rule.',['PHB-RULE-009'])
    problem('STARTING_EQUIPMENT_CONTENT_BLOCKED','inventory','Complete class loadout cannot yet be validated.',['PHB-RULE-024','PHB-RULE-051'])
    problem('PLAYABLE_PROFILE_MISSING','rulesetLock','No source-reviewed playable PHB profile/lock is available.')
    if level and level>=4:problem('ADVANCEMENT_POLICY_BLOCKED','selections.answers','ASI/Talent validation needs rulings.',['PHB-RULE-015','PHB-RULE-016'])
    if not isinstance(draft.get('inventory',[]),list):problem('INVENTORY_ARRAY','inventory','Inventory must be an array.',invalid=True)
    for n,item in enumerate(draft.get('inventory',[]) if isinstance(draft.get('inventory',[]),list) else []):
        if not isinstance(item,dict):problem('ITEM_SHAPE',f'inventory.{n}','Expected inventory item.',invalid=True);continue
        if type(item.get('quantity')) is not int or item['quantity']<1:problem('ITEM_QUANTITY',f'inventory.{n}.quantity','Quantity must be a positive integer.',invalid=True)
        definition=item.get('definition',{})
        if not isinstance(definition,dict) or set(definition)!={'id'} or not isinstance(definition['id'],str):problem('ITEM_REFERENCE_INVALID',f'inventory.{n}.definition','Expected one item content ID.',invalid=True);continue
        if definition['id'] not in records:problem('ITEM_CONTENT_BLOCKED',f'inventory.{n}.definition','Item is not canonical yet.');continue
        e=records[definition['id']]
        if e['kind'] not in ['weapon','armour','shield','equipment','ammunition','consumable','tool','augmetic']:problem('ITEM_KIND',f'inventory.{n}.definition','Reference is not equipment.',invalid=True)
        req=e['data'].get('requirements',{}).get('equip')
        if item.get('equipped') and req:
            allowed=policy.evaluate(req,snapshot)
            if allowed is False:problem('ITEM_NOT_ELIGIBLE',f'inventory.{n}','Actor cannot equip this item.',invalid=True)
            elif allowed is None:problem('ITEM_ELIGIBILITY_UNRESOLVED',f'inventory.{n}','Equipment prerequisite is unresolved.')
    status='INVALID' if errors else ('INCOMPLETE' if unresolved else 'VALID')
    training=next((x for x in ci.read(ci.PACKAGE/'review/class-calculation-inputs.json') if klass and x['class']['id']==klass['id']),None)
    known_powers=next((x for x in training.get('knownPowers',[]) if x['level']==level),None) if training else None
    return {'status':status,'eligibilityStatus':eligibility_status,'eligibilityScope':'species/origin/class/subclass prerequisites only','errors':errors,'unresolved':unresolved,'projection':{
        'actorId':draft.get('id'),'engineVersion':'phb-readiness-offline.1','lockDigest':None,
        'classTraining':{'hitDie':training['hitDie'],'savingThrowAttributes':training['savingThrows'],'source':training['source']} if training else None,
        'knownPowerCounts':known_powers,
        'values':{'level':level,'attributes':attributes,'proficiencyBonus':policy.proficiency(level) if level else None,'movement':{'baseWalk':{'value':speed,'unit':'ft'}} if speed is not None else {},'attributeModifiers':None,'maximumWounds':None,'defence':None,'initiative':None,'skills':None,'saves':None},
        'features':[{'id':i} for i in sorted(features)],'proficiencies':[{'id':i} for i in sorted(proficiencies)],'manualRules':manual,'pendingChoices':list(pending.values()),
        'actions':[],'rollDefinitions':[],'resources':None,'resistances':None,
        'unresolvedFields':['attributeModifiers','maximumWounds','defence','initiative','skills','saves','actions','rollDefinitions','resources','resistances'],
        'readiness':'INCOMPLETE','note':'Draft projection; not a published CalculatedCharacter or playable character. Base movement may have unresolved feature/condition adjustments.'}}

def validateCharacterSelection(characterDraft):
    return validate_character_selection(characterDraft)

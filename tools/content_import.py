"""Validate and prepare the explicitly supported PHB draft subset; never publish it.

Standard-library only. This is not a general JSON Schema interpreter or database writer.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'content/packages/di_phb_1_0'
ID = re.compile(r'^[a-z][a-z0-9_]{1,31}\.[a-z][a-z0-9_]{1,31}\.[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$')
LOCAL = re.compile(r'^[a-z][a-z0-9_]{0,63}$')

class InvalidContent(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise InvalidContent(message)

def pairs(items):
    obj = {}
    for key, value in items:
        require(key not in obj, 'DUPLICATE_JSON_KEY: ' + key)
        obj[key] = value
    return obj

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs)

def canonical(value):
    # This import subset contains only exact safe integers, strings, booleans and containers.
    # Object keys are ASCII schema keys. Do not generalize to arbitrary RFC 8785 numbers/keys.
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def shape(value, required, optional=()):
    require(isinstance(value, dict), 'OBJECT_REQUIRED')
    require(set(required) <= value.keys(), 'MISSING_FIELD: ' + str(set(required)-value.keys()))
    require(value.keys() <= set(required)|set(optional), 'UNKNOWN_FIELD: ' + str(value.keys()-set(required)-set(optional)))

def integer(value, low, high):
    require(type(value) is int and low <= value <= high, 'INTEGER_BOUNDS: ' + str(value))

def ref(value, records, kind=None):
    shape(value, ['id'])
    require(value['id'] in records, 'REFERENCE_NOT_FOUND: ' + value['id'])
    if kind:
        require(records[value['id']]['kind'] == kind, 'REFERENCE_KIND: ' + value['id'])

def refs(values, records, kind):
    require(isinstance(values, list), 'REFERENCE_ARRAY_REQUIRED')
    require(len({x['id'] for x in values}) == len(values), 'DUPLICATE_REFERENCE')
    for value in values: ref(value, records, kind)

def local(value):
    require(isinstance(value, str) and LOCAL.fullmatch(value), 'LOCAL_ID: ' + str(value))

def number(value):
    require(isinstance(value, dict), 'NUMBER_VALUE')
    if value.get('kind') == 'constant':
        shape(value, ['kind', 'value']); integer(value['value'], -1000000, 1000000)
    else:
        raise InvalidContent('UNSUPPORTED_NUMBER_VALUE_IN_IMPORT_SUBSET')

def predicate(value, records, depth=0, budget=None):
    if budget is None: budget=[0]
    budget[0]+=1
    require(depth<=8 and budget[0]<=100, 'PREDICATE_BOUNDS')
    require(isinstance(value,dict),'PREDICATE_OBJECT')
    k=value.get('kind')
    if k in ['all','any']:
        shape(value,['kind','predicates'])
        require(isinstance(value['predicates'],list) and value['predicates'],'PREDICATE_SIZE')
        for child in value['predicates']:predicate(child,records,depth+1,budget)
    elif k=='not':
        shape(value,['kind','predicate']);predicate(value['predicate'],records,depth+1,budget)
    elif k=='selected':shape(value,['kind','content']);ref(value['content'],records)
    elif k=='proficient':shape(value,['kind','proficiency']);ref(value['proficiency'],records,'proficiency')
    elif k=='level':
        shape(value,['kind','axis','operator','value']);a=value['axis']
        if a.get('kind')=='class_level':shape(a,['kind','class']);ref(a['class'],records,'class')
        else:shape(a,['kind']);require(a['kind']=='total_level','LEVEL_AXIS')
        require(value['operator'] in ['eq','lt','lte','gt','gte'],'COMPARISON');integer(value['value'],0,20)
    elif k=='stat':
        shape(value,['kind','key','operator','value'])
        require(value['key'] in ['attribute.'+a+'.score' for a in ['strength','dexterity','constitution','intelligence','wisdom','charisma']],'STAT_KEY')
        require(value['operator'] in ['eq','lt','lte','gt','gte'],'COMPARISON');integer(value['value'],-1000000,1000000)
    elif k=='fact':
        shape(value,['kind','key','equals'])
        require(value['key'] in {x['key'] for x in read(PACKAGE/'review/prerequisite-facts.json')} and type(value['equals']) is bool,'FACT_VOCABULARY')
    elif k=='equipped':
        shape(value,['kind'],['itemKind','property','slot']);require(len(value)>1,'EQUIPPED_SELECTOR')
        if 'itemKind' in value:require(value['itemKind'] in ['weapon','armour','shield','equipment'],'ITEM_KIND')
        if 'property' in value:ref(value['property'],records,'property')
        if 'slot' in value:require(isinstance(value['slot'],str) and value['slot'],'SLOT')
    elif k=='tagged':
        shape(value,['kind','scope','tag']);require(value['scope'] in ['self','action_target','attack_weapon'],'SCOPE');ref(value['tag'],records,'tag')
    elif k=='health_ratio':
        shape(value,['kind','scope','operator','numerator','denominator'])
        require(value['scope'] in ['self','action_target'],'SCOPE');require(value['operator'] in ['eq','lt','lte','gt','gte'],'COMPARISON')
        integer(value['numerator'],0,1000000);integer(value['denominator'],1,1000000)
    else:raise InvalidContent('UNSUPPORTED_PREDICATE_IN_IMPORT_SUBSET: '+str(k))


def manuals(values):
    require(isinstance(values,list), 'MANUAL_ARRAY')
    require(len({x['id'] for x in values})==len(values),'DUPLICATE_MANUAL_ID')
    for m in values:
        shape(m,['id','automation','text','adjudicator','context','reason'])
        local(m['id']); require(m['automation']=='manual' and m['adjudicator'] in ['gm','player'],'MANUAL_AUTOMATION')
        require(all(isinstance(m[x],str) and m[x].strip() for x in ['text','context','reason']),'EMPTY_MANUAL')

def grants(values, records):
    require(isinstance(values,list), 'GRANT_ARRAY')
    require(len({g['id'] for g in values})==len(values),'DUPLICATE_GRANT')
    for g in values:
        local(g['id']); k=g['kind']
        if k=='attribute_increase':
            shape(g,['id','kind','attributeKey','amount']);integer(g['amount'],1,2)
            require(g['attributeKey'] in ['strength','dexterity','constitution','intelligence','wisdom','charisma'],'ATTRIBUTE_KEY')
        else:
            field={'feature':'feature','proficiency':'proficiency','choice':'choice','select':'content'}.get(k)
            require(field is not None,'UNSUPPORTED_GRANT');shape(g,['id','kind',field]);ref(g[field],records,None if k=='select' else k)

def effects(values, records=None):
    require(isinstance(values,list), 'EFFECT_ARRAY')
    require(len({x['id'] for x in values})==len(values),'DUPLICATE_EFFECT_ID')
    for e in values:
        shape(e,['id','automation','activation','target','operation','value','duration','stacking','priority'],['when'])
        local(e['id']); require(e['automation'] in ['automatic','conditional'] and e['activation']=='continuous','EFFECT_SUBSET')
        if e['automation']=='conditional':require('when' in e,'CONDITION_REQUIRED')
        if 'when' in e:require(e['automation']=='conditional','CONDITIONAL_AUTOMATION');predicate(e['when'],records)
        shape(e['target'],['kind','key','scope']);require(e['target']['kind']=='stat' and e['target']['scope']=='self','TARGET_SUBSET')
        require(e['target']['key'] in ['movement.walk','initiative','defence','sense.darkvision','action.attack.capacity']+['attribute.'+a+'.score' for a in ['strength','dexterity','constitution','intelligence','wisdom','charisma']],'STAT_KEY')
        require(e['operation'] in ['add','base'],'OPERATION');number(e['value'])
        require(e['duration']=={'kind':'while_source'},'DURATION');shape(e['stacking'],['group','mode'])
        require(e['stacking']['mode'] in (['max'] if e['target']['key'] in ['sense.darkvision','action.attack.capacity'] else ['sum','replace']),'STACK_MODE');integer(e['priority'],-1000,1000)
        if e['target']['key']=='action.attack.capacity':require(e['operation']=='base' and e['automation']=='automatic' and e['value']['kind']=='constant' and 1<=e['value']['value']<=20,'ATTACK_CAPACITY_POLICY')
        if e['target']['key']=='sense.darkvision':require(e['operation']=='base' and e['automation']=='automatic' and e['value']['kind']=='constant' and e['value']['value']>=0,'DARKVISION_POLICY')

FIELDS={
 'skill':(['attributeKey'],[]), 'proficiency':(['category','appliesTo'],[]),
 'feature':(['flavor','effects','grants','manualRules'],['choices','requirements','mechanics']),
 'choice':(['purpose','selectionMode','cardinality','repeatScope','options'],[]),
 'species':(['features','size'],['choices']), 'background':(['features'],['choices','requirements','originAvailability']),
 'property':(['appliesToKinds','parameters','effects','manualRules'],[]),
 'rule':(['role','automation','effects','manualRules'],[]),
 'progression':(['axis','maxLevel','entries'],[]),
 'class':(['features','progression'],['requirements','allowedSubclasses']),
 'subclass':(['parentClass','features','progression'],['requirements']),
 'damage_type':(['category'],[]),
 'armour':(['category','equip','properties','features','defence'],['requirements','availability','dexterityBonus']),
 'shield':(['equip','properties','features','defence'],['proficiencyGroups','aliases']),
 'weapon':(['category','subcategory','hands','properties','features','modes','proficiencyGroups','availability','abilityBinding'],['deployment','manualRules','requirements']),
 'equipment':(['features','manualRules','functionalTags'],['availability','aliases']),
 'tool':(['features','manualRules','functionalTags'],['availability']),
 'augmetic':(['features','manualRules','functionalTags','availability'],[]),
 'action':(['economy','target','costs','outcomes'],['rolls'])}

def validate_species_mechanics(values,records):
    require(isinstance(values,list),'MECHANICS_ARRAY')
    for m in values:
        k=m.get('kind')
        if k=='score_adjustment':
            shape(m,['kind','attribute','amount','minimum','phase']);require(m['attribute'] in ['strength','dexterity','constitution','intelligence','wisdom','charisma'],'ATTRIBUTE_KEY');integer(m['amount'],-20,20);integer(m['minimum'],1,30);require(m['phase']=='after_species','SPECIES_PHASE')
        elif k=='hp_per_level':shape(m,['kind','amount']);integer(m['amount'],1,20)
        elif k=='duplicate_proficiency_bonus':
            shape(m,['kind','proficiency','amount']);ref(m['proficiency'],records,'proficiency');integer(m['amount'],1,1)
        elif k=='psychic_prohibition':shape(m,['kind','classes','traits']);refs(m['classes'],records,'class');refs(m['traits'],records,'feature')
        elif k=='contextual_size':
            shape(m,['kind','increase','contexts']);require(m['increase']==1 and set(m['contexts'])<=set(['carrying','lifting','pushing','dragging','grappling','shoving','breaking']),'CONTEXTUAL_SIZE')
        elif k=='equipment_frame':shape(m,['kind','frame','text']);require(m['frame']=='ogryn' and bool(m['text']),'FRAME')
        elif k=='innate_damage':
            shape(m,['kind','name','count','sides','ability','damageType']);integer(m['count'],1,1);integer(m['sides'],6,6);require(m['ability']=='strength','INNATE_ABILITY');ref(m['damageType'],records,'damage_type')
        elif k=='open_tool_pool':
            shape(m,['kind','domains']);require(set(m['domains'])==set(['engineering','mining','weapons','armour','voidcraft']),'GUILD_TOOL_DOMAINS')
        else:raise InvalidContent('UNKNOWN_SPECIES_MECHANIC')

def validate_records(records):
    for id,e in records.items():
        shape(e,['schemaVersion','id','kind','revision','name','summary','descriptionMarkdown','lifecycle','verification','sources','tags','data'])
        require(e['id']==id and len(id)<=160 and ID.fullmatch(id),'CONTENT_ID')
        require(e['kind']==id.split('.')[1] and e['kind'] in FIELDS,'CONTENT_KIND')
        require(e['schemaVersion']==1 and e['lifecycle']=='draft' and e['verification']=='transcribed','IMPORT_ENVELOPE_STATE')
        integer(e['revision'],1,2147483647)
        require(isinstance(e['name'],str) and 1<=len(e['name'])<=160 and isinstance(e['summary'],str) and len(e['summary'])<=500,'TEXT_LENGTH')
        require(isinstance(e['descriptionMarkdown'],str),'DESCRIPTION')
        require(e['sources'] and isinstance(e['sources'],list),'SOURCE_REQUIRED')
        for source in e['sources']:
            shape(source,['sourceId','sourceVersion','locator']);loc=source['locator']
            shape(loc,['sectionKey','heading','pdfPage','printedPage'])
            integer(loc['pdfPage'],14,125);require(loc['printedPage']==loc['pdfPage']-13,'SOURCE_PAGE_OFFSET')
        refs(e['tags'],records,'tag')
        d=e['data'];k=e['kind'];shape(d,*FIELDS[k])
        if 'features' in d:refs(d['features'],records,'feature')
        if 'choices' in d:refs(d['choices'],records,'choice')
        if 'effects' in d:effects(d['effects'],records)
        if 'manualRules' in d:manuals(d['manualRules'])
        if 'requirements' in d and k not in ['armour','shield']:predicate(d['requirements'],records)
        if k in ['weapon','equipment','tool','augmetic','armour','shield']:
            from phb_equipment import validate_equipment
            validate_equipment(e,records)
        if k=='background' and 'originAvailability' in d:
            rows=d['originAvailability'];require(isinstance(rows,list) and rows,'ORIGIN_AVAILABILITY_REQUIRED')
            require(len({x['species']['id'] for x in rows})==len(rows),'DUPLICATE_ORIGIN_SPECIES')
            for row in rows:
                shape(row,['species','state']);ref(row['species'],records,'species')
                require(row['state'] in ['NORMAL','RARE','LIMITED'],'ORIGIN_AVAILABILITY_STATE')
        if k=='feature':
            validate_species_mechanics(d.get('mechanics',[]),records)
            require(d['flavor'] in ['general','feat','species_trait','background_feature','class_feature','subclass_feature'],'FLAVOR');grants(d['grants'],records)
        elif k=='proficiency':
            require(d['category'] in ['skill','weapon','weapon_group','tool','armour'],'PROFICIENCY_CATEGORY')
            if d['category']=='weapon_group':
                from phb_policies import WEAPON_GROUPS
                shape(d['appliesTo'],['groups']);require(bool(d['appliesTo']['groups']) and set(d['appliesTo']['groups'])<=WEAPON_GROUPS,'WEAPON_GROUP')
            else:shape(d['appliesTo'],['ids']);refs(d['appliesTo']['ids'],records,d['category'])
        elif k=='skill':require(d['attributeKey'] in ['strength','dexterity','constitution','intelligence','wisdom','charisma'],'ATTRIBUTE_KEY')
        elif k=='species':require(d['size'] in ['small','medium'],'SIZE_KEY')
        elif k=='choice':
            require(d['purpose'] in ['skill','attribute','subclass','species','background','class','feature','equipment','proficiency'],'CHOICE_PURPOSE')
            require(d['selectionMode']=='options' and d['repeatScope']=='once_per_actor','CHOICE_MODE')
            c=d['cardinality'];shape(c,['min','max','unique']);integer(c['min'],0,500);integer(c['max'],c['min'],500)
            require(c['unique'] is True and len(d['options'])>=c['max'],'CHOICE_UNSATISFIABLE')
            require(len({o['id'] for o in d['options']})==len(d['options']),'DUPLICATE_OPTION')
            for o in d['options']:shape(o,['id','label','grants']);local(o['id']);grants(o['grants'],records)
        elif k=='property':
            require(d['appliesToKinds']==['weapon'],'PROPERTY_APPLICABILITY')
            for p in d['parameters']:
                shape(p,['name','type','required','min'],['max']);require(p['type']=='integer' and p['required'] is True,'PARAMETER_SUBSET');integer(p['min'],1,1000)
        elif k=='rule':require(d['automation']=='manual' and d['role'] in ['general','rest','perils','psyker'],'RULE_SUBSET')
        elif k=='progression':
            shape(d['axis'],['kind','class']);require(d['axis']['kind']=='class_level','PROGRESSION_AXIS');ref(d['axis']['class'],records,'class');integer(d['maxLevel'],1,20)
            levels=[r['level'] for r in d['entries']];require(levels==sorted(set(levels)),'PROGRESSION_ORDER')
            allkeys=[]
            for row in d['entries']:
                shape(row,['level','grants']);integer(row['level'],1,d['maxLevel']);grants(row['grants'],records);allkeys += [g['id'] for g in row['grants']]
            require(len(allkeys)==len(set(allkeys)),'PROGRESSION_GRANT_IDS')
        elif k in ['class','subclass']:
            ref(d['progression'],records,'progression');p=records[d['progression']['id']]['data']
            parent=id if k=='class' else d['parentClass']['id']
            if k=='subclass':ref(d['parentClass'],records,'class')
            require(p['axis']['class']['id']==parent,'PROGRESSION_PARENT')
            if 'requirements' in d:predicate(d['requirements'],records)
            for sub in d.get('allowedSubclasses',[]):ref(sub,records,'subclass');require(records[sub['id']]['data']['parentClass']['id']==id,'SUBCLASS_PARENT')
        elif k in ['armour','shield']:
            require(d['properties']==[],'UNSUPPORTED_PROPERTIES');shape(d['equip'],['slots','hands']);integer(d['equip']['hands'],0,2)
            shape(d['defence'],['value','mode','stackGroup']);number(d['defence']['value']);require(d['defence']['mode'] in ['base','add'],'DEFENCE_MODE')
            if 'requirements' in d:shape(d['requirements'],['equip']);predicate(d['requirements']['equip'],records)
        elif k=='action':
            require(d['economy']=='manual' and d['costs']==[],'ACTION_SUBSET');require(d['target']=={'kind':'single','scope':'actor'},'ACTION_TARGET')
            for o in d['outcomes']:
                shape(o,['id','on','effects','manualRules']);local(o['id']);require(o['on']=='always','OUTCOME');effects(o['effects'],records);manuals(o['manualRules'])
            for roll in d.get('rolls',[]):
                shape(roll,['id','category','label','groups','modifiers'],['damageBindings']);local(roll['id']);require(roll['category']=='damage' and roll['modifiers']==[],'ROLL_SUBSET')
                require(len(roll['groups'])>0,'DICE_REQUIRED')
                group_ids={g['id'] for g in roll['groups']}
                require(len(group_ids)==len(roll['groups']),'DUPLICATE_ROLL_GROUP')
                if 'damageBindings' in roll:
                    bindings=roll['damageBindings']
                    require(len(bindings)==len(group_ids) and {b['groupId'] for b in bindings}==group_ids,'DAMAGE_BINDING_COVERAGE')
                    require(len({b['componentId'] for b in bindings})==len(bindings),'DUPLICATE_DAMAGE_COMPONENT')
                    for b in bindings:
                        shape(b,['groupId','componentId','damageType']);local(b['componentId']);ref(b['damageType'],records,'damage_type')
                for g in roll['groups']:shape(g,['id','count','sides']);local(g['id']);integer(g['count'],1,100);integer(g['sides'],2,1000)
        elif k=='damage_type':require(isinstance(d['category'],str) and d['category'],'DAMAGE_CATEGORY')
        def safe(v):
            require(v is not None and not isinstance(v,float),'NON_SUBSET_VALUE')
            if isinstance(v,dict):
                if set(v)=={'id'}:ref(v,records)
                for child in v.values():safe(child)
            if isinstance(v,list):
                for child in v:safe(child)
        safe(e)

def load(package=PACKAGE):
    manifest=read(package/'manifest.json');records={}
    source_pairs={(s['sourceId'],s['sourceVersion']) for s in read(package/'sources.json')['sources']}
    paths=[]
    for item in manifest['entities']:
        path=(package/item['path']).resolve();require(path.is_relative_to((package/'entities').resolve()),'PATH_ESCAPE');paths.append(path)
        e=read(path);require(e['id'] not in records,'DUPLICATE_ID');records[e['id']]=e
        require(e['id']==item['id'] and e['revision']==item['revision'],'MANIFEST_ID');require(digest(e)==item['sha256'],'DIGEST_MISMATCH')
        for source in e['sources']:require((source['sourceId'],source['sourceVersion']) in source_pairs,'SOURCE_NOT_FOUND')
    require(set(paths)==set(p.resolve() for p in (package/'entities').rglob('*.json')),'UNLISTED_ENTITY')
    validate_records(records)
    validate_candidates(package,records)
    return manifest,records

def validate_candidates(package,records):
    """Validate represented fields only. Missing fields remain explicit incomplete mappings."""
    ids=set()
    for path in (package/'review/candidates').rglob('*.json'):
        c=read(path)
        shape(c,['proposedId','kind','name','status','coverage','issues','proposedData','evidence'])
        require(ID.fullmatch(c['proposedId']) and c['proposedId'].split('.')[1]==c['kind'],'CANDIDATE_ID')
        require(c['proposedId'] not in ids and c['proposedId'] not in records,'CANDIDATE_COLLISION');ids.add(c['proposedId'])
        require(c['issues'] and c['evidence'] and c['coverage']=='PARTIALLY_STRUCTURED','CANDIDATE_EVIDENCE')
        for evidence in c['evidence']:
            shape(evidence,['text','source']);require(isinstance(evidence['text'],str) and evidence['text'].strip(),'CANDIDATE_TEXT')
            src=evidence['source'];require((src['sourceId'],src['sourceVersion']) in {(s['sourceId'],s['sourceVersion']) for s in read(package/'sources.json')['sources']},'CANDIDATE_SOURCE')
            loc=src['locator'];integer(loc['pdfPage'],14,125);require(loc['printedPage']==loc['pdfPage']-13,'CANDIDATE_PAGE')
        d=c['proposedData']
        for component in [component for mode in d.get('modes',[]) for component in mode.get('damage',[])]:
            shape(component,['id','dice','bonus','damageType']);shape(component['dice'],['count','sides','bonus'])
            integer(component['dice']['count'],1,100);integer(component['dice']['sides'],2,1000);integer(component['dice']['bonus'],-1000000,1000000)
            number(component['bonus']);ref(component['damageType'],records,'damage_type')
        for r in [mode['range'] for mode in d.get('modes',[]) if 'range' in mode]:
            if r['kind']=='distance':
                require(r['normal']['unit']==r['long']['unit']=='ft','RANGE_UNIT')
                integer(r['normal']['value'],0,1000000);integer(r['long']['value'],r['normal']['value'],1000000)
            elif r['kind']=='area':
                require(r['shape']=='cone' and r['size']['unit']=='ft','AREA_SUBSET');integer(r['size']['value'],1,1000000)
            else:raise InvalidContent('RANGE_KIND')
        for prop in d.get('properties',[]):
            ref(prop['property'],records,'property')
            params=records[prop['property']['id']]['data']['parameters'];args=prop['arguments']
            require(set(args)=={p['name'] for p in params},'PROPERTY_ARGUMENTS')
            for p in params:integer(args[p['name']],p.get('min',-1000000),p.get('max',1000000))
        if 'parentClass' in d:ref(d['parentClass'],records,'class')

def plan(records, existing=None):
    """Produce deterministic candidate operations. existing maps (id,revision) to digest."""
    existing=existing or {};operations=[]
    for id,e in sorted(records.items()):
        key=(id,e['revision']);sha=digest(e)
        if key in existing:
            require(existing[key]==sha,'IMMUTABLE_REVISION_CONFLICT: '+id)
            operation='no_op'
        else:operation='stage_candidate'
        operations.append({'operation':operation,'id':id,'revision':e['revision'],'sha256':sha,'payload':e})
    return operations

def publication_gate(manifest,records):
    require(manifest['lifecycle']=='published' and not manifest.get('publicationBlocked',True),'PUBLICATION_BLOCKED_DRAFT')
    require(sum(e['kind']=='profile' for e in records.values())==1,'PROFILE_REQUIRED')
    require(all(e['verification'] in ['reviewed','authoritative'] for e in records.values()),'SOURCE_REVIEW_REQUIRED')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--plan',type=Path);parser.add_argument('--publication-check',action='store_true');args=parser.parse_args()
    manifest,records=load()
    if args.publication_check:publication_gate(manifest,records)
    if args.plan:
        args.plan.parent.mkdir(parents=True,exist_ok=True)
        args.plan.write_bytes(b'\n'.join(canonical(x) for x in plan(records))+b'\n')
    print(f'PASS: {len(records)} draft records; supported-subset structures, references, source versions and digests. Publication remains blocked.')

if __name__=='__main__':main()

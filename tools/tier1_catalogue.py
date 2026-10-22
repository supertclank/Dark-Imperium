"""Deterministic, non-publishing tier-1 dependency inventory.

No approval, rarity permission, legal selection, or production profile is created
by this audit. Counterfactuals explicitly remove only an Origin gate.
"""
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
import content_import as c
import phb_policies as policy

ORIGIN_RULES={
 'hiveborn':['001','007'],'penal_worlder':['002','007'],
 'voidborn':['003','007'],'forge_world':['004','007'],
 'militarum_regiment':['005','007'],'underhive':['006','007'],'shrine_worlder':['007']}
ITEM_KINDS={'weapon','armour','shield','equipment','tool','ammunition','consumable','augmetic'}
ROOT=c.ROOT
OUT=c.PACKAGE/'review/level-1-3-catalogue.json'

def ids(value):
    if isinstance(value,dict):
        if set(value)=={'id'} and isinstance(value['id'],str) and value['id'].startswith('di.'):yield value['id']
        else:
            for v in value.values():yield from ids(v)
    elif isinstance(value,list):
        for v in value:yield from ids(v)

def validate_approval(entry,package=c.PACKAGE,origin=False):
    """Verify provenance, not merely a RESOLVED label. Never infer approval."""
    a=entry.get('approval',{});decision=entry.get('decision')
    if entry.get('status')!='RESOLVED' or not isinstance(decision,str) or not decision.strip():return False
    if a.get('approvedBy')!='user' or not (a.get('recordedAt') or a.get('date')):return False
    if origin and (not a.get('recordedAt') or not a.get('sourceRelationship') or not entry.get('affectedIds')):return False
    try:
        path=(package/a['path']).resolve()
        if not path.is_relative_to(package.resolve()):return False
        raw=path.read_bytes()
        return hashlib.sha256(raw).hexdigest()==a.get('sha256') and decision.replace('\r\n','\n').strip() in raw.decode('utf-8-sig').replace('\r\n','\n')
    except (KeyError,OSError,UnicodeError):return False

def selected_features(records,roots,level,subclass=None):
    """Traverse granted features only, never all alternatives or prerequisite refs."""
    features=set();choices=set();missing=set();visiting=set()
    def visit(key):
        if key in visiting:return
        visiting.add(key)
        e=records.get(key)
        if not e:missing.add(key);return
        d=e['data']
        if e['kind']=='feature':features.add(key)
        if e['kind']=='choice':choices.add(key);return
        for ref in d.get('features',[]):visit(ref['id'])
        for ref in d.get('choices',[]):visit(ref['id'])
        for g in d.get('grants',[]):
            if g['kind'] in ('feature','choice'):visit(g[g['kind']]['id'])
        if 'progression' in d:visit(d['progression']['id'])
        if e['kind']=='progression':
            for row in d['entries']:
                if row['level']<=level:
                    for g in row['grants']:
                        if g['kind'] in ('feature','choice'):visit(g[g['kind']]['id'])
    for key in roots+([subclass] if subclass else []):visit(key)
    return {'features':sorted(features),'choices':sorted(choices),'missing':sorted(missing)}

def execution(e):
    d=e['data'];automatic=any(x.get('automation')=='automatic' for x in d.get('effects',[])) or bool(d.get('grants'))
    manual=bool(d.get('manualRules'))
    return 'PARTIALLY_AUTOMATED' if automatic and manual else 'AUTOMATED' if automatic else 'MANUAL' if manual else 'DISPLAY_ONLY'

def eligible(e,species,klass=None,level=1):
    return policy.evaluate(e['data']['requirements'],{'selected':[species]+([klass] if klass else []),'classLevels':{klass:level} if klass else {},'totalLevel':level,'facts':{}}) if 'requirements' in e['data'] else True

def build():
    _,records=c.load();c.validate_records(records)
    spec=c.read(ROOT/'content/profiles/di-phb-1.0-narrow-v1.json')
    bundle=c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json')
    ledger=c.read(c.PACKAGE/'review/decisions.json')
    original=c.read(c.PACKAGE/'review/human-rulings-integration.json')
    assert len(original)==36,'Historical denominator changed'
    approved=[x for x in original if validate_approval(x)]
    origins_approved=[x for x in ledger['humanRulings'] if x['id'] in {f'PHB-RULE-{n:03}' for n in range(1,8)} and validate_approval(x,origin=True)]
    assert not origins_approved,'New approvals require explicit integration before regenerating this blocked audit'
    groups={kind:sorted((e for e in records.values() if e['kind']==kind),key=lambda e:e['id']) for kind in ['species','background','class','subclass']}
    candidates={e['proposedId']:e for p in sorted((c.PACKAGE/'review/candidates').rglob('*.json')) if isinstance((e:=c.read(p)),dict) and 'proposedId' in e}
    bindings=c.read(c.PACKAGE/'review/starting-reference-bindings.json')['bindings']
    kits=c.read(c.PACKAGE/'review/starting-equipment-audit.json');training=c.read(c.PACKAGE/'review/class-calculation-inputs.json')
    inputs={x['class']['id']:x for x in training};kit_by_class={}
    equipment_ids=set()
    for klass in groups['class']:
        row=next(x for x in kits if x['className']==klass['name'])
        found={x['id'] for x in row['exactNameMatches']}
        alias_hits={k:v for k,v in bindings.items() if k.casefold() in row['sourceText'].casefold()}
        found.update(ids(alias_hits))
        # Expand approved choice pools for inventory coverage, not for permission.
        for key in list(found):
            if key in records and records[key]['kind']=='choice':found.update(ids(records[key]['data'].get('options',[])))
        found={key for key in found if (records.get(key) or candidates.get(key,{})).get('kind') in ITEM_KINDS}
        equipment_ids.update(found)
        kit_by_class[klass['id']]={'sourcePdfPage':row['sourcePdfPage'],'sourceText':row['sourceText'],'identifiedItemIds':sorted(found),'approvedAliasMatches':alias_hits,
          'structuredPackage':'review/veteran-starting-package.json' if klass['id']=='di.class.veteran' else None,
          'status':'PARTIAL_SUPPORTED_BRANCH' if klass['id']=='di.class.veteran' else 'BLOCKED_BY_CONTENT',
          'gaps':([] if klass['id']=='di.class.veteran' else ['PHB-CAT-001'])+(['PHB-CAT-002'] if any(k not in records for k in found) else [])}
    equipment=[]
    for key in sorted(equipment_ids):
        e=records.get(key);candidate=candidates.get(key);d=e['data'] if e else {}
        published=key in spec['equipment'];is_manual=published and e['kind'] in {'equipment','tool','consumable'}
        equipment.append({'id':key,'kind':(e or candidate)['kind'],'status':('MANUAL' if is_manual else 'SUPPORTED') if published else 'BLOCKED' if not e else 'COMING_LATER',
          'canonical':bool(e),'productionAllowed':published,'sources':e.get('sources',[]) if e else candidate.get('evidence',[]),
          'checks':{'quantityGrant':'REVIEWED_NARROW_KIT_ONLY' if published else 'NOT_VALIDATED',
           'proficiencyGroups':d.get('proficiencyGroups'),'abilityBinding':d.get('abilityBinding'),'hands':d.get('hands'),'range':d.get('range'),
           'armourProfile':d.get('armourClass') or d.get('defence'),'requirements':d.get('requirements'),'schema':'CANONICAL_VALIDATED' if e else 'CANDIDATE'},
          'reason':'Existing narrow publication' if published else 'Canonical definition is not an executable class package or engine certification' if e else 'Incomplete candidate cannot be selected'})
    table=next(t for t in c.read(c.PACKAGE/'evidence/tables.json') if t['rows'][0]==['Origin','Human','Ogryn','Ratling','Skitarii','Squat/Kin','Aeldari'])
    species_cols=['human','ogryn','ratling','skitarii','kin','aeldari'];origin_rows={}
    for row in table['rows'][1:]:
        key=row[0].lower().replace(' / ','_').replace(' ','_');origin_rows['di.background.'+key]=dict(zip(species_cols,row[1:]))
    origins=[]
    for e in groups['background']:
        rules=['PHB-RULE-'+x for x in ORIGIN_RULES.get(e['id'].split('.')[-1],[])]
        origins.append({'id':e['id'],'name':e['name'],'rulingIds':rules,'eligibility':e['data']['requirements'],
         'published':e['id'] in spec['origins'],'availability':'BLOCKED' if rules else 'EXISTING_PROFILE_ONLY' if e['id'] in spec['origins'] else 'UNPUBLISHED',
         'proseEvidenceOnly':e['descriptionMarkdown'],'matrixEvidenceOnly':origin_rows[e['id']],'matrixSourcePdfPage':26,'proseSource':e['sources'],
         'warning':'Matrix labels are source evidence, not resolved Rare/Limited permissions.'})
    classes=[];subclasses=[]
    for klass in groups['class']:
        progression=records[klass['data']['progression']['id']]['data']['entries']
        assert all(sum(row['level']==n for row in progression)==1 for n in (1,2,3))
        classes.append({'id':klass['id'],'name':klass['name'],'eligibleSpecies':[s['id'] for s in groups['species'] if eligible(klass,s['id']) is True],
          'training':inputs[klass['id']],'classSourceText':klass['descriptionMarkdown'],'trainingGrants':records[klass['data']['features'][0]['id']]['data'],'source':klass['sources'],'startingKit':kit_by_class[klass['id']],
          'levels':{str(n):selected_features(records,[klass['id']],n) for n in (1,2,3)},
          'publishedLevels':[1] if klass['id'] in spec['classes'] else [],'resources':'NARROW_ONLY' if klass['id'] in spec['classes'] else 'MAPPING_REQUIRED',
          'psychic':{'status':'BLOCKED_BY_CONTENT','knownPowerCounts':[v for v in inputs[klass['id']].get('knownPowers',[]) if v['level']<=3],'gaps':['PHB-CAT-003','PHB-CAT-004']} if klass['id'] in ['di.class.psyker','di.class.aeldari_warlock'] else None})
        for ref in klass['data']['allowedSubclasses']:
            sub=records[ref['id']];assert sub['data']['parentClass']['id']==klass['id']
            dep=selected_features(records,[],3,sub['id']);assert not dep['missing']
            subclasses.append({'id':sub['id'],'classId':klass['id'],'requirements':sub['data'].get('requirements'),'sources':sub['sources'],**dep,
             'status':'BLOCKED_BY_ENGINE','gaps':['PHB-CAT-004'],'published':False})
    species=[]
    for e in groups['species']:
        dep=selected_features(records,[e['id']],1)
        species.append({'id':e['id'],'name':e['name'],'size':e['data']['size'],'sources':e['sources'],**dep,
          'published':e['id'] in spec['species'],'status':'READY_WITH_MANUAL_RULES' if e['id'] in spec['species'] else 'BLOCKED_BY_ENGINE',
          'mechanicalEffects':[effect for key in dep['features'] for effect in records[key]['data'].get('effects',[])],
          'manualCoreReview':[{'id':key,'text':records[key]['data'].get('manualRules',[])} for key in dep['features'] if records[key]['data'].get('manualRules')],
          'classAccess':[k['id'] for k in groups['class'] if eligible(k,e['id']) is True],
          'gapIds':[] if e['id'] in spec['species'] else ['PHB-CAT-005']})
    feature_ruling_refs={key:['PHB-RULE-011'] for key,e in records.items() if e['kind']=='feature' and 'expertise' in str(e['data'].get('manualRules',[])).casefold()}
    rows=[]
    for s,o,k in itertools.product(groups['species'],groups['background'],groups['class']):
        origin_rules=['PHB-RULE-'+v for v in ORIGIN_RULES.get(o['id'].split('.')[-1],[])]
        class_ok=eligible(k,s['id']);origin_ok=eligible(o,s['id'])
        levels=[(1,None),(2,None)]+[(3,ref['id']) for ref in k['data']['allowedSubclasses']]
        for level,sub in levels:
            key='|'.join([s['id'],o['id'],k['id'],str(level),sub or '-'])
            invalid=class_ok is False or origin_ok is False
            existing=(s['id'] in spec['species'] and o['id'] in spec['origins'] and k['id'] in spec['classes'] and level==1)
            gaps=[]
            if not existing:
                gaps.append('PHB-CAT-004')
                if s['id'] not in spec['species']:gaps.append('PHB-CAT-005')
                if k['id']!='di.class.veteran':gaps.append('PHB-CAT-001')
                if 'PHB-CAT-002' in kit_by_class[k['id']]['gaps']:gaps.append('PHB-CAT-002')
                if k['id'] in ['di.class.psyker','di.class.aeldari_warlock']:gaps.append('PHB-CAT-003')
            status='UNSUPPORTED' if invalid else 'READY_WITH_MANUAL_RULES' if existing else 'BLOCKED_BY_RULING' if origin_rules else 'BLOCKED_BY_CONTENT' if any(g in gaps for g in ['PHB-CAT-001','PHB-CAT-002','PHB-CAT-003']) else 'BLOCKED_BY_ENGINE'
            after='UNSUPPORTED' if class_ok is False else 'BLOCKED_BY_CONTENT' if any(g in gaps for g in ['PHB-CAT-001','PHB-CAT-002','PHB-CAT-003']) else 'BLOCKED_BY_ENGINE'
            deps=selected_features(records,[s['id'],o['id'],k['id']],level,sub)
            conditional_refs=sorted({rule for fid in deps['features'] for rule in feature_ruling_refs.get(fid,[])})
            rows.append({'conditionalFeatureRulingReview':conditional_refs,'id':key,'species':s['id'],'origin':o['id'],'class':k['id'],'level':level,'subclass':sub,
             'status':status,'eligibility':'INVALID' if invalid else 'UNRESOLVED' if origin_rules else 'KNOWN_BASE_ELIGIBLE',
             'rulingIds':origin_rules if not invalid else [],'gapIds':gaps,'productionAllowed':existing,
             'traitScope':spec['traits'] if existing else [],'equipmentScope':spec['equipment'] if existing else [],
             'ifOriginExplicitlyPermittedAndAvailabilitySatisfied':after if origin_rules and class_ok is True else None})
    features={key for row in classes for level in row['levels'].values() for key in level['features']}
    features.update(key for row in subclasses+species for key in row['features'])
    traits=[records[g['feature']['id']] for option in records['di.choice.creation.universal_trait']['data']['options'] for g in option['grants'] if g['kind']=='feature']
    features.update(e['id'] for e in traits)
    dispositions={x['id']:x for x in c.read(c.PACKAGE/'review/creation-candidate-dispositions.json')}
    powers=[{'requiredForTier1Pool':dispositions.get(key,{}).get('status')=='BLOCKS_CHARACTER_CREATION','id':key,'status':'BLOCKED','kind':e['kind'],'evidence':e['evidence'],'reason':'No canonical power record or validated choice pool'} for key,e in sorted(candidates.items()) if e['kind']=='power']
    conditional=[{'id':x['id'],'question':x['question'],'impact':x['creationImpact'],'scope':'Apply only when the selected configuration actually exercises this unresolved mechanic; broad historical affectedIds are not a dependency graph.'} for x in original if x['status']=='UNRESOLVED' and x['id'] not in {f'PHB-RULE-{n:03}' for n in range(1,8)}]
    return {'schemaVersion':1,'scope':'AUDIT_ONLY_NOT_PUBLICATION','sourceProfile':{'id':spec['id'],'digest':bundle['digest']},
     'approvalGate':{'originalTotal':36,'originalResolved':len(approved),'originalUnresolved':36-len(approved),'originNewlyResolved':0,'originBlocked':[f'PHB-RULE-{n:03}' for n in range(1,8)]},
     'counts':{'species':len(species),'origins':len(origins),'classes':len(classes),'subclasses':len(subclasses),'combinations':len(rows),'statuses':dict(sorted(Counter(x['status'] for x in rows).items())),
      'equipmentIdentified':len(equipment),'equipmentStatuses':dict(sorted(Counter(x['status'] for x in equipment).items())), 'powerCandidates':len(powers),'powerRequiredTier1':sum(x['requiredForTier1Pool'] for x in powers),'traits':len(traits)},
     'origins':origins,'species':species,'classes':classes,'subclasses':subclasses,'equipment':equipment,'powers':powers,
     'features':[{'id':key,'execution':execution(records[key]),'conditionalRulingReview':feature_ruling_refs.get(key,[]),'published':key in selected_features(records,spec['species']+spec['origins']+spec['classes'],1)['features'] or key in spec['traits'],'sources':records[key]['sources']} for key in sorted(features)],
     'traits':[{'id':e['id'],'execution':execution(e),'productionAllowed':e['id'] in spec['traits'],'requirements':e['data'].get('requirements')} for e in traits],
     'conditionalRulings':conditional,'rows':rows}

GAPS={
 'PHB-CAT-001':'Starting-package compiler absent outside Veteran: source tokens/approved aliases are not executable quantity, choice, proficiency and inventory grants.',
 'PHB-CAT-002':'At least one identified starting option remains an incomplete candidate; source alternatives must be independently certified.',
 'PHB-CAT-003':'Psychic power candidates lack canonical power schema/choice pools and production execution boundaries; no manual shortcut can validate unknown creation choices.',
 'PHB-CAT-004':'Only narrow-kotlin-v1 is production-registered. Tier-1 selected-level choice/resource/projection/roll compilation and golden certification are not implemented.',
 'PHB-CAT-005':'Non-Human species traits include unmapped core calculations/proficiencies/restrictions. Manual prose cannot substitute for those calculations.'}

def render(data):
    lines=['# Level 1–3 publication matrix','', 'Generated by `tools/tier1_catalogue.py`. AUDIT ONLY. No approvals or production publication.', '',
      'Rows enumerate species × Origin × class at levels 1/2 and each parent-class subclass at level 3. They are family readiness rows, not approval of every attribute/trait/equipment permutation. The sole ready row is restricted to the existing Twitchy/kit/choice scope. Invalid species/class or known Origin restrictions are UNSUPPORTED, not invented rulings.', '',
      'All 001–007 remain blocked. The hypothetical column requires an explicit species permission AND satisfaction of the future approved Rare/Limited policy. It neither selects matrix/prose precedence nor assumes GM permission. It reports the remaining gate, not legal approval. No additional row becomes publishable from Origin rulings alone.', '',
      'Machine-readable detail: `content/packages/di_phb_1_0/review/level-1-3-catalogue.json`.', '',
      '| Species | Origin | Class | Level | Subclass | Current | Rulings | Other gaps | Hypothetical Origin gate removed |','|---|---|---|---:|---|---|---|---|---|']
    for r in data['rows']:
        lines.append('| '+' | '.join([r['species'].removeprefix('di.species.'),r['origin'].removeprefix('di.background.'),r['class'].removeprefix('di.class.'),str(r['level']),(r['subclass'] or '-').removeprefix('di.subclass.'),r['status'],', '.join(r['rulingIds']) or '-',', '.join(r['gapIds']) or '-',r['ifOriginExplicitlyPermittedAndAvailabilitySatisfied'] or '-'])+' |')
    return '\n'.join(lines)+'\n'

def write(check=False):
    data=build();plan={'id':'di-phb-1.0-tier1-v1','status':'PLANNED_NOT_PUBLISHED','engineVersion':'phb-tier1-kotlin-v1','levels':[1,2,3],
      'productionAllowed':False,'allowlist':[],'blockingOriginRulings':data['approvalGate']['originBlocked'],'sourceProfile':data['sourceProfile'],
      'activationRequirements':['Approved Origin ledger entries with exact decision, hash, user provenance, timestamp, source relationship and affected IDs','Explicit eligible tuple allowlist, selected-choice dependency certification and golden fixtures','New adapter registration and immutable export; old snapshots retain their adapter','Server filtering, authoritative validation, creation/retrieval/rolling/browser regression'],
      'gapDefinitions':GAPS,'auditDigest':c.digest(data)}
    outputs={OUT:json.dumps(data,ensure_ascii=False,indent=2)+'\n',c.PACKAGE/'review/tier1-publication-plan.json':json.dumps(plan,ensure_ascii=False,indent=2)+'\n',ROOT/'docs/import/LEVEL_1_3_PUBLICATION_MATRIX.md':render(data)}
    for path,text in outputs.items():
        if check:assert path.read_text(encoding='utf-8')==text,f'Stale audit: {path}'
        else:path.write_text(text,encoding='utf-8')
    print(json.dumps(data['counts'],indent=2));return data

if __name__=='__main__':write('--check' in sys.argv)

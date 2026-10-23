"""Level 5 overlay; historical snapshots remain immutable."""
import copy,sys
import content_import as c
import tier1_catalogue as audit

def build():
 old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v7.json')
 assert old['digest']=='af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5'
 p=copy.deepcopy(old['payload']);s=p['spec'];r=p['records'];support=p['featureSupport']
 s.update(id='di-phb-1.0-tier1-v8',name='PHB 1.0 · Martial progression through level 5',levels=[1,2,3,4,5],attackActionVersion=1)
 classes=[]
 for cid in s['classes']:
  grants=next(x for x in r[r[cid]['data']['progression']['id']]['data']['entries'] if x['level']==5)['grants'];fids=[g['feature']['id'] for g in grants];extra=[];resources=[]
  for fid in fids:
   f=r[fid];f['revision']+=1
   if fid.endswith('.extra_attack'):
    assert 'attack twice when you take the Attack' in f['descriptionMarkdown']
    effect=copy.deepcopy(r['di.feature.universal.twitchy']['data']['effects'][0]);effect.update(id='attack_capacity',operation='base');effect['target']['key']='action.attack.capacity';effect['value']['value']=2;effect['stacking']={'group':'di.action.attack.capacity','mode':'max'}
    f['data']['effects']=[effect];f['data']['manualRules']=[];extra.append(fid)
    support[fid]=dict(classification='AUTOMATED',playerNote='Two individual weapon attacks within one Attack action on your turn. Does not grant another action, bonus action, reaction or grenade use.',rulingIds=[],resources=[])
   else:
    note='Conditional damage and timing remain manual; no automatic hit, critical damage or condition resolution.'
    if fid.endswith('.backstabber_3d6'):
     f['descriptionMarkdown']='At level 5, your Dirty Fighter damage increases to +3d6. It increases again to +4d6 at level 11, +5d6 at level 15, and +6d6 at level 18.'
     f['summary']='Dirty Fighter increases to +3d6 at level 5; its once-per-turn conditions remain manual.';f['sources'][0]['locator'].update(heading='Backstabber',sectionKey='11.6.5');f['data']['manualRules'][0]['text']=f['descriptionMarkdown']
     note='Dirty Fighter is +3d6, once per turn under its original hit/target conditions, not once per attack. Replaces +1d6; do not add both. Conditions and damage remain manual.'
    if fid.endswith('.killshot'):
     resources=[dict(key='killshot',maximum=1,recovery='short_rest',automation='manual')]
     note='Once per short rest after a ranged hit with an Accurate weapon: optionally make that hit critical. Deadeye becomes +2d6 under its original once-per-turn/advantage conditions, replacing +1d6. Critical damage, stationary sniper bonuses and recovery remain manual. No Extra Attack.'
    support[fid]=dict(classification='MANUAL',playerNote=note,rulingIds=[],resources=resources)
  classes.append(dict(classId=cid,name=r[cid]['name'],previousMaximumLevel=4,status='READY_WITH_MANUAL_RULES',level5Features=fids,attacksPerAttackAction=2 if extra else 1,extraAttackFeatures=extra,newChoices=[],newResources=resources,newWeaponActions=[],engineBlockers=[],rulesBlockers=[],contentBlockers=[],sources=[src for f in fids for src in r[f]['sources']]))
 for base in list(s['pathConfigurations']):
  if base['level']!=4:continue
  dep=audit.selected_features(r,[base[k] for k in ['speciesId','originId','classId']],5);assert not dep['missing'],dep
  cfg=copy.deepcopy(base);cfg.update(level=5,features=sorted(dep['features']),choices=sorted(set(dep['choices'])-{'di.choice.creation.universal_trait'}));assert set(cfg['choices'])==set(base['choices']),(base,cfg);s['pathConfigurations'].append(cfg)
 for family in list(s['certifiedPaths']):
  if family['level']==4:s['certifiedPaths'].append(dict(family,level=5))
 subclasses=[]
 for sid in sorted({x['subclassId'] for x in s['certifiedPaths'] if x.get('subclassId')}):
  entries=r[r[sid]['data']['progression']['id']]['data']['entries'];assert not [x for x in entries if x['level'] in [4,5]],sid
  subclasses.append(dict(id=sid,status='READY_WITH_MANUAL_RULES',level5Features=[],reason='No new subclass feature at level 5; certified level-3 features persist with existing manual restrictions.',sources=r[sid]['sources']))
 s['upgradeContracts']=[dict(version='v7-v8-level5-1',fromProfile=old['payload']['spec']['id'],fromDigest=old['digest'],toProfile=s['id'],fromLevel=4,toLevel=5,speciesIds=s['species'],classIds=s['classes'],preserve=['choices','inventory','resources','currentHp','conditions','temporaryEffects','rollHistory'])]
 s['availability'][0]['message']='Certified martial paths through level 5. Create at level 1 and advance explicitly. Conditional effects remain manual.'
 s['availability'][-1]['message']='Level 6+, psychic classes and previously blocked subclass, equipment and ruling branches remain unavailable. Historical profiles stay pinned.'
 p['level5Audit']=dict(classes=classes,subclasses=subclasses,ammunition='Manual; no new automatic costs.',consumables='Grenades remain separate transactional uses, excluded from Attack-action sequences.',thunderHammer=dict(policy='VERIFIED_STRENGTH',productionOwnership='BLOCKED_BY_CONTENT',reason='No published class/package or level-5 feature grants this candidate weapon.'),timing='Extra Attack changes capacity only for the Attack action. Once-per-turn/hit/round, bonus and reaction effects remain separate and manual.',previousFamilies=len(old['payload']['spec']['certifiedPaths']),families=len(s['certifiedPaths']))
 c.validate_records(r)
 return dict(digest=c.digest(p),payload=p)

def fixtures(b):
 p=b['payload'];s=p['spec'];r=p['records'];out=[]
 for family in s['certifiedPaths']:
  cfg=next(x for x in s['pathConfigurations'] if all(x[k]==family[k] for k in ['speciesId','originId','classId','level']));answers={}
  for key in cfg['choices']:
   choice=r[key]['data'];opts=choice['options']
   if choice['purpose']=='subclass':opts=[o for o in opts if any(g.get('content',{}).get('id')==family['subclassId'] for g in o['grants'])]
   if key==s['level4Advancement']['choiceId']:opts=[o for o in opts if o['id']=='plus_two_constitution']
   answers[key]=[o['id'] for o in opts[:choice['cardinality']['min']]]
  pack=p['packages'][family['classId']]['display'];pc={x['id']:x['options'][0]['id'] for x in pack['choices']}
  inv=[dict(definitionId=x['item']['id'],quantity=x['quantity'],equipped=x['item']['id'] in s['armour']) for x in pack['fixed']]+[dict(definitionId=pc[x['id']],quantity=x['quantity'],equipped=pc[x['id']] in s['armour']) for x in pack['choices']]
  out.append(dict(profileId=s['id'],profileDigest=b['digest'],name='Level 5 certification '+family['classId'].split('.')[-1],**{k:family[k] for k in ['speciesId','originId','classId','level','traitId']},attributes=dict(zip(s['attributes'],[15,14,13,12,10,8])),answers=answers,packageChoices=pc,inventory=inv))
 return out

if __name__=='__main__':
 b=build()
 for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v8.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v8.json',b['payload']['spec'])]:
  raw=c.canonical(value)+b'\n'
  if path.exists():assert path.read_bytes()==raw,'Immutable release differs: '+str(path)
  elif '--write' in sys.argv:path.write_bytes(raw)
  elif '--check' in sys.argv:raise AssertionError('Missing release')
 if '--write' in sys.argv:
  d=c.ROOT/'backend/src/test/resources/tier8';d.mkdir(exist_ok=True);(d/'all-paths.json').write_bytes(c.canonical(fixtures(b))+b'\n')
  (c.PACKAGE/'review/level5-certification.json').write_bytes(c.canonical(b['payload']['level5Audit']|dict(profileId=b['payload']['spec']['id'],digest=b['digest'],families=b['payload']['spec']['certifiedPaths']))+b'\n')
 print(b['digest'],len(b['payload']['spec']['certifiedPaths']),'family rows')


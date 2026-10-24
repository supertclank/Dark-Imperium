"""Candidate twelve-class profile. Publication is a separate certification step."""
import copy,sys
import content_import as c
import tier1_catalogue as audit
from export_tier1_v2_profile import package
import psychic_catalogue
NEW=['zealot','arbites_enforcer','psyker','aeldari_warlock']

def build():
 p=copy.deepcopy(c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v9.json')['payload']);s=p['spec'];r=p['records'];support=p['featureSupport'];s.update(id='di-phb-1.0-tier1-v10',name='PHB 1.0 · Twelve classes through level 5',psychicMechanicsVersion=1,resourceScalingVersion=1);s['upgradeContracts']=[]
 source=r['di.class.psyker']['sources']
 def entity(key,name,data,sources=source,text=None):
  e=copy.deepcopy(r['di.feature.species.ratling.traits']);e.update(id=key,kind=key.split('.')[1],name=name,data=data,sources=copy.deepcopy(sources),summary=(text or name)[:500],descriptionMarkdown=text or name);r[key]=e;return e
 def choice(key,name,options,count=1):
  entity(key,name,dict(purpose='feature',selectionMode='options',repeatScope='once_per_actor',cardinality=dict(min=count,max=count,unique=True),options=[dict(id=k,label=v,grants=[]) for k,v in options]))
 def manual(fid,note=None):
  support[fid]=dict(classification='MANUAL',playerNote=note or 'Apply conditional effects and target outcomes manually. The full canonical feature remains available.',rulingIds=[],resources=[])
 def resource(fid,key,rest='long_rest',maximum=1):
  support[fid]['resources'].append(dict(key=key,maximum=maximum,recovery=rest,automation='manual',**({'maximumPolicy':'proficiency_bonus'} if maximum=='proficiency_bonus' else {})))
  if maximum=='proficiency_bonus':support[fid]['resources'][-1]['maximum']=2
 for cl in NEW:
  s['classes'].append('di.class.'+cl)
  p['classTraining']['di.class.'+cl]=next(x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json') if x['class']['id']=='di.class.'+cl)
  for key in r:
   if key.startswith('di.feature.class.'+cl+'.') or key.startswith('di.feature.subclass.'+cl+'.'):manual(key)
  fid='di.feature.class.'+cl+'.level_4.ability_score_improvement_talent'
  r[fid]['data']['grants']=copy.deepcopy(r['di.feature.class.veteran.level_4.ability_score_improvement_talent']['data']['grants']);support[fid]=copy.deepcopy(support['di.feature.class.veteran.level_4.ability_score_improvement_talent'])
 for cl in ['zealot','arbites_enforcer']:
  key='di.feature.class.'+cl+'.level_5.extra_attack';r[key]['data']['effects']=copy.deepcopy(r['di.feature.class.veteran.level_5.extra_attack']['data']['effects']);support[key]['classification']='PARTIAL'
 # Psyker discipline is selected at level 1; its subclass feature still starts at 3.
 pg=r['di.progression.psyker']['data']['entries'];grant=next(g for row in pg for g in row['grants'] if g.get('choice',{}).get('id')=='di.choice.psyker.subclass')
 for row in pg:row['grants']=[g for g in row['grants'] if g is not grant]
 pg[0]['grants'].append(grant)
 for sub in r['di.class.psyker']['data']['allowedSubclasses']:
  r[sub['id']]['data']['requirements']=dict(kind='level',operator='gte',value=1,axis=dict(kind='class_level',**{'class':{'id':'di.class.psyker'}}))
 # Investigator records its required skill without inventing Expertise's multiplier.
 opts=r['di.choice.arbites_enforcer.subclass']['data']['options'];inv=next(x for x in opts if x['id']=='investigator');opts.remove(inv)
 for skill in ['investigation','insight']:
  opt=copy.deepcopy(inv);opt.update(id='investigator_'+skill,label='Investigator — '+skill.title()+' Expertise (manual / rule-pending)');opts.append(opt)
 support['di.feature.subclass.arbites_enforcer.investigator.level_3'].update(rulingIds=['PHB-RULE-011'],playerNote='Selected Expertise skill is recorded in the doctrine answer. Its numerical effect remains MANUAL / RULE-PENDING (PHB-RULE-011). Studied target adjudication is manual; uses are tracked.')
 for cl,level,slug in [('zealot',1,'martyrs_mercy'),('zealot',2,'charge_of_conviction'),('arbites_enforcer',1,'authority')]:resource(f'di.feature.class.{cl}.level_{level}.{slug}',slug,maximum='proficiency_bonus')
 resource('di.feature.subclass.arbites_enforcer.investigator.level_3','investigator_study',maximum='proficiency_bonus')
 for cl,slug in [('psyker','empowered_manifestation'),('aeldari_warlock','empowered_rune')]:resource(f'di.feature.class.{cl}.level_5.{slug}',slug,'short_rest')
 for cl,sub in [('psyker','diviner'),('aeldari_warlock','seer_of_battle')]:resource(f'di.feature.subclass.{cl}.{sub}.level_3',cl+'_fate','short_rest')
 choice('di.choice.psychic.ability','Psychic ability',[('intelligence','Intelligence'),('wisdom','Wisdom')])
 choice('di.choice.zealot.mercy_ability','Martyr’s Mercy ability',[('wisdom','Wisdom'),('charisma','Charisma')])
 p['psychic']=psychic_catalogue.build()
 for tier,levels in [('minor',[(1,2),(3,1)]),('standard',[(1,2),(2,1),(4,1)])]:
  for level,n in levels:choice(f'di.choice.psychic.{tier}_level_{level}',f'{tier.title()} powers — level {level}',[(x['id'].split('.')[-1],x['name']) for x in p['psychic']['powers'] if x['tier']==tier],n)
 # Inventory-only grenade records preserve absent procedures instead of inventing actions.
 for slug in ['firebomb','stun_grenade','smoke_grenade']:
  candidate=c.read(c.PACKAGE/f'review/candidates/weapon/{slug}.json');text=candidate['evidence'][0]['text']
  entity('di.weapon.'+slug,candidate['name'],dict(category='grenade',subcategory='grenade',hands=1,properties=[],features=[],modes=[],proficiencyGroups=['grenade'],availability='Controlled',abilityBinding={'attack':'none','damage':'none'},manualOnly=True,manualRules=[dict(id='manual_use',automation='manual',text=text,adjudicator='gm',context='Grenade use',reason='Specific outcome/condition procedure remains manual; no guessed damage/save resolution.')]),[e['source'] for e in candidate['evidence']],text)
  p['equipmentSupport']['di.weapon.'+slug]='MANUAL / RULE-PENDING: '+text+' PHB-RULE-018/046; no automatic outcome is assumed.'
 for slug in ['force_sword','force_staff','witchblade','singing_spear']:
  candidate=c.read(c.PACKAGE/f'review/candidates/weapon/{slug}.json');d=copy.deepcopy(r['di.weapon.combat_blade']['data']);d.update(properties=candidate['proposedData']['properties'],proficiencyGroups=['force'] if slug.startswith('force') else ['aeldari'],abilityBinding={'attack':'strength','damage':'strength'})
  # No Thrown range or multiple-type policy is inferred. Spear melee uses the explicit class override.
  for prop in d['properties']:
   params=r[prop['property']['id']]['data']['parameters'];prop['arguments']={x['name']:x['min'] for x in params} if params else {}
  mode=d['modes'][0];mode['damage']=copy.deepcopy(candidate['proposedData']['modes'][0].get('damage',r['di.weapon.combat_blade']['data']['modes'][0]['damage']));mode['damage'][0]['dice'].update(count=1,sides=6 if slug=='force_staff' else 8,bonus=0)
  if slug in ['witchblade','singing_spear']:mode['damage'][0]['damageType']={'id':'di.damage_type.slashing' if slug=='witchblade' else 'di.damage_type.piercing'}
  aid='di.action.'+slug+'.attack';mode['action']={'id':aid};a=copy.deepcopy(r['di.action.combat_blade.attack']);a.update(id=aid,name=candidate['name']+' attack',sources=[e['source'] for e in candidate['evidence']]);r[aid]=a
  entity('di.weapon.'+slug,candidate['name'],d,[e['source'] for e in candidate['evidence']],candidate['evidence'][0]['text'])
  p['equipmentSupport']['di.weapon.'+slug]='Base melee dice only. Weapon properties and slash-separated damage types are manual; do not infer extra damage. Singing Spear thrown mode is not automated.'
 for slug,base,cap in [('carapace_armour',15,2),('riot_armour',16,2),('rune_armour',13,None)]:
  candidate=c.read(c.PACKAGE/f'review/candidates/armour/{slug}.json');d=copy.deepcopy(r['di.armour.flak_armour']['data']);d['defence']['value']['value']=base;d['dexterityBonus']=dict(enabled=True,**({'cap':cap} if cap is not None else {}));d.pop('requirements',None)
  entity('di.armour.'+slug,candidate['name'],d,[e['source'] for e in candidate['evidence']],candidate['evidence'][0]['text']);s['armour'].append('di.armour.'+slug)
  p['equipmentSupport']['di.armour.'+slug]=candidate['evidence'][0]['text']
 kitSource=copy.deepcopy(source[0]);kitSource['locator'].update(pdfPage=100,printedPage=87,sectionKey='17.1',heading='Class starting equipment')
 for cl in ['zealot','arbites_enforcer']:
  p['packages']['di.class.'+cl]=c.read(c.PACKAGE/f'review/starting-packages/{cl}-prepared.json');p['packages']['di.class.'+cl].pop('status',None)
 p['packages']['di.class.psyker']=package([('di.weapon.laspistol',1),('di.equipment.sanctioning_brands_restraints',1),('di.equipment.psychic_focus',1)],[('force_weapon',['di.weapon.force_sword','di.weapon.force_staff']),('armour',['di.armour.heavy_clothing','di.armour.armoured_bodyglove','di.armour.mesh_armour'])],s['armour']+['di.armour.armoured_bodyglove','di.armour.mesh_armour'],kitSource)
 p['packages']['di.class.aeldari_warlock']=package([('di.weapon.shuriken_pistol',1),('di.armour.rune_armour',1),('di.equipment.spirit_charm',1)],[('rune_weapon',['di.weapon.witchblade','di.weapon.singing_spear']),('focus',['di.equipment.psychic_focus','di.equipment.rune_stones'])],s['armour'],kitSource)
 s['armour']=sorted(set(s['armour']+['di.armour.armoured_bodyglove','di.armour.mesh_armour']))
 for cl in NEW:
  items={key for key in audit.ids(p['packages']['di.class.'+cl]['display']) if key in r and r[key]['kind'] in audit.ITEM_KINDS};s['equipment']=sorted(set(s['equipment'])|items)
 # Preserve starting shield as carried until the unresolved combined-armour policy is decided.
 # Each path retains the source-defined shield item and manual doctrine benefits.
 for cl in NEW:
  species='di.species.aeldari' if cl=='aeldari_warlock' else 'di.species.human'
  for origin in s['origins']:
   if not any(a['species']['id']==species and a['state']=='NORMAL' for a in r[origin]['data'].get('originAvailability',[])):continue
   for level in range(1,6):
    dep=audit.selected_features(r,[species,origin,'di.class.'+cl],level);assert not dep['missing'],dep
    choices=set(dep['choices'])-{'di.choice.creation.universal_trait'}
    if species=='di.species.human':choices.update(['di.choice.human.broad_training_proof'])
    if cl=='zealot':choices.add('di.choice.zealot.mercy_ability')
    if cl in ['psyker','aeldari_warlock']:
     choices.add('di.choice.psychic.ability')
     choices.update(k for k in r if k.startswith('di.choice.psychic.') and '_level_' in k and int(k[-1])<=level)
    cfg=dict(speciesId=species,originId=origin,classId='di.class.'+cl,level=level,features=dep['features'],choices=sorted(choices));s['pathConfigurations'].append(cfg)
    subs=r['di.class.'+cl]['data']['allowedSubclasses'] if level>=3 or cl=='psyker' else [None]
    for sub in subs:s['certifiedPaths'].append({k:cfg[k] for k in ['speciesId','originId','classId','level']}|dict(subclassId=sub['id'] if sub else None,traitId='di.feature.universal.twitchy'))
 s['choices']=sorted({k for cfg in s['pathConfigurations'] for k in cfg['choices']})
 s['availability'][0]['message']='All twelve PHB classes through level 5. Create at level 1; advance one level at a time. Conditional effects remain manual.'
 s['availability'][-1]['message']='Rare/Limited Origins, Blank / Null-Bound and Warlock Pyromancy require trusted approval. Unresolved effects are marked manual. No level 6 or Major powers.'
 p['rosterReleaseStatus']='CANDIDATE_NOT_CERTIFIED'
 return dict(digest=c.digest(p),payload=p)

if __name__=='__main__':
 b=build();out=c.ROOT/'content/packages/di_phb_1_0/review/tier10-candidate.json';out.write_bytes(c.canonical(b)+b'\n');print(b['digest'],len(b['payload']['spec']['classes']),len(b['payload']['psychic']['powers']))

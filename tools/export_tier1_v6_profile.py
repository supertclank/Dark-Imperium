"""Source-backed v6 overlay; historical snapshots are read-only inputs.
Run --write only after closure and engine checks; --check never mutates releases.
"""
import copy, itertools, json, sys
from collections import Counter
import content_import as c
import tier1_catalogue as audit
import export_tier1_v5_profile as v5
import prepare_sharpshooter_v4 as sharp
from phb_policies import weapon_hands
CHOICE=v5.CHOICE
CLASSES={
 'veteran':['shock_trooper','marksman','sergeant'],
 'hive_scum':['gunslinger'],
 'ratling_sharpshooter':['long_las_sniper','spotter','black_market_gremlin'],
 'ogryn_skullbreaker':['bone_ead','brute','bulwark','gun_lugger'],
 'skitarii_veteran':['infiltrator','protector','ranger','vanguard'],
 'kin_armsman':['guild_militant','hearthguard','ironhead'],
 'hernkyn_prospector':['outrider','trail_gunner'],
 'aeldari_outcast':['ranger']}
BLOCKED={
 'hive_scum.sump_ghost':('BLOCKED_BY_RULING','PHB-RULE-011: mandatory Expertise.'),
 'hive_scum.chem_user':('BLOCKED_BY_RULING','PHB-RULE-046: exhaustion and an unspecified Constitution save DC.'),
 'hive_scum.knife_rat':('BLOCKED_BY_ENGINE','Conditional light-melee critical threshold requires an authoritative attack-mode contract.'),
 'ratling_sharpshooter.underhive_rat':('BLOCKED_BY_RULING','PHB-RULE-011: mandatory Expertise.'),
 'skitarii_veteran.data_hunter':('BLOCKED_BY_RULING','PHB-RULE-011: mandatory Expertise.'),
 'skitarii_veteran.ruststalker':('BLOCKED_BY_CONTENT','Mandatory blades proficiency lacks a certified complete weapon domain; equipment ownership is not that mapping.'),
 'hernkyn_prospector.claim_staker':('BLOCKED_BY_RULING','PHB-RULE-011: mandatory Expertise.'),
 'aeldari_outcast.shadow_guide':('BLOCKED_BY_RULING','PHB-RULE-011: mandatory Expertise.'),
 'aeldari_outcast.corsair':('BLOCKED_BY_CONTENT','Mandatory blades proficiency lacks a certified complete weapon domain.')}
MANUAL_TALENTS=['alien_reflexes','ancestors_grudge','bigger_gun','cold_logic','cooks_morale','impossible_shot','iron_stance','loyal_as_stone','machine_precision','noospheric_burst','ogryn_wall','path_discipline','pocket_marksman','rangers_cloak','ratling_vanish','sacred_augmetics','scavvers_luck','too_angry_to_notice','void_stock']

def build():
 old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v5.json');p=copy.deepcopy(old['payload']);s=p['spec'];r=p['records'];support=p['featureSupport']
 s.update(id='di-phb-1.0-tier1-v6',name='PHB 1.0 · Martial advancement through level 4',creationLevels=[1],advancementMechanicsVersion=1)
 s.pop('upgradeContract',None)
 def entity(key,name,data,source,text):
  e=copy.deepcopy(r['di.feature.species.ratling.traits']);e.update(id=key,kind=key.split('.')[1],revision=1,name=name,summary=text[:500],descriptionMarkdown=text,sources=copy.deepcopy(source),data=data);r[key]=e;return e
 def grant(key):return dict(id=key.split('.')[-1],kind='proficiency',proficiency={'id':key})
 def manual(fid,note=None,classification='MANUAL',**extra):
  support[fid]=dict(classification=classification,playerNote=note or 'Apply the canonical effect only in its stated context. Baseline rolls exclude conditional modifiers; no condition or combined-source stacking rule is inferred.',rulingIds=[],resources=[],**extra)
 def resource(fid,key,rest):support[fid]['resources'].append(dict(key=key,maximum=1,recovery=rest,automation='manual'))
 prepared=sharp.build();source=r['di.class.ratling_sharpshooter']['sources'];training=r['di.feature.class.ratling_sharpshooter.training']['data']
 for slug,label in [('cooks_utensils','Cook’s Utensils'),('thieves_tools','Thieves’ Tools')]:
  entity('di.tool.'+slug,label,dict(features=[],manualRules=[],functionalTags=['tool']),source,label+'; source-defined training and equipment. No inherent numeric bonus.')
  entity('di.proficiency.tool.'+slug,label+' proficiency',dict(category='tool',appliesTo={'ids':[{'id':'di.tool.'+slug}]}),source,'Proficiency with '+label+'.')
 toolkey='di.choice.ratling_sharpshooter.training_tool'
 entity(toolkey,'Sharpshooter tool training',dict(purpose='proficiency',selectionMode='options',cardinality=dict(min=1,max=1,unique=True),repeatScope='once_per_actor',options=[dict(id=x,label=r['di.tool.'+x]['name'],grants=[grant('di.proficiency.tool.'+x)]) for x in ['cooks_utensils','thieves_tools']]),source,'Choose exactly one tool proficiency. Equipment possession is a separate source choice.')
 training['grants']=[grant('di.proficiency.weapon_group.'+g) for g in ['pistol','shotgun','sniper']]+[dict(id='tool_training',kind='choice',choice={'id':toolkey})]
 # Actual source explicitly lists these three weapons, not all basic firearms or all melee weapons.
 for slug in ['knife','lasgun','long_las']:
  entity('di.proficiency.weapon.'+slug,r.get('di.weapon.'+slug,{'name':'Long-las'})['name']+' proficiency',dict(category='weapon',appliesTo={'ids':[{'id':'di.weapon.'+slug}]}),source,'Individual weapon training: '+slug.replace('_',' ')+'.')
  training['grants'].append(grant('di.proficiency.weapon.'+slug))
 promotions=[]
 for slug,kind in [('long_las','weapon'),('heavy_clothing','armour')]:
  candidate=c.read(c.PACKAGE/f'review/candidates/{kind}/{slug}.json');d=copy.deepcopy(candidate['proposedData']);key='di.'+kind+'.'+slug
  if kind=='weapon':
   mode=d['modes'][0];mode.update(attackKind='ranged',delivery='attack_roll',costs=[],action={'id':'di.action.long_las.attack'})
   d.update(category='ranged',subcategory='sniper',hands=weapon_hands('sniper'),features=[],proficiencyGroups=['sniper'],availability=candidate['evidence'][0]['text'].split('Availability: ')[-1],abilityBinding={'attack':'dexterity','damage':'dexterity'})
   a=copy.deepcopy(r['di.action.lasgun.attack']);a.update(id='di.action.long_las.attack',name='Long-las attack',sources=[x['source'] for x in candidate['evidence']]);r[a['id']]=a
  else:
   d=copy.deepcopy(r['di.armour.flak_armour']['data']);d.update(category='light',defence={'value':{'kind':'constant','value':11},'mode':'base','stackGroup':'di.defence.armour'},dexterityBonus={'enabled':True});d.pop('requirements',None)
  entity(key,candidate['name'],d,[x['source'] for x in candidate['evidence']],'\n'.join(x['text'] for x in candidate['evidence']));promotions.append(dict(id=key,candidateSha256=c.digest(candidate),sources=r[key]['sources']))
 for slug in ['heavy_clothing','flak_armour']:
  key='di.proficiency.armour.'+slug
  if key not in r:entity(key,r['di.armour.'+slug]['name']+' proficiency',dict(category='armour',appliesTo={'ids':[{'id':'di.armour.'+slug}]}),source,'Source-backed Sharpshooter armour training.')
  training['grants'].append(grant(key))
 # Keep the complete light-armour training label as a procedural proficiency until other armour is published.
 manual('di.feature.class.ratling_sharpshooter.training','Specific weapon, armour and selected tool training are structured. No skill grants appear in the class source.',classification='PARTIAL',proceduralProficiencies=['Light armour'])
 p['packages']['di.class.ratling_sharpshooter']=prepared['packageProposal']
 p['classTraining']['di.class.ratling_sharpshooter']=next(x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json') if x['class']['id']=='di.class.ratling_sharpshooter')
 s['classes'].append('di.class.ratling_sharpshooter');s['armour']=sorted(set(s['armour']+['di.armour.heavy_clothing']))
 s['equipment']=sorted(set(s['equipment'])|{x for x in audit.ids(p['packages']['di.class.ratling_sharpshooter']['display']) if x in r and r[x]['kind'] in audit.ITEM_KINDS})
 p['equipmentSupport']['di.weapon.long_las']='Source: 1d10 radiant, range 150/600 ft, two hands, Accurate, Reload 10. Accurate conditional +1 and reload are manual; baseline attack and damage use authoritative rolls.'
 p['equipmentSupport']['di.armour.heavy_clothing']='Light armour: AC 11 + Dexterity modifier, no Dexterity cap.'
 p['equipmentSupport']['di.equipment.camo_cloak']='Canonical contextual utility; no numeric bonus is invented.'
 for fid in ['di.feature.class.ratling_sharpshooter.level_1.small_target','di.feature.class.ratling_sharpshooter.level_1.deadeye']:manual(fid)
 support['di.feature.class.ratling_sharpshooter.level_1.small_target']['playerNote']='Conditional cover/prone benefits are manual. Do not double-apply overlapping Species/Class Small Target; PHB-RULE-046/058 remain unresolved.'
 # All subclass choices are independently reviewed; source tables do not certify every alternative.
 subclass_audit=[]
 for cl,allowed in CLASSES.items():
  key='di.choice.'+cl+'.subclass';options=r[key]['data']['options'];r[key]['data']['options']=[o for o in options if o['id'] in allowed]
  for o in options:
   fid='di.feature.subclass.'+cl+'.'+o['id']+'.level_3';sub='di.subclass.'+cl+'.'+o['id']
   state,reason=('READY_WITH_MANUAL_RULES','Selected dependency closure certified; conditional effects remain manual.') if o['id'] in allowed else BLOCKED[cl+'.'+o['id']]
   subclass_audit.append(dict(id=sub,status=state,reason=reason,sources=r[fid]['sources'],benefit=r[fid]['descriptionMarkdown']))
   if o['id'] in allowed:manual(fid)
  for fid in list(r):
   if fid.startswith('di.feature.class.'+cl+'.level_2.') and fid not in support:manual(fid)
  f='di.feature.class.'+cl+'.level_4.ability_score_improvement_talent'
  r[f]['data']['grants']=[dict(id='improvement',kind='choice',choice={'id':CHOICE})];r[f]['data']['manualRules']=[]
  support[f]=copy.deepcopy(support['di.feature.class.veteran.level_4.ability_score_improvement_talent'])
 # Structured subclass grants and numeric additions.
 fid='di.feature.subclass.ratling_sharpshooter.black_market_gremlin.level_3';r[fid]['data']['grants']=[grant('di.proficiency.tool.thieves_tools')];support[fid]['classification']='PARTIAL'
 fid='di.feature.subclass.skitarii_veteran.infiltrator.level_3';r[fid]['data']['grants']=[grant('di.proficiency.skill.stealth')];support[fid]['classification']='PARTIAL';resource(fid,'infiltrator','short_rest')
 fid='di.feature.class.skitarii_veteran.level_2.augmetic_reflexes';manual(fid,'Intelligence modifier is added to initiative.',classification='AUTOMATED',initiativeAttributes=['intelligence'])
 fid='di.feature.subclass.hernkyn_prospector.outrider.level_3';effect=copy.deepcopy(r['di.feature.universal.twitchy']['data']['effects'][0]);effect.update(id='outrider_speed');effect['target']['key']='movement.walk';effect['stacking']['group']='di.movement.walk';effect['value']['value']=5;r[fid]['data']['effects']=[effect];support[fid]['classification']='PARTIAL'
 # Encode the Bone 'ead skill as part of the subclass choice so it is mandatory only in that selected context.
 fid='di.feature.subclass.ogryn_skullbreaker.bone_ead.level_3';support[fid]['savingThrows']=['wisdom'];support[fid]['classification']='PARTIAL'
 opts=r['di.choice.ogryn_skullbreaker.subclass']['data']['options'];bone=next(o for o in opts if o['id']=='bone_ead');opts.remove(bone)
 for skill in sorted(e['id'] for e in r.values() if e['kind']=='skill'):
  o=copy.deepcopy(bone);o.update(id='bone_ead_'+skill.split('.')[-1],label="Bone ’ead — "+r[skill]['name']);o['grants'].append(grant('di.proficiency.skill.'+skill.split('.')[-1]));opts.append(o)
 # Extend the existing Talent options; requirements remain canonical predicates.
 extra=MANUAL_TALENTS+['kin_weapon_master','hold_born_engineer','aeldari_grace']
 options=r[CHOICE]['data']['options'];metadata=s['level4Advancement']['options']
 for short in extra:
  fid='di.feature.talent.'+short;record=r[fid];manual(fid)
  note=support[fid]['playerNote'];grants=[dict(id='talent',kind='feature',feature={'id':fid})]
  kw={}
  if short=='hold_born_engineer':
   grants.append(grant('di.proficiency.skill.technology'));kw=dict(subchoiceId='di.proficiency.skill.technology',subchoiceLabel='Technology (engineering-tool branch not certified)');note='Only the explicit Technology alternative is certified. Engineering-tool alternatives remain unavailable; contextual repair advantage is manual.'
  if short=='kin_weapon_master':support[fid]['classification']='PARTIAL';support[fid]['weaponDamageGroups']=['kin'];note='Standalone +1 damage with Kin weapons is calculated. Combined-source stacking remains manual under PHB-RULE-058.'
  if short=='aeldari_grace':support[fid]['classification']='PARTIAL';support[fid]['armourMovement']={'categories':['light','aeldari'],'amount':5};note='The equipped armour category controls the +5-ft movement bonus.'
  support[fid]['playerNote']=note
  options.append(dict(id=short,label=record['name'],grants=grants));metadata.append(dict(id=short,label=record['name'],branch='TALENT',talentId=fid,requirement=record['descriptionMarkdown'].split('Requirement: ')[1].split('\n')[0],benefit=record['descriptionMarkdown'],classification=support[fid]['classification'],note=note,**kw))
  if short in ['ancestors_grudge','impossible_shot','machine_precision','noospheric_burst','too_angry_to_notice']:resource(fid,short,'short_rest')
  if short in ['cold_logic','path_discipline','scavvers_luck']:resource(fid,short,'long_rest')
 # Explicit, reviewable catalogue of selected Talent gaps; never publish by merely parsing prose.
 p['level4TalentReadiness']=[dict(id=e['id'],name=e['name'],status='READY_WITH_MANUAL_RULES' if e['id'] in {m.get('talentId') for m in metadata} else 'BLOCKED_BY_CONTENT',requirements=e['data'].get('requirements'),sources=e['sources'],benefit=e['descriptionMarkdown'],reason=(support.get(e['id'],{}).get('playerNote') or {'bone_ead_implant':'Feature-specific Intelligence maximum and mandatory saving-throw/skill choice await executable mapping; ASI maximum is not substituted.','rad_hardened':'Poison-or-radiation resistance selection requires a canonical resistance choice.','witchblade_adept':'Warlock-specific; psychic path is not published.','sanctioning_scars':'Psyker-specific; psychic path is not published.','witch_sight':'Psyker-specific; psychic path is not published.'}.get(e['id'].split('.')[-1],'See v5 withheld-content audit; unchanged blocker.'))) for e in r.values() if e['id'].startswith('di.feature.talent.')]
 # Build complete per-level configurations from selected roots; retain original Human scope.
 starts=[copy.deepcopy(x) for x in s['pathConfigurations'] if x['level']==1 and x['speciesId']!='di.species.human']
 for origin in sorted({x['originId'] for x in starts if x['speciesId']=='di.species.ratling'}):starts.append(dict(speciesId='di.species.ratling',originId=origin,classId='di.class.ratling_sharpshooter',level=1))
 for base in starts:
  cl=base['classId'].split('.')[-1]
  for level in range(1,5):
   if any(all(x[k]==base[k] for k in ['speciesId','originId','classId']) and x['level']==level for x in s['pathConfigurations']):continue
   dep=audit.selected_features(r,[base[k] for k in ['speciesId','originId','classId']],level);assert not dep['missing'],dep
   cfg={k:base[k] for k in ['speciesId','originId','classId']};cfg.update(level=level,choices=sorted(set(dep['choices'])-{'di.choice.creation.universal_trait'}),features=sorted(dep['features']))
   s['pathConfigurations'].append(cfg)
   for sub in CLASSES[cl] if level>=3 else [None]:s['certifiedPaths'].append({k:v for k,v in cfg.items() if k not in ['choices','features']}|dict(subclassId='di.subclass.'+cl+'.'+sub if sub else None,traitId='di.feature.universal.twitchy'))
 for cfg in s['pathConfigurations']:
  for fid in cfg['features']:
   if fid not in support:manual(fid,classification='PARTIAL' if r[fid]['data']['grants'] else 'MANUAL')
 s['choices']=sorted({v for x in s['pathConfigurations'] for v in x['choices']})
 prior=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json')
 s['upgradeContracts']=[dict(version='nonhuman-v4-v6-1',fromProfile=prior['payload']['spec']['id'],fromDigest=prior['digest'],toProfile=s['id'],fromLevel=1,toLevel=2,speciesIds=sorted({x['speciesId'] for x in starts}),classIds=sorted({x['classId'] for x in starts if x['classId']!='di.class.ratling_sharpshooter'}),preserve=['choices','inventory','resources','currentHp','conditions','temporaryEffects','rollHistory'])]
 s['availability'][0]['message']='Certified martial paths through level 4, with explicit subclass and Talent restrictions. New characters start at level 1. Conditional effects remain manual.'
 s['availability'][-1]['message']='Expertise-dependent paths, unmapped blades proficiency, psychic classes, open tool/vehicle alternatives and level 5 remain unavailable. Older characters retain their pinned profile.'
 p['nonhumanAdvancementAudit']=dict(subclasses=subclass_audit,promotions=promotions,sourcePreparation='review/starting-packages/ratling_sharpshooter-prepared.json',unchangedRulings={'resolved':15,'unresolved':21,'total':36},restrictions=['No level 5 or Extra Attack','Hernkyn Vehicles remains unavailable only in that optional training branch','Magna-rail requires GM approval','Ogryn Flak Plate remains PHB-RULE-030 blocked'])
 c.validate_records(r)
 return dict(digest=c.digest(p),payload=p)

if __name__=='__main__':
 b=build()
 if '--write' in sys.argv or '--check' in sys.argv:
  for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v6.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v6.json',b['payload']['spec'])]:
   raw=c.canonical(value)+b'\n'
   if path.exists():assert path.read_bytes()==raw,'Immutable release differs: '+str(path)
   elif '--write' in sys.argv:path.write_bytes(raw)
   else:raise AssertionError('Missing release')
 print(b['digest'],len(b['payload']['spec']['certifiedPaths']),'family rows')

"""Compose v4 from preserved v3 plus explicitly reviewed level-one paths."""
import copy,sys
import content_import as c
import export_tier1_v3_profile as old
import export_tier1_v2_profile as kit
import tier1_catalogue as audit

def build():
 _,r=c.load();p=copy.deepcopy(old.build()['payload']);s=p['spec'];p['records']=r
 s.update(id='di-phb-1.0-tier1-v4',name='PHB 1.0 · Six species',speciesMechanicsVersion=1)
 new=[('ogryn','penal_worlder','ogryn_skullbreaker'),('ogryn','militarum_regiment','ogryn_skullbreaker'),('skitarii','forge_world','skitarii_veteran'),('kin','mining_hold_guild','kin_armsman'),('kin','mining_hold_guild','hernkyn_prospector'),('aeldari','craftworld_outcast','aeldari_outcast')]
 for species,origin,klass in new:
  a,b,d='di.species.'+species,'di.background.'+origin,'di.class.'+klass
  assert a in r and b in r and d in r,(a,b,d)
  assert next(x for x in r[b]['data']['originAvailability'] if x['species']['id']==a)['state']=='NORMAL'
  dep=audit.selected_features(r,[a,b,d],1);assert not dep['missing']
  cfg=dict(speciesId=a,originId=b,classId=d,level=1,choices=sorted(set(dep['choices'])-{'di.choice.creation.universal_trait'}),features=sorted(dep['features']))
  s['pathConfigurations'].append(cfg);s['certifiedPaths'].append({k:v for k,v in cfg.items() if k not in ('choices','features')}|dict(subclassId=None,traitId='di.feature.universal.twitchy'))
 for field,key in [('species','speciesId'),('origins','originId'),('classes','classId')]:s[field]=list(dict.fromkeys(s[field]+[x[key] for x in s['pathConfigurations']]))
 s['choices']=sorted({v for x in s['pathConfigurations'] for v in x['choices']})
 armour=['di.armour.'+x for x in ['ogryn_plate','flak_armour','kin_mesh','hearthkyn_plate','prospector_rig','aeldari_mesh','ranger_weave']];s['armour']=sorted(set(s['armour']+armour))
 source=copy.deepcopy(p['package']['source']);source['locator'].update(pdfPage=100,printedPage=87,heading='Class starting packages')
 def package(klass,fixed,choices):p['packages']['di.class.'+klass]=kit.package(fixed,choices,s['armour'],source)
 package('ogryn_skullbreaker',[('di.armour.ogryn_plate',1),('di.weapon.frag_bomb',1),('di.equipment.rations',1),('di.equipment.lucky_charm',1)],[('primary',['di.weapon.ripper_gun','di.weapon.ogryn_club'])])
 package('skitarii_veteran',[('di.weapon.laspistol',1),('di.equipment.auspex',1),('di.tool.maintenance_tools',1),('di.weapon.frag_grenade',2)],[('primary',['di.weapon.lasgun']),('melee',['di.weapon.taser_goad','di.weapon.combat_blade']),('armour',['di.armour.flak_armour'])])
 package('kin_armsman',[('di.weapon.frag_grenade',2),('di.equipment.oath_token',1)],[('primary',['di.weapon.ion_blaster']),('pistol',['di.weapon.autoch_pattern_pistol']),('armour',['di.armour.kin_mesh','di.armour.hearthkyn_plate']),('melee',['di.weapon.kin_power_axe','di.weapon.concussion_hammer'])])
 package('hernkyn_prospector',[('di.equipment.survey_auspex',1),('di.tool.climbing_kit',1),('di.equipment.claim_marker',1)],[('pistol',['di.weapon.autoch_pattern_pistol']),('primary',['di.weapon.ion_blaster']),('armour',['di.armour.prospector_rig']),('melee',['di.weapon.knife'])])
 package('aeldari_outcast',[('di.weapon.shuriken_pistol',1),('di.weapon.monomolecular_blade',1),('di.equipment.spirit_token',1),('di.equipment.camo_cloak',1)],[('primary',['di.weapon.shuriken_catapult','di.weapon.ranger_long_rifle']),('armour',['di.armour.aeldari_mesh','di.armour.ranger_weave'])])
 items=set(s['equipment'])
 for pack in p['packages'].values():
  items.update(x['item']['id'] for x in pack['display']['fixed']);items.update(o['id'] for x in pack['display']['choices'] for o in x['options'])
 s['equipment']=sorted(items)
 p['classTraining'].update({x['class']['id']:x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json') if x['class']['id'] in s['classes']})
 # Verified Ogryn fit is an explicit closed certification scope, not an inferred prohibition on all other gear.
 s['equipmentCompatibility']={'di.species.ogryn':{'allowedIds':['di.weapon.ripper_gun','di.weapon.ogryn_club','di.weapon.frag_bomb','di.armour.ogryn_plate','di.equipment.rations','di.equipment.lucky_charm'],'message':'Only these reviewed Ogryn-frame starting items are certified; other fit/modification contexts require review.'}}
 s['blockedEquipmentOptions']=[{'id':'di.weapon.magna_rail_rifle','code':'GM_APPROVAL_REQUIRED','message':'Hernkyn starting Magna-rail Rifle explicitly requires GM approval; no self-service approval exists.'}]
 for cfg in s['pathConfigurations']:
  for fid in cfg['features']:
   if fid not in p['featureSupport']:
    p['featureSupport'][fid]={'classification':'PARTIAL' if r[fid]['data'].get('manualRules') else 'AUTOMATED','playerNote':'Required fixed calculations and selected proficiencies are included. Conditional source benefits require manual adjudication.','rulingIds':[],'resources':[]}
 def resource(fid,key,maximum,recovery):p['featureSupport'][fid]['resources'].append(dict(key=key,maximum=maximum,recovery=recovery,automation='manual'))
 for fid,key,n,rest in [('di.feature.species.ogryn.traits','simple_solutions',1,'short_rest'),('di.feature.species.skitarii.traits','integrated_auspex',1,'short_rest'),('di.feature.class.skitarii_veteran.level_1.targeting_protocol','targeting_protocol',2,'long_rest'),('di.feature.species.kin.traits','grudge_memory',1,'long_rest'),('di.feature.class.kin_armsman.level_1.oath_mark','oath_mark',2,'long_rest'),('di.feature.class.hernkyn_prospector.level_1.claim_sight','claim_sight',2,'long_rest'),('di.feature.species.aeldari.traits','battle_trance',1,'short_rest'),('di.feature.origin.craftworld_outcast','path_discipline',1,'long_rest'),('di.feature.origin.mining_hold_guild','hold_fast',1,'short_rest')]:resource(fid,key,n,rest)
 p['featureSupport']['di.feature.species.kin.traits']['playerNote']='Guild-Craft: the named Technology/Investigation branches are certified. The source also permits a related artisan/tool proficiency; that open tool domain remains recorded but is not a self-service branch until each tool mapping is certified. Durability and Grudge Memory are manual.'
 p['featureSupport']['di.feature.species.aeldari.traits']['playerNote']='Keen Senses adds +1 once when another selected source grants Perception; this is not Expertise. Battle Trance and contextual traits remain manual.'
 p['featureSupport']['di.feature.species.skitarii.traits']['playerNote']='No Psychic Potential is enforced. No default darkvision. Auspex targeting, poison resistance, disease/charm advantages and Cybernetic Maintenance remain manual.'
 p['featureSupport']['di.feature.class.hernkyn_prospector.level_1.prospector_training']['playerNote']='Survival and the reviewed skill choices are calculated. The source Vehicles branch remains unavailable pending canonical proficiency mapping.'
 for item in items-set(old.build()['payload']['spec']['equipment']):
  if r[item]['kind']=='weapon':p['equipmentSupport'][item]='Baseline attack/damage only. Apply weapon properties, targets, conditions and ammunition manually; no Burst or Suppression automation.'
 p['equipmentSupport']['di.weapon.frag_bomb']='Ogryn only. Failure: 4d6 piercing and prone. Success: half damage and no prone. Exact fractional damage is displayed; any integer rounding and target condition application remain manual. Distinct from Frag Grenade and generic Blast.'
 for item in items:
  if r[item]['kind']=='armour' and item not in old.build()['payload']['spec']['equipment']:p['equipmentSupport'][item]=r[item]['descriptionMarkdown']+' Conditional armour benefits are manual.'
 s['availability'][0]['message']='Six species: existing Human/Ratling paths plus level-one Ogryn Skullbreaker, Skitarii Veteran, Kin Armsman/Hernkyn and Aeldari Outcast in their certified NORMAL Origins. Twitchy and explicitly reviewed package/choice branches only.'
 s['availability'][-1]['message']='Non-Human higher levels, psychic paths, unmapped tool/vehicle choices and unreviewed equipment remain unavailable. Magna-rail requires trusted GM approval. Prior snapshots remain unchanged.'
 return {'digest':c.digest(p),'payload':p}
if __name__=='__main__':
 b=build()
 for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v4.json',b['payload']['spec'])]:
  content=c.canonical(value)+b'\n'
  if '--check' in sys.argv or path.exists():assert path.read_bytes()==content,'Immutable release differs: '+str(path)
  else:path.write_bytes(content)
 print(b['digest'])

"""Source-bounded non-Human level-one mapping. Original candidate bytes are archived."""
import copy,json,re,hashlib,shutil
from pathlib import Path
import content_import as c
from phb_policies import weapon_hands

def main():
 if (c.PACKAGE/'review/nonhuman-v4-promotions.json').exists():
  c.load();print('Already mapped; canonical release records preserved. Use export_tier1_v4_profile.py --check to verify.');return
 manifest,r=c.load();original=copy.deepcopy(r);added=[];promoted=[]
 candidates={c.read(p)['proposedId']:(p,c.read(p)) for p in (c.PACKAGE/'review/candidates').rglob('*.json')}
 def entity(key,name,data,source,text):
  e=copy.deepcopy(r['di.feature.species.ratling.traits']);e.update(id=key,kind=key.split('.')[1],revision=1,name=name,summary=text[:500],descriptionMarkdown=text,sources=copy.deepcopy(source),data=data);return e
 def manual(text):return {'id':'source_rule','automation':'manual','text':text,'adjudicator':'gm','context':'PHB selected source context','reason':'Baseline only; contextual rules are adjudicated manually.'}
 def put(e):r[e['id']]=e;added.append(e['id'])
 def skillgrant(skill):return {'id':skill,'kind':'proficiency','proficiency':{'id':'di.proficiency.skill.'+skill}}
 def choice(fid,suffix,skills,n=1):
  key='di.choice.'+suffix;f=r[fid];options=[{'id':x,'label':r['di.skill.'+x]['name'],'grants':[skillgrant(x)]} for x in skills]
  put(entity(key,f['name']+' choice',{'purpose':'skill','selectionMode':'options','cardinality':{'min':n,'max':n,'unique':True},'repeatScope':'once_per_actor','options':options},f['sources'],f['descriptionMarkdown']))
  f['data']['grants'].append({'id':suffix.replace('.','_'),'kind':'choice','choice':{'id':key}})
 def mechanics(key,*values):r[key]['data']['mechanics']=list(values)
 def vision(species,n):
  e=copy.deepcopy(r['di.feature.species.ratling.traits']['data']['effects'][0]);e['value']['value']=n;r['di.feature.species.'+species+'.traits']['data']['effects'].append(e)
 choice('di.feature.species.skitarii.traits','skitarii.noospheric_focus',['investigation','perception','technology'])
 choice('di.feature.class.skitarii_veteran.level_1.machine_focus','skitarii_veteran.machine_focus',['investigation','technology'])
 choice('di.feature.species.kin.traits','kin.guild_craft',['technology','investigation'])
 mechanics('di.feature.species.kin.traits',{'kind':'open_tool_pool','domains':['engineering','mining','weapons','armour','voidcraft']})
 choice('di.feature.species.aeldari.traits','aeldari.inhuman_grace',['acrobatics','stealth'])
 r['di.feature.species.aeldari.traits']['data']['grants'].append(skillgrant('perception'))
 mechanics('di.feature.species.aeldari.traits',{'kind':'duplicate_proficiency_bonus','proficiency':{'id':'di.proficiency.skill.perception'},'amount':1})
 vision('kin',60);vision('aeldari',90)
 mechanics('di.feature.species.skitarii.traits',{'kind':'psychic_prohibition','classes':[{'id':'di.class.psyker'}],'traits':[{'id':e['id']} for e in r.values() if e['kind']=='feature' and e['id'].startswith('di.feature.universal.') and ('psychic powers' in e['descriptionMarkdown'].lower() or 'minor psychic' in e['descriptionMarkdown'].lower())]})
 mechanics('di.feature.species.ogryn.traits',{'kind':'hp_per_level','amount':3},{'kind':'contextual_size','increase':1,'contexts':['carrying','lifting','pushing','dragging','grappling','shoving']},{'kind':'equipment_frame','frame':'ogryn','text':'Most standard armour, delicate weapons, compact firearms and subtle tools require Ogryn modification.'},{'kind':'innate_damage','name':'Brute Strength unarmed damage','count':1,'sides':6,'ability':'strength','damageType':{'id':'di.damage_type.bludgeoning'}})
 big='di.feature.class.ogryn_skullbreaker.level_1.big_lad';r[big]['data']['grants'].append(skillgrant('athletics'))
 mechanics(big,{'kind':'score_adjustment','attribute':'dexterity','amount':-2,'minimum':6,'phase':'after_species'},{'kind':'contextual_size','increase':1,'contexts':['grappling','shoving','carrying','lifting','dragging','breaking']})
 choice('di.feature.class.kin_armsman.level_1.kin_training','kin_armsman.training',['athletics','insight','investigation','perception','survival','technology','persuasion'],2)
 # Vehicles is not a canonical skill; retain the complete source domain as a certification blocker for that branch.
 choice('di.feature.class.hernkyn_prospector.level_1.prospector_training','hernkyn_prospector.training',['investigation','perception','stealth','technology'])
 r['di.feature.class.hernkyn_prospector.level_1.prospector_training']['data']['grants'].append(skillgrant('survival'))
 r['di.feature.class.aeldari_outcast.level_1.ranger_training']['data']['grants'] += [skillgrant('stealth'),skillgrant('perception')]
 def promote(key,data):
  path,can=candidates[key];text='\n'.join(x['text'] for x in can['evidence']);put(entity(key,can['name'],data,[x['source'] for x in can['evidence']],text));promoted.append({'id':key,'originalPath':str(path.relative_to(c.PACKAGE)),'rawSha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 def weapon(slug,category,groups):
  key='di.weapon.'+slug;can=candidates[key][1];d=copy.deepcopy(can['proposedData']);props={p['property']['id'].split('.')[-1] for p in d['properties']};melee=category=='melee';action='di.action.'+slug+'.attack'
  mode=d['modes'][0];mode.update(attackKind='melee' if melee else 'ranged',delivery='attack_roll',costs=[],action={'id':action})
  if melee:mode['range']={'kind':'reach','distance':{'value':5,'unit':'ft'}}
  d.update(category='melee' if melee else 'ranged',subcategory=category,hands=weapon_hands(category,heavy='heavy' in props),features=[],proficiencyGroups=groups,availability=can['evidence'][0]['text'].split('Availability: ')[-1],abilityBinding={'attack':'finesse' if 'finesse' in props else 'strength' if melee else 'dexterity','damage':'finesse' if 'finesse' in props else 'strength' if melee else 'dexterity'})
  promote(key,d);a=copy.deepcopy(r['di.action.shock_maul.attack']);a.update(id=action,name=can['name']+' attack',sources=r[key]['sources']);put(a)
 for slug,cat,groups in [('ogryn_club','melee',['ogryn']),('ripper_gun','basic_firearm',['ogryn']),('taser_goad','melee',['mechanicus','shock']),('ion_blaster','basic_firearm',['kin']),('autoch_pattern_pistol','pistol',['kin','pistol']),('kin_power_axe','melee',['kin']),('concussion_hammer','melee',['kin','shock']),('shuriken_pistol','pistol',['aeldari','pistol']),('shuriken_catapult','basic_firearm',['aeldari']),('ranger_long_rifle','sniper',['aeldari','sniper']),('monomolecular_blade','melee',['aeldari'])]:weapon(slug,cat,groups)
 for slug,ac,cap,species in [('kin_mesh',14,2,'kin'),('hearthkyn_plate',15,2,'kin'),('prospector_rig',14,2,'kin'),('aeldari_mesh',12,None,'aeldari'),('ranger_weave',13,None,'aeldari')]:
  d=copy.deepcopy(r['di.armour.flak_armour']['data']);d.update(category=species,defence={'value':{'kind':'constant','value':ac},'mode':'base','stackGroup':'di.defence.armour'},dexterityBonus={'enabled':True,**({'cap':cap} if cap is not None else {})},requirements={'equip':{'kind':'selected','content':{'id':'di.species.'+species}}},availability='Controlled')
  promote('di.armour.'+slug,d)
 # Auspex is explicitly named in the starting package. Its numerical/target use remains manual.
 source=r['di.equipment.survey_auspex']['sources'];put(entity('di.equipment.auspex','Auspex',{'features':[],'manualRules':[manual('Auspex from the Skitarii starting package. Resolve scans and target context manually; no inherent numerical bonus is assumed.')],'functionalTags':['scanner']},source,'Auspex; Skitarii Veteran starting package, PHB PDF 100.'))
 # Source-complete Frag Bomb profile is distinct from PHB-RULE-059. Preserve exact half damage without supplying an unapproved integer rounding policy.
 d=copy.deepcopy(r['di.weapon.frag_grenade']['data']);d['proficiencyGroups']=['ogryn','grenade'];m=d['modes'][0];m['action']={'id':'di.action.frag_bomb.use'};m['damage'][0]['dice']['count']=4;m['area']['radius']['value']=20
 m['save']['outcomes']['success']['rounding']='exact_fraction';m['save']['outcomes']['failure']['rounding']='exact_fraction';m['manualRules']=[manual('Ogryn only. Failure: full damage and knocked prone. Success: half damage and not knocked prone. Prone application and any integer rounding are manual. No generic Blast or Frag Grenade ruling is imported.')]
 d['requirements']={'kind':'selected','content':{'id':'di.species.ogryn'}};promote('di.weapon.frag_bomb',d);a=copy.deepcopy(r['di.action.frag_grenade.use']) if 'di.action.frag_grenade.use' in r else copy.deepcopy(r['di.action.shock_maul.attack']);a.update(id='di.action.frag_bomb.use',name='Frag Bomb use',sources=r['di.weapon.frag_bomb']['sources']);a['data'].pop('rolls',None);put(a)
 for key,e in r.items():
  if key in original and e!=original[key]:e['revision']=original[key]['revision']+1
 c.validate_records(r)
 entries={x['id']:x for x in manifest['entities']}
 for key,e in r.items():
  if key in original and e==original[key]:continue
  path=c.PACKAGE/(entries[key]['path'] if key in entries else 'entities/'+e['kind']+'/'+key.split('.',2)[2]+'.json')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  entries[key]={'id':key,'path':path.relative_to(c.PACKAGE).as_posix(),'revision':e['revision'],'sha256':c.digest(e)}
 for row in promoted:
  src=(c.PACKAGE/row['originalPath']).resolve();dst=(c.PACKAGE/'review/archive/nonhuman-v4'/Path(row['originalPath']).relative_to('review/candidates')).resolve();assert src.is_relative_to(c.PACKAGE.resolve()) and dst.is_relative_to(c.PACKAGE.resolve());dst.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(src),str(dst));row['archivePath']=dst.relative_to(c.PACKAGE).as_posix()
 manifest['entities']=sorted(entries.values(),key=lambda x:x['id']);manifest['packageVersion']='1.0-nonhuman-tier1.4';(c.PACKAGE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (c.PACKAGE/'review/nonhuman-v4-promotions.json').write_text(json.dumps({'promotions':promoted,'addedRecords':added,'basis':'PHB source profiles and approved PHB-RULE-024; no new ruling decisions.'},indent=2)+'\n',encoding='utf-8')
 print(len(r),'records',len(promoted),'promotions');c.load()
if __name__=='__main__':main()

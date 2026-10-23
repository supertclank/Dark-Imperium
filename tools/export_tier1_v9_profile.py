"""v9 extends existing Human Hive Scum paths; no unresolved equipment or rulings promoted."""
import copy,sys
import content_import as c
import tier1_catalogue as audit
import export_tier1_v8_profile as v8

def build():
 old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v8.json');p=copy.deepcopy(old['payload']);s=p['spec'];r=p['records']
 s.update(id='di-phb-1.0-tier1-v9',name='PHB 1.0 · Audited class roster through level 5')
 for base in list(s['pathConfigurations']):
  if base['speciesId']!='di.species.human' or base['classId']!='di.class.hive_scum' or base['level']!=1:continue
  for level in range(2,6):
   dep=audit.selected_features(r,[base[k] for k in ['speciesId','originId','classId']],level);assert not dep['missing']
   cfg=dict(base,level=level,features=sorted(dep['features']),choices=sorted((set(dep['choices'])|set(base['choices']))-{'di.choice.creation.universal_trait'}))
   s['pathConfigurations'].append(cfg)
   s['certifiedPaths'].append({k:cfg[k] for k in ['speciesId','originId','classId','level']}|dict(subclassId='di.subclass.hive_scum.gunslinger' if level>=3 else None,traitId='di.feature.universal.twitchy'))
 s['choices']=sorted({k for x in s['pathConfigurations'] for k in x['choices']})
 s['upgradeContracts']=[]
 for version in [7,8]:
  source=c.read(c.ROOT/f'backend/src/main/resources/profiles/di-phb-1.0-tier1-v{version}.json')
  s['upgradeContracts'].append(dict(version=f'v{version}-v9-human-scum-1',fromProfile=source['payload']['spec']['id'],fromDigest=source['digest'],toProfile=s['id'],fromLevel=1,toLevel=2,speciesIds=['di.species.human'],classIds=['di.class.hive_scum'],preserve=['choices','inventory','resources','currentHp','conditions','temporaryEffects','rollHistory']))
 s['availability'][0]['message']='Certified martial paths through level 5, including Human Hive Scum Gunslinger. Create at level 1 and advance one level at a time. Conditional effects remain manual.'
 s['availability'][-1]['message']='Zealot and Arbites await required starting-equipment rule completion. Psyker and Aeldari Warlock require the shared psychic framework. Other unreviewed subclasses, equipment and level 6+ remain unavailable.'
 p.pop('level5Audit',None)
 c.validate_records(r)
 return dict(digest=c.digest(p),payload=p)

if __name__=='__main__':
 b=build()
 for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v9.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v9.json',b['payload']['spec'])]:
  raw=c.canonical(value)+b'\n'
  if path.exists():assert path.read_bytes()==raw,'Immutable release differs: '+str(path)
  elif '--write' in sys.argv:path.write_bytes(raw)
  else:raise AssertionError('Missing release')
 if '--write' in sys.argv:
  d=c.ROOT/'backend/src/test/resources/tier9';d.mkdir(exist_ok=True);(d/'all-paths.json').write_bytes(c.canonical(v8.fixtures(b))+b'\n')
 print(b['digest'],len(b['payload']['spec']['certifiedPaths']),'family rows')

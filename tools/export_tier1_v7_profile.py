"""PHB-RULE-024 fixed weapon ability amendment. Historical releases remain byte-identical."""
import copy,sys
import content_import as c

def build():
 old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v6.json')
 p=copy.deepcopy(old['payload']);s=p['spec'];r=p['records']
 s.update(id='di-phb-1.0-tier1-v7',name='PHB 1.0 · Fixed weapon abilities · Martial levels 1–4',weaponAbilityPolicyVersion=2)
 s.pop('upgradeContracts',None) # No implicit migration from any historical profile.
 p['weaponAbilityAmendments']=c.read(c.PACKAGE/'review/weapon-ability-amendments.json')
 changed=[]
 for key,e in r.items():
  if e['kind']!='weapon':continue
  binding=e['data']['abilityBinding']
  if 'finesse' in binding.values():
   e['revision']+=1
   for field in ['attack','damage']:
    if binding.get(field)=='finesse':binding[field]='dexterity'
   e['descriptionMarkdown']+='\nPHB-RULE-024 amendment (23 October 2026): Finesse uses Dexterity for attack and damage; no player ability choice.'
   changed.append(key)
 prop=r['di.property.weapon.finesse'];prop['revision']+=1
 prop['descriptionMarkdown']=prop['summary']='Uses Dexterity for attack and damage. PHB-RULE-024 amendment approved 23 October 2026; supersedes the original choice wording.'
 for rule in prop['data']['manualRules']:rule['text']=prop['descriptionMarkdown']
 p['weaponAbilityAmendments'][0]['affectedPublishedWeapons']=sorted(changed)
 c.validate_records(r)
 return dict(digest=c.digest(p),payload=p)

if __name__=='__main__':
 b=build()
 for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v7.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v7.json',b['payload']['spec'])]:
  raw=c.canonical(value)+b'\n'
  if path.exists():assert path.read_bytes()==raw,'Immutable release differs: '+str(path)
  elif '--write' in sys.argv:path.write_bytes(raw)
  elif '--check' in sys.argv:raise AssertionError('Missing release')
 print(b['digest'],len(b['payload']['spec']['certifiedPaths']),'unchanged family rows')

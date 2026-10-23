"""Deterministic selected-context fixtures for the v6 engine and browser acceptance."""
import copy,itertools
import content_import as c
from export_tier1_v6_profile import build,CHOICE

def build_fixtures():
 b=build();p=b['payload'];s=p['spec'];r=p['records'];fixtures=[]
 for family in s['certifiedPaths']:
  cfg=next(x for x in s['pathConfigurations'] if all(x[k]==family[k] for k in ['speciesId','originId','classId','level']))
  answers={}
  for key in cfg['choices']:
   choice=r[key]['data'];opts=choice['options']
   if choice['purpose']=='subclass':opts=[o for o in opts if any(g.get('content',{}).get('id')==family['subclassId'] for g in o['grants'])]
   if key==CHOICE:opts=[o for o in opts if o['id']=='plus_two_constitution']
   answers[key]=[o['id'] for o in opts[:choice['cardinality']['min']]]
  pack=p['packages'][family['classId']]['display'];pc={x['id']:x['options'][0]['id'] for x in pack['choices']}
  inventory=[dict(definitionId=x['item']['id'],quantity=x['quantity'],equipped=x['item']['id'] in s['armour']) for x in pack['fixed']]+[dict(definitionId=pc[x['id']],quantity=x['quantity'],equipped=pc[x['id']] in s['armour']) for x in pack['choices']]
  fixtures.append(dict(profileId=s['id'],profileDigest=b['digest'],name='v6 '+family['speciesId'].split('.')[-1]+' '+family['classId'].split('.')[-1]+' '+str(family['level']),speciesId=family['speciesId'],originId=family['originId'],classId=family['classId'],level=family['level'],traitId=family['traitId'],attributes=dict(zip(s['attributes'],[15,14,13,12,10,8])),answers=answers,packageChoices=pc,inventory=inventory))
 return fixtures
if __name__=='__main__':
 path=c.ROOT/'backend/src/test/resources/tier6/all-paths.json';path.parent.mkdir(exist_ok=True);path.write_bytes(c.canonical(build_fixtures())+b'\n');print(len(build_fixtures()),'fixtures')

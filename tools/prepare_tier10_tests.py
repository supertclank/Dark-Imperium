import sys
sys.path.insert(0,'tools')
import content_import as c
import export_tier1_v10_profile as v10
import export_tier1_v8_profile as v8
b=v10.build();c.validate_records(b['payload']['records']);d=c.ROOT/'backend/src/test/resources/tier10';d.mkdir(exist_ok=True)
(d/'candidate.json').write_bytes(c.canonical(b)+b'\n')
fixtures=v8.fixtures(b)
for f in fixtures:
 for key in f['answers']:
  if key.startswith('di.choice.psychic.') and '_level_' in key:
   f['answers'][key]={'minor_level_1':['warp_spark','kinetic_push'],'minor_level_3':['mind_lumen'],'standard_level_1':['focused_rupture','psychic_shield'],'standard_level_2':['assail'],'standard_level_4':['soulfire']}[key.removeprefix('di.choice.psychic.')]
(d/'all-paths.json').write_bytes(c.canonical(fixtures)+b'\n')
print(len(fixtures),'candidate fixtures')

import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import export_tier1_v8_profile as v8
class Level5ContentTests(unittest.TestCase):
 def test_reproducible_release(self):
  b=v8.build();self.assertEqual(b,c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v8.json'));self.assertEqual(len(v8.fixtures(b)),297)
 def test_selected_level5_closure(self):
  b=v8.build();s=b['payload']['spec'];a=b['payload']['level5Audit'];self.assertEqual(len(a['classes']),8);self.assertEqual(len(a['subclasses']),21)
  self.assertEqual(sum(x['attacksPerAttackAction']==2 for x in a['classes']),6)
  self.assertEqual(sum(x['level']==5 for x in s['certifiedPaths']),77)
  self.assertEqual(s['creationLevels'],[1]);self.assertEqual(s['levels'],[1,2,3,4,5])
 def test_no_new_equipment_or_psychic_paths(self):
  b=v8.build()['payload'];old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v7.json')['payload']
  self.assertEqual(b['spec']['equipment'],old['spec']['equipment']);self.assertEqual(b['packages'],old['packages'])
  self.assertEqual(b['spec']['classes'],old['spec']['classes']);self.assertEqual(b['level5Audit']['thunderHammer']['productionOwnership'],'BLOCKED_BY_CONTENT')
 def test_explicit_upgrade_and_no_historical_snapshot_changes(self):
  b=v8.build();contract=b['payload']['spec']['upgradeContracts'][0];self.assertEqual((contract['fromLevel'],contract['toLevel']),(4,5));self.assertEqual(contract['fromDigest'],'af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5')
 def test_capacity_rejects_ambiguous_sum_or_conditional_policy(self):
  import copy
  b=v8.build();r=b['payload']['records'];e=r['di.feature.class.veteran.level_5.extra_attack']['data']['effects'][0]
  for key,value in [('operation','add'),('value',{'kind':'constant','value':0}),('stacking',{'group':'di.action.attack.capacity','mode':'sum'})]:
   bad=copy.deepcopy(e);bad[key]=value
   with self.assertRaises(c.InvalidContent):c.effects([bad],r)

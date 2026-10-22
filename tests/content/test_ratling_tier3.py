import sys,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import export_tier1_v3_profile as export
class RatlingReleaseTests(unittest.TestCase):
 def test_snapshot_reproduces_and_keeps_all_human_paths(self):
  b=export.build();self.assertEqual(b,c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v3.json'))
  old=c.read(ROOT/'content/profiles/di-phb-1.0-tier1-v2.json')
  self.assertEqual(old['certifiedPaths'],[x for x in b['payload']['spec']['certifiedPaths'] if x['speciesId']=='di.species.human'])
 def test_all_ten_ratling_paths_are_normal_level_one(self):
  p=export.build()['payload'];paths=[x for x in p['spec']['certifiedPaths'] if x['speciesId']=='di.species.ratling'];self.assertEqual(10,len(paths))
  for x in paths:
   self.assertEqual(1,x['level']);self.assertEqual('NORMAL',next(a['state'] for a in p['records'][x['originId']]['data']['originAvailability'] if a['species']['id']==x['speciesId']))
 def test_darkvision_max_does_not_authorize_generic_stacking(self):
  _,records=c.load();bad=copy.deepcopy(records);e=bad['di.feature.species.ratling.traits']['data']['effects'][0];e['target']['key']='defence'
  with self.assertRaises(Exception):c.validate_records(bad)

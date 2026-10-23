import hashlib, itertools, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if not (ROOT/'tools').exists():ROOT=Path(r'C:/Users/tgccl/OneDrive/Documents/localdev/Dark-Imperium')
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import content_import as c
import prepare_sharpshooter_v4 as prep

class SharpshooterPreparationTests(unittest.TestCase):
 def test_source_and_candidate_bytes_remain_verifiable(self):
  data=prep.build()
  for candidate in data['preservedCandidates']:
   raw=(c.PACKAGE/candidate['path']).read_bytes()
   self.assertEqual(candidate['sha256'],hashlib.sha256(raw).hexdigest())
  self.assertEqual('PREPARATION_ONLY_NOT_PUBLISHED',data['status'])
  self.assertEqual([150,600],data['equipmentReview'][0]['rangeFeet'])
  self.assertEqual(11,data['equipmentReview'][1]['baseAC'])
 def test_package_all_branches_have_one_armour_six_items_and_no_grenades(self):
  steps=prep.build()['packageProposal']['executable']['steps']
  fixed=[s for s in steps if s['kind']=='item']
  choices=[s for s in steps if s['kind']=='choice']
  self.assertEqual(16,len(list(itertools.product(*(s['options'] for s in choices)))))
  for branch in itertools.product(*(s['options'] for s in choices)):
   resolved=fixed+[s for opt in branch for s in opt['steps']]
   items=[s for s in resolved if s['kind']=='item']; equipped=[s for s in resolved if s['kind']=='equip']
   self.assertEqual(6,len(items));self.assertEqual(1,len(equipped))
   self.assertTrue(all(s['quantity']==1 for s in items))
   self.assertFalse(any('grenade' in s['itemId'] for s in items))
   self.assertIn(equipped[0]['itemId'],[s['itemId'] for s in items])
 def test_training_does_not_broaden_groups_or_resolve_expertise(self):
  data=prep.build();training=data['trainingProposal'];choice=training['toolChoice']
  self.assertNotIn('basic_firearm',training['weaponGroups']);self.assertNotIn('simple_melee',training['weaponGroups'])
  self.assertEqual((1,1),(choice['min'],choice['max']));self.assertEqual(2,len({x['proficiencyId'] for x in choice['options']}))
  expert=next(f for f in data['featureReview'] if 'underhive_rat' in f['id'])
  self.assertEqual('BLOCKED',expert['classification']);self.assertEqual(['PHB-RULE-011'],expert['rulingIds'])
  self.assertTrue(all(f['classification']=='MANUAL' for f in data['featureReview'] if 'level_1' in f['id']))

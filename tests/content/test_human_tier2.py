import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import export_tier1_v2_profile as export
import tier1_catalogue as audit

class HumanTier2Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.bundle=export.build();cls.p=cls.bundle['payload'];cls.r=cls.p['records'];cls.s=cls.p['spec']
 def test_reproducible_immutable_release(self):
  self.assertEqual(self.bundle,c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v2.json'));self.assertEqual(self.s,c.read(ROOT/'content/profiles/di-phb-1.0-tier1-v2.json'))
 def test_every_published_path_is_normal_human_and_parent_correct(self):
  self.assertEqual(48,len(self.s['certifiedPaths']))
  for x in self.s['certifiedPaths']:
   self.assertEqual('di.species.human',x['speciesId']);self.assertTrue(audit.eligible(self.r[x['classId']],x['speciesId']))
   state=next(a['state'] for a in self.r[x['originId']]['data']['originAvailability'] if a['species']['id']==x['speciesId']);self.assertEqual('NORMAL',state)
   if x['level']==3:self.assertEqual(x['classId'],self.r[x['subclassId']]['data']['parentClass']['id']);self.assertTrue(audit.eligible(self.r[x['subclassId']],x['speciesId'],x['classId'],3))
 def test_scum_has_real_two_skill_grant_and_contact_not_inventory(self):
  choice=self.r['di.choice.hive_scum.streetwise']['data'];self.assertEqual(2,choice['cardinality']['min']);self.assertEqual(6,len(choice['options']))
  package=self.p['packages']['di.class.hive_scum'];self.assertEqual(1,sum(s['kind']=='contact' for s in package['executable']['steps']));self.assertFalse(any('contact' in s['item']['id'] for s in package['display']['fixed']))
 def test_selected_level_dependencies_only(self):
  for x in self.s['pathConfigurations']:
   self.assertEqual(x['level']==3,'di.choice.veteran.subclass' in x['choices']);self.assertFalse(any('level_4.' in f for f in x['features']))
 def test_promotions_preserve_complete_profile_and_candidate_evidence(self):
  for key in c.read(c.PACKAGE/'review/human-tier1-promotions.json')['promotedWeapons']:
   d=self.r[key]['data'];self.assertTrue(self.r[key]['sources'])
   for field in ['hands','proficiencyGroups','abilityBinding','properties','modes']:self.assertIn(field,d)
   self.assertIn(d['modes'][0]['action']['id'],self.r)
   self.assertFalse(any(c.read(p).get('proposedId')==key for p in (c.PACKAGE/'review/candidates').rglob('*.json')))
 def test_unresolved_procedures_never_become_automatic(self):
  support=self.p['featureSupport'];self.assertEqual('BLOCKED',support['di.feature.class.veteran.level_2.suppressing_fire']['classification'])
  for sub in ['shock_trooper','marksman','sergeant']:self.assertEqual('MANUAL',support['di.feature.subclass.veteran.'+sub+'.level_3']['classification'])
  self.assertNotIn('di.class.psyker',self.s['classes']);self.assertNotIn('di.weapon.firebomb',self.s['equipment'])

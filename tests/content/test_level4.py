import copy,hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import export_tier1_v5_profile as v5
import tier1_catalogue as audit
class Level4ContentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.b=v5.build();cls.p=cls.b['payload'];cls.s=cls.p['spec']
 def test_exact_approvals_provenance_and_denominator(self):
  ledger=c.read(c.PACKAGE/'review/decisions.json')['humanRulings'];history=c.read(c.PACKAGE/'review/human-rulings-integration.json')
  self.assertEqual(36,len(history));self.assertEqual(15,sum(x['status']=='RESOLVED' for x in history))
  for n in [14,15,16]:
   x=next(x for x in ledger if x['id']==f'PHB-RULE-{n:03}');self.assertTrue(audit.validate_approval(x,origin=True));self.assertIn('Mark '+x['id']+' RESOLVED.',x['decision'])
 def test_reproducible_immutable_snapshot_and_explicit_upgrade_contract(self):
  self.assertEqual(self.b,c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v5.json'))
  old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json');self.assertEqual(old['digest'],self.s['upgradeContract']['fromDigest']);self.assertEqual('2ef85cd454999670ee61f51eebcc9b23e6805d5220b518d2c5643001831c5119',old['digest'])
  self.assertEqual(old['payload']['spec']['certifiedPaths'],self.s['certifiedPaths'][:64])
  self.assertEqual(24,len(self.s['certifiedPaths'][64:]));self.assertTrue(all(x['speciesId']=='di.species.human' and x['classId']=='di.class.veteran' and x['level']==4 for x in self.s['certifiedPaths'][64:]))
 def test_exclusive_complete_ASI_options_and_safe_talent_pool(self):
  p=self.s['level4Advancement'];options=p['options'];self.assertEqual(6,sum(x['branch']=='ASI_PLUS_TWO' for x in options));self.assertEqual(15,sum(x['branch']=='ASI_SPLIT' for x in options))
  self.assertTrue(all(len(set(x['abilities']))==2 for x in options if x['branch']=='ASI_SPLIT'))
  talents={x['talentId'] for x in options if x['branch']=='TALENT'};self.assertEqual(18,len(talents));self.assertNotIn('di.feature.talent.suppressive_discipline',talents)
  self.assertTrue(all(v5.eligible(self.p['records'][x]['data'].get('requirements'),{'di.species.human','di.class.veteran'}) for x in talents))
 def test_subchoices_use_source_groups_and_approved_minor_pool(self):
  options=self.s['level4Advancement']['options'];self.assertEqual({'pistol','basic_firearm','sniper','shotgun','chain','shock','plasma','melta','heavy'},{x['subchoiceId'] for x in options if x.get('talentId')=='di.feature.talent.weapon_specialist'})
  approved={x['grants'][0]['content']['id'] for x in self.p['records']['di.choice.starting.minor_augmetic']['data']['options']}
  self.assertEqual(approved,{x['subchoiceId'] for x in options if x.get('talentId')=='di.feature.talent.cybernetic_implant'})
 def test_every_talent_has_individual_readiness_and_source(self):
  rows=self.p['level4TalentReadiness'];self.assertEqual({x for x in self.p['records'] if x.startswith('di.feature.talent.')},{x['id'] for x in rows})
  for x in rows:self.assertTrue(x['reason']);self.assertTrue(x['sources']);self.assertTrue(x['benefit'])
if __name__=='__main__':unittest.main()

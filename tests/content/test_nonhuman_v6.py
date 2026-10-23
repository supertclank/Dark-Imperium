import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import export_tier1_v6_profile as v6
import tier1_catalogue as audit
class Tier6ContentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.b=v6.build();cls.p=cls.b['payload'];cls.s=cls.p['spec'];cls.r=cls.p['records']
 def test_release_reproducible_and_historical_profiles_pinned(self):
  self.assertEqual(self.b,c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v6.json'))
  self.assertEqual('b061617c32eb325d73552b56b7e7c240faf77b5ac44de309375c929574dbf98b',c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v5.json')['digest'])
  self.assertEqual(220,len(self.s['certifiedPaths']));self.assertEqual([1],self.s['creationLevels'])
 def test_every_published_tuple_has_selected_dependency_closure(self):
  for f in self.s['certifiedPaths']:
   deps=audit.selected_features(self.r,[f['speciesId'],f['originId'],f['classId'],f['traitId']],f['level'],f['subclassId'])
   self.assertFalse(deps['missing'],f)
   self.assertTrue(all(x in self.p['featureSupport'] or (not self.r[x]['data']['manualRules'] and bool(self.r[x]['data']['effects'] or self.r[x]['data']['grants'] or self.r[x]['data'].get('choices'))) for x in deps['features']),f)
   self.assertNotIn('expertise',' '.join(self.r[x]['descriptionMarkdown'].lower() for x in deps['features'] if '.subclass.' in x))
 def test_explicit_nonhuman_upgrade_contract_and_no_psychic_or_level_five(self):
  con=self.s['upgradeContracts'][0];self.assertEqual((1,2),(con['fromLevel'],con['toLevel']));self.assertNotIn('di.species.human',con['speciesIds']);self.assertEqual(c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json')['digest'],con['fromDigest'])
  self.assertFalse(set(self.s['classes'])&{'di.class.psyker','di.class.aeldari_warlock'});self.assertTrue(all(x['level']<=4 for x in self.s['certifiedPaths']))
 def test_sharpshooter_source_tool_choices_and_equipment(self):
  r=self.r;tool=r['di.choice.ratling_sharpshooter.training_tool']['data'];self.assertEqual({'min':1,'max':1,'unique':True},tool['cardinality']);self.assertEqual(2,len(tool['options']))
  gun=r['di.weapon.long_las']['data'];self.assertEqual(2,gun['hands']);self.assertEqual(['sniper'],gun['proficiencyGroups']);self.assertEqual(10,gun['modes'][0]['damage'][0]['dice']['sides'])
  armour=r['di.armour.heavy_clothing']['data'];self.assertEqual(11,armour['defence']['value']['value']);self.assertEqual({'enabled':True},armour['dexterityBonus'])
  self.assertTrue((c.PACKAGE/'review/candidates/weapon/long_las.json').exists())
 def test_subclass_gates_are_local_and_rulings_remain_unresolved(self):
  rows=self.p['nonhumanAdvancementAudit']['subclasses'];blocked=[x for x in rows if 'PHB-RULE-011' in x['reason']];self.assertEqual(5,len(blocked));self.assertTrue(all(x['status']=='BLOCKED_BY_RULING' for x in blocked))
  ledger=c.read(c.PACKAGE/'review/human-rulings-integration.json');self.assertEqual(15,sum(x['status']=='RESOLVED' for x in ledger));self.assertEqual(36,len(ledger))
 def test_talents_keep_structured_requirements_and_exclude_uncertified_branches(self):
  opts=self.s['level4Advancement']['options'];talents={x.get('talentId') for x in opts}-{None};self.assertEqual(40,len(talents));self.assertNotIn('di.feature.talent.bone_ead_implant',talents)
  self.assertNotIn('di.feature.talent.rad_hardened',talents);self.assertEqual('di.proficiency.skill.technology',next(x for x in opts if x['id']=='hold_born_engineer')['subchoiceId'])
  self.assertTrue(all('requirements' in self.r[x]['data'] for x in talents if x.split('.')[-1] in v6.MANUAL_TALENTS))

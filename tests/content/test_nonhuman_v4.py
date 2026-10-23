import copy,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import export_tier1_v4_profile as v4
class NonhumanV4Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.bundle=v4.build();cls.p=cls.bundle['payload'];cls.r=cls.p['records']
 def test_export_matches_new_snapshot_and_exact_six_families(self):
  self.assertEqual(self.bundle,c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json'))
  old=c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v3.json')['payload']['spec']['certifiedPaths'];paths=self.p['spec']['certifiedPaths']
  self.assertEqual(old,paths[:58]);self.assertEqual(64,len(paths));self.assertEqual({'di.species.ogryn','di.species.skitarii','di.species.kin','di.species.aeldari'},{x['speciesId'] for x in paths[58:]})
 def test_original_candidate_bytes_are_archived_and_not_silently_lost(self):
  rows=c.read(c.PACKAGE/'review/nonhuman-v4-promotions.json')['promotions'];self.assertEqual(17,len(rows))
  for x in rows:
   self.assertEqual(x['rawSha256'],hashlib.sha256((c.PACKAGE/x['archivePath']).read_bytes()).hexdigest());self.assertFalse((c.PACKAGE/x['originalPath']).exists());self.assertIn(x['id'],self.r)
 def test_frag_bomb_has_own_source_save_policy(self):
  d=self.r['di.weapon.frag_bomb']['data'];m=d['modes'][0]
  self.assertEqual({'kind':'selected','content':{'id':'di.species.ogryn'}},d['requirements']);self.assertEqual(4,m['damage'][0]['dice']['count']);self.assertEqual(20,m['area']['radius']['value']);self.assertEqual('exact_fraction',m['save']['outcomes']['success']['rounding']);self.assertIn('not knocked prone',m['manualRules'][0]['text'])
  self.assertEqual('floor',self.r['di.weapon.frag_grenade']['data']['modes'][0]['save']['outcomes']['success']['rounding'])
 def test_resource_recovery_matches_species_and_origin_sources(self):
  support=self.p['featureSupport']
  self.assertEqual([{'key':'grudge_memory','maximum':1,'recovery':'long_rest','automation':'manual'}],support['di.feature.species.kin.traits']['resources'])
  self.assertEqual('short_rest',support['di.feature.species.aeldari.traits']['resources'][0]['recovery'])
  self.assertEqual('short_rest',support['di.feature.species.skitarii.traits']['resources'][0]['recovery'])
 def test_required_choices_and_prohibition_are_explicit(self):
  for key in ['di.choice.skitarii.noospheric_focus','di.choice.kin.guild_craft','di.choice.aeldari.inhuman_grace']:self.assertEqual(1,self.r[key]['data']['cardinality']['min'])
  rule=self.r['di.feature.species.skitarii.traits']['data']['mechanics'][0];self.assertIn({'id':'di.feature.universal.touched_by_the_warp'},rule['traits'])
  self.assertEqual(['engineering','mining','weapons','armour','voidcraft'],self.r['di.feature.species.kin.traits']['data']['mechanics'][0]['domains'])
 def test_unknown_mechanic_and_unapproved_fraction_policy_are_rejected(self):
  r=copy.deepcopy(self.r);r['di.feature.species.ogryn.traits']['data']['mechanics'][0]['kind']='invented_rule'
  with self.assertRaises(c.InvalidContent):c.validate_records(r)
  r=copy.deepcopy(self.r);r['di.weapon.frag_grenade']['data']['modes'][0]['save']['outcomes']['success']['rounding']='exact_fraction'
  with self.assertRaises(c.InvalidContent):c.validate_records(r)
 def test_all_selected_starting_items_are_canonical_and_no_gm_item_is_published(self):
  items=set(self.p['spec']['equipment']);self.assertNotIn('di.weapon.magna_rail_rifle',items)
  for key in items:self.assertIn(key,self.r)
  self.assertEqual('GM_APPROVAL_REQUIRED',self.p['spec']['blockedEquipmentOptions'][0]['code'])
if __name__=='__main__':unittest.main()

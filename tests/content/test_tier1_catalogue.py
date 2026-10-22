import copy,hashlib,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import tier1_catalogue as audit
import tier1_calculations as calc
import export_narrow_profile

class Tier1CatalogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=audit.build();cls.records=c.load()[1]
 def rows(self,**criteria):return [r for r in self.data['rows'] if all(r[k]==v for k,v in criteria.items())]
 def test_reproducible_audit_and_plan_digest(self):
  self.assertEqual(self.data,c.read(audit.OUT));plan=c.read(c.PACKAGE/'review/tier1-publication-plan.json');self.assertEqual(c.digest(self.data),plan['auditDigest']);self.assertTrue(plan['productionAllowed']);self.assertEqual(48,len(plan['allowlist']))
 def test_all_dimensions_and_subclasses_are_covered(self):
  self.assertEqual((6,10,12,45,4140),tuple(self.data['counts'][k] for k in ['species','origins','classes','subclasses','combinations']));self.assertEqual(4140,len({x['id'] for x in self.data['rows']}))
 def test_origin_gate_preserves_original_denominator(self):
  self.assertEqual(36,self.data['approvalGate']['originalTotal']);self.assertEqual(24,self.data['approvalGate']['originalUnresolved']);self.assertEqual(7,self.data['approvalGate']['originNewlyResolved'])
 def test_every_affected_origin_is_resolved_but_approval_is_separate(self):
  self.assertFalse(any(r['status']=='BLOCKED_BY_RULING' for r in self.data['rows']))
  for row in self.data['rows']:
   if row['originAvailability'] in ('RARE','LIMITED') and row['eligibility']!='INVALID':
    self.assertEqual('BLOCKED_BY_APPROVAL',row['status']);self.assertFalse(row['productionAllowed'])
 def test_rarity_is_never_self_service_permission(self):
  states=[x['state'] for o in self.data['origins'] for x in o['originAvailability']]
  self.assertEqual((18,3,1),tuple(states.count(s) for s in ['NORMAL','RARE','LIMITED']))
 def test_invalid_species_and_origin_combinations(self):
  self.assertTrue(all(r['status']=='UNSUPPORTED' for r in self.rows(species='di.species.human',**{'class':'di.class.ogryn_skullbreaker'})))
  self.assertTrue(all(r['status']=='UNSUPPORTED' for r in self.rows(species='di.species.ratling',origin='di.background.schola_progenium')))
 def test_no_invalid_or_missing_subclass_is_publishable(self):
  parents={s['id']:s['classId'] for s in self.data['subclasses']}
  for row in self.data['rows']:
   if row['level']==3:self.assertIsNotNone(row['subclass']);self.assertEqual(row['class'],parents[row['subclass']]);self.assertEqual(row['productionAllowed'],row['species']=='di.species.human' and row['class']=='di.class.veteran' and row['originAvailability']=='NORMAL')
 def test_dependency_walk_does_not_pull_other_subclasses_or_later_levels(self):
  dep=audit.selected_features(self.records,['di.class.veteran'],1)
  self.assertFalse(any('level_2.' in key or 'level_3.' in key or '.subclass.' in key for key in dep['features']))
  dep=audit.selected_features(self.records,['di.class.veteran'],3,'di.subclass.veteran.marksman')
  self.assertFalse(any('.sergeant.' in key or '.shock_trooper.' in key for key in dep['features']));self.assertFalse(dep['missing'])
 def test_unrelated_rulings_do_not_block_known_narrow_path(self):
  ready=[r for r in self.data['rows'] if r['productionAllowed']];self.assertEqual(48,len(ready));self.assertEqual('READY_WITH_MANUAL_RULES',ready[0]['status']);self.assertEqual([],ready[0]['rulingIds']);self.assertEqual(['di.feature.universal.twitchy'],ready[0]['traitScope'])
 def test_hypothetical_origin_approval_is_not_publication(self):
  cases=[r for r in self.data['rows'] if r['ifOriginExplicitlyPermittedAndAvailabilitySatisfied']]
  self.assertEqual(37,len(cases));self.assertTrue(all(r['ifOriginExplicitlyPermittedAndAvailabilitySatisfied'].startswith('BLOCKED_') for r in cases))
 def test_equipment_status_does_not_publish_candidates_or_whole_packages(self):
  for e in self.data['equipment']:
   if not e['canonical']:self.assertEqual('BLOCKED',e['status']);self.assertFalse(e['productionAllowed'])
  self.assertEqual(10,sum(e['productionAllowed'] for e in self.data['equipment']))
  self.assertTrue(all(k['startingKit']['structuredPackage'] is None for k in self.data['classes'] if k['id'] not in ['di.class.veteran','di.class.hive_scum','di.class.zealot','di.class.arbites_enforcer']))
 def test_psychic_counts_and_required_pools_are_audited_separately(self):
  for k in self.data['classes']:
   if k['psychic']:self.assertEqual([(2,2),(2,3),(3,3)],[(x['minor'],x['standard']) for x in k['psychic']['knownPowerCounts']]);self.assertEqual('BLOCKED_BY_CONTENT',k['psychic']['status'])
  self.assertEqual(38,sum(p['requiredForTier1Pool'] for p in self.data['powers']));self.assertTrue(all(p['status']=='BLOCKED' for p in self.data['powers']))
 def test_family_fixtures_are_not_fake_playable_characters(self):
  fixtures=c.read(ROOT/'tests/fixtures/tier1/family-readiness.json');self.assertEqual(36,len(fixtures))
  for fixture in fixtures:
   row=self.rows(**fixture['tuple']);self.assertEqual(1,len(row));self.assertEqual(fixture['expectedStatus'],row[0]['status']);self.assertEqual('FAMILY_READINESS_NOT_VALID_CHARACTER',fixture['scope'])
 def test_narrow_snapshot_remains_byte_compatible(self):
  bundle=c.read(ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json');self.assertEqual(export_narrow_profile.build(),bundle);self.assertEqual('3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af',bundle['digest'])
 def test_no_approval_from_resolved_label_or_forged_digest(self):
  self.assertFalse(audit.validate_approval({'id':'PHB-RULE-001','status':'RESOLVED','decision':'Use matrix'},origin=True))
  valid=copy.deepcopy(next(x for x in c.read(c.PACKAGE/'review/human-rulings-integration.json') if x['status']=='RESOLVED'))
  self.assertTrue(audit.validate_approval(valid));valid['approval']['sha256']='0'*64;self.assertFalse(audit.validate_approval(valid))
 def test_origin_approval_requires_timestamp_relationship_and_affected_ids(self):
  valid=copy.deepcopy(next(x for x in c.read(c.PACKAGE/'review/human-rulings-integration.json') if x['status']=='RESOLVED'))
  valid['approval'].pop('recordedAt',None)
  self.assertFalse(audit.validate_approval(valid,origin=True));valid['approval']['path']='../manifest.json';self.assertFalse(audit.validate_approval(valid))

class Tier1CalculationTests(unittest.TestCase):
 def project(self,die=10,level=3,**changes):
  args=dict(hit_die=die,level=level,scores=dict(strength=17,dexterity=15,constitution=13,intelligence=12,wisdom=10,charisma=8),constitution_at_acquisition=[1]*level,save_attributes=['dexterity','wisdom'],skill_attributes={'athletics':'strength','stealth':'dexterity'},proficient_skills=['athletics'],armour_base=12,armour_dex_cap=2,walk=30,initiative_bonus=2);args.update(changes);return calc.fixed_core(**args)
 def test_fixed_hp_by_hit_die_levels_1_to_3(self):
  for die,expected in [(6,[7,12,17]),(8,[9,15,21]),(10,[11,18,25]),(12,[13,21,29])]:
   for level,total in enumerate(expected,1):self.assertEqual(total,self.project(die,level)['maximumHp'])
 def test_shared_saves_skills_armour_and_initiative(self):
  r=self.project();self.assertEqual((14,4,2),(r['armourClass'],r['initiative'],r['proficiencyBonus']));self.assertEqual(5,r['skills']['athletics']);self.assertEqual(2,r['skills']['stealth']);self.assertEqual(4,r['saves']['dexterity']);self.assertEqual(3,r['saves']['strength'])
 def test_changing_constitution_requires_ruling_not_recalculation(self):
  with self.assertRaisesRegex(c.InvalidContent,'PHB-RULE-014'):self.project(constitution_at_acquisition=[0,1,1])
 def test_nonpositive_hp_gain_does_not_invent_floor(self):
  scores=dict(strength=15,dexterity=14,constitution=1,intelligence=12,wisdom=10,charisma=8)
  with self.assertRaisesRegex(c.InvalidContent,'PHB-RULE-014'):self.project(die=6,scores=scores,constitution_at_acquisition=[-5]*3)
 def test_no_level_four_or_missing_training(self):
  with self.assertRaises(c.InvalidContent):self.project(level=4)
  with self.assertRaises(c.InvalidContent):self.project(save_attributes=['unknown'])
  with self.assertRaises(c.InvalidContent):self.project(proficient_skills=['unknown'])
 def test_explicitly_not_an_eligibility_or_character_certificate(self):
  self.assertEqual('CALCULATION_PROOF_NOT_PLAYABLE_CHARACTER',self.project()['scope'])

if __name__=='__main__':unittest.main()

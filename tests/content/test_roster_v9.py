import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import export_tier1_v9_profile as v9
import audit_class_roster_level5 as roster
class RosterParityTests(unittest.TestCase):
 def test_complete_source_roster_and_mutually_exclusive_class_outcomes(self):
  a=roster.build();self.assertEqual(a,c.read(c.PACKAGE/'review/class-roster-level5-audit.json'));self.assertEqual(len(a['classes']),12);self.assertEqual(len(a['subclasses']),45)
  self.assertEqual(sum(x['completionCategory']=='CERTIFIED_LEVEL_1_TO_5' for x in a['classes']),8);self.assertEqual(sum(x['completionCategory']=='EXPLICITLY_BLOCKED' for x in a['classes']),4)
  for x in a['classes']:
   self.assertEqual([x['level'] for x in x['levels']],[1,2,3,4,5]);self.assertTrue(x['sources']);self.assertTrue(x['equipment']);self.assertTrue(x['hitDie'])
   if x['completionCategory']=='EXPLICITLY_BLOCKED':self.assertTrue(x['knownBlockers'])
 def test_subclasses_cannot_disappear_or_publish_while_blocked(self):
  a=roster.build();b=v9.build()['payload'];published={x['subclassId'] for x in b['spec']['certifiedPaths'] if x['subclassId']}
  self.assertEqual(published,{x['subclassId'] for x in a['subclasses'] if x['status']=='CERTIFIED'})
  for x in a['subclasses']:
   self.assertTrue(x['sources']);self.assertTrue(x['reason'])
   if x['status']!='CERTIFIED':self.assertNotIn(x['subclassId'],published)
 def test_release_is_reproducible_and_existing_families_preserved(self):
  b=v9.build();self.assertEqual(b,c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v9.json'));old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v8.json')['payload'];new=b['payload']
  self.assertEqual(len(new['spec']['certifiedPaths']),329)
  for row in old['spec']['certifiedPaths']:self.assertIn(row,new['spec']['certifiedPaths'])
  for field in ['records','featureSupport','packages','classTraining','equipmentSupport']:self.assertEqual(old[field],new[field])
 def test_human_scum_has_all_five_levels_at_every_previously_published_origin(self):
  s=v9.build()['payload']['spec'];paths=[x for x in s['certifiedPaths'] if x['speciesId']=='di.species.human' and x['classId']=='di.class.hive_scum'];self.assertEqual(len(paths),40)
  for origin in {x['originId'] for x in paths}:self.assertEqual({x['level'] for x in paths if x['originId']==origin},{1,2,3,4,5})
  self.assertEqual({x['subclassId'] for x in paths if x['level']>=3},{'di.subclass.hive_scum.gunslinger'})
 def test_upgrades_are_narrow_and_do_not_rebind_level_five_characters(self):
  s=v9.build()['payload']['spec'];self.assertEqual(len(s['upgradeContracts']),2)
  for contract in s['upgradeContracts']:
   self.assertEqual((contract['fromLevel'],contract['toLevel']),(1,2));self.assertEqual(contract['classIds'],['di.class.hive_scum']);self.assertEqual(contract['speciesIds'],['di.species.human'])
  self.assertEqual(s['levels'],[1,2,3,4,5]);self.assertEqual(s['creationLevels'],[1])
 def test_required_equipment_and_psychic_gates_remain_explicit(self):
  a=roster.build();by={x['classId']:x for x in a['classes']};self.assertEqual(by['di.class.zealot']['status'],'BLOCKED_BY_RULE');self.assertEqual(by['di.class.arbites_enforcer']['status'],'BLOCKED_BY_RULE')
  for cl in ['psyker','aeldari_warlock']:self.assertEqual(by['di.class.'+cl]['status'],'PSYCHIC_FRAMEWORK_REQUIRED')
  self.assertEqual(a['counts']['partiallyCertified'],0)

import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import tier1_catalogue as audit
import export_tier1_profile as export

class OriginApprovalsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.records=c.load()[1]
 def test_exact_approved_normal_rare_limited_sets(self):
  expected={
   'hiveborn':{'human':'NORMAL','ratling':'NORMAL','ogryn':'RARE'},
   'shrine_worlder':{'human':'NORMAL','ratling':'RARE'},
   'penal_worlder':{'human':'NORMAL','ogryn':'NORMAL','ratling':'NORMAL'},
   'voidborn':{'human':'NORMAL','ratling':'NORMAL','ogryn':'RARE'},
   'forge_world':{'human':'NORMAL','skitarii':'NORMAL'},'schola_progenium':{'human':'NORMAL'},
   'militarum_regiment':{'human':'NORMAL','ogryn':'NORMAL','ratling':'NORMAL','skitarii':'LIMITED'},
   'underhive':{'human':'NORMAL','ratling':'NORMAL'},'craftworld_outcast':{'aeldari':'NORMAL'},'mining_hold_guild':{'kin':'NORMAL'}}
  for origin,states in expected.items():
   e=self.records['di.background.'+origin]
   self.assertEqual(states,{x['species']['id'].split('.')[-1]:x['state'] for x in e['data']['originAvailability']})
   for s in ['human','ogryn','ratling','skitarii','kin','aeldari']:self.assertEqual(s in states,audit.eligible(e,'di.species.'+s))
 def test_seven_exact_approvals_and_historical_denominator(self):
  history=c.read(c.PACKAGE/'review/human-rulings-integration.json');self.assertEqual(36,len(history));self.assertEqual(12,sum(x['status']=='RESOLVED' for x in history))
  ledger=c.read(c.PACKAGE/'review/decisions.json')['humanRulings']
  for n in range(1,8):
   entry=next(x for x in ledger if x['id']==f'PHB-RULE-{n:03}');self.assertTrue(audit.validate_approval(entry,origin=True));self.assertTrue(entry['affectedIds'])
   self.assertIn(f'Mark PHB-RULE-{n:03} RESOLVED.',entry['decision'])
 def test_schema_rejects_invalid_state_duplicate_species_and_wrong_ref(self):
  for change in ['state','duplicate','reference']:
   records=copy.deepcopy(self.records);rows=records['di.background.hiveborn']['data']['originAvailability']
   if change=='state':rows[0]['state']='GM_CLICKED_APPROVE'
   elif change=='duplicate':rows.append(copy.deepcopy(rows[0]))
   else:rows[0]['species']['id']='di.class.veteran'
   with self.assertRaises(c.InvalidContent):c.validate_records(records)
 def test_tier1_snapshot_is_reproducible_and_separately_versioned(self):
  b=export.build();self.assertEqual(b,c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v1.json'))
  self.assertEqual('phb-tier1-kotlin-v1',b['payload']['spec']['engineVersion']);self.assertEqual([1],b['payload']['spec']['levels'])
  self.assertEqual(1,len(b['payload']['spec']['certifiedPaths']))
 def test_ratling_core_proficiency_is_structured_but_not_published(self):
  e=self.records['di.feature.species.ratling.traits']
  self.assertIn('di.proficiency.skill.stealth',[x['proficiency']['id'] for x in e['data']['grants'] if x['kind']=='proficiency'])
  self.assertNotIn('di.species.ratling',export.build()['payload']['spec']['species'])

if __name__=='__main__':unittest.main()

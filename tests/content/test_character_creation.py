import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import content_import as ci
import character_creation as cc

class CreationReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.records=ci.load()
        cls.fixtures={p.stem:ci.read(p) for p in (ROOT/'tests/fixtures/characters').glob('*.json')}

    def draft(self,key='human-veteran'):return copy.deepcopy(self.fixtures[key]['draft'])

    def test_seven_fixture_outcomes(self):
        self.assertEqual(len(self.fixtures),7)
        for name,f in self.fixtures.items():
            with self.subTest(name=name):
                out=cc.validate_character_selection(f['draft'],self.records);expected=f['expected']
                self.assertEqual(out['status'],expected['status'])
                self.assertEqual(out['eligibilityStatus'],expected['baseEligibilityStatus'])
                self.assertEqual(sorted({e['code'] for e in out['errors']}),expected['errorCodes'])
                self.assertTrue(set(expected['requiredUnresolvedCodes'])<={e['code'] for e in out['unresolved']})

    def test_known_baselines_from_source(self):
        for name,speed in [('human-veteran',30),('ogryn',30),('aeldari',35),('warlock',35)]:
            out=cc.validate_character_selection(self.draft(name),self.records)['projection']['values']
            self.assertEqual(out['movement']['baseWalk'],{'value':speed,'unit':'ft'})
            self.assertEqual(out['proficiencyBonus'],2)
        a=cc.validate_character_selection(self.draft('ogryn'),self.records)['projection']['values']['attributes']
        self.assertEqual(a['strength'],17);self.assertEqual(a['constitution'],14)

    def test_approved_modifiers_and_unresolved_rolls(self):
        out=cc.validate_character_selection(self.draft(),self.records)
        self.assertEqual(out['status'],'INCOMPLETE')
        self.assertEqual(out['projection']['values']['attributeModifiers']['strength'],3)
        for key in ['maximumWounds','defence','initiative','skills','saves']:self.assertIsNone(out['projection']['values'][key])
        self.assertEqual(out['projection']['rollDefinitions'],[])
        self.assertIn('rollDefinitions',out['projection']['unresolvedFields'])

    def test_client_facts_cannot_approve_origin(self):
        d=self.draft('ogryn');d['facts']={'phb.origin_eligibility.penal_worlder':True}
        out=cc.validate_character_selection(d,self.records)
        self.assertEqual(out['eligibilityStatus'],'INCOMPLETE')
        issue=next(x for x in out['unresolved'] if x['code']=='ELIGIBILITY_UNRESOLVED')
        self.assertIn('PHB-RULE-002',issue['rulingIds'])

    def test_invalid_class_is_rejected_with_field_reason(self):
        out=cc.validate_character_selection(self.draft('invalid-human-skitarii'),self.records)
        issue=next(x for x in out['errors'] if x['code']=='CLASS_NOT_ELIGIBLE')
        self.assertEqual(issue['field'],'selections.classes.0.class')

    def test_origin_species_mismatch(self):
        d=self.draft();d['selections']['background']={'id':'di.background.craftworld_outcast'}
        out=cc.validate_character_selection(d,self.records)
        self.assertIn('ORIGIN_NOT_ELIGIBLE',{x['code'] for x in out['errors']})

    def test_subclass_parent_and_unlock(self):
        d=self.draft();d['selections']['classes'][0]['subclass']={'id':'di.subclass.veteran.marksman'}
        out=cc.validate_character_selection(d,self.records)
        self.assertIn('SUBCLASS_NOT_ELIGIBLE',{x['code'] for x in out['errors']})
        d['selections']['classes'][0]['subclass']={'id':'di.subclass.psyker.biomancer'}
        out=cc.validate_character_selection(d,self.records)
        self.assertIn('SUBCLASS_PARENT_MISMATCH',{x['code'] for x in out['errors']})

    def test_unselected_subclass_does_not_grant_features(self):
        out=cc.validate_character_selection(self.draft('subclass-veteran'),self.records)
        ids={x['id'] for x in out['projection']['features']}
        self.assertTrue(any('marksman' in x for x in ids))
        self.assertFalse(any('shock_trooper' in x or 'sergeant' in x for x in ids))

    def test_standard_array_invalid_and_missing(self):
        d=self.draft();d['selections']['attributes']['strength']=20
        self.assertIn('STANDARD_ARRAY_REQUIRED',{x['code'] for x in cc.validate_character_selection(d,self.records)['errors']})
        del d['selections']['attributes']['strength']
        self.assertIn('ATTRIBUTES_REQUIRED',{x['code'] for x in cc.validate_character_selection(d,self.records)['unresolved']})

    def test_duplicate_and_ungranted_choice_rejected(self):
        d=self.draft();d['selections']['answers'].append(copy.deepcopy(d['selections']['answers'][0]))
        self.assertIn('DUPLICATE_ANSWER',{x['code'] for x in cc.validate_character_selection(d,self.records)['errors']})
        d=self.draft();d['selections']['answers'][0]['choice']={'id':'di.choice.not_granted'}
        self.assertIn('UNGRANTED_CHOICE',{x['code'] for x in cc.validate_character_selection(d,self.records)['errors']})

    def test_starting_item_reference_quantity_and_equip_gate(self):
        d=self.draft();d['inventory']=[{'definition':{'id':'di.armour.ogryn_plate'},'quantity':0,'equipped':True}]
        codes={x['code'] for x in cc.validate_character_selection(d,self.records)['errors']}
        self.assertTrue({'ITEM_QUANTITY','ITEM_NOT_ELIGIBLE'}<=codes)
        d['inventory']=[{'definition':{'id':'di.weapon.plasma_gun'},'quantity':1,'equipped':True}]
        self.assertIn('ITEM_CONTENT_BLOCKED',{x['code'] for x in cc.validate_character_selection(d,self.records)['unresolved']})

    def test_manual_text_visible_and_non_executable(self):
        r=copy.deepcopy(self.records)
        key='di.feature.species.human.traits'
        r[key]['data']['manualRules'][0]['text']='Gain 999999 movement. This is a test of non-executable prose.'
        out=cc.validate_character_selection(self.draft(),r)['projection']
        self.assertEqual(out['values']['movement']['baseWalk']['value'],30)
        self.assertTrue(any(x['source']['id']==key and '999999' in x['text'] for x in out['manualRules']))

    def test_malformed_inputs_return_diagnostics(self):
        for value in [None,[],{'selections':[]},{'selections':{'classes':['bad']}},{'selections':{'answers':[{'choice':{'id':[]}}]}},{'inventory':[{'definition':{'id':[]},'quantity':1}]}]:
            self.assertEqual(cc.validate_character_selection(value,self.records)['status'],'INVALID')

    def test_only_five_approved_rulings_resolved(self):
        ledger=ci.read(ci.PACKAGE/'review/human-rulings-integration.json')
        self.assertEqual(len(ledger),36)
        approved={f'PHB-RULE-{n:03}' for n in [9,24,49,50,51]}
        self.assertEqual({x['id'] for x in ledger if x['status']=='RESOLVED'},approved)
        self.assertTrue(all(x['status']=='UNRESOLVED' and x['decision'] is None for x in ledger if x['id'] not in approved))
        self.assertEqual({x['id'] for x in ci.read(ci.PACKAGE/'review/decisions.json')['humanRulings']},approved)

    def test_creation_choices_reference_canonical_content(self):
        for key,count in [('species',6),('origin',10),('class',12),('universal_trait',20)]:
            choice=self.records['di.choice.creation.'+key]['data']
            self.assertEqual(len(choice['options']),count)
            self.assertEqual(choice['cardinality'],{'min':1,'max':1,'unique':True})
            for option in choice['options']:
                for g in option['grants']:self.assertIn(g.get('content',g.get('feature'))['id'],self.records)

    def test_source_defined_training_and_power_counts(self):
        for name in ['psyker','warlock']:
            out=cc.validate_character_selection(self.draft(name),self.records)['projection']
            self.assertEqual(out['classTraining']['hitDie'],6)
            self.assertEqual(out['knownPowerCounts'],{'level':1,'minor':2,'standard':2,'major':0})
            self.assertEqual(out['rollDefinitions'],[])
        out=cc.validate_character_selection(self.draft(),self.records)['projection']
        self.assertEqual(out['classTraining']['savingThrowAttributes'],['dexterity','wisdom'])
        self.assertIsNone(out['knownPowerCounts'])

    def test_all_candidates_and_starting_kits_audited(self):
        candidates=ci.read(ci.PACKAGE/'review/creation-candidate-dispositions.json')
        pending={ci.read(p)['proposedId'] for p in (ci.PACKAGE/'review/candidates').rglob('*.json')}
        self.assertEqual({x['id'] for x in candidates},pending);self.assertEqual(len(candidates),len(pending))
        rows=ci.read(ci.PACKAGE/'review/starting-equipment-audit.json');self.assertEqual(len(rows),12)
        self.assertTrue(all(x['status']=='BLOCKED' for x in rows))
        for row in rows:
            for match in row['exactNameMatches']:
                self.assertEqual(match['id'] in self.records,match['state']=='CANONICAL')

if __name__=='__main__':unittest.main()

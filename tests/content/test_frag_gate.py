import copy
import hashlib
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import phb_policies as p
import narrow_character as n

class FragGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _,cls.records=c.load();cls.fixture=c.read(ROOT/'tests/fixtures/narrow/veteran-level-1.json')
        cls.mode=cls.records['di.weapon.frag_grenade']['data']['modes'][0]
    def test_failed_save_full_11(self):
        self.assertEqual(p.save_damage(11,False,self.mode['save']['outcomes']),11)
    def test_success_even_10_is_5(self):
        self.assertEqual(p.save_damage(10,True,self.mode['save']['outcomes']),5)
    def test_success_odd_11_is_5_and_all_3d6_totals(self):
        self.assertEqual(p.save_damage(11,True,self.mode['save']['outcomes']),5)
        for total in range(3,19):
            self.assertEqual(p.save_damage(total,True,self.mode['save']['outcomes']),total//2)
            self.assertEqual(p.save_damage(total,False,self.mode['save']['outcomes']),total)
    def test_grenade_roll_excludes_modifiers(self):
        projection=n.project(self.fixture['draft'],self.records)['projection']
        intent=n.compile_grenade_intent(projection,self.fixture['context'],self.records)
        comp=intent['damageRoll']['components'][0]
        self.assertEqual(comp['groups'],[{'id':'base','count':3,'sides':6}]);self.assertEqual(comp['modifiers'],[])
        self.assertEqual(comp['damageType'],{'id':'di.damage_type.piercing'})
        self.assertEqual(intent['dc'],12);self.assertEqual(intent['saveAttribute'],'dexterity')
        altered=copy.deepcopy(projection);altered['values']['attributeModifiers']['dexterity']=9
        changed=n.compile_grenade_intent(altered,self.fixture['context'],self.records)
        self.assertEqual(changed['damageRoll']['components'],intent['damageRoll']['components'])
        self.assertEqual(changed['dc'],19)
    def test_structured_area_and_consumption(self):
        self.assertEqual(self.mode['area'],{'shape':'sphere','radius':{'value':15,'unit':'ft'}})
        self.assertEqual(self.mode['consumption'],{'resource':'item_quantity','quantity':1,'on':'committed_use'})
        self.assertEqual(self.records['di.weapon.frag_grenade']['data']['abilityBinding']['damage'],'none')
    def test_scope_no_blast_or_other_grenade_default(self):
        original=c.read(c.PACKAGE/'review/human-rulings-integration.json')
        blast=next(x for x in original if x['id']=='PHB-RULE-018')
        self.assertEqual(blast['status'],'UNRESOLVED');self.assertIsNone(blast['decision'])
        for e in self.records.values():
            for mode in e['data'].get('modes',[]):
                if 'outcomes' in mode.get('save',{}):self.assertEqual(e['id'],'di.weapon.frag_grenade')
        for key in ['firebomb','krak_grenade']:
            candidate=c.read(c.PACKAGE/f'review/candidates/weapon/{key}.json')
            self.assertNotIn('outcomes',candidate['proposedData'].get('save',{}))
        with self.assertRaises(c.InvalidContent):p.save_damage(11,True,{})
    def test_malformed_outcomes_rejected(self):
        for change in ['denominator','rounding','missing','script']:
            records=copy.deepcopy(self.records);outcomes=records['di.weapon.frag_grenade']['data']['modes'][0]['save']['outcomes']
            if change=='denominator':outcomes['success']['damageMultiplier']['denominator']=0
            elif change=='rounding':outcomes['success']['rounding']='nearest'
            elif change=='missing':del outcomes['failure']
            else:outcomes['success']['script']='damage/2'
            with self.assertRaises(c.InvalidContent):c.validate_records(records)
        for total,succeeded in [(11.5,True),(-1,True),(True,True),(11,'success')]:
            with self.assertRaises(c.InvalidContent):p.save_damage(total,succeeded,self.mode['save']['outcomes'])
    def test_narrow_gate_and_all_starting_weapon_rolls(self):
        out=n.project(self.fixture['draft'],self.records);proj=out['projection']
        self.assertEqual(out['status'],'VALID');self.assertEqual(out['playability'],'PLAYABLE_WITH_MANUAL_RULES')
        self.assertEqual(proj['readiness'],'READY_WITH_MANUAL_RULES');self.assertEqual(out['dependencyAnalysis']['creationBlockers'],[])
        rolls=n.compile_rolls(proj,self.fixture['context'],self.records,weapon_ids=['di.weapon.lasgun','di.weapon.combat_blade','di.weapon.laspistol'])
        rolls.append(n.compile_grenade_intent(proj,self.fixture['context'],self.records)['damageRoll'])
        self.assertEqual(len(rolls),11);self.assertEqual(len({r['id'] for r in rolls}),11)
        for roll in rolls:n.validate_roll(roll,self.records)
        self.assertEqual(sum(m['value'] for m in rolls[8]['components'][0]['modifiers']),4)
        self.assertEqual(sum(m['value'] for m in rolls[9]['components'][0]['modifiers']),2)
    def test_missing_save_structure_reblocks(self):
        records=copy.deepcopy(self.records);del records['di.weapon.frag_grenade']['data']['modes'][0]['save']['outcomes']
        out=n.project(self.fixture['draft'],records)
        self.assertEqual(out['status'],'INCOMPLETE');self.assertNotIn('playability',out)
        self.assertIn('FRAG_SAVE_STRUCTURE_REQUIRED',{x['code'] for x in out['unresolved']})
    def test_no_runtime_mutation_and_no_sharing_assumption(self):
        draft=copy.deepcopy(self.fixture['draft']);original=copy.deepcopy(draft)
        out=n.project(draft,self.records);intent=n.compile_grenade_intent(out['projection'],self.fixture['context'],self.records)
        self.assertEqual(draft,original);self.assertEqual(intent['multiTargetDamageRollPolicy'],'DEFERRED')
        self.assertIn('runtimeActionTransactions',out['projection']['runtimeDeferred'])
        self.assertEqual(next(i['quantity'] for i in out['projection']['inventory'] if i['definition']['id']=='di.weapon.frag_grenade'),2)
    def test_audit_provenance_and_original_count(self):
        item=c.read(c.PACKAGE/'review/item-rulings.json')[0]
        self.assertEqual(item['id'],'PHB-RULE-059');self.assertEqual(item['status'],'RESOLVED')
        raw=(c.PACKAGE/item['approval']['path']).read_bytes()
        self.assertEqual(item['approval']['sha256'],hashlib.sha256(raw).hexdigest())
        self.assertIn('Frag Grenade only',raw.decode('utf8'));self.assertEqual(item['affectedIds'],['di.weapon.frag_grenade','di.action.frag_grenade.throw'])
        original=c.read(c.PACKAGE/'review/human-rulings-integration.json')
        self.assertEqual(len(original),36);self.assertEqual(sum(x['status']=='UNRESOLVED' for x in original),31)
    def test_missing_grenade_not_authorized_by_definition(self):
        out=n.project(self.fixture['draft'],self.records)
        out['projection']['inventory']=[i for i in out['projection']['inventory'] if i['definition']['id']!='di.weapon.frag_grenade']
        with self.assertRaises(c.InvalidContent):n.compile_grenade_intent(out['projection'],self.fixture['context'],self.records)

if __name__=='__main__':unittest.main()

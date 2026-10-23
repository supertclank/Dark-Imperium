import copy
import hashlib
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
import phb_policies as p
import narrow_character as n

class MinimumRulingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.records=c.load();cls.fixture=c.read(ROOT/'tests/fixtures/narrow/veteran-level-1.json')
    def draft(self):return copy.deepcopy(self.fixture['draft'])
    def test_modifier_odd_even_negative_above_twenty(self):
        for score,expected in [(1,-5),(8,-1),(9,-1),(10,0),(11,0),(15,2),(20,5),(21,5),(22,6),(31,10)]:self.assertEqual(p.ability_modifier(score),expected)
        for bad in [0,-1,10.0,True,'15',None]:
            with self.assertRaises(c.InvalidContent):p.ability_modifier(bad)
    def test_explicit_bounds_only(self):
        self.assertEqual(p.increase_score(20,2),22)
        self.assertEqual(p.increase_score(19,2,maximum=20),20)
        self.assertEqual(p.increase_score(3,-4,minimum=1),1)
        with self.assertRaises(c.InvalidContent):p.increase_score(1,-1)
    def test_weapon_default_and_explicit_binding(self):
        self.assertEqual(p.weapon_ability('melee'),'strength');self.assertEqual(p.weapon_ability('ranged'),'dexterity')
        self.assertEqual(p.weapon_ability('thrown'),'strength')
        self.assertEqual(p.weapon_ability('ranged',override='wisdom'),'wisdom')
    def test_finesse_same_selected_attack_and_damage(self):
        proj=n.project(self.draft(),self.records)['projection'];ctx=copy.deepcopy(self.fixture['context']);ctx['finesseAbility']='dexterity'
        rolls=n.compile_rolls(proj,ctx,self.records)
        for roll in rolls[-2:]:self.assertEqual(next(m['value'] for m in roll['components'][0]['modifiers'] if m['id']=='ability'),2)
        with self.assertRaises(c.InvalidContent):p.weapon_ability('melee',finesse=True)
    def test_spirit_weapon_requires_psychic_binding(self):
        self.assertEqual(p.weapon_ability('melee',spirit=True,selected='psychic',psychic='wisdom'),'wisdom')
        self.assertEqual(p.weapon_ability('melee',spirit=True),'strength')
        with self.assertRaises(c.InvalidContent):p.weapon_ability('melee',spirit=True,selected='psychic')
    def test_hands_reach_force_staff_and_versatile(self):
        for category in ['pistol','melee','shield']:self.assertEqual(p.weapon_hands(category),1)
        for category in ['basic_firearm','shotgun','sniper','heavy']:self.assertEqual(p.weapon_hands(category),2)
        self.assertEqual(p.weapon_hands('melee',heavy=True),2)
        self.assertEqual(p.weapon_hands('melee',override=c.read(c.PACKAGE/'review/weapon-taxonomy.json')['forceStaffHands']),2)
        for hands in [1,2]:self.assertEqual(p.weapon_hands('melee',versatile=True,chosen=hands),hands)
        self.assertEqual(p.weapon_reach('thrown'),5);self.assertEqual(p.weapon_reach('melee'),5);self.assertIsNone(p.weapon_reach('ranged'))
    def test_groups_multigroup_and_specific_package_proficiency(self):
        self.assertTrue(p.weapon_proficient('x',['basic_firearm'],['basic_firearm']))
        self.assertTrue(p.weapon_proficient('x',['aeldari','sniper'],['sniper']))
        self.assertTrue(p.weapon_proficient('x',['aeldari'],starting_weapons=['x']))
        self.assertFalse(p.weapon_proficient('other',['aeldari'],starting_weapons=['x']))
        self.assertFalse(p.weapon_proficient('x',['aeldari'],['pistol']))
    def test_shield_proficiency_and_emplaced_not_proficiency(self):
        shield=self.records['di.shield.shield']['data']
        self.assertTrue(p.weapon_proficient('di.shield.shield',shield['proficiencyGroups'],starting_weapons=['di.shield.shield']))
        self.assertNotIn('emplaced',p.WEAPON_GROUPS)
        with self.assertRaises(c.InvalidContent):p.weapon_proficient('x',['emplaced'],['emplaced'])
    def test_grenade_save_dc_and_no_ability_damage(self):
        mode=self.records['di.weapon.frag_grenade']['data']['modes'][0]
        self.assertEqual(mode['save']['attribute'],'dexterity');self.assertEqual(p.grenade_dc(1,2),12)
        self.assertEqual(mode['damage'][0]['dice'],{'count':3,'sides':6,'bonus':0})
        self.assertEqual(p.save_weapon_damage_bonus(5),0);self.assertEqual(p.save_weapon_damage_bonus(-2),0)
        self.assertEqual(p.save_weapon_damage_bonus(5,explicitly_add=True),5)
        self.assertEqual(mode['save']['outcomes']['success']['damageMultiplier'],{'numerator':1,'denominator':2})
        intent=n.project(self.draft(),self.records)['projection']['grenadeSaveIntent']
        self.assertEqual((intent['dc'],intent['abilityDamageBonus'],intent['area']['radius']['value']),(12,0,15))
    def test_medkit_alias_and_riot_same_profile(self):
        bindings=c.read(c.PACKAGE/'review/starting-reference-bindings.json')['bindings']
        self.assertEqual(bindings['medkit'],{'id':'di.equipment.med_pack'})
        self.assertEqual(bindings['riot shield'],{'id':'di.shield.shield'})
        shield=self.records['di.shield.shield']['data'];self.assertEqual(shield['defence']['value']['value'],2);self.assertEqual(shield['equip']['hands'],1)
        self.assertNotIn('di.equipment.medkit',self.records);self.assertNotIn('di.shield.riot_shield',self.records)
    def test_light_armour_and_minor_augmetic_pools(self):
        options=self.records['di.choice.starting.light_armour']['data']['options']
        self.assertEqual({o['grants'][0]['content']['id'] for o in options},{'di.armour.armoured_bodyglove','di.armour.mesh_armour'})
        options=self.records['di.choice.starting.minor_augmetic']['data']['options'];self.assertEqual(len(options),10)
        for o in options:self.assertEqual(self.records[o['grants'][0]['content']['id']]['data']['availability'],'Controlled')
    def test_narrative_items_contact_and_focus_tags(self):
        bindings=c.read(c.PACKAGE/'review/starting-reference-bindings.json')['bindings']
        self.assertEqual(bindings['black-market contact'],{'kind':'character_contact','inventory':False})
        for key in ['psychic_focus','rune_stones']:self.assertIn('psychic_focus',self.records['di.equipment.'+key]['data']['functionalTags'])
        for key in ['symbol_of_faith','oath_token','spirit_charm']:
            e=self.records['di.equipment.'+key];self.assertEqual(e['data']['features'],[]);self.assertTrue(e['data']['manualRules'])
    def test_projection_exact_values_and_approved_outcome_gate(self):
        out=n.project(self.draft(),self.records);v=out['projection']['values']
        self.assertEqual(v['attributes'],dict(zip(['strength','dexterity','constitution','intelligence','wisdom','charisma'],[17,15,13,12,10,8])))
        self.assertEqual((v['maximumWounds'],v['defence'],v['initiative'],v['proficiencyBonus']),(11,14,4,2))
        self.assertEqual(v['saves']['dexterity']['modifier'],4);self.assertEqual(v['saves']['wisdom']['modifier'],2)
        self.assertEqual(v['skills']['di.skill.athletics']['modifier'],5)
        self.assertEqual(out['errors'],[]);self.assertEqual(out['status'],'VALID')
        self.assertEqual(out['unresolved'],[])
        self.assertEqual(out['playability'],'PLAYABLE_WITH_MANUAL_RULES')
    def test_eight_deterministic_roll_definitions(self):
        proj=n.project(self.draft(),self.records)['projection'];a=n.compile_rolls(proj,self.fixture['context'],self.records);b=n.compile_rolls(proj,self.fixture['context'],self.records)
        self.assertEqual(a,b);self.assertEqual(len(a),8);self.assertEqual(len({r['id'] for r in a}),8)
        self.assertEqual([sum(m['value'] for m in r['components'][0]['modifiers']) for r in a],[3,5,4,4,4,2,5,3])
        for i in [4,6]:
            self.assertEqual(a[i]['action']['executionId'],a[i+1]['action']['executionId']);self.assertNotEqual(a[i]['action']['stageId'],a[i+1]['action']['stageId'])
        self.assertEqual(a[5]['components'][0]['damageType'],{'id':'di.damage_type.radiant'})
        for r in a:n.validate_roll(r,self.records)
    def test_changed_context_changes_roll_identity(self):
        proj=n.project(self.draft(),self.records)['projection'];ctx=copy.deepcopy(self.fixture['context']);ctx['executionNonce']='another'
        self.assertNotEqual(n.compile_rolls(proj,ctx,self.records)[0]['id'],n.compile_rolls(proj,self.fixture['context'],self.records)[0]['id'])
    def test_invalid_and_outside_scope_not_certified(self):
        d=self.draft();d['selections']['background']={'id':'di.background.craftworld_outcast'}
        self.assertEqual(n.project(d,self.records)['status'],'INVALID')
        d=self.draft();d['inventory'][0]['quantity']=0;self.assertEqual(n.project(d,self.records)['status'],'INVALID')
        d=self.draft();d['selections']['classes'][0]['level']=2;self.assertEqual(n.project(d,self.records)['status'],'INCOMPLETE')
    def test_missing_kit_and_specialist_choice_block(self):
        d=self.draft();d['inventory'].pop();self.assertIn('STARTING_PACKAGE_MISMATCH',{x['code'] for x in n.project(d,self.records)['unresolved']})
        d=self.draft();d['selections']['answers']=[a for a in d['selections']['answers'] if a['choice']['id']!='di.choice.veteran.specialist_group'];self.assertIn('CHOICE_REQUIRED',{x['code'] for x in n.project(d,self.records)['unresolved']})
    def test_rulings_provenance_and_31_remain(self):
        rows=c.read(c.PACKAGE/'review/human-rulings-integration.json');self.assertEqual(sum(x['status']=='UNRESOLVED' for x in rows),21)
        sha=hashlib.sha256((c.PACKAGE/'review/approved-minimum-rulings.txt').read_bytes()).hexdigest()
        for x in rows:
            if x['id'] in ['PHB-RULE-009','PHB-RULE-024','PHB-RULE-049','PHB-RULE-050','PHB-RULE-051']:self.assertEqual(x['approval']['sha256'],sha)
    def test_promotions_remove_candidate_duplicates_retain_evidence(self):
        ledger=c.read(c.PACKAGE/'review/minimum-rulings-promotions.json')
        for id in ledger['promoted']:
            self.assertIn(id,self.records);path=Path(id.split('.')[1])/(id.split('.',2)[2]+'.json')
            self.assertFalse((c.PACKAGE/'review/candidates'/path).exists());self.assertTrue((c.PACKAGE/'review/promoted-evidence'/path).exists())
    def test_unknown_groups_and_missing_damage_type_rejected(self):
        records=copy.deepcopy(self.records);records['di.weapon.lasgun']['data']['proficiencyGroups']=['emplaced']
        with self.assertRaises(c.InvalidContent):c.validate_records(records)
        proj=n.project(self.draft(),self.records)['projection'];roll=n.compile_rolls(proj,self.fixture['context'],self.records)[5];del roll['components'][0]['damageType']
        with self.assertRaises(c.InvalidContent):n.validate_roll(roll,self.records)

if __name__=='__main__':unittest.main()

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import content_import as ci
import phb_policies as pp

class CanonicalisationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.records=ci.load()
        cls.triage=ci.read(ci.PACKAGE/'review/candidate-triage.json')

    def test_all_original_candidates_have_exactly_one_disposition(self):
        self.assertEqual(len(self.triage),385)
        self.assertEqual(len({x['id'] for x in self.triage}),385)
        for x in self.triage:
            if x['category'] in ['AUTO_COMPLETABLE','HUMAN_RULING_PROMOTED','SOURCE_REVIEW_PROMOTED']:self.assertIn(x['id'],self.records)
            else:self.assertNotIn(x['id'],self.records)
        self.assertEqual(sum(x['category']=='AUTO_COMPLETABLE' for x in self.triage),52)

    def test_global_identity_reference_and_source_closure(self):
        ids=ci.read(ROOT/'content/CONTENT_MANIFEST.json')['identities']
        self.assertEqual(len(ids),len({x['id'] for x in ids}))
        pending={ci.read(f)['proposedId'] for f in (ci.PACKAGE/'review/candidates').rglob('*.json')}
        self.assertFalse(pending & self.records.keys())
        self.assertEqual({x['id'] for x in ids},pending|self.records.keys())
        ci.validate_records(self.records) # recursively validates typed refs/action/feature/progression/damage bindings
        ci.validate_candidates(ci.PACKAGE,self.records)

    def test_all_45_subclass_level_skeletons(self):
        subs=[e for e in self.records.values() if e['kind']=='subclass']
        self.assertEqual(len(subs),45)
        for sub in subs:
            parent=sub['data']['parentClass']['id']
            expected=([1,3,7,14] if parent=='di.class.psyker' else
                      [3,7,14] if parent in ['di.class.veteran','di.class.hive_scum'] else [3,7,14,18])
            prog=self.records[sub['data']['progression']['id']]['data']
            self.assertEqual([r['level'] for r in prog['entries']],expected,sub['id'])
            self.assertIn({'id':sub['id']},self.records[parent]['data']['allowedSubclasses'])
            for row in prog['entries']:
                self.assertEqual(len(row['grants']),1)
                self.assertIn(row['grants'][0]['feature']['id'],self.records)

    def test_parent_grants_do_not_double_subclass_features(self):
        for e in self.records.values():
            if e['kind']!='class':continue
            sublevels={r['level'] for sub in e['data']['allowedSubclasses'] for r in self.records[self.records[sub['id']]['data']['progression']['id']]['data']['entries']}
            rows=self.records[e['data']['progression']['id']]['data']['entries']
            for row in rows:
                if row['level'] not in sublevels:continue
                for grant in row['grants']:
                    self.assertTrue(grant['kind']=='choice' or (e['id']=='di.class.psyker' and row['level']==1 and 'warp_pressure' in grant.get('feature',{}).get('id','')))

    def test_split_warlock_rows_survive_extraction(self):
        checks=[('spirit_guardian',7,'temporary HP'),('storm_warlock',14,'+1d8'),('spirit_guardian',14,'advantage')]
        for key,level,phrase in checks:
            self.assertIn(phrase,self.records[f'di.feature.subclass.aeldari_warlock.{key}.level_{level}']['descriptionMarkdown'])
        tables=ci.read(ci.PACKAGE/'evidence/tables.json')
        aligned=[t for t in tables if t['pdfPage']==84 and abs(t['top']-46.8)<.11]
        self.assertEqual(len(aligned),2)
        self.assertNotEqual(aligned[0]['x0'],aligned[1]['x0'])

    def test_talent_and_trait_species_prerequisites(self):
        feats=[e for e in self.records.values() if e['id'].startswith('di.feature.talent.') and 'requirements' in e['data']]
        self.assertEqual(len(feats),30)
        witch=self.records['di.feature.talent.witch_sight']['data']['requirements']
        self.assertFalse(pp.evaluate(witch,{'selected':['di.species.human']}))
        self.assertTrue(pp.evaluate(witch,{'selected':['di.species.human','di.class.psyker']}))
        hive=self.records['di.feature.talent.hive_blooded']['data']['requirements']
        self.assertTrue(pp.evaluate(hive,{'selected':['di.species.ratling']}))
        touched=self.records['di.feature.universal.touched_by_the_warp']['data']['requirements']
        self.assertFalse(pp.evaluate(touched,{'selected':['di.species.skitarii']}))

    def test_origin_conflicts_fail_closed(self):
        clean=self.records['di.background.schola_progenium']['data']['requirements']
        self.assertTrue(pp.evaluate(clean,{'selected':['di.species.human']}))
        self.assertFalse(pp.evaluate(clean,{'selected':['di.species.kin']}))
        conflict=self.records['di.background.voidborn']['data']['requirements']
        self.assertTrue(pp.evaluate(conflict,{'selected':['di.species.human']}));self.assertFalse(pp.evaluate(conflict,{'selected':['di.species.kin']}))

    def test_class_species_restrictions(self):
        for cls,allowed,denied in [('ogryn_skullbreaker','ogryn','human'),('skitarii_veteran','skitarii','human'),('psyker','human','skitarii'),('aeldari_warlock','aeldari','human')]:
            req=self.records['di.class.'+cls]['data']['requirements']
            self.assertTrue(pp.evaluate(req,{'selected':['di.species.'+allowed]}))
            self.assertFalse(pp.evaluate(req,{'selected':['di.species.'+denied]}))

    def test_three_valued_nested_logic_and_negation(self):
        known={'kind':'selected','content':{'id':'di.species.human'}}
        unknown={'kind':'stat','key':'attribute.strength.score','operator':'gte','value':15}
        self.assertIsNone(pp.evaluate({'kind':'all','predicates':[known,unknown]},{'selected':['di.species.human']}))
        self.assertFalse(pp.evaluate({'kind':'all','predicates':[known,unknown]},{'selected':[]}))
        self.assertTrue(pp.evaluate({'kind':'any','predicates':[known,unknown]},{'selected':['di.species.human']}))
        self.assertIsNone(pp.evaluate({'kind':'not','predicate':unknown},{}))

    def test_min_max_level_and_pregrant_attributes(self):
        p={'kind':'all','predicates':[{'kind':'level','axis':{'kind':'total_level'},'operator':'gte','value':3},{'kind':'level','axis':{'kind':'total_level'},'operator':'lte','value':7}]}
        ci.predicate(p,self.records)
        self.assertFalse(pp.evaluate(p,{'totalLevel':2}));self.assertTrue(pp.evaluate(p,{'totalLevel':7}));self.assertFalse(pp.evaluate(p,{'totalLevel':8}))
        p={'kind':'stat','key':'attribute.strength.score','operator':'gte','value':15}
        self.assertFalse(pp.evaluate(p,{'stats':{'attribute.strength.score':14}}))

    def test_predicate_validation_rejects_bad_refs_keys_and_budget(self):
        for p in [{'kind':'proficient','proficiency':{'id':'di.species.human'}},{'kind':'fact','key':'phb.unregistered','equals':True},{'kind':'selected','content':{'id':'di.feature.missing'}},{'kind':'stat','key':'eval(script)','operator':'gte','value':1},{'kind':'all','predicates':[{'kind':'selected','content':{'id':'di.species.human'}}]*100}]:
            with self.assertRaises(ci.InvalidContent):ci.predicate(p,self.records)

    def test_conditional_shield_effect(self):
        e=self.records['di.feature.subclass.arbites_enforcer.riot_shield.level_3']['data']
        self.assertEqual(e['effects'][0]['value']['value'],1)
        p=e['effects'][0]['when']
        self.assertIsNone(pp.evaluate(p,{}))
        self.assertFalse(pp.evaluate(p,{'equipped':[]}))
        self.assertTrue(pp.evaluate(p,{'equipped':[{'kind':'shield'}]}))
        self.assertNotIn('+1 AC',e['manualRules'][0]['text'])

    def test_bloodied_is_not_below_half(self):
        p={'kind':'health_ratio','scope':'self','operator':'lte','numerator':1,'denominator':2}
        ctx={'health':{'self':{'current':5,'maximum':10}}}
        self.assertTrue(pp.evaluate(p,ctx));p['operator']='lt';self.assertFalse(pp.evaluate(p,ctx))
        self.assertIsNone(pp.evaluate(p,{'health':{'self':{'current':0,'maximum':0}}}))
        self.assertNotIn('di.condition.bloodied',self.records)

    def test_proficiency_boundaries_and_once_only(self):
        self.assertEqual([pp.proficiency(x) for x in [1,4,5,8,9,12,13,16,17,20]],[2,2,3,3,4,4,5,5,6,6])
        self.assertEqual(pp.check_modifier(3,5,True),6)
        self.assertEqual(pp.check_modifier(3,5,False),3)
        with self.assertRaises(ci.InvalidContent):pp.proficiency(21)

    def test_hp_source_fixed_and_rolled_values(self):
        self.assertEqual(pp.hp_gain(10,2,first=True),12)
        self.assertEqual([pp.hp_gain(d,2) for d in (6,8,10,12)],[6,7,8,9])
        self.assertEqual(pp.hp_gain(8,1,roll=3),4)
        with self.assertRaises(ci.InvalidContent):pp.hp_gain(8,1,roll=9)

    def test_armour_cap_does_not_erase_negative_dex(self):
        self.assertEqual(pp.armour_ac(13,4,2),15)
        self.assertEqual(pp.armour_ac(13,-1,2),12)
        self.assertEqual(pp.armour_ac(11,4),15)

    def test_fixed_ogryn_plate_promoted_without_dexterity_assumption(self):
        e=self.records['di.armour.ogryn_plate']
        self.assertEqual(e['data']['defence']['value'],{'kind':'constant','value':16})
        self.assertEqual(e['sources'][0]['locator']['pdfPage'],42)
        self.assertFalse((ci.PACKAGE/'review/candidates/armour/ogryn_plate.json').exists())

    def test_advantage_stacking(self):
        self.assertEqual(pp.advantage(True,False),'advantage')
        self.assertEqual(pp.advantage(True,True),'normal')
        self.assertEqual(pp.advantage(False,True),'disadvantage')
        with self.assertRaises(ci.InvalidContent):pp.advantage(None,False)

    def test_critical_preserves_flat_modifiers_and_types(self):
        c=[{'id':'a','dice':{'count':1,'sides':10,'bonus':0},'bonus':{'kind':'constant','value':3},'damageType':{'id':'di.damage_type.piercing'}},{'id':'b','dice':{'count':1,'sides':4,'bonus':0},'bonus':{'kind':'constant','value':0},'damageType':{'id':'di.damage_type.thunder'}}]
        out=pp.critical_dice(c)
        self.assertEqual([x['dice']['count'] for x in out],[2,2])
        self.assertEqual(out[0]['bonus']['value'],3);self.assertEqual(out[1]['damageType'],c[1]['damageType'])
        self.assertEqual(c[0]['dice']['count'],1)

    def test_damage_threshold_whole_hit_and_boundary(self):
        self.assertEqual(pp.hull_damage([8,5],10),13)
        self.assertEqual(pp.hull_damage([9],10),0)
        self.assertEqual(pp.hull_damage([10],10),10)
        self.assertEqual(pp.hull_damage([5],11,True),5)
        self.assertEqual(pp.hull_damage([4],11,True),0)

    def test_psychic_pressure_and_open_ended_perils(self):
        self.assertEqual(pp.pressure_after_power(5,'standard'),7)
        self.assertEqual(pp.pressure_after_power(0,'major',True),4)
        self.assertTrue(pp.perils_trigger(7,7));self.assertFalse(pp.perils_trigger(8,7))
        self.assertTrue(pp.perils_trigger(20,21))
        self.assertEqual(pp.severity_band(1,30),'catastrophic_perils')
        self.assertEqual(pp.severity_band(6,1),'bleeding_eyes')

    def test_unresolved_calculations_do_not_inherit_other_games(self):
        self.assertEqual(pp.ability_modifier(9),-1)
        for name in ['resistance','expertise','asi','post_perils_rounding']:
            with self.assertRaisesRegex(ci.InvalidContent,'HUMAN_RULING_REQUIRED'):pp.unsupported(name)

    def test_dependency_graph_rejects_cycles(self):
        self.assertEqual(pp.topological_order({'attack':['modifier','pb'],'modifier':['score'],'score':[],'pb':[]}),['score','modifier','pb','attack'])
        with self.assertRaisesRegex(ci.InvalidContent,'CALCULATION_CYCLE'):pp.topological_order({'a':['b'],'b':['a']})

    def test_damage_types_and_template_readiness(self):
        self.assertEqual(len([e for e in self.records.values() if e['kind']=='damage_type']),13)
        self.assertIn('di.damage_type.acid',self.records)
        for invalid in ['energy','physical','plasma','melta','bolt']:self.assertNotIn('di.damage_type.'+invalid,self.records)
        for key,damage in [('lasgun','radiant'),('warp_spark','force')]:
            roll=self.records[f'di.action.{key}.base_damage']['data']['rolls'][0]
            self.assertEqual(roll['damageBindings'][0]['damageType']['id'],'di.damage_type.'+damage)
            self.assertNotIn('snapshot',roll) # explicitly not an actor-resolved RollDefinition

    def test_bad_damage_binding_and_duplicate_effect_rejected(self):
        for mutation in ['kind','group','duplicate']:
            records=copy.deepcopy(self.records)
            b=records['di.action.lasgun.base_damage']['data']['rolls'][0]['damageBindings'][0]
            if mutation=='kind':b['damageType']['id']='di.species.human'
            elif mutation=='group':b['groupId']='missing'
            else:
                e=records['di.feature.subclass.arbites_enforcer.riot_shield.level_3']['data']['effects'];e.append(copy.deepcopy(e[0]))
            with self.assertRaises(ci.InvalidContent):ci.validate_records(records)

    def test_starting_equipment_and_class_training_evidence(self):
        rows=ci.read(ci.PACKAGE/'review/class-calculation-inputs.json')
        self.assertEqual(len(rows),12)
        self.assertEqual(next(x for x in rows if x['class']['id']=='di.class.psyker')['hitDie'],6)
        self.assertTrue(all(x['savingThrows'] for x in rows))
        self.assertNotIn('di.equipment.medkit',self.records)
        self.assertNotIn('di.shield.riot_shield',self.records)

    def test_resolution_and_coverage_ledgers_are_complete(self):
        issues=ci.read(ci.PACKAGE/'review/rules-resolution.json')
        self.assertEqual({x['group'] for x in issues},{f'PHB-{n:03}' for n in range(1,17)})
        self.assertEqual(len({x['id'] for x in issues}),len(issues))
        self.assertEqual(set(ci.read(ci.PACKAGE/'review/canonical-coverage.json')),set(self.records))
        self.assertEqual(len(ci.read(ci.PACKAGE/'review/calculation-policies.json')),30)
        with self.assertRaises(ci.InvalidContent):ci.publication_gate(self.manifest,self.records)

if __name__=='__main__':unittest.main()

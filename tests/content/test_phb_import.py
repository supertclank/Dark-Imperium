import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import content_import as ci

class PHBImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.records=ci.load()
        cls.candidates={c['proposedId']:c for f in (ci.PACKAGE/'review/candidates').rglob('*.json') for c in [ci.read(f)]}
        cls.tables=ci.read(ci.PACKAGE/'evidence/tables.json')

    def test_source_integrity_and_page_identity(self):
        source=ci.read(ci.PACKAGE/'sources.json')['sources'][0]
        self.assertEqual(hashlib.sha256((ROOT/source['repositoryFile']).read_bytes()).hexdigest(),source['fileSha256'])
        self.assertEqual(source['pdfPages'],125)
        self.assertEqual(source['editionLabel'],'Version 1.0')

    def test_species_baselines(self):
        species=[e for e in self.records.values() if e['kind']=='species']
        self.assertEqual(len(species),6)
        for key,speed in [('human',30),('ogryn',30),('ratling',25),('skitarii',30),('kin',25),('aeldari',35)]:
            e=self.records['di.feature.species.'+key+'.baseline']
            self.assertEqual(e['data']['effects'][0]['value']['value'],speed)
        choice=self.records['di.choice.human.ability_scores']['data']
        self.assertEqual(len(choice['options']),30)
        for option in choice['options']:
            self.assertEqual(sum(g['amount'] for g in option['grants']),3)
            self.assertEqual(len({g['attributeKey'] for g in option['grants']}),2)

    def test_origin_skill_choices(self):
        self.assertEqual(len([e for e in self.records.values() if e['kind']=='background']),10)
        self.assertEqual(self.records['di.choice.underhive.skills']['data']['cardinality']['min'],2)
        self.assertEqual(len(self.records['di.choice.underhive.skills']['data']['options']),5)

    def test_all_class_level_tables(self):
        classes=[e for e in self.records.values() if e['kind']=='class']
        self.assertEqual(len(classes),12)
        for e in classes:
            progression=self.records[e['data']['progression']['id']]['data']
            self.assertEqual([x['level'] for x in progression['entries']],list(range(1,21)))
        row=self.records['di.progression.veteran']['data']['entries'][4]
        self.assertEqual(row['grants'][0]['feature']['id'],'di.feature.class.veteran.level_5.extra_attack')

    def test_subclass_relationship_and_no_duplicate_doctrine(self):
        e=self.records['di.subclass.veteran.shock_trooper']
        self.assertEqual(e['data']['parentClass']['id'],'di.class.veteran')
        rows=self.records[e['data']['progression']['id']]['data']['entries']
        self.assertEqual([x['level'] for x in rows],[3,7,14])
        class_rows=self.records['di.progression.veteran']['data']['entries']
        self.assertEqual(class_rows[6]['grants'],[])
        self.assertEqual(class_rows[13]['grants'],[])

    def test_starting_equipment_evidence_not_invented_choice(self):
        t=next(t for t in self.tables if t['rows'][0]==['Class','Starting Equipment'])
        self.assertEqual(len(t['rows'])-1,12)
        veteran=next(r[1] for r in t['rows'][1:] if r[0]=='Veteran')
        self.assertIn('Lasgun or autogun',veteran)
        self.assertIn('medkit or auspex',veteran)
        # Equipment names with unresolved stat entries are not silently minted as valid item grants.
        self.assertNotIn('di.equipment.medkit',self.records)

    def test_promoted_weapon_preserves_damage_range_and_approved_hands(self):
        w=self.records['di.weapon.lasgun']['data']
        self.assertEqual(w['modes'][0]['damage'][0]['dice'],{'count':1,'sides':8,'bonus':0})
        self.assertEqual(w['modes'][0]['damage'][0]['damageType']['id'],'di.damage_type.radiant')
        self.assertEqual(w['modes'][0]['range']['normal'],{'value':80,'unit':'ft'})
        self.assertEqual(w['hands'],2)
        self.assertNotIn('di.weapon.lasgun',self.candidates)
        self.assertEqual(self.candidates['di.weapon.plasma_gun']['status'],'AMBIGUOUS')

    def test_armour_and_shield(self):
        self.assertEqual(self.records['di.armour.ogryn_leathers']['data']['defence']['value']['value'],12)
        shield=self.records['di.shield.shield']['data']
        self.assertEqual(shield['defence']['mode'],'add')
        self.assertEqual(shield['equip']['hands'],1)

    def test_weapon_properties(self):
        self.assertEqual(len([e for e in self.records.values() if e['kind']=='property']),31)
        self.assertEqual(self.records['di.property.weapon.reload']['data']['parameters'][0]['name'],'capacity')
        self.assertIn('natural 1',self.records['di.property.weapon.overheat']['descriptionMarkdown'])

    def test_feat_and_conditional_manual_feature(self):
        feats=[e for e in self.records.values() if e['kind']=='feature' and e['data']['flavor']=='feat']
        self.assertEqual(len(feats),50)
        conditional=self.records['di.feature.talent.armour_familiarity']['data']
        self.assertEqual(conditional['effects'],[])
        self.assertIn('While wearing armour',conditional['manualRules'][0]['text'])
        self.assertEqual(conditional['manualRules'][0]['automation'],'manual')
        automatic=self.records['di.feature.universal.twitchy']['data']
        self.assertEqual(automatic['effects'][0]['value']['value'],2)
        self.assertEqual(automatic['manualRules'],[])

    def test_psychic_and_vehicle_candidates_preserve_evidence(self):
        self.assertEqual(len([c for c in self.candidates.values() if c['kind']=='power']),52)
        self.assertIn('1d8 force',self.candidates['di.power.warp_spark']['evidence'][0]['text'])
        vehicle=self.candidates['di.vehicle.civilian_autocar']
        self.assertEqual(vehicle['proposedData']['hull']['value'],35)
        self.assertIn('DT 0',vehicle['evidence'][0]['text'])
        self.assertEqual(len([c for c in self.candidates.values() if c['kind']=='vehicle']),12)

    def test_action_base_roll_template(self):
        action=self.records['di.action.lasgun.base_damage']['data']
        self.assertEqual(action['economy'],'manual')
        self.assertEqual(action['rolls'][0]['groups'],[{'id':'base','count':1,'sides':8}])
        self.assertEqual(action['rolls'][0]['modifiers'],[])
        # A RollTemplate is not a fabricated actor-resolved RollDefinition.
        self.assertNotIn('actor',action['rolls'][0])

    def test_identity_registry_and_manifest_closure(self):
        registry=ci.read(ROOT/'content/CONTENT_MANIFEST.json')['identities']
        ids=[x['id'] for x in registry]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),set(self.records)|set(self.candidates))

    def test_deterministic_plan_and_identical_reimport(self):
        a=ci.plan(self.records);b=ci.plan(dict(reversed(list(self.records.items()))))
        self.assertEqual(ci.canonical(a),ci.canonical(b))
        existing={(x['id'],x['revision']):x['sha256'] for x in a}
        self.assertTrue(all(x['operation']=='no_op' for x in ci.plan(self.records,existing)))
        existing[next(iter(existing))]='0'*64
        with self.assertRaisesRegex(ci.InvalidContent,'IMMUTABLE_REVISION_CONFLICT'):ci.plan(self.records,existing)

    def test_bad_reference_dice_cardinality_and_unknown_field_rejected(self):
        for change in ['reference','dice','choice','field']:
            r=copy.deepcopy(self.records)
            if change=='reference':r['di.species.human']['data']['features'][0]['id']='di.feature.missing'
            elif change=='dice':r['di.action.lasgun.base_damage']['data']['rolls'][0]['groups'][0]['count']=0
            elif change=='choice':r['di.choice.underhive.skills']['data']['cardinality']['min']=6
            else:r['di.species.human']['data']['script']='eval(1)'
            with self.subTest(change=change),self.assertRaises(ci.InvalidContent):ci.validate_records(r)

    def test_bad_progression_parent_and_duplicate_json_rejected(self):
        r=copy.deepcopy(self.records)
        r['di.subclass.veteran.shock_trooper']['data']['parentClass']['id']='di.class.psyker'
        with self.assertRaises(ci.InvalidContent):ci.validate_records(r)
        with self.assertRaises(ci.InvalidContent):json.loads('{"id":1,"id":2}',object_pairs_hook=ci.pairs)

    def test_publication_fails_closed(self):
        with self.assertRaisesRegex(ci.InvalidContent,'PUBLICATION_BLOCKED_DRAFT'):
            ci.publication_gate(self.manifest,self.records)

if __name__=='__main__':unittest.main()

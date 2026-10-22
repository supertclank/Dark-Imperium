"""Production adapter checks; existing offline proof tests retain their engine identity."""
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import content_import as c
import export_narrow_profile as export
import narrow_character as narrow

class ProductionProfileTests(unittest.TestCase):
    def test_export_matches_immutable_snapshot(self):
        expected=export.build()
        actual=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json')
        self.assertEqual(expected,actual)
        fixture=c.read(c.ROOT/'frontend/tests/fixtures/profile.json')
        self.assertEqual(actual['digest'],fixture['digest'])
        self.assertNotIn('records',fixture)

    def test_production_wire_roll_definitions_conform(self):
        _,records=c.load()
        sheet=c.read(c.ROOT/'frontend/tests/fixtures/character.json')
        rolls=sheet['calculated']['rollDefinitions']
        self.assertEqual(35,len(rolls))
        self.assertEqual(35,len({r['id'] for r in rolls}))
        for roll in rolls:
            narrow.validate_roll(roll,records,engine_version='narrow-kotlin-v1')
            self.assertEqual(sheet['rulesetDigest'],roll['snapshot']['rulesetLockDigest'])
        self.assertEqual('DISPLAY_ONLY_NOT_AUTHORIZATION',sheet['calculated']['rollAuthority'])

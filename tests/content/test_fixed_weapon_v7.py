import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import export_tier1_v7_profile as export
import content_import as c
from phb_policies import fixed_weapon_ability
class FixedWeaponTests(unittest.TestCase):
 def test_release_reproduces_without_catalogue_expansion(self):
  actual=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v7.json')
  self.assertEqual(export.build(),actual)
  old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v6.json')
  self.assertEqual(old['payload']['spec']['certifiedPaths'],actual['payload']['spec']['certifiedPaths'])
  self.assertEqual(set(old['payload']['records']),set(actual['payload']['records']))
  self.assertEqual('fc78eebe9eab846b96aecf4823f88185e6d9818a1cde59bf255368be37db7769',old['digest'])
 def test_fixed_bindings(self):
  self.assertEqual('dexterity',fixed_weapon_ability('melee',finesse=True))
  self.assertEqual('strength',fixed_weapon_ability('melee'))
  self.assertEqual('dexterity',fixed_weapon_ability('ranged'))
  self.assertEqual('intelligence',fixed_weapon_ability('melee',override='intelligence'))
  self.assertEqual('dexterity',fixed_weapon_ability('thrown',normal_ability='dexterity'))
  self.assertIsNone(fixed_weapon_ability('ranged',save_based=True))
 def test_approval_provenance_is_hash_verified(self):
  import hashlib
  approval=c.read(c.PACKAGE/'review/weapon-ability-amendments.json')[0]
  for path,sha in [('approvalPath','approvalSha256'),('priorApprovalPath','priorApprovalSha256')]:
   self.assertEqual(approval[sha],hashlib.sha256((c.PACKAGE/approval[path]).read_bytes()).hexdigest())

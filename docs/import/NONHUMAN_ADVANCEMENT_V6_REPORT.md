# Non-Human advancement through level 4 and Ratling Sharpshooter

Release `di-phb-1.0-tier1-v6` materially expands all eight requested martial class contexts through level 4, with selected subclass and Talent restrictions. There are **220 certified READY_WITH_MANUAL_RULES family rows**, up from 88. No transition is counted as a family. New creation starts at level 1; existing non-Human v4 characters must explicitly approve a compatibility-checked upgrade during 1 → 2 advancement.

## Completion report

1. **Ratling Veteran:** levels 2–4 certified across five NORMAL Origins: Hiveborn, Penal Worlder, Voidborn, Militarum Regiment and Underhive. Existing Veteran training, fixed HP, Species effects, inventory and actions compose. Suppressing Fire remains explicitly unavailable under PHB-RULE-022.
2. **Ratling Hive Scum:** levels 2–4 certified in those five Origins through Gunslinger. Cunning Action and reload timing remain manual. Knife Rat awaits an authoritative conditional critical-threshold contract; Chem-User lacks a save DC and depends on unresolved exhaustion; Sump Ghost requires PHB-RULE-011 Expertise.
3. **Sharpshooter level 1:** certified in all five NORMAL Ratling Origins. Saving throws are Dexterity/Wisdom; hit die d8. Structured weapon groups are pistol, shotgun and sniper, with individual Knife, Lasgun and Long-las grants. Tool training requires exactly one canonical Cook’s Utensils/Thieves’ Tools choice. The PHB grants no additional class skills at this level; no skills were invented. The supported armour profiles have explicit proficiency records; the broader light-armour training label remains displayed as procedural training.
4. **Sharpshooter level 2:** Scamper certified as MANUAL: bonus-action Dash/Disengage/Hide and movement through larger allies are contextual permissions, not baseline numeric bonuses.
5. **Sharpshooter subclasses:** Long-Las Sniper and Spotter are MANUAL; Black-Market Gremlin is PARTIAL with an executable Thieves’ Tools proficiency grant and manual contraband access. Underhive Rat stays BLOCKED_BY_RULING, PHB-RULE-011. No conditional hit bonus is injected into ordinary rolls.
6. **Sharpshooter level 4:** all three certified subclasses support ASI or individually eligible Talents through the existing engine. Every starting-package combination and both independent training-tool alternatives pass backend validation.
7. **Ogryn levels 2–4:** certified in Penal Worlder and Militarum Regiment. Brutal Impact is manual: once-per-turn melee-hit trigger, Strength save DC 8 + proficiency + Strength modifier, 10-ft push. It does not alter baseline attack damage or invent condition/stacking rules. Big Lad applies after Species adjustments, floors Dexterity at 6, then ASI applies. Massive Build adds 3 HP per level exactly once; retroactive Constitution is applied to class HP separately.
8. **Ogryn Roles:** Bone ’ead, Brute, Bulwark and Gun Lugger certified. Bone ’ead requires a skill selection encoded in its subclass option and calculates Wisdom-save proficiency. Other benefits remain conditional/manual. Bulwark grants no free shield; its benefit applies only when the required equipment context exists. Ogryn Flak Plate remains blocked under PHB-RULE-030; owned Ogryn Plate remains legal.
9. **Skitarii levels 2–4:** certified in Forge World. Augmetic Reflexes adds the current Intelligence modifier to initiative from level 2. No Psychic Potential remains enforced.
10. **Skitarii subclasses:** Infiltrator, Protector, Ranger and Vanguard certified. Infiltrator grants Stealth and a one-use short-rest manual resource. Data Hunter remains blocked by Expertise (011). Ruststalker remains content-blocked because mandatory blades proficiency lacks a certified complete domain; its equipment ownership is not a substitute.
11. **Kin Armsman levels 2–4:** certified in Mining Hold/Guild. Steady Advance is manual; conditional half-speed AC does not enter baseline AC. Kin ability adjustments, 60-ft darkvision, existing Guild-Craft skill branches and training remain intact.
12. **Kin subclasses:** Guild-Militant, Hearthguard and Ironhead certified with source-specific conditional/manual effects. Armour-dependent incoming reduction and ally bonuses are not globally applied.
13. **Hernkyn levels 2–4:** certified in Mining Hold/Guild using the already executable non-Vehicles training alternatives. Surveyor’s Step is manual. The optional Vehicles branch remains unavailable; it is not a mandatory dependency for those selected skill branches. Magna-rail remains GM_APPROVAL_REQUIRED and unavailable to self-service selection.
14. **Hernkyn subclasses:** Outrider and Trail Gunner certified. Outrider’s unconditional +5-ft speed is calculated; its Dash interaction is manual. Trail Gunner’s contextual damage remains manual. Claim-Staker remains blocked by Expertise (011).
15. **Aeldari Outcast levels 2–4:** certified in Craftworld Outcast. Ghostwalk remains manual. Dexterity +2, selected Intelligence/Wisdom +1, 35-ft baseline movement, 90-ft darkvision and the approved duplicate-Perception +1 policy remain intact. No duplicate proficiency becomes Expertise.
16. **Aeldari subclasses:** Ranger certified with its conditional Long Rifle modifier kept out of baseline rolls. Shadow Guide remains blocked by Expertise (011). Corsair remains content-blocked until the mandatory blades proficiency domain is certified; Ranger is unaffected.
17. **Talents:** 40 distinct Talent alternatives are in the v6 catalogue, filtered on the server by canonical structured Species/class predicates. This adds 22 individually reviewed Species-specific alternatives to v5. Kin Weapon Master calculates standalone +1 damage for Kin-group weapons; Aeldari Grace calculates +5-ft movement for qualifying equipped armour; Hold-Born Engineer exposes only its explicit Technology branch and keeps the engineering-tool branch unavailable. Other new effects are manual with source-defined limited-use resources where applicable. Talent ownership remains non-repeatable. See the [50-Talent audit](NONHUMAN_V6_TALENT_READINESS.md) and the new-alternatives appendix below.
18. **Promoted equipment/tools:** v6 contains canonical Long-las, its attack action and generated authoritative attack/damage RollDefinitions; Heavy Clothing; Cook’s Utensils and Thieves’ Tools items and proficiencies; and a required tool-training choice. The starting package is Long-las/Lasgun, Stub Pistol/Laspistol, Knife, Heavy Clothing/Flak Armour, Camo Cloak, and Cook’s Utensils/Thieves’ Tools, one each. Armour is equipped; other items are carried. Training and equipment tool choices are independent source choices. Long-las is 1d10 radiant, 150/600 ft, two hands, Accurate and Reload 10; conditional Accurate/reload handling stays manual. Heavy Clothing is AC 11 + uncapped Dexterity, distinct from Flak Armour. Camo Cloak stays manual without an invented bonus. These mappings are canonical in the immutable v6 overlay; original review candidate bytes and historical package snapshots are retained.
19. **Profile:** `di-phb-1.0-tier1-v6`, adapter `phb-tier1-kotlin-v1`. Digest: `fc78eebe9eab846b96aecf4823f88185e6d9818a1cde59bf255368be37db7769`.
20. **Upgrade contract:** `nonhuman-v4-v6-1` checks the exact v4 digest, explicit non-Human Species/class allowlists, source level 1, destination level 2 and certified configuration. It compares existing selections/calculations, subclass, features, actions, inventory and resource maxima before any write. Consent is required. The shared transaction preserves current HP, equipped/consumed inventory, resources, conditions, temporary effects and roll history; new resources initialise full. Idempotency, state-version conflicts and rollback are retained. Human v4→v5 remains the existing contract; v5 characters are not forced onto v6.
21. **Matrix:** the existing 4,140 level-1–3 slots were regenerated into `nonhuman-v6-publication-matrix.json`. Counts are shown below. There are 143 published tuples in those slots, plus a separate 77-family level-4 appendix, giving 220 total. This preserves the original matrix denominator rather than counting advancement transitions. All original 88 v5 family tuples remain included; 132 additional tuples are certified.
22. **Content tests:** 152 pass, preserving all 146 previous tests. New coverage validates reproducibility, dependency closure per published tuple, explicit upgrade scope, training/equipment and local subclass/ruling gates.
23. **Backend tests:** 97 pass, preserving all 88 previous tests. All 220 tuples and every eligible ASI/Talent option execute. Tests cover Ogryn floors/HP, Skitarii initiative, Hernkyn movement, all 16 Sharpshooter kit combinations × both training-tool choices, invalid choices, eight-class sequential upgrades, injuries, spent Frag Grenades/Frag Bombs, resources, conditions, temporary effects, original roll history, idempotency, stale state and rollback. Existing unknown runtime conditions still block authoritative baseline rolls; advancement preserves them rather than silently clearing them.
24. **Frontend tests:** 72 pass, preserving all 69 previous tests; TypeScript passes. Additional regressions cover level-two upgrade consent, creation-only level choices and excluding unearned future subclass prose from sheets. The generic subclass presentation displays granted features, with no class-specific React descriptions or formula calculations.
25. **Browser acceptance:** all eight representative class contexts were opened at level 1, advanced sequentially to 2, selected a subclass at 3, selected an ASI/Talent at 4, reloaded, verified pinned v6/current HP and executed an authoritative roll with stored-result 3D replay. A separate Sharpshooter was created entirely through the browser wizard. This is actual browser evidence, not an inference from tests. The inspected browser console had no errors/warnings. Character IDs, saved values and roll results are in `NONHUMAN_V6_BROWSER_EVIDENCE.json`.
26. **Backwards compatibility:** representative narrow-v1, tier1-v1, v2, v3, v4 and v5 characters were reopened in the browser and retained their profile labels. Historical snapshot files are unchanged. New creation begins at level 1 on v6; sequential advancement does not offer level-down, respec or level 5.
27. **Production build:** backend installDist succeeds. Frontend compilation, TypeScript and all eight static pages succeed. Standalone output copying remains blocked by Windows EPERM under `.next/standalone/node_modules/next/dist/...`; a complete deployable frontend artifact is unverified. No security settings were weakened.
28. **Docker:** Compose configuration validates. The Docker Linux engine pipe is unavailable; Docker startup remains unverified. PostgreSQL integration and browser checks ran against the local native PostgreSQL instance.
29. **Exact remaining blockers:** the nine withheld subclasses are listed below. Bone ’ead Implant needs a feature-specific Intelligence maximum/mandatory proficiency-choice mapping; the ASI-only cap must not be substituted. Rad-Hardened needs a structured resistance alternative. Grenadier needs range/DC engine mapping; Suppressive Discipline and Dead Calm retain their unresolved-rule dependencies. Imperial Flexibility and Last Order Standing retain v5 content/engine gaps. Open Guild-Craft engineering/tool domains, Hernkyn Vehicles, broader blades proficiencies and unreviewed equipment remain unavailable in those selected contexts. Warlock/Psyker still lack complete power pools/choices, Warp Pressure, Perils and execution contracts. PHB-RULE-011, 020, 022, 030, 046 and 058 remain unresolved. No Rare/Limited self-approval exists. The original ledger remains **15 resolved / 21 unresolved / 36 total**, with 059 separate.
30. **Next milestone:** implement level 5 and Extra Attack across certified martial classes using each class’s actual progression, while separately continuing psychic-content canonicalisation for Psyker and Aeldari Warlock. Ratling Sharpshooter’s level-5 Killshot/Deadeye entry must be assessed on its own source rather than receiving a generic Extra Attack grant. Outstanding subclass/Talent branches can continue independently.

## Publication matrix

| Status | Existing level-1–3 slots |
|---|---:|
| BLOCKED_BY_APPROVAL | 37 |
| BLOCKED_BY_CONTENT | 167 |
| BLOCKED_BY_ENGINE | 13 |
| BLOCKED_BY_RULING | 34 |
| READY | 0 |
| READY_WITH_MANUAL_RULES | 143 |
| UNSUPPORTED | 3746 |

Level-4 appendix: **77** certified families. Total published: **220**.

## Selected subclass blockers

| Subclass | State | Reason |
|---|---|---|
| di.subclass.hive_scum.chem_user | BLOCKED_BY_RULING | PHB-RULE-046: exhaustion and an unspecified Constitution save DC. |
| di.subclass.hive_scum.knife_rat | BLOCKED_BY_ENGINE | Conditional light-melee critical threshold requires an authoritative attack-mode contract. |
| di.subclass.hive_scum.sump_ghost | BLOCKED_BY_RULING | PHB-RULE-011: mandatory Expertise. |
| di.subclass.ratling_sharpshooter.underhive_rat | BLOCKED_BY_RULING | PHB-RULE-011: mandatory Expertise. |
| di.subclass.skitarii_veteran.data_hunter | BLOCKED_BY_RULING | PHB-RULE-011: mandatory Expertise. |
| di.subclass.skitarii_veteran.ruststalker | BLOCKED_BY_CONTENT | Mandatory blades proficiency lacks a certified complete weapon domain; equipment ownership is not that mapping. |
| di.subclass.hernkyn_prospector.claim_staker | BLOCKED_BY_RULING | PHB-RULE-011: mandatory Expertise. |
| di.subclass.aeldari_outcast.corsair | BLOCKED_BY_CONTENT | Mandatory blades proficiency lacks a certified complete weapon domain. |
| di.subclass.aeldari_outcast.shadow_guide | BLOCKED_BY_RULING | PHB-RULE-011: mandatory Expertise. |

## New Species-specific Talent alternatives

Alien Reflexes, Ancestor’s Grudge, Bigger Gun, Cold Logic, Cook’s Morale, Impossible Shot, Iron Stance, Loyal as Stone, Machine Precision, Noospheric Burst, Ogryn Wall, Path Discipline, Pocket Marksman, Ranger’s Cloak, Ratling Vanish, Sacred Augmetics, Scavver’s Luck, Too Angry to Notice, Void Stock, Kin Weapon Master, Hold-Born Engineer, Aeldari Grace.

Source-specific conditions and stacking are manual unless explicitly described above. Each option retains its original requirement predicate and source locator.

## Browser acceptance values

| Class | Subclass | Level-four selection | Current / max HP |
|---|---|---|---:|
| veteran | Marksman | Constitution +2 | 11 / 36 |
| hive_scum | Gunslinger | Impossible Shot | 9 / 27 |
| ogryn_skullbreaker | Bone ’ead | Constitution +2 | 17 / 57 |
| skitarii_veteran | Infiltrator Protocol | Intelligence +2 | 12 / 36 |
| kin_armsman | Hearthguard | Kin Weapon Master | 12 / 36 |
| hernkyn_prospector | Outrider | Constitution +2 | 10 / 35 |
| aeldari_outcast | Ranger | Aeldari Grace | 9 / 27 |
| ratling_sharpshooter | Black-Market Gremlin | Dexterity +2 | 9 / 27 |

## Reproduction

Run `tools/export_tier1_v6_profile.py --check` for immutable release verification, `tools/tier6_fixtures.py` for tuple fixtures, and `tools/tier6_matrix.py` for the 4,140-slot matrix plus level-4 appendix. Existing content test, backend test and frontend test commands remain unchanged. No new database migration is required: the existing V7 upgrade-history/level-four schema supports this release.

# Level 1–3 catalogue readiness — 22 October 2026

## Outcome and scope

Independent audit complete; catalogue expansion is NOT READY for production. The owner confirmed that PHB-RULE-001–007 have no approved decisions and requested an audit-only continuation. No Origin ruling was integrated, no additional combination was published, and no production adapter, builder UI, saved character or narrow profile was changed.

The original 36-question ledger remains at 5 resolved and 31 unresolved. The separate item-specific Frag Grenade ruling remains separate from that denominator. PHB-CAT identifiers below are implementation findings, not new human rulings.

## Inventory and counting boundaries

948 canonical records are schema/reference validated. The audit covers 6 species, 10 Origins, 12 classes, 45 subclasses and 20 universal traits. Its 4,140 rows enumerate Species × Origin × class at levels 1 and 2, and each parent-class subclass at level 3. They do not enumerate all attribute, trait, skill, equipment or optional feature selections.

| Family readiness | Rows |
|---|---:|
| BLOCKED_BY_CONTENT | 44 |
| BLOCKED_BY_ENGINE | 4 |
| BLOCKED_BY_RULING | 560 |
| READY_WITH_MANUAL_RULES | 1 |
| UNSUPPORTED | 3531 |

The sole ready row is restricted to Human / Schola Progenium / Veteran level 1, Twitchy and the existing reviewed kit/choices. Known-invalid species/class or known Origin restrictions are UNSUPPORTED. Status precedence retains ruling blockers ahead of content/engine gaps; all gaps remain in the JSON. The 560 Origin-gated rows still require content or engine work even if future rulings permit them. Another 48 unpublished rows have known base eligibility but content/engine gaps.

See [full publication matrix](LEVEL_1_3_PUBLICATION_MATRIX.md) and [Origin scenarios](LEVEL_1_3_ORIGIN_SCENARIOS.md). Machine-readable evidence is in `content/packages/di_phb_1_0/review/level-1-3-catalogue.json`.

## Species and class access

| Species | Canonical class access | Production scope |
|---|---|---|
| Aeldari / Eldar | aeldari_outcast, aeldari_warlock | Blocked: PHB-CAT-005 and path-specific gaps |
| Human | arbites_enforcer, hive_scum, psyker, veteran, zealot | Existing narrow only |
| Squat / Kin | hernkyn_prospector, kin_armsman | Blocked: PHB-CAT-005 and path-specific gaps |
| Ogryn Abhuman | ogryn_skullbreaker | Blocked: PHB-CAT-005 and path-specific gaps |
| Ratling Abhuman | hive_scum, ratling_sharpshooter, veteran | Blocked: PHB-CAT-005 and path-specific gaps |
| Skitarii Augmented Human | skitarii_veteran | Blocked: PHB-CAT-005 and path-specific gaps |

Baseline species movement/ability effects and references are present. Non-Human manual traits still contain core proficiencies, restrictions and calculations requiring mapping. Ogryn per-level HP and Ratling proficiency effects cannot be silently treated as flavour. Skitarii access points to the dedicated Skitarii Veteran class, not generic Veteran.

## Level 1–3 class and subclass dependencies

Every class has exactly one progression entry at each of levels 1, 2 and 3. Every subclass points to its actual parent and its granted dependency closure resolves. Choice alternatives are canonical-reference validated but are not automatically selected or certified by this traversal. No level-3 subclass is published.

| Class | Hit die | Saving throws | Level 2 newly reached features | Kit |
|---|---|---|---|---|
| Aeldari Outcast | 8 | ['dexterity', 'wisdom'] | ghostwalk | BLOCKED_BY_CONTENT |
| Aeldari Warlock | 6 | ['wisdom', 'intelligence'] | rune_ward | BLOCKED_BY_CONTENT |
| Arbites Enforcer | 10 | ['strength', 'wisdom'] | breach_and_clear | BLOCKED_BY_CONTENT |
| Hernkyn Prospector | 8 | ['dexterity', 'wisdom'] | surveyors_step | BLOCKED_BY_CONTENT |
| Hive Scum | 8 | ['dexterity', 'charisma'] | cunning_action | BLOCKED_BY_CONTENT |
| Kin Armsman | 10 | ['constitution', 'wisdom'] | steady_advance | BLOCKED_BY_CONTENT |
| Ogryn Skullbreaker | 12 | ['strength', 'constitution'] | brutal_impact | BLOCKED_BY_CONTENT |
| Psyker | 6 | ['intelligence', 'wisdom'] | psychic_ward | BLOCKED_BY_CONTENT |
| Ratling Sharpshooter | 8 | ['dexterity', 'wisdom'] | scamper | BLOCKED_BY_CONTENT |
| Skitarii Veteran | 10 | ['dexterity', 'intelligence'] | augmetic_reflexes | BLOCKED_BY_CONTENT |
| Veteran | 10 | ['dexterity', 'wisdom'] | suppressing_fire | PARTIAL_SUPPORTED_BRANCH |
| Zealot | 10 | ['strength', 'charisma'] | charge_of_conviction | BLOCKED_BY_CONTENT |

| Subclass | Parent | Granted feature dependencies |
|---|---|---|
| corsair | aeldari_outcast | level_3 |
| ranger | aeldari_outcast | level_3 |
| shadow_guide | aeldari_outcast | level_3 |
| seer_of_battle | aeldari_warlock | level_3 |
| spirit_guardian | aeldari_warlock | level_3 |
| storm_warlock | aeldari_warlock | level_3 |
| executioner | arbites_enforcer | level_3 |
| investigator | arbites_enforcer | level_3 |
| riot_shield | arbites_enforcer | level_3 |
| claim_staker | hernkyn_prospector | level_3 |
| outrider | hernkyn_prospector | level_3 |
| trail_gunner | hernkyn_prospector | level_3 |
| chem_user | hive_scum | level_3 |
| gunslinger | hive_scum | level_3 |
| knife_rat | hive_scum | level_3 |
| sump_ghost | hive_scum | level_3 |
| guild_militant | kin_armsman | level_3 |
| hearthguard | kin_armsman | level_3 |
| ironhead | kin_armsman | level_3 |
| bone_ead | ogryn_skullbreaker | level_3 |
| brute | ogryn_skullbreaker | level_3 |
| bulwark | ogryn_skullbreaker | level_3 |
| gun_lugger | ogryn_skullbreaker | level_3 |
| biomancer | psyker | level_1, level_3 |
| blank_null_bound | psyker | level_1, level_3 |
| diviner | psyker | level_1, level_3 |
| malefic_touched | psyker | level_1, level_3 |
| pyromancer | psyker | level_1, level_3 |
| telekine | psyker | level_1, level_3 |
| black_market_gremlin | ratling_sharpshooter | level_3 |
| long_las_sniper | ratling_sharpshooter | level_3 |
| spotter | ratling_sharpshooter | level_3 |
| underhive_rat | ratling_sharpshooter | level_3 |
| data_hunter | skitarii_veteran | level_3 |
| infiltrator | skitarii_veteran | level_3 |
| protector | skitarii_veteran | level_3 |
| ranger | skitarii_veteran | level_3 |
| ruststalker | skitarii_veteran | level_3 |
| vanguard | skitarii_veteran | level_3 |
| shock_trooper | veteran | level_3 |
| marksman | veteran | level_3 |
| sergeant | veteran | level_3 |
| flagellant | zealot | level_3 |
| preacher | zealot | level_3 |
| purifier | zealot | level_3 |

Expertise mentions are flagged for PHB-RULE-011 review on selected feature dependencies; this is not a blanket block on all subclasses. The six level-3 families are Outcast Shadow Guide, Arbites Investigator, Hernkyn Claim Staker, Hive Scum Sump Ghost, Ratling Underhive Rat and Skitarii Data Hunter. Full source references, choices and feature execution classifications are in the audit JSON. MANUAL/PARTIALLY_AUTOMATED labels describe representation, not production certification.

## Starting equipment and psychic paths

74 unique item dependencies are identified from literal kit matches, approved aliases and referenced choice pools: 5 SUPPORTED, 1 MANUAL, 23 canonical COMING_LATER and 45 incomplete candidates BLOCKED. This is an identified union, not a claim that unresolved category pools are complete. Canonical definitions alone do not establish legal quantities, proficiency, inventory grants or generated actions.

Only Veteran has a structured reviewed starting package. Its published branch remains lasgun, laspistol, combat blade, flak armour, two Frag Grenades and a manually adjudicated medpack. Autogun is not added to production; auspex remains blocked. Other eleven packages require executable quantity/choice/proficiency grants. Equipment checks retain source provenance, requirements and available structured fields; absent fields are not represented as validated.

Psyker and Warlock have known-power counts of Minor/Standard 2/2 at level 1, 2/3 at level 2 and 3/3 at level 3; Major is zero. There are no canonical power records. Of 52 candidates, 38 required Minor/Standard candidates block creation pools and 14 Major candidates are deferred. No psychic character is certified through a manual shortcut.

## Independent calculation work and fixtures

`tools/tier1_calculations.py` composes existing policies for fixed HP, ability modifiers, proficiency, saves, skills, explicit armour, movement and initiative across levels 1–3. It requires resolved inputs and is review-only, not a registered production adapter. Constitution changes and nonpositive HP gains remain blocked by PHB-RULE-014; no minimum gain or retroactivity is invented. It does not implement species grants, selected-choice resources, goldens for new playable characters or roll compilation.

36 family-readiness fixtures cover twelve eligible Species/class families at levels 1–3, including one parent-valid subclass per family at level 3. They explicitly record expected blockers and are not valid-character golden fixtures. Independent numeric proofs cover d6/d8/d10/d12 HP across all three levels. Negative tests cover invalid eligibility, subclass dependencies, missing approval provenance, source hash mismatch, path traversal, unresolved Constitution policy and unsupported level/skill inputs. Existing narrow character goldens and immutable bundle hash checks remain in place.

## Blockers and publication plan

- **PHB-CAT-001**: Starting-package compiler absent outside Veteran: source tokens/approved aliases are not executable quantity, choice, proficiency and inventory grants.
- **PHB-CAT-002**: At least one identified starting option remains an incomplete candidate; source alternatives must be independently certified.
- **PHB-CAT-003**: Psychic power candidates lack canonical power schema/choice pools and production execution boundaries; no manual shortcut can validate unknown creation choices.
- **PHB-CAT-004**: Only narrow-kotlin-v1 is production-registered. Tier-1 selected-level choice/resource/projection/roll compilation and golden certification are not implemented.
- **PHB-CAT-005**: Non-Human species traits include unmapped core calculations/proficiencies/restrictions. Manual prose cannot substitute for those calculations.

PHB-RULE-001–006 gate their affected Origin predicates; PHB-RULE-007 gates Rare/Limited availability. No matrix/prose precedence or GM-permission default is inferred. The smallest ruling set for one affected Origin is its corresponding 001–006 plus 007; Shrine Worlder depends on 007. These are necessary Origin decisions, not sufficient character certificates. All seven are required for the requested complete Origin integration. Existing narrow creation needs none of these new decisions.

Other unresolved rules are configuration-specific: 011 expertise, 014 changed Constitution/minimum HP, 015 ASI, 016 repeated talents, 026 slash damage, 028 Powered Carapace, 029 Exo-frame, 030 Ogryn flak, 032 unarmoured/competing protection and 058 stacking apply when the selected path exercises them. They are not global substitutes for a dependency audit. Alternate arrays (012), runtime resistance (010), overheat (017), generic Blast (018), Burst (020), suppression (022), concentration (035), pressure halving (037), Warp Step (038), conditions (046), injuries (047), Aim (055), cover (056) and rest/Hit Dice (057) may remain unresolved for paths that do not require them; manual runtime scope must remain explicit. Exact questions and existing impact classifications remain in the ledger and audit JSON.

Reserved plan: `di-phb-1.0-tier1-v1`, proposed adapter `phb-tier1-kotlin-v1`. This is PLANNED_NOT_PUBLISHED with an empty allowlist. There is no new production profile digest. Its auditDigest detects inventory changes only. Activation requires explicit approvals, tuple and choice certification, executable packages, a registered adapter, immutable export, server validation and browser acceptance.

Existing production profile: `di-phb-1.0-narrow-v1`, digest `3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af`, adapter `narrow-kotlin-v1`. No migrations or snapshot rebinding were introduced.

## Verification

| Check | Result |
|---|---|
| Content | 117 passed, including 22 new audit/calculation tests |
| Frontend | 46 passed |
| TypeScript | Passed, no emit |
| Backend | 43 passed against local PostgreSQL; zero skipped/failures/errors |
| Migrations | Five existing migrations validated; existing schema up to date; no new migration |
| Generated inventory | Reproducibility check passed |
| Narrow profile | Export check and pinned digest compatibility passed |
| Production build | Compilation, TypeScript and eight static pages succeeded; standalone packaging failed with Windows EPERM mkdir under .next/standalone/node_modules/next |
| Docker | UNVERIFIED: dockerDesktopLinuxEngine named pipe unavailable |
| Browser | New paths not applicable; existing browser acceptance not rerun in this audit pass |

These are checks of the independently completed audit and existing application, not certification of the unpublished tier-1 plan. New-path browser acceptance is not applicable: no new path is published. Existing browser flows were not re-exercised in this audit pass; automated regression and profile-byte compatibility checks are reported separately.

## Next milestone

Receive the explicit approved 001–007 ruling set, integrate it with provenance, then implement and certify selected tier-1 paths using this inventory. Character advancement and levels 4–20 remain later work; this audit does not justify starting them.

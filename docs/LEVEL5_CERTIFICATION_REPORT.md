# Level 5 and Extra Attack certification

23 October 2026. **Rules/content: READY_WITH_MANUAL_RULES for all 77 previously certified level-4 families.** All are extended to level 5. No level 6 or psychic expansion. Native and Docker-served browser acceptance pass. The user rebuilt the host Docker stack; v8 is verified at http://localhost:3100. Earlier production/CSP reporting does not gate this rules milestone.

| # | Requested result | Evidence / outcome |
|---|---|---|
| 1 | Previous profile | `di-phb-1.0-tier1-v7` |
| 2 | New profile | `di-phb-1.0-tier1-v8` |
| 3 | Digest | `ebb729c9d8953afbe5053085374279053f446551181ec7ea1e409d8c711ec4b5` |
| 4 | Previous families | 220 level-specific family rows. |
| 5 | New families | 297; 77 added at level 5. Creation remains level 1. |
| 6 | Class audit | Eight classes audited against canonical class progressions. Six grant Extra Attack; Hive Scum grants Backstabber +3d6 and Ratling Sharpshooter grants Killshot / Deadeye +2d6. No new mandatory choices or weapon grants. See machine-readable audits below. |
| 7 | Subclass audit | All 21 published subclasses/doctrines have no new level-5 progression entry; existing level-3 grants and manual restrictions persist. Every extended family validates. |
| 8 | Extra Attack eligible | Veteran, Ogryn Skullbreaker, Skitarii Veteran, Kin Armsman, Hernkyn Prospector, Aeldari Outcast. |
| 9 | Not eligible | Hive Scum and Ratling Sharpshooter retain one attack per Attack action. |
| 10 | Capacity | Feature effects set `action.attack.capacity`, operation `base`, constant 2, max stacking. v8 opts into `attackActionVersion=1`; the calculator exposes `attacksPerAttackAction`, feature IDs and eligible action IDs. No class-name branching. |
| 11 | Action generation | Existing owned weapon roll definitions remain independent. Sequence eligibility is restricted to weapon attack-roll delivery without consumption. Grenade uses, feature-specific actions, bonus actions and reactions are not duplicated. |
| 12 | Sheet | Compact Extra Attack banner states two attacks when taking the Attack action on your turn. Individual weapon buttons remain usable. |
| 13 | Sequence | Optional Start Attack action; choose each weapon immediately before rolling; advances on successful completion only. One Attack action contains two independently finalised attacks. Damage buttons remain attached to their respective attack results. |
| 14 | Inspector | Generic inspector shows canonical text, Level 5, capacity 2, action scope and PHB source. Killshot and Backstabber use the existing feature inspector. |
| 15 | Knife | Fixed Dexterity attack and damage retained; validation and forged-context tests pass. No ability selector. |
| 16 | Strength melee | Kin Power Axe independently resolves Strength for attack and linked damage; browser and server tests pass. Thunder Hammer policy remains Strength. |
| 17 | Ranged | Dexterity preserved, including two separate ranged attacks in server tests and browser Ion Blaster attack/damage. |
| 18 | Thrown | Existing canonical mode policy preserved. Knife retains Finesse/Dexterity; no invented thrown-mode override. Frag uses its existing save/DC and transactional damage flow, not an Attack-action slot. |
| 19 | Overrides | Existing explicit ability/none overrides remain authoritative; historical and override regression tests pass. |
| 20 | Mixed weapons | Legal Kin Ion Blaster (DEX) then Kin Power Axe (STR), verified in browser and physical-session integration tests. No published package owns both Knife and a Strength melee weapon, so that exact example is unavailable without inventing ownership. Knife tested separately. |
| 21 | Sessions | Every attack and damage roll has its own server-authorised physical session and request ID. Forged second-attack context rejected; failed submissions, retries and duplicate finalisation tested. Sequence state never participates in canonical result validity. |
| 22 | Physics | Browser evidence contains four distinct `PHYSICS` sessions with persisted physical raw values matching result dice: attacks 8 and 20; damage 1 and 6. Second attack screenshot shows top face 20 and stored raw 20. First attack's live top face was not captured; persisted physical data and replay were checked. No physics implementation/preselection/corrective flip change. |
| 23 | Damage | Ion Blaster 1+2=3 Radiant and Axe 6+2=8 Slashing stored separately with the correct parent attack IDs and abilities. Natural 20 remained a critical candidate; no automatic hit or critical damage. |
| 24 | Ammo | Remains manual. Reload capacities stay visible; no executable per-shot ammunition decrement was invented. |
| 25 | Consumables | Grenades excluded from sequence, with reserve → physical roll → finalise → consume once unchanged. v8 duplicate-finalisation and quantity assertions pass alongside existing reservation tests. |
| 26 | Timing/resources | 24 timing-bearing features inventoried with canonical text and sources. Once-per-turn effects (Dirty Fighter/Backstabber, Deadeye, Shuriken Grace, Brutal Impact, Brute, Shock Trooper, Vanguard, Sacred Hatred, Gunslinger reload) retain their original limits. Killshot is once per short rest after an Accurate ranged hit. Bonus/reaction effects stay separate; unresolved conditions/stacking stay manual. No sequence-wide resource spending. |
| 27 | Human | 24 Veteran level-5 families. Human Hive Scum remains level-1-only because no level-4 path was previously certified; this release does not invent its missing lower-level certification. |
| 28 | Ratling | 35: Veteran 15, Hive Scum Gunslinger 5, Sharpshooter 15. |
| 29 | Ogryn | 8 Skullbreaker families. Massive Build +3 HP per level includes level 5; representative maximum 70 verified. |
| 30 | Skitarii | 4 Veteran families. |
| 31 | Kin | 5: Armsman 3 and Hernkyn Prospector 2. |
| 32 | Aeldari | 1 Outcast family. Psychic/Warlock branches remain blocked. |
| 33 | Sharpshooter | 15 families; Killshot manual 1/short rest resource added, Deadeye becomes +2d6 under original once-per-turn advantage/hit conditions, replacing +1d6. No Extra Attack. Long-Las Accurate, stationary/movement and sniper conditions remain manual. Browser level 5: current HP 9 unchanged, maximum 31→38; Knife/Long-Las/Stub Pistol remain DEX. |
| 34 | Thunder Hammer | Policy VERIFIED; production ownership BLOCKED_BY_CONTENT. No level-5 class feature or existing package grants it. No shop or test-only production grant added. |
| 35 | v7 immutability | Digest remains `af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5`. All historical bundle/spec/migration byte hashes match the pre-task baseline. Existing level 1–4 calculated shapes remain unchanged. |
| 36 | Upgrade | Explicit confirmed v7 level 4 → v8 level 5, atomic/idempotent through existing framework. No silent rebinding. Level-4 ASI/Talent, choices, inventory, current resources, conditions and history retained. PHB-RULE-014 applies current CON retroactively; current HP does not heal and clamps to max if required. V11 only widens advancement audit level constraint to 5. |
| 37 | Content tests | 160 pass, including reproducible v8 bytes, 297 family fixtures, all class/subclass progressions and invalid capacity rejection. |
| 38 | Backend tests | 117 pass against PostgreSQL, including all 77 level-5 families and all eligible ASI/Talent alternatives. Existing historical tests retained. |
| 39 | Frontend tests | 132 pass in 21 files, including optional sequence completion, duplicate callbacks, weapon switching, separate damage parents and exclusion of consumables. |
| 40 | TS/build | TypeScript passes. Backend `installDist` passes. Clean-copy Next production compile, typecheck and all eight static pages pass; final standalone trace copying fails with Windows EPERM. v8 Docker build/startup is user-verified; rebuilt application and physical dice verified through production HTTP/browser acceptance. |
| 41 | Level-5 browser | Kin and Ratling explicitly upgraded through real UI, pinned v7 level-4 state observed before upgrade. Native API 8082 + development frontend 3200, separate verification account/database. |
| 42 | Extra Attack browser | Banner, canonical inspector, optional two-step flow and two independent stored physical attacks pass. Cancelling a new physical attack leaves the sequence at Attack 1 and creates no history result. |
| 43 | Mixed browser | Ion Blaster DEX → Kin Power Axe STR, linked damage and first-attack-only replay pass. Replay leaves four history results, quantities/resources and state version unchanged. |
| 44 | Mobile | 390px and 320px viewports have no horizontal overflow (document widths 375 and 305 respectively). Sequence remains inline, with tabs, inspector and free dice controls in their existing layout. Actual phone hardware and named-browser coverage not claimed. |
| 45 | Level-5 blockers | None for the 77 extended families. Human Hive Scum lacks earlier path certification; Thunder Hammer ownership lacks content; the exact Knife+STR package example unavailable. v8 Docker deployment acceptance verified. |
| 46 | Unresolved rules | No rulings changed. Expertise, Burst, Suppression, conditional effects, generic stacking, psychic branches and other previously blocked alternatives retain existing gates/manual handling. |
| 47 | Next milestone | Consider targeted lower-level catalogue gaps or manual-effect UX; v8 Docker acceptance is now verified. Do not proceed automatically to level 6. |

## Audit artefacts

- [Class and subclass source audit](../content/packages/di_phb_1_0/review/level5-certification.json)
- [Species/class eligibility matrix](../content/packages/di_phb_1_0/review/level5-eligibility-matrix.json)
- [Timing and resource audit](../content/packages/di_phb_1_0/review/level5-timing-audit.json)
- [Browser sessions and upgrade evidence](verification/level5/browser-evidence.json)
- [All 297 fixtures](../backend/src/test/resources/tier8/all-paths.json)
- [Reproducible exporter](../tools/export_tier1_v8_profile.py): `python tools/export_tier1_v8_profile.py --check`

Sequence grouping is a transient play aid. It resets on tab navigation/reload; persisted history stays individual. Optional grouping metadata is not stored. There is no turn ownership, action-spent state, hit determination, target AC or automatic ammo/critical/conditional damage.

Host Docker runtime, earlier Compose startup and localhost access remain VERIFIED from user evidence. Codex-session Docker-engine access remains ENVIRONMENT_BLOCKED, and runtime verification inside Codex is NOT POSSIBLE DUE TO SESSION PERMISSIONS. No Docker repair was attempted. The subsequent host rebuild and production browser/API acceptance now verify the deployed v8 application; engine access from this session remains blocked.

Browser screenshots: [Level 5 inspector](verification/level5/sheet-inspector.png), [mixed attack sequence](verification/level5/mixed-attack.png).

## Docker follow-up: verified

User confirmed the host rebuild completed. Production on port 3100 serves the expected v8 digest. A separate legal Kin Armsman was created on historical v7 and advanced through level 4, then explicitly upgraded to v8 level 5 through the browser. Maximum HP 40→49, current HP 12 unchanged, Constitution improvement preserved. The pre-existing v7 level-1 Ratling remains pinned.

Production attacks: Ion Blaster DEX raw 7 +5 =12; Kin Power Axe STR raw 4 +5 =9. Both visible top faces matched raw results. Separate linked damage: Ion Blaster raw 9 +2 =11 Radiant; Axe raw 2 +2 =4 Slashing. All four stored results have distinct physical session IDs and PHYSICS provenance. Damage parents match their attacks. First-attack replay created no additional history. State persists on reload. Inspector works; no browser warnings/errors captured. 320px and 390px layouts have no horizontal overflow.

Production CSP includes wasm-unsafe-eval and excludes JavaScript unsafe-eval. The previous WASM-blocking production failure is resolved in this rebuild. Windows standalone packaging EPERM remains a separate local limitation; it does not block the verified Docker deployment. Broader named-browser/device coverage remains as previously documented.

[Machine-readable Docker acceptance](verification/level5/docker-acceptance.json) · [Physical roll screenshot](verification/level5/docker-physical-sequence.png) · [Production inspector](verification/level5/docker-v8-inspector.png).

# Character Sheet Play UX & Fixed Weapon Abilities

23 October 2026. The playable sheet and fixed-ability profile are implemented. Thunder Hammer live-character acceptance and deployable packaging remain gated as described below. No blocked catalogue content was published.

| # | Requirement | Result |
|---|---|---|
| 1 | Character-sheet layout | Compact identity/combat header, six abilities, saves/training, skills, and central play area. Current/max HP are displayed; no unsupported temporary-HP or healing mechanics were invented. |
| 2 | Main tabs | Actions, Inventory, Features & Traits, Origin & Character, Notes, Extras. Keyboard tab navigation; inventory search/category filters; only populated feature categories. Notes save privately with optimistic revision checks and survive reload. |
| 3 | Inspector | Owned-character details come from its pinned snapshot. Weapons, inventory, skills, training, features, species, origin, class, trait and subclass expose details. Desktop side panel and mobile drawer; close, Escape, focus return and mobile focus wrapping. Resource inspection labels manual tracking. |
| 4 | Direct controls | Abilities, saves, skills and initiative dispatch existing server-calculated RollDefinitions. No modifier arithmetic added to React. |
| 5 | Weapon rows | Compact range, attack modifier, damage formula/type, fixed ability labels and rules button. Inspector uses the same roll workflow, including consumable confirmation. |
| 6 | PHB-RULE-024 amendment | Explicit user approval preserved in review/approved-weapon-ability-amendment.txt; separate hash-verified amendment ledger references the original approval. Original decision/provenance retained. No other ruling resolved. |
| 7 | Data model | Canonical attack/damage bindings are resolved independently. Calculated actions expose attackAbilityId and damageAbilityId. Policy version 2 marks the new profile. |
| 8 | Knife | v7 automatically uses Dexterity for attack and damage. Acceptance character: DEX +3, proficiency +2, attack +5, damage 1d4 +3. |
| 9 | Thunder Hammer | Standard melee Strength policy is tested. Thunder Hammer is still an unpublished partial candidate, absent from certified equipment/packages; no production character can legally own it. Its item-specific production acceptance remains blocked. |
| 10 | Ranged | Existing explicit Dexterity bindings retained; Long-Las and Stub Pistol display Dexterity. |
| 11 | Thrown | Normal fixed weapon binding applies; Knife is Dexterity. Existing GM-approved improvised-range restriction remains; no automatic thrown range/mode invented. |
| 12 | Overrides | Explicit attribute bindings remain authoritative; Intelligence override and no-ability save damage covered by policy tests. Linked damage checks the parent's canonical attack binding separately. |
| 13 | Selector removal | Removed from both current and legacy sheet layouts. v7 rejects client ability overrides instead of accepting arbitrary substitution. |
| 14 | History | Existing characters retain their pinned profiles; stored rolls and historical profile bytes unchanged. Historical default calculations remain historical, including pre-amendment Finesse. No silent rebind or v7 migration contract. |
| 15 | Immutable release | di-phb-1.0-tier1-v7; digest af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5. Same 220 certified families and entity set as v6. New characters default to v7. |
| 16 | Roll sessions | Existing authorize/simulate/finalize design retained. Backend validates ownership, pinned profile, state, exact raw count/range and versions; it applies modifiers and persists once. |
| 17 | Physics | Existing Rapier 0.21.0 seeded rigid-body simulation, fixed timestep and convex physical geometry retained. |
| 18 | Collisions | Physical floor, walls and die/die contacts retained; simulation/geometry regression tests pass. |
| 19 | Top-face detection | Settled orientation determines raw face; result finalization uses those values. Stability and face-normal confidence gates retained. |
| 20 | Cocked dice | Selective bounded rerolls retained. A cocked reroll occurred during the new four-dice browser check; other accepted dice remain frozen. |
| 21 | No corrective flip | Renderer copies simulation poses. No post-result face alignment or outcome-forcing stage added. Regression coverage checks accepted pose stability. |
| 22 | Free roller | Persistent launcher, add/remove/clear/mixed pools, private history; remains on the character page. Large pools use complete text output. |
| 23 | d100 | Existing paired percentile dice implementation and tests retained. Previous browser proof (16) remains in the preceding milestone evidence; not newly rerolled in this pass. |
| 24 | Consumables | Existing transactional reservation/finalization, cancellation/expiry release, duplicate protection and rollback tests retained and passing. No new inventory spending path. |
| 25 | History/replay | Persisted raw values and server context remain authoritative. Replay cannot create/alter a canonical roll; mismatch falls back to stored results. |
| 26 | Accessible modes | Reduced Motion, Text Only, Skip and explicit server fallback retained. Existing regression coverage passes; new inspector keyboard controls also browser-checked. |
| 27 | Ability tests | All 220 family fixtures validate under v7; Knife DEX, historical STR, standard STR, explicit override, no ability, thrown policy, immutable v6 digest and forged context covered. |
| 28 | Frontend | 110 tests across 16 files pass; TypeScript passes. Added inspector, notes draft/conflict and proxy dotted-ID/Unicode PUT coverage. |
| 29 | Backend | 105 tests pass, including HTTP notes length/ownership, version conflicts, immutable runtime state, linked Knife damage and forged ability rejection. Native distribution builds. |
| 30 | Content | 155 tests pass. Reproducible v7 export, unchanged catalogue families/entities and hash-verified current/prior approvals covered. |
| 31 | Browser Knife | New legal v7 Ratling Sharpshooter fixture 076d5e3f-c9ce-4f43-b7d1-46185d116f15. No selector; DEX displayed; attack +5; damage 1d4 +3; inspector pinned to v7; physical attack persisted with dexterity context and request ability null. |
| 32 | Browser Thunder Hammer | NOT VERIFIED: no legal published ownership path. Candidate remains unpublished; no test-only equipment was injected into a production character. |
| 33 | Forged context | Live session request supplying Knife + strength returns INVALID_CONTEXT. Backend integration test independently verifies rejection. |
| 34 | d20 proof | Visible face 18 = submitted physical raw [[18]] = persisted dice [18]; server +5 = 23. Screenshot and saved API history under verification/sheet-v7. |
| 35 | Multi-dice proof | Visible 4,6,1,2 = persisted raw [[4,6,1,2]], total 13. Cocked reroll notice visible. Screenshot and persisted history agree. |
| 36 | Responsive | Desktop and 390×844 checked. Mobile document scrollWidth 375 at viewport 390: no horizontal overflow. Drawer scrolls, focus wraps, Escape closes. Inventory search and notes save/reload verified. |
| 37 | Production build | Optimized compilation, TypeScript and all eight static pages pass. Standalone traced dependency packaging fails with Windows EPERM mkdir. Deployable standalone bundle is NOT certified. See v7-build.log. |
| 38 | Docker | Compose configuration validates. Docker Desktop Linux engine pipe unavailable; startup remains UNVERIFIED as previously accepted. Native API runs and migrated preview database to V10. |
| 39 | Limitations | Thunder Hammer ownership/publication gate; packaging and Docker limits; no server physics re-simulation or statistical fairness certification; cross-device replay equality not certified. Existing historical characters do not receive v7 mechanics automatically. Unsupported temporary HP, conditions, damage application and psychic paths remain unsupported. |
| 40 | Next milestone | Non-human advancement through 2–4 and Ratling Sharpshooter certification already exist in v6 and remain preserved in v7. Prioritise deployment verification and broader device checks; resolve a legal Thunder Hammer publication/ownership path explicitly before claiming its browser acceptance. No level 5 or Extra Attack expansion in this pass. |

## Verification evidence

[Desktop inspector](verification/sheet-v7/v7-inspector.png), [mobile inspector](verification/sheet-v7/v7-mobile-inspector.png), [d20](verification/sheet-v7/v7-d20.png), [four dice](verification/sheet-v7/v7-multidice.png), [persisted results](verification/sheet-v7/v7-persisted-rolls.json), [production build log](verification/sheet-v7/v7-build.log).

The new fixture is a local verification character. Existing user characters were not migrated. The earlier physics report is historical; its architecture and tests remain applicable, while this report supersedes its current-profile and sheet-tab descriptions.

Migration V10 adds private notes and notes_version separately from combat stateVersion. GET details validates ownership and restricts access to the character's actual pinned entities. The browser proxy permits canonical dotted IDs only in the details route and applies the larger bounded body allowance only to notes; other endpoint limits remain unchanged.

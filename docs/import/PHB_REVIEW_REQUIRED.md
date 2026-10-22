# PHB review required

All issues remain open. Source ambiguities, specification mappings and implementation backlog are distinguished. Stable IDs are retained for future decisions. No issue authorizes a silent rule change.

## PHB-001 — Origins species eligibility

- Status: DUPLICATE_OR_CONFLICT
- Type: Source rule
- Source: Printed 13–14 (PDF 26–27), chapter 4

Problem: The eligibility matrix allows Rare Kin for Hiveborn, Penal Worlder, Forge World, Militarum Regiment and Underhive, but their Allowed Species prose omits Kin. Voidborn matrix permits Kin and rare Aeldari, whereas prose lists Human, Ratling and rare Ogryn.

Affected content: Six background definitions and future builder eligibility.

Recommended resolution: Choose the authoritative matrix/prose values, and define approval requirements for Rare/Limited. No eligibility is silently selected.

## PHB-002 — Foundational calculation definitions

- Status: MISSING_REFERENCE
- Type: Source rule
- Source: Printed 4–5, 19, 22, 37–71 (PDF 17–18,32,35,50–84)

Problem: Ability modifiers, general resistance arithmetic and expertise are referenced without a located explicit defining table/formula. Point-buy and rolled-score methods need GM approval but their procedures are not given. The phrase familiar 5e-style is not permission to import external rules.

Affected content: All calculated sheets and derived roll modifiers.

Recommended resolution: Supply exact rules or approve explicit profile policies with citations. Keep imported ft values; do not reuse foundation metre statistics.

## PHB-003 — Ability Score Improvement and Talent acquisition

- Status: AMBIGUOUS
- Type: Source rule
- Source: Printed 37,73,99 (PDF 50,86,112)

Problem: Class tables consistently grant ASI/Talent at levels 4,8, 12,16,19. The amount, distribution and cap of ASI are not defined in the inspected text. General Talent repeatability is also not established.

Affected content: All twelve class progressions and feat choices.

Recommended resolution: Confirm ASI amount/cap and repeatability. Level labels are structured, but improvement mechanics remain manual.

## PHB-004 — Personal weapon property details

- Status: AMBIGUOUS
- Type: Source rule
- Source: Printed 22 and108 (PDF35, 121)

Problem: Overheat does not state its damage amount/type. Blast generally lacks an exact area. Heavy movement penalty is discretionary. Personal Burst extra ammunition is unspecified; chapter21 specifies three shots for mounts, not necessarily personal weapons. Suppression trigger/save is clearer for mounts than generic personal properties.

Affected content: Overheat/Burst/Blast/Heavy/Suppression weapons.

Recommended resolution: Define missing parameters or explicitly retain GM procedures. Do not export mounted Burst rules to personal weapons without approval. Twin-Linked is unusual but preserved exactly.

## PHB-005 — Weapon required fields and equipment taxonomy

- Status: AMBIGUOUS
- Type: Source rule and mapping
- Source: Printed 24–27,34,108 (PDF37–40,47, 121)

Problem: Armoury rows provide damage/range/properties but generally not explicit hands, reach for melee, or full proficiency-category membership. Required canonical weapon fields cannot be guessed. Grenade Launcher damage depends on another item.

Affected content: 101 reserved weapon candidates including 84 chapter8 weapons, 10 additional mounted identities and 7 grenades.

Recommended resolution: Confirm equipment taxonomy/hands/reach and map grenade payloads. Preserve known components/ranges/properties in review candidates until complete.

## PHB-006 — Slash-separated damage types

- Status: AMBIGUOUS
- Type: Source rule
- Source: Printed24–27,34,79–80 (PDF37–40,47,92–93)

Problem: Examples include radiant/fire, poison/piercing, slashing/psychic and piercing/radiation. The source does not explain split damage, choice of type, or simultaneous type semantics. An explicit plus, such as bolter piercing + thunder, is distinct and is split into components.

Affected content: Plasma, needle, several xenos/Mechanicus weapons and psychic powers.

Recommended resolution: State slash-type semantics. Candidates retain the original wording; no half-and-half split or extra damage dice are invented.

## PHB-007 — Armour AC expression and protection fields

- Status: AMBIGUOUS
- Type: Source rule and mapping
- Source: Printed29 (PDF42)

Problem: Powered Carapace and Exo-Frame Plate read 17, max Dex +1; Ogryn Flak Plate reads 14 but says does not limit Dexterity. Confirm exact AC arithmetic. Other base-plus-Dex formulas need registered derived statistics; reactive fields are not zero-AC armour.

Affected content: Armour, fields and future defence calculation.

Recommended resolution: Confirm ambiguous formulas; map remaining clear formulas via the existing stat-derivation mechanism. Ogryn Leathers AC12 and Shield +2 are imported as a small explicit slice.

## PHB-008 — Psychic membership and access

- Status: SPEC_EXTENSION_REQUIRED
- Type: Specification mapping
- Source: Printed43,70,78–80 (PDF56,83,91–93)

Problem: Power tables carry multiple tags (Universal, Telekinesis, Warlock, Divination, etc.), while the canonical power requires one discipline ref. The access rules must not lose alternate list membership.

Affected content: 52 power candidates and discipline-locked choices.

Recommended resolution: Review either a plural discipline membership field or a documented access policy over canonical tags. No unrelated architecture change is needed. The Aeldari Warlock rules explicitly grant power access despite chapter14 general wording; record the specific exception.

## PHB-009 — Psychic duration, pressure and roll policy

- Status: SPEC_EXTENSION_REQUIRED
- Type: Specification mapping and source rule
- Source: Printed78–83 (PDF91–96)

Problem: Current duration union lacks minutes/concentration. Warp Pressure increases rather than spends and has no located cap; do not invent a maximum. Perils severity needs current pressure modifier and a 31+ open-ended band, unlike the current fixed-Dice table. Warp Step says roll even if Pressure would not normally trigger it, while chapter15 calls for a roll after every power.

Affected content: Psychic actions, resources, Perils and concentration.

Recommended resolution: Add only reviewed duration/table/resource capabilities and clarify concentration/extra-roll wording. Continue manual until approved.

## PHB-010 — Vehicle DT, Handling and mounted context

- Status: SPEC_EXTENSION_REQUIRED
- Type: Specification mapping
- Source: Printed101–108 (PDF114–121)

Problem: The PHB defines DT, Handling, per-mount limits, crew control, arcs, supplies and breakdown timing. Existing common stats/features/damageRule can host much of this, but no reviewed profile policy currently executes whole-hit DT or crew-dependent attack resolution.

Affected content: 12 vehicle candidates, mounted weapons and repairs.

Recommended resolution: Register typed statistics and a bounded vehicle damage/control policy. Preserve DT as a threshold, not subtraction, and reuse shared weapon IDs with mounting context. No microservice or separate vehicle engine.

## PHB-011 — First-slice mapping and publication review

- Status: MANUAL_RULE
- Type: Implementation backlog
- Source: All chapters

Problem: Most mechanical clauses are transcribed as ManualRule pending fine-grained effect/action mapping. No playable PHB profile/lock or complete actor-roll compiler exists. Canonical draft validity is not automatic gameplay support.

Affected content: All draft packages; especially restrictions, class hit dice/resources and event-driven features.

Recommended resolution: Review transcriptions, map clauses incrementally, register policies, and publish only a closed, validated profile. Scope this as implementation work, not a claim that the PHB is ambiguous.

## PHB-012 — Remaining subclass and feature mappings

- Status: MANUAL_RULE
- Type: Implementation backlog
- Source: Printed37–71 (PDF50–84)

Problem: All 12 class level tables are captured. Veteran has three explicit subclass progressions. The other 42 subclasses are reserved candidates; their repeated/split tables need level mapping. Some progression labels do not directly match section headings and are retained as labelled incomplete feature records.

Affected content: Class progression feature details and 42 subclass candidates.

Recommended resolution: Match each source heading/table to level and parent, preserving upgrades and replacements. Do not label an unconverted clause as absent from the PHB.

## PHB-013 — Conditions and referenced states

- Status: AMBIGUOUS
- Type: Source rule and mapping
- Source: Printed19–20,80 (PDF32–33,93)

Problem: 15 condition/state rows plus Exhaustion exist. Bloodied is explicitly a state. Default stacking/removal is not uniformly specified. Flesh Reforged mentions diseased, bleeding and crippled conditions without located canonical condition definitions; concentration also needs procedure review.

Affected content: 16 condition/state candidates, psychic healing and runtime statuses.

Recommended resolution: Separate defined states from unresolved narrative injuries; confirm defaults or retain explicit manual handling.

## PHB-014 — Starting equipment, tools and minor augmetics

- Status: MISSING_REFERENCE
- Type: Source rule and mapping
- Source: Printed76,87–88,91–97 (PDF89,100–101,104–110)

Problem: Starting lists use medkit, riot shield, light armour, survey auspex, maintenance tools, psychic focus, symbols/tokens and similar terms without a located complete dedicated entry for every name. Med-Pack is defined but not silently equated to medkit; Shield is not automatically riot shield. Minor augmetic upgrades are granted without an enumerated minor subset.

Affected content: Starting item choices, augmetic choices and remaining equipment candidates.

Recommended resolution: Approve aliases or provide missing definitions; distinguish narrative belongings from mechanical items. Frag Bomb and Ogryn Club DO have entries and are not missing.

## PHB-015 — RollTemplate damage and contextual binding

- Status: SPEC_EXTENSION_REQUIRED
- Type: Specification mapping
- Source: DICE_ROLLING and PHB printed18,24,78,108

Problem: RollDefinition can carry typed damage components, but embedded RollTemplate groups currently have no explicit damage-type/component binding. Attack ability selection, healing, pressure modifiers and target context need a documented binding/compilation contract.

Affected content: Two imported base-dice action templates and future attack/damage generation.

Recommended resolution: Extend only the template-to-component binding when implementing the compiler. Base templates are not complete calculated attacks or actor-resolved RollDefinitions.

## PHB-016 — Aim and inconsistent cover terminology

- Status: MISSING_REFERENCE
- Type: Source rule
- Source: Printed22,91 (PDF35,104)

Problem: Targeting Optic refers to Aim, but the generic action list has no Aim procedure. Veteran Tactical Aim is a named class feature and cannot silently become a universal action. Armour-Breaking mentions half cover whereas combat uses Light/Heavy/Full Cover.

Affected content: Targeting Optic, Armour-Breaking and available generic actions.

Recommended resolution: Identify the intended Aim procedure and cover mapping or retain explicit GM adjudication.

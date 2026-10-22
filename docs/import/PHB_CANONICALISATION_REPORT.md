# PHB rules resolution and canonicalisation report

Pass completed 2026-10-22 against the preserved PHB v1.0 source SHA-256 `a58335b1264ac40e30ff0b310626d306fc88f7003e0c3af345e0d55c978e94b7`. Application behaviour is unchanged. The package remains a private draft and is not publishable.

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical draft records |600|870|
| Incomplete candidates |385|333|
| Canonical subclasses |3|45|
| Original review groups analysed |16|16|
| Concrete review issues |not expanded|58|
| Concrete resolutions applied |0 in this pass|15|
| Concrete issues still open |—|43|
| Questions requiring human rulings |—|36|
| Original grouped issues fully closed |0|0|
| Candidate conversions |—|52|
| Supporting definitions added |—|218|
| Canonical manual entries / records containing them |not counted|659 / 659|
| Calculation policies assessed |—|30|
| Damage types |12|13|
| Content tests passing |17|44|

52 candidates completed to canonical **draft shape**:42 subclasses,9 masterwork features and Ogryn Plate.218 supporting definitions comprise164 subclass features,42 progressions,11 choices and Acid. This does not mean52 fully automated mechanics or870 publication-ready records. All 385 original candidates have individual dispositions, source pages and reasons. Converted IDs were removed from the candidate collection; IDs are never repurposed.

## Resolutions and source verification

All 45 subclass level skeletons now have parent classes, level prerequisites, selected-subclass choices and source-cited progression features. Parent progression placeholders no longer grant the same subclass mechanics twice. Rules remain manual where effect/resource/upgrade mapping is incomplete. Some old unreferenced draft placeholder features remain reserved for editorial continuity; they are not active duplicate grants.

The extractor previously combined two tables at the same vertical position across columns. It now separates table grids by horizontal gaps:158 tables, with three restored Warlock feature rows checked against a rendered PDF page. Class level tables, not section-number suffixes, determine grant levels. Other table rows were checked for name/count/parent/level closure; this pass is not a claim of full visual review of all 125 pages.

30 species-restricted Talents and Touched by the Warp now have typed prerequisites. Three Origins have unambiguous species gates; seven remain explicitly unresolved. One apparent eligibility conflict is resolved: Aeldari Warlock access follows the specific Runes of Battle rule under §1.5. Six Origin matrix/prose conflicts remain. No starting-kit/proficiency conflict was silently resolved through invented aliases.

Damage decisions: retain13 explicit PHB types, adding Acid; keep radiant/radiation distinct; preserve explicit plus components; keep weapon families separate from damage labels; do not infer energy/physical parents or slash semantics. Two base-damage templates now carry validated typed bindings. Bloodied remains a derived state, not a condition. A shield-dependent Riot Shield AC contribution is conditional; shove advantage remains manual.

## Calculation and validation scope

[CALCULATION_POLICIES](../content/CALCULATION_POLICIES.md) assesses30 policies, including inputs, output, order, source, stacking/caps/floors and automation boundary. Offline conformance functions implement source-supported proficiency, check sums, HP acquisition, explicit armour arithmetic, advantage cancellation, critical dice, vehicle DT, pressure/perils and prerequisite logic. These tools do not implement the production character engine or fabricate a profile.

44 content tests pass: the original 17 plus 27 regression/integrity tests. Coverage includes identity/reference/digest/source closure, all subclass levels, split-table extraction evidence, prerequisites and three-valued unknowns, class/species/Origin restrictions, feature conditions, damage types/bindings, progression duplicate prevention, starting equipment evidence, calculation boundaries, defined stacking, cycle rejection and fail-closed publication. There are no complete PHB RollDefinitions to certify yet; tests validate base-template bindings and explicitly reject treating them as actor-resolved rolls. No runtime or database changes were made. Docker startup remains unverified as previously requested.

## Readiness

| Area | Result | Why |
| --- | --- | --- |
| Character Builder |**NOT_READY**|Ability modifiers, ASI, Origin rulings, starting item closure, core AC and power options remain incomplete.|
| Rules Engine |**PARTIAL**|Known policy slices are tested; no executable complete profile or runtime compiler.|
| Dice Engine |**PARTIAL**|Base typed dice and known formulas exist; actor/context/resource compilation remains incomplete.|

Manual narrative features alone do not block the builder. Missing core rules and required selections do. See [builder blockers](CHARACTER_BUILDER_BLOCKERS.md), [engine readiness](RULES_ENGINE_READINESS.md) and [dice readiness](PHB_DICE_READINESS.md).

## Remaining decisions and specification work

The exact36 human questions, each with a stable ID, are in [PHB_HUMAN_RULINGS](PHB_HUMAN_RULINGS.md). They cover six Origin conflicts, Rare/Limited, attribute modifiers, resistance/vulnerability/expertise, alternative abilities, HP changes, ASI/Talent repetition, personal weapon details, slash damage, three armour formulas, unarmoured/protection stacking, concentration, pressure rounding/floor, Warp Step, conditions/injuries, starting gear aliases/pools, Aim/cover, Hit Dice rounding and general stacking. Not all are equally necessary for a minimal creation slice; the blocker report identifies critical dependencies.

8 expanded specification/mapping issues are distinguished from human rule questions. Small proposals cover plural power lists, durations/concentration, unbounded pressure gain, open-ended tables, mounted/payload bindings, vehicle profile stats and remaining feature/roll compilation. The implemented additive damage-binding capability is documented separately; unsupported mechanics are not hidden in arbitrary fields or scripts.

## Recommended next task

**Resolve the isolated PHB rule questions, then complete and validate the minimum character-creation content package and profile.** Include required starting items, psychic choices, typed class training/resources and a closed source-reviewed ruleset lock. Only after that gate should the full data-driven Dark Imperium character builder be implemented.

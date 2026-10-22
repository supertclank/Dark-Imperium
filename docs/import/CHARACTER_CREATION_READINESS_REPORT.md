> **Current Frag gate pass:** [Results](PHB_FRAG_GATE_REPORT.md). Narrow profile PLAYABLE_WITH_MANUAL_RULES; narrow builder data READY_WITH_MANUAL_RULES. 93 tests; 948 drafts; 310 candidates. Generic Blast and 31 original rulings remain unresolved. Earlier pass statements below are historical.

> **Historical pass; superseded by [Minimum rulings report](PHB_MINIMUM_RULINGS_REPORT.md).** Current: five approved, 31 unanswered; 948 drafts, 310 candidates, 81 tests. Narrow and full playable gates remain BLOCKED.

# Human rulings integration and character creation readiness

The user confirmed that **no approved human rulings exist**. This pass integrated **0**, preserved all 36 as UNRESOLVED and made independent progress only. The full builder UI was not implemented.

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical drafts |870|874|
| Incomplete candidates |333|333|
| Human questions unresolved |36|36|
| Origin conflicts unresolved |6|6|
| Manual entries |659|659|
| Content tests passing |44|61|
| Representative draft fixtures |—|7|
| Complete valid characters |0|0|

## Work completed independently

Added four canonical creation choice pools with source citations: species 6, Origins 10, classes 12 and Universal Traits 20. Existing referenced eligibility remains binding. All 45 subclass progressions, 12 class tables, canonical reference/digest/source closure, prerequisite shapes and unambiguous policy slices validate.

Implemented an offline `validateCharacterSelection` conformance adapter with field-specific INVALID/INCOMPLETE diagnostics, known prerequisite evaluation, selected-class/subclass progression expansion, granted-choice/cardinality checks, standard-array/species increases, source base movement, proficiency, typed class training and Psyker/Warlock known-power counts. Manual text stays source-attributed and non-executable. Unapproved facts cannot satisfy an Origin gate. This is not a production API, full choice-provenance engine or playable profile.

All 12 starting-kit rows were audited without inventing aliases/quantities. All 333 candidates received creation dispositions:92 blocking initial-item/power dependencies, 82 non-blocking in the literal audit, 159 deferred/uncertain or later-level. The 92 are catalog coverage dependencies, not 92 selections required by each character. Major powers are deferred only for the level 1–3 analysis; later-level creation still needs them.

Seven mechanical regression fixtures exercise Human Veteran (the PHB's guardsman class), Ogryn, Psyker, Aeldari Outcast, Aeldari Warlock, a level 3 Veteran subclass and an illegal Human/Skitarii combination. Five pass known base eligibility; Ogryn eligibility remains incomplete; the illegal combination is rejected. Six overall drafts remain INCOMPLETE and one INVALID. None is falsely certified as a playable character. Full golden calculated outputs cannot be produced without009 and the remaining selected content dependencies.

## Rules-blocked versus implementation work

Rules-blocked: all 36 questions retain their exact IDs and no decision. See [human ruling status](PHB_HUMAN_RULINGS_RESOLVED.md) and the [prioritised minimum agenda](PHB_MINIMUM_RULINGS.md). Twelve existing questions block the full level 1–3 Origin/starting-option catalog; eight more are conditional creation blockers and sixteen can wait for runtime/optional use with their mechanics blocked. Full 1–20 support adds applicable conditional rulings. This is scope classification, not an approval or change to the game.

Implementation still needed independently of rulings: complete canonical starting item/power references, source-supported class/feature/resource/vision mappings, psychic list choices, selected-level grant/compiler coverage, a reviewed profile/lock, production eligibility/occurrence/state validation and action/RollDefinition compilation. Answering rulings alone does not finish those tasks.

Calculated draft outputs deliberately leave unknown attribute modifiers, HP, AC, initiative, skill/save totals, resources and resistances unresolved. There are no generated complete actor RollDefinitions. The two source base-damage templates remain validated, and unambiguous pressure/PB/HP-gain/DT/critical/advantage policy slices remain tested. See [calculation flow](../content/CHARACTER_CREATION_FLOW.md), [dataset manifest](CHARACTER_CREATION_DATASET.md), [equipment audit](PHB_STARTING_EQUIPMENT_READINESS.md) and [dice readiness](PHB_DICE_READINESS.md).

## Verification

**61 Python content/readiness tests pass**, including all 44 prior tests and 17 new tests. Existing example/dice fixture checks also run independently. Tests cover source-defined baselines, prerequisites, parent/unlock gates, selected-only subclass features, blocked Origin facts, malformed/duplicate/ungranted choices, illegal equipment, typed training/power counts and manual-text isolation. No test invents an approved ruling or treats missing values as zero.

Native frontend/backend test suites were attempted but could not run successfully in this environment: pnpm symlink access/dependency-junction failure and Gradle daemon connection failure; the native test PostgreSQL server was not running. Therefore a full application-suite PASS is not claimed. Application source remains unchanged.

Docker build and startup were attempted and remain **UNVERIFIED**: buildx lock access denied; Docker Desktop Linux engine named pipe missing. No container health, migration or seed/import success claimed. Exact commands and failures: [infrastructure verification](PHB_DOCKER_VERIFICATION.md).

## Readiness and next task

| Area | Result |
| --- | --- |
| Character Builder gate |**BLOCKED** (report status **NOT_READY**)|
| Rules Engine |**PARTIAL**|
| Dice Engine |**PARTIAL**, not READY_FOR_ROLL_DEFINITIONS|

Next task: **answer009 first, then024 and 051 for a narrow source-supported creation path, and complete the corresponding item/profile/compiler mapping.** For the complete initial catalog, also resolve001–007 and 049/050, then retest the gate; handle conditional rulings for selected configurations. The [minimum ruling agenda](PHB_MINIMUM_RULINGS.md) contains exact questions and deferral reasons. Do not start the full builder UI against a purportedly valid PHB lock yet.

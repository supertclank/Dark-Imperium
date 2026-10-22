# Validation contract

Publication requires structural validation, semantic validation and human source review. A syntactically valid JSON file is not necessarily a valid rule, and a valid rule is not necessarily faithful to a book.

## Structural schema

The implementation milestone should produce JSON Schema **2020-12** with `$defs` for the common envelope, ContentRef, SourceCitation, NumberValue, Dice, Distance, Predicate, Effect, ManualRule, Grant, Choice, Progression, Action and every entity payload. Use `oneOf` with a `const` discriminator per union and `unevaluatedProperties: false` after composition. Do not merely validate `data` as an arbitrary object.

Each kind's required/optional field sets are defined in ENTITY_TYPES and DOMAIN_SCHEMAS. Numeric targets/units, payload kinds and operations are constrained enums or registered profile vocabulary. Unknown keys are errors, except explicitly namespaced non-mechanical `extensions`. No implicit string-to-number conversion. Reject duplicate JSON keys before schema validation; most default JSON parsers otherwise silently keep the last value.

Schema responsibilities include:

- Envelope required fields, lengths, ID regex, positive revision, lifecycle/verification enum and nonempty sources.
- Discriminated effect/condition/value/range/target shapes and exact required fields per variant.
- Positive dice counts/sides; nonnegative distance/capacity/quantity limits; rational denominators > 0.
- Unique local IDs where structural comparison suffices, bounded arrays/strings/nesting, no null-by-default ambiguity.
- Weapon damaging modes have a damage type and dice or explicit nonzero/variable damage bonus; melee/ranged/area shapes are distinct.
- Property parameter definitions have appropriate bounds/defaults; usages have typed arguments, checked semantically against the referenced property schema.
- Manual entries cannot carry hidden automatic numeric effects. Automatic entries cannot depend on required runtime facts.

Proposed safety limits: 1 MiB per entity, 160-character ContentId, 64-character local key, 100 predicate nodes, depth 8, 500 effects per entity, 500 options per explicit choice, 100 progression levels per technical schema and 100 damage dice per component. The game profile may impose much smaller bounds. These are parser/resource ceilings, not Dark Imperium rules.

## Semantic checks

| Area | Mandatory checks |
| --- | --- |
| Identity | No duplicate identity/revision bytes; namespace ownership allowed; kind matches ID; no repurposed/deleted identity reuse |
| Release | Exact lock closure; one revision per ID; all digests match; supported schema and capabilities; source versions resolve |
| References | Referenced entity exists in the lock and has the expected kind; local IDs resolve in the stated owner revision |
| Choices | Cardinality is attainable after eligibility/exclusions; option IDs unique; bundle grants valid; repeat/exclusion scopes agree |
| Builder | No circular unlocks or self-justifying prerequisites; all required answers valid; no stale or surplus grants |
| Classes | Subclass parent is a class; class's allowed list agrees with subclass parent; progression axis and source relationships agree |
| Progression | Levels sorted/unique/in bounds; grant keys unique; replacement references strictly earlier grants in the same progression; no forward/cyclic replacement |
| Effects | Target exists with compatible unit/type; operation compatible; parameter/stat refs valid; stat dependency graph acyclic; base/stacking ties unambiguous |
| Conditions | Unknown facts remain unresolved; automatic rules do not require contextual facts; durations have valid anchors/removal policies |
| Equipment | Range bands ordered in a common unit; property arguments valid; ammo compatibility, capacity, reload and costs agree; hands/slots within applicable capacities |
| Powers/actions | Power template has no duplicate mechanical outcomes; test outcomes align; reaction trigger exists; resource cost scope/type valid; failure/Perils rule roles correct |
| Creatures/vehicles | Base stat keys known; threat scale named; valid mount/crew/system keys; typed overrides name existing modes and never mutate referenced definitions |
| Resources | Initial/current values valid under declared policy; nonnegative costs; no repeated recharge by UI reload; max dependencies acyclic |
| Taxonomy | Parent hierarchies acyclic; actual relations do not exist only as free-text tags |
| Content access | GM/private material not returned or indexed for unauthorized viewers; imported flags do not grant publication rights |

Reference cycles are not universally illegal. A class can reference a progression whose axis references that class; an adventure can link a location that links an encounter. Distinguish the **reference graph** (closure/type checks), **containment/taxonomy graph** (acyclic where defined), and **calculation/unlock graph** (must be acyclic). Rejecting every cycle would reject valid content; accepting every cycle would allow unbounded grants/calculation.

Choice satisfiability must consider exclusions and prerequisites, not just option count. A “choose 2” pool with two mutually exclusive options is invalid. For complex bounded combinations, use a bounded solver/enumeration in the validator; if the validation budget is exceeded, block publication for manual review rather than assert validity. A content validator cannot prove every future runtime context; it must distinguish impossible creation choices from conditionally available actions.

## Validation stages

| Stage | Work | Result |
| --- | --- | --- |
| Editing | Immediate field/union checks, reference pickers, source completeness, preview calculations | Inline errors; incomplete drafts may be saved, cannot publish |
| Extraction/import staging | Duplicate detection, source anchors, normalize units/IDs, parse structure, unresolved-rule issue queue | No direct writes to published tables |
| Candidate assembly | Full dependency closure, semantic checks, capability/lock validation and impact diff | Deterministic report and review candidate |
| CI | Schemas, all examples, golden cases, negative fixtures, digest stability, link checks, migration compatibility | Fail closed on unsupported mechanics/unresolved required references |
| Application startup | Validate configured published lock/digests/capabilities once; cache valid immutable artifacts | Do not serve mechanics from an invalid lock; existing unrelated valid locks may remain available |
| State mutation | Ownership, expected state version, current prerequisites/costs, complete draft and transactional invariants | Reject conflicts/invalid actions with structured errors |

An existing draft may have unresolved references only when explicitly marked incomplete. Placeholder/manual content is not a bypass for malformed structures. Production lock policies determine whether reviewed manual rules are allowed; placeholder test fixtures remain excluded by default.

## Diagnostics

Return `{code,severity,entityId,revision,jsonPointer,sourceLocator?,message,relatedIds?,suggestedFix?}`. Use stable codes such as `REFERENCE_NOT_FOUND`, `REFERENCE_KIND`, `UNKNOWN_OPERATION`, `CHOICE_UNSATISFIABLE`, `CALCULATION_CYCLE`, `LOCK_DIGEST_MISMATCH`, `SOURCE_REVIEW_REQUIRED`. Never expose hidden GM text or internal filesystem paths in a player's diagnostic.

Errors block publication; warnings require explicit reviewer disposition; informational notices do not change legality. A source transcription uncertainty is an editorial issue, not a silently chosen default.

## Required future conformance cases

- Human + Guardsman fixture calculates movement 6 and maximum wounds 10; Ogryn + Guardsman calculates movement 5 and maximum wounds 14. These test fixture arithmetic, not real game rules.
- Conditional two-handed damage adds 2 only for the selected attack weapon carrying that property; an unrelated carried weapon does not qualify. Missing attack context yields unresolved, not an unconditional bonus.
- Manual contacts adds no numeric bonus. Recorded adjudication creates a separate bounded temporary instance with provenance.
- Replacement of level-one steady-hands grant retracts that source only; another independent proficiency source survives.
- Multiple base armour values cannot be silently added; illegal slot combinations fail before calculation.
- Once-per-rest cost cannot be spent twice concurrently; duplicate rest occurrence cannot recharge twice.
- 1d8→1d10 revision update leaves the old lock's attacks unchanged; migration requires an explicit new lock.
- Absent damage type, inverted range, wrong-kind property, invalid subclass parent, missing feature, impossible choice, duplicate local IDs, unknown capabilities and embedded script fields fail validation.

This task supplies specification/example checks, not the production schema validator, interpreter or all conformance tests. Those are the recommended next implementation task after rules clarification.

## Integrated dice extension

Future dice validation must enforce bounded dice/counts/modifiers; unique groups/components; disjoint complete kept/discarded partitions; face ranges; deterministic keep ties; arithmetic/provenance integrity; single-kept-die natural selection; policy availability; critical detection from natural rather than total; and no doubled advantage or literal damage bonus. Validate audience authorization, stale snapshots, idempotency collisions and costs across retry/multi-stage execution. Manual total-only reports must not acquire fabricated faces or server authority. See [Integrated dice rolling](DICE_ROLLING.md).

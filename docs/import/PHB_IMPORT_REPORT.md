# PHB import report — first staged slice

Date: 22 October 2026. **Partial import; not a published ruleset and not ready for the full builder.** No gameplay, frontend, backend or database migration changes were made.

## Source

- Filename: `dark_imperium_player_handbook (2).pdf`
- Visible version: Version 1.0; 125 PDF pages.
- SHA-256: `a58335b1264ac40e30ff0b310626d306fc88f7003e0c3af345e0d55c978e94b7`
- Selected because the user supplied this exact file; no competing project PHB was found. Newest outside this project is unverified.
- Immutable project copy: [PHB](../../content/sources/phb-1.0-a58335b1.pdf). Registry and citations distinguish printed/PDF page numbers. No rulebook versions or example-fixture mechanics were mixed.

## Inventory and structured output

The [inventory](PHB_CONTENT_INVENTORY.md) spans all 22 chapters and 156 extracted tables, with 2506 evidence/entity/candidate ledger rows. These overlap and are **not** a unique-content total. The ID registry allocates 985 draft/reserved identities.

There are **600 canonical draft records** and **385 incomplete review candidates**. Every canonical record is draft/transcribed, never authoritative. Candidates retain source text and available fields but are deliberately outside the importer. Many canonical features are manual or incomplete mappings; the record count is not an automation count.

| Kind | Canonical drafts | Review candidates |
| --- | ---: | ---: |
| action | 2 | 9 |
| ammunition | 0 | 7 |
| armour | 1 | 25 |
| augmetic | 0 | 22 |
| background | 10 | 0 |
| choice | 17 | 0 |
| class | 12 | 0 |
| condition | 0 | 16 |
| consumable | 0 | 1 |
| damage_type | 12 | 0 |
| equipment | 0 | 37 |
| feature | 367 | 9 |
| power | 0 | 52 |
| proficiency | 15 | 0 |
| progression | 15 | 0 |
| property | 31 | 0 |
| rule | 93 | 0 |
| shield | 1 | 2 |
| skill | 15 | 0 |
| species | 6 | 0 |
| subclass | 3 | 42 |
| system | 0 | 41 |
| vehicle | 0 | 12 |
| weapon | 0 | 110 |

The feature count includes 50 Talents (`flavor:feat`), 20 Universal Traits, species/Origin bundles, class-feature entries and Veteran subclass benefits. All 12 classes have 20 level rows. Only 3 of 45 subclasses have explicit canonical progressions. Weapons, 52 psychic powers, 12 vehicles and 16 conditions/states are inventoried/candidate-staged, **not fully converted**. Two base-dice action templates are present; complete actor-resolved RollDefinitions: 0. Starting equipment source rows are retained, but resolved equipment-choice records: 0.

## Validation

Run from the project root:

```text
python tools/content_import.py
python -m unittest discover -s tests/content -v
python tools/content_import.py --plan <private-output-path>.jsonl
```

Results: 17 tests passed. Draft validator passed all 600 records for the supported import subset, exact source versions, IDs, reference closure, parent/progression links, choice cardinality, fixed effects, dice bounds, unknown-field rejection and manifest digests. Tests also exercise duplicate JSON keys, invalid references/dice/choices, immutable-revision conflict, deterministic plans, identical re-import no-op and publication rejection.

Representative source tests cover species, Origins, class levels, Veteran subclasses, starting-equipment evidence, Lasgun candidate, armour, properties, feats, manual conditional features, power/vehicle evidence and base-roll templates. **They are not runtime tests of unfinished weapon, power, vehicle, condition or builder engines.** No full JSON Schema 2020-12 implementation is claimed; the validator deliberately accepts only this emitted subset and rejects unsupported fields. Complete publication/semantic/source review remains outstanding.

Original PDF SHA and manifest content digests are checked. PDF pages 23, 37 and 50 were rendered; representative layouts/tables were visually inspected. Full-book text/table extraction is retained, but not every cell has independent visual review. Candidate completeness and source fidelity cannot be proven by structural tests alone.

Application builds/database tests were not rerun because application code and migrations are unchanged. Docker startup remains unverified as previously requested.

## Review and coverage

There are 16 grouped open issues: 6 AMBIGUOUS, 3 MISSING_REFERENCE, 1 DUPLICATE_OR_CONFLICT, 4 SPEC_EXTENSION_REQUIRED and 2 MANUAL_RULE backlog groups. These are grouped findings, not claimed counts of every ambiguous sentence. See [review required](PHB_REVIEW_REQUIRED.md) and [cross-reference audit](PHB_CROSS_REFERENCE_AUDIT.md).

Coverage estimate: all major categories are inventoried; 6/6 species, 10/10 Origins and 12/12 class identities/progression tables have partial canonical drafts; 3/45 subclasses have mapped progressions; 2 explicit armour/shield records form the equipment slice. Most feature clauses are MANUAL_ONLY or PARTIALLY_STRUCTURED. 83 records have READY technical mapping status, but none forms a publishable package by itself. Whole-book executable coverage is not meaningfully measurable yet; **publishable coverage is 0%**. This is intentionally not a 100% completion claim.

## Database preparation and next step

Canonical source is one JSON file per entity. `content_import.py --plan` emits deterministic candidate operations ordered by permanent ID. The planning API accepts existing (id, revision) digests, returns no_op for identical content and rejects different bytes at the same immutable revision. It does **not** write PostgreSQL or publish a lock. Existing runtime tables do not yet represent the full revision/package/source/lock contract.

The eventual PostgreSQL adapter must stage these operations in one transaction, map canonical IDs to storage UUIDs, preserve immutable revisions/source citations, validate the complete dependency closure and publish only after source review. A failed operation rolls back the candidate transaction. No handwritten SQL game-content inserts were added.

Recommended next task: resolve PHB-001–016 and complete a source-reviewed, end-to-end PHB creation slice with a playable profile/lock, then expand remaining subclass/equipment/power mappings. The full data-driven character builder follows once [readiness gates](PHB_BUILDER_READINESS.md) pass.

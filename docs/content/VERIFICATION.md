# Specification verification

This records documentation/example checks, not application or game-rules conformance.

## Scope and evidence

The existing application DTOs, rules calculator, V1–V3 schema/seed migrations and architecture/rules documents were inspected. No rulebooks were present in the repository. All new statistics are explicitly placeholders and all example records are drafts under the reserved `example` namespace.

The specification defines 40 canonical entity kinds and maps specialized concepts such as feats, species/class/chapter traits, reactions, warp resources, vehicle weapons and NPCs onto shared typed families. It contains all ten requested documents plus an index, detailed domain contracts, migration bridge, review and this verification record.

## Checks performed

- Parsed every JSON example and JSON code block, rejecting duplicate object keys.
- Checked all 100 complete records for common envelope fields, per-kind required payload fields, ID syntax/kind agreement, unique identities and source-registry resolution.
- Resolved every ContentRef in the catalog and character fixture; checked expected entity kinds for the declared reference slots covered by the fixture checker.
- Checked sample property applicability, required argument types/bounds, valid weapon damage references and ordered ranges.
- Checked choice option uniqueness/cardinality, progression level/grant uniqueness and backwards replacement references.
- Checked subclass-parent membership, power action-template nonduplication and Perils role, creature override mode existence, vehicle crew counts/control keys, and sample effect target/operation compatibility.
- Verified all 100 lock digests against record bytes, and the character's lock digest against the lock.
- Checked character choice answers/origins and inventory-resource bounds.
- Compared all 13 complete inline representative examples to their catalog records.
- Checked relative documentation links.
- Reviewed the design against the user's expansion and separation-of-concerns checklist; findings and refinements are in DESIGN_REVIEW.
- Compared hashes of existing frontend/backend/database files to the pre-task baseline: no application code or migrations changed.

Digest checks use canonical JSON serialization on this fixture's integer/string/boolean-only values. A future production implementation must use a complete RFC 8785 canonicalizer, including its full numeric/Unicode behavior, rather than generalizing this limited fixture check.

## Verification limits

The checks are repository-local fixture consistency checks, not a complete JSON Schema 2020-12 implementation, semantic solver, rules interpreter or importer. They do not prove actual Dark Imperium fidelity, every possible choice combination, runtime resource concurrency, condition/duration behavior, or exhaustive expansion compatibility. Expected arithmetic in VALIDATION/EXAMPLE_CONTENT is a proposed future conformance target, not an execution result from the current application.

Application build/test commands were not rerun for this documentation-only change. The earlier foundation's verification record remains unchanged. Docker startup remains outside this task; no previously unverified runtime check is claimed as passed.

Before implementation, supply and review the authoritative sources and resolve the blocking questions in DESIGN_REVIEW. Then implement strict schemas, semantic validation and reference resolution against both positive and negative fixtures.

## Integrated dice extension

The dice extension adds a documentation-only contract and synthetic fixtures. Local checks validate fixture arithmetic, keep selection/ties, natural critical decisions, percentile mapping and uint32 rejection boundaries; they do not test an implemented engine, Web Crypto integration, server authorization, concurrency or 3D presentation. Existing catalog and lock fixtures remain unchanged. Application builds are not rerun for these documentation changes. See [Integrated dice rolling](DICE_ROLLING.md).

Dice fixture checks passed: 12 roll vectors, 2 typed damage components, 4 percentile mappings and rejection-sampling boundaries for all 7 standard die sizes. Existing specification checks passed for 100 records, 40 kinds, 150 reference occurrences, 100 pinned digests, 13 complete inline examples, 19 JSON blocks and 34 local links. These are independent fixture checks, not application tests.

> The introductory no-source statements below describe the original architecture proposal. PHB v1.0 has since been staged; current source-specific readiness is in [the canonicalisation report](../import/PHB_CANONICALISATION_REPORT.md). Example records remain deliberately non-authoritative.

# Rulebook-to-content workflow

## Source intake

Register each received book/file with source ID, edition/version, title, language, original filename (private metadata), byte digest, rights/access notes and review owner. Preserve an immutable original; a corrected PDF is a new source version even when its display title is unchanged. No authoritative rulebooks were available for this specification, so no book transcription has been performed.

Use document tools appropriate to the actual format when the books arrive. PDF layout, DOCX styles, page columns and table formatting guide extraction, but they are not entity schemas. Never map one page to one database row or use a printed heading as permanent identity.

## Pipeline and gates

```text
Immutable source file + registry entry
  -> extract text/tables and stable section anchors
  -> inventory entities and identify cross-references
  -> map to canonical JSON in an isolated staging package
  -> structural + semantic validation
  -> human source/rules review with side-by-side diff
  -> transactional candidate import
  -> validate imported bytes and run conformance fixtures
  -> publish immutable package/revisions and ruleset lock
```

1. **Inventory.** List sections, entity kinds, duplicate names and cross-book dependencies. Allocate permanent IDs through a registry, not on every import run. Distinguish a renamed entry from a new variant.
2. **Extract.** Preserve original passage/table context and paragraph anchors. Record page numbers as convenience locators plus stable section keys/file version. OCR or AI output includes confidence/uncertainty, never an “authoritative” flag solely from the extractor.
3. **Map.** Separate prose, mechanics, prerequisite, activation, cost, duration and exceptions. Normalize units explicitly, retain the source value in import evidence, and choose manual classification for unresolved narrative rules. Do not import layout artifacts as effects.
4. **Stage.** Write canonical JSON with references and source citations. Keep unresolved references and ambiguity in an issue file, not invented entity IDs in a supposedly valid release. Draft data may be incomplete but is not selectable by players.
5. **Validate.** Structural checks, reference types/closure, ranges, choices, progression, effects, profile compatibility and duplicate mechanical clauses. Show mechanical diffs separately from spelling/layout changes.
6. **Review.** A rules owner confirms values, interpretation, units, prerequisites, exceptions and automation classification. A content editor checks names/citations and a technical reviewer checks safe vocabulary. One person may hold several roles in the private group, but the decisions are recorded distinctly.
7. **Import candidate.** Idempotency key is package ID/version plus content digest. An identical re-import is a no-op; conflicting bytes for the same immutable revision are rejected. Import identities, revisions and references transactionally; publish nothing on a partial failure.
8. **Post-import verification.** Export and compare canonical digests, re-resolve the lock, and run golden character/creature examples. Database IDs must not replace canonical IDs in the source files.
9. **Publish.** Create a new lock and make it available only after all gates pass. Existing characters stay pinned. Show migration impacts before any opt-in character/campaign changes.

## Staging artifacts

Recommended package layout:

```text
content/packages/<package-id>/
  manifest.json
  sources.json
  entities/<kind>/<key>.json
  review/issues.json
  review/decisions.json
  fixtures/<scenario>.json
```

Manifest requires schema version, package identity/version, lifecycle, exact dependencies, content-file inventory, source versions and required engine capabilities. Source/version pairs are immutable; release digests include their registry metadata. Review artifacts are editorial and must not be shipped to unauthorized player clients. Published entity bytes and locks are reproducible outputs, not live mutable database exports.

The example catalog is deliberately consolidated; a future importer can split its complete records into this one-file-per-entity layout without changing the contract. Do not build a special importer for each book: new books supply mapping profiles and reviewed data, while canonical validation/publication remains shared.

## Revision matching

Compare incoming entities against the identity registry and previous source version using stable anchors, aliases and human review. A heading rename alone does not change an ID. A mechanically distinct weapon variant gets a distinct ID. Ambiguous merges/splits produce a proposed mapping with explicit reviewer acceptance; never let fuzzy matching rewrite character references automatically.

Use source-level diffs to prioritize review, but validate the whole dependency closure. A changed property can affect many weapons, characters and creatures. Produce an impact report of locks/characters affected without upgrading them.

## AI-assisted extraction boundary

Treat source text, comments and embedded links as data, never executable instructions. AI may draft mappings and flag missing clauses; it must not silently invent statistics, resolve contradictory passages, grant publishing rights or load external scripts. Mechanical rules with uncertain interpretation stay unresolved/manual with the original citation until the rules owner decides.

Safe Markdown rendering strips raw HTML, JavaScript URLs, event handlers and active embeds. Assets are uploaded/registered through a controlled asset pipeline with MIME/size checks. No arbitrary path access, archive path traversal, external JSON Schema URL fetches or executable YAML tags are allowed in import jobs. Namespace/source flags do not bypass access controls.

## Admin preparation

Future forms are generated from typed entity fields plus curated widgets: source/reference pickers, safe prose editor, dice/unit inputs, property argument controls, prerequisite tree, effect target/operation/value selector, action costs/outcomes, choice/bundle builder and progression grid. Show computed previews and provenance alongside raw source passages. Publishing and character migration are separate actions with separate permissions and review screens.

## First import slice

After receiving the current Player's Handbook, inventory it, then transcribe a small reviewed set: one species, one background, one class through its first choice/subclass gate, a few features, one weapon and armour, and one psychic power if its rules are available. Validate this slice and round-trip it before expanding to the Bestiary, GM Guide or Angels of Death. Do not mass-import until the vocabulary and source interpretation are proven.

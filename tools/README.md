> **Current Frag gate pass:** [Results](../docs/import/PHB_FRAG_GATE_REPORT.md). Narrow profile PLAYABLE_WITH_MANUAL_RULES; narrow builder data READY_WITH_MANUAL_RULES. 93 tests; 948 drafts; 310 candidates. Generic Blast and 31 original rulings remain unresolved. Earlier pass statements below are historical.

> **Current pass:** [Minimum rulings and narrow proof](../docs/import/PHB_MINIMUM_RULINGS_REPORT.md). Five rulings approved, 31 unresolved. 948 canonical drafts; 310 candidates; 81 content tests pass. The narrow core calculates, but a mandatory Frag Grenade save outcome keeps playable readiness BLOCKED. Earlier sections below describe historical scope.

# PHB content tools

## Character creation readiness adapter

`character_creation.py` provides offline `validateCharacterSelection(characterDraft)` validation and partial projection against the existing CharacterModel selections. Run its regression fixtures with `python -m unittest discover -s tests/content -v`. It does not publish content or authorize gameplay. All 36 human rulings remain unresolved; current representative drafts are INCOMPLETE or INVALID, never complete valid characters.

See [creation flow](../docs/content/CHARACTER_CREATION_FLOW.md), [current readiness report](../docs/import/CHARACTER_CREATION_READINESS_REPORT.md) and [prioritised ruling agenda](../docs/import/PHB_MINIMUM_RULINGS.md). Fixture inputs and expected results are in `tests/fixtures/characters`; source-derived audit results are in the package's `review` directory. Client-supplied facts cannot approve unresolved rules.

`content_import.py` uses only Python's standard library. Run `python tools/content_import.py` and `python -m unittest discover -s tests/content -v` from the project root. `--plan output.jsonl` writes deterministic private staging operations; it never connects to PostgreSQL. `--publication-check` is expected to fail for this incomplete draft package.

The validator is intentionally limited to the structures emitted by this first slice, including canonical drafts and the known fields of quarantined candidates. It is not a complete JSON Schema or game engine. Manual clauses, missing profile policies and source ambiguity are publication blockers even when technical validation passes.

Optional source extraction uses `python tools/extract_phb.py <source.pdf> <scratch-output-directory>`. Install the pinned extraction requirements separately if needed. These libraries are tooling dependencies, not additions to the Kotlin/Next.js runtime. The extractor uses table grid lines/column boundaries and excludes coloured section-heading gaps; generic PDF extraction initially missed alternate shaded rows, which is why representative rendered pages were inspected. Review all extracted cells before publication. Text evidence was extracted with pypdf6.10.0; pdfplumber0.11.9 supplied table cells; pypdfium2 supplied visual-review renders. No OCR was required.

Canonical JSON is the editable source of truth after transcription. Do not regenerate permanent IDs from renamed headings. `CONTENT_MANIFEST.json` is the reserved identity registry; candidate promotions must preserve or explicitly deprecate identities rather than silently reuse IDs. No human decisions have been prefilled in review/decisions.json.


## Canonicalisation conformance tools

`phb_policies.py` contains pure offline source-policy conformance functions and a three-valued prerequisite evaluator. It is not imported by the application. The strict validator now supports the additional used prerequisite/conditional shapes and damage-template bindings; it still is not a complete JSON Schema implementation. Tests run with `python -m unittest discover -s tests/content -v`.

The table extractor separates independent tables at matching vertical coordinates by horizontal grid gaps. The review folder carries all385 original candidate dispositions, all45 subclass level mappings, policy/eligibility/manual ledgers and the58 expanded issues. `decisions.json` contains source-supported interpretations; its human-ruling array remains empty. Do not rerun the historical intake generator over canonical edits.

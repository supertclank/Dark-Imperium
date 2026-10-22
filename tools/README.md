# PHB content tools

`content_import.py` uses only Python's standard library. Run `python tools/content_import.py` and `python -m unittest discover -s tests/content -v` from the project root. `--plan output.jsonl` writes deterministic private staging operations; it never connects to PostgreSQL. `--publication-check` is expected to fail for this incomplete draft package.

The validator is intentionally limited to the structures emitted by this first slice, including canonical drafts and the known fields of quarantined candidates. It is not a complete JSON Schema or game engine. Manual clauses, missing profile policies and source ambiguity are publication blockers even when technical validation passes.

Optional source extraction uses `python tools/extract_phb.py <source.pdf> <scratch-output-directory>`. Install the pinned extraction requirements separately if needed. These libraries are tooling dependencies, not additions to the Kotlin/Next.js runtime. The extractor uses table grid lines/column boundaries and excludes coloured section-heading gaps; generic PDF extraction initially missed alternate shaded rows, which is why representative rendered pages were inspected. Review all extracted cells before publication. Text evidence was extracted with pypdf6.10.0; pdfplumber0.11.9 supplied table cells; pypdfium2 supplied visual-review renders. No OCR was required.

Canonical JSON is the editable source of truth after transcription. Do not regenerate permanent IDs from renamed headings. `CONTENT_MANIFEST.json` is the reserved identity registry; candidate promotions must preserve or explicitly deprecate identities rather than silently reuse IDs. No human decisions have been prefilled in review/decisions.json.

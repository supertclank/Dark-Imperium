# Content and ruleset versioning

## Four independent versions

| Axis | Example | Purpose |
| --- | --- | --- |
| Format | `schemaVersion: 1` | Parser/contract compatibility |
| Source edition | `sourceVersion: "draft-2026-10"` | Which book/file was transcribed |
| Content revision | `(example.weapon.lasgun, 2)` | Immutable change to one entity |
| Ruleset lock | `id: example.ruleset.foundation`, `revision: 1` | Exact complete playable set and policies |

Source edition labels need not be semantic versions. Content/lock revisions are increasing positive integers within identity. Release packages use ordinary version labels and exact dependency versions. A lock has exactly one revision per ContentId, plus SHA-256, one profile reference, package identities, source-registry identities, required engine capabilities and an audience/verification policy.

Published content is immutable, including text, tags, sources and mechanics. Draft edits are mutable under optimistic concurrency until publication allocates a revision; exporting two different bytes for a published `(id, revision)` is an error. Drafts can be previewed in isolated draft locks but never leak into a campaign's published lock. Verification and lifecycle are editorial states, not authorization tokens.

## Default policy: pin, then migrate explicitly

New characters pin the selected ruleset lock. Campaign membership may require a campaign lock, but joining does not silently rewrite character selections: validate compatibility, show a diff and ask the owner/GM to accept an allowed migration. Existing characters never follow “latest” automatically. Standalone characters choose their own eligible lock. Runtime encounters pin the actor snapshots/lock used when they begin; a book update cannot change an attack halfway through resolution.

If Lasgun changes from 1d8 at revision 1 to 1d10 at revision 2, lock A continues to resolve revision 1. A newly published lock B may choose revision 2. Migration A→B previews attack differences, changes in prerequisites, invalidated choices and resource limits, then atomically updates the character's lock and any explicitly approved state transformations. The old lock remains available for audit/replay of saved reports, without implementing event sourcing.

Pure display errata also receive a new revision so pinned citations and descriptions remain reproducible. A UI can offer a newer-edition notice without replacing the pinned rules. Separate translation assets can later have their own release policy.

## Publication and dependencies

1. Assemble candidate package plus exact dependencies.
2. Resolve the transitive reference closure and check expected kinds.
3. Reject duplicate ContentIds with conflicting revisions. There is no implicit load-order override.
4. Validate profile/capability compatibility, references, progression/choice cycles and example calculations.
5. Review source fidelity and mechanical diffs.
6. Create immutable records and the lock atomically; only then make the lock selectable.

A homebrew fork receives a new namespace/identity and may link `variantOf` to an original. To replace a canonical choice in a campaign, the campaign publishes a new lock containing an explicit selection pool with the homebrew option. Arbitrary JSON patches and package precedence are not rules-resolution mechanisms.

## Deprecation, withdrawal and deletion

Deprecated definitions remain resolvable in old locks and may suggest `replacedBy`. They are hidden from new-choice defaults unless the lock explicitly permits them. Withdrawn content is unavailable to newly published locks; retained historical access follows rights/security policy. If historic bytes must be removed for a legal/security reason, old actors become explicitly unavailable for calculation rather than falling forward to another revision. Never reuse the ID.

## State migration

Migration plans specify old/new lock digests, changed references, invalid answers, resource reconciliation and human approvals. Examples: clamp current wounds to a new maximum only under an approved policy; preserve missing charges as an explicit unresolved issue; replace a removed feature grant by its declared successor. Recalculation alone must not heal a character, replenish ammunition or silently discard inventory.

Each migration records timestamp, actor/approver, from/to lock, reason, expected character state version and a before/after summary. Keep a bounded pre-migration snapshot for reversal where permitted. Concurrent state edits cause a conflict and a fresh preview. This is transaction/audit history, not an event-sourced gameplay architecture.

## Foundation compatibility

The current application follows mutable content rows and UUID references. It does not implement locks, immutable content revisions or migration previews. See FOUNDATION_MAPPING for an additive transition; this proposal does not retroactively change current sheet behavior.

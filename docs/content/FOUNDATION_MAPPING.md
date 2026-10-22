# Bridge from the existing foundation

This task changes documentation and example data only. Existing application source, migrations, endpoints and behavior remain unchanged. The new contract is a proposed future boundary, not a description of already implemented support.

| Existing foundation | Proposed canonical contract | Safe transition |
| --- | --- | --- |
| UUID species/class/weapon IDs plus slugs | Permanent namespaced ContentIds with immutable revisions | Add a unique identity mapping; preserve UUID FKs and explicitly map old seed identities |
| Mutable content rows and integer `version` | Immutable revisions plus ruleset locks | Add revision/lock tables and pin existing characters through a reviewed one-time migration |
| Species/class inline `rules.effects` | Feature refs with typed effect targets, conditions and provenance | Adapt existing movement/max-wounds effects into first-class feature records; retain old evaluator until new contract tests pass |
| String target `movement` / `maxWounds` and `add` | Registered `stat` target with key `movement` / `max_wounds`, typed value, activation, duration and stacking | Explicit adapter; do not feed new JSON directly into current Kotlin DTOs |
| Weapon damage/ranges as columns, property labels/parameters | Attack modes, damage components, property refs, units, costs and metadata | Map the single current weapon mode into a full default mode; no behavior invented from a label |
| V3 shared item identity with weapon detail table | Same item identity principle plus versioned definitions and owned instances | Extend detail kinds additively; keep equipment/ownership constraints |
| Character equipment rows with item ID/quantity/equipped | Instance UUIDs with definition refs, resource/ammo/attachment state | Existing row UUID can become an instance identity; new mutable fields need explicit defaults/reconciliation |
| Current attributes/wounds stored; max/movement derived | Broader separation of base state, runtime context and calculated projections | Retain persisted facts; add engine/lock/state versions before caching expanded projections |
| Level-one builder with three content selections | Profile creation plan plus reusable choice/grant occurrences and progression | Introduce one generic choice slice before adding more classes or bespoke UI |
| Direct mutable content reads | Resolve through a validated lock | Update services centrally; do not scatter revision selection into UI components |

## Constraints on adoption

Do not edit V1–V3 once applied. Future migrations must preserve user IDs, character ownership, names, equipment and current wounds. Decide whether legacy seed placeholders become a private legacy lock or are replaced through explicit owner review. The sample `example.*` namespace must not be mistaken for approved publisher data.

Current `rules.schemaVersion = 1` and this proposal's envelope `schemaVersion = 1` are different contracts. Name the adapters explicitly; matching integer values do not imply wire compatibility. The future implementation should use an unambiguous media/schema identifier alongside its version when transporting canonical documents.

The legacy calculator starts maximum wounds at zero, adds effects and clamps the result to at least one. The demonstration profile instead has base one and an explicit Guardsman `base: 10` effect. A future adapter must preserve the legacy base-zero-then-clamp policy, or explicitly review/normalize that contribution; blindly mapping legacy `add: 10` onto the demo base one would incorrectly produce 11 wounds. Matching example totals is not proof of wire-format compatibility.

The existing frontend/API UUID routes continue to work until a planned API change. Proposed compendium ContentId URLs are new endpoints, not a silent replacement of character UUIDs. Session/ownership protections stay in the existing backend; content JSON cannot grant user permissions.

## Recommended implementation sequence

1. Resolve the blocking game-rule questions and approve a small vocabulary/profile.
2. Implement canonical structural/semantic validation and reference resolution as a pure module, with the example fixtures and negative cases.
3. Add immutable revision/lock persistence with an adapter for the current seed slice; test migration and old-lock stability.
4. Implement the initial automatic/conditional projection evaluator and provenance, without resource-spending runtime features.
5. Wire one generic builder choice and version-pinned sheet read into the existing vertical flow.

Only then add action transactions, resources, progression, publishing UI and larger book imports. No microservices, generic scripting or event sourcing is required.

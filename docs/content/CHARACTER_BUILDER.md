> The introductory no-source statements below describe the original architecture proposal. PHB v1.0 has since been staged; current source-specific readiness is in [the canonicalisation report](../import/PHB_CANONICALISATION_REPORT.md). Example records remain deliberately non-authoritative.

# Data-driven builder and progression

No rulebook is available, so the proposed order is a configurable example, **not the verified Dark Imperium creation sequence**. A locked profile defines steps with stable IDs, display labels and references to reusable choice/input definitions. The client renders those definitions; the server computes eligibility and validates the completed draft.

## Profile creation plan

```json
{
  "creationPlan": [
    {"id":"identity","input":"name"},
    {"id":"species","choice":{"id":"example.choice.creation.species"}},
    {"id":"background","choice":{"id":"example.choice.creation.background"}},
    {"id":"class","choice":{"id":"example.choice.creation.class"}},
    {"id":"attributes","input":"attributes"},
    {"id":"granted_choices","input":"pending_choices"},
    {"id":"review","input":"review"}
  ]
}
```

`name`, `attributes`, `pending_choices`, `review` are known generic widgets. Skills, feats, equipment and powers appear as pending choice occurrences unlocked by selected content/level. Separate optional display groups may organize them in the approximate order skills → class choices → feats → equipment → powers, but dependencies determine eligibility. No bespoke Guardsman/Psyker/Astartes screen is needed. Identity inputs are not hidden rule expressions.

## Choice entity

Required payload: `purpose`, `selectionMode`, `cardinality`, `options`, `repeatScope`. Optional: `requirements`, `pool`, `exclusions`, `allocation`, `presentationGroup`, `helpMarkdown`.

- `purpose`: `species`, `background`, `class`, `subclass`, `skill`, `feature`, `feat`, `equipment`, `power`, `affiliation` or `attribute`.
- `selectionMode`: `options` or `allocation`. `options` mode requires explicit options or a pool; allocation requires its bounded allocation contract.
- `cardinality`: `{min,max,unique}`. Count selected option IDs, not total items granted by a bundle.
- `repeatScope`: `once_per_actor`, `once_per_grant`, or `repeatable`; profile rules may additionally cap recurrence.
- Each option is `{id,label,grants,requirements?,exclusiveGroup?}`. Its local `id` remains stable across revisions. Grants are typed instructions below. All grants in an option are atomic.
- `pool`: optional `{kind,ids?,requiredTags?,excludedIds?}`. A pool query is a bounded declarative selector over the **locked** catalog only, never SQL or an external search. Explicit and pooled options may not duplicate the same semantic selection. Generated option keys use the selected ContentId, not array position.
- `exclusions`: explicit `{withChoice?,withOption?,withContent?}` conflicts. At least one target is required; symmetric exclusion is validated whether one or both sides declares it.

### Grant contract

Each grant is `{id,kind,...}`. Allowed `kind` values and required fields:

| Kind | Fields | Meaning |
| --- | --- | --- |
| `select` | `content` | Record a selection of an allowed content kind |
| `feature` | `feature` | Activate a reusable feature |
| `proficiency` | `proficiency` | Grant a proficiency |
| `item` | `item`, `quantity` | Acquire owned item(s) once; not on every recalculation |
| `power` | `power` | Acquire a power selection |
| `choice` | `choice` | Open a child choice occurrence |
| `attribute_increase` | `attributeKey`, `amount` | Apply a recorded advancement increment subject to caps |
| `resource` | `resource` | Establish a resource entitlement; initial value follows its definition |

Acquisition transactions are idempotent by grant occurrence and grant key. Reopening a draft/sheet cannot grant equipment again. Retracting an invalidated choice affects draft entitlements; already-played character changes require a migration/respec policy rather than automatic inventory deletion.

### Bundle example

```json
{
  "purpose":"equipment",
  "selectionMode":"options",
  "cardinality":{"min":1,"max":1,"unique":true},
  "repeatScope":"once_per_grant",
  "options":[
    {"id":"line_kit","label":"Lasgun and combat knife","grants":[
      {"id":"primary","kind":"item","item":{"id":"example.weapon.lasgun"},"quantity":1},
      {"id":"backup","kind":"item","item":{"id":"example.weapon.combat_knife"},"quantity":1}
    ]},
    {"id":"close_kit","label":"Shotgun and sidearm","grants":[
      {"id":"primary","kind":"item","item":{"id":"example.weapon.shotgun"},"quantity":1},
      {"id":"backup","kind":"item","item":{"id":"example.weapon.sidearm"},"quantity":1}
    ]}
  ]
}
```

One-skill-from-four is the same shape with one `proficiency`/`select` grant per option and cardinality 1. Unknown Founding's illustrative two-trait selection uses cardinality 2 and a locked feature pool. It does not establish that those are the actual rules. The complete fixture includes both choices and their referenced options.

Allocation mode uses `{budget,minPerKey,maxPerKey,allowedAttributeKeys,totalPolicy:"exact"|"at_most"}` with integer units. Point-buy costs require a reviewed table in the profile; rolled attributes record roll evidence and assignments separately. Never assume a D&D point-buy table. Feat-versus-attribute improvement can be an ordinary choice with a child bounded allocation option.

## Dependencies and invalidation

The dependency graph includes parent selections, progression grants, prerequisites and exclusions. Evaluate it topologically; cycles, self-justifying prerequisites and mutually unlocking choices are publication errors. Source requirements reference content IDs/tags/proficiencies, not labels. Class equipment choices, subclass level gates, psyker disciplines and chapter restrictions all use these primitives.

When species/class/chapter changes in a draft: retain entered text and previous answers, recompute eligibility, mark invalid dependent answers `stale`, list affected choices and require correction. Do not silently reselect the first valid option or erase user input. Submit only when all required occurrences are valid and reviewed. The API revalidates against the same lock and expected draft version in one transaction.

Unknown runtime facts cannot satisfy builder requirements. Prerequisites requiring human adjudication must be explicitly approved and recorded, or remain blocked. Owning an item does not imply proficiency; an item requirement separately specifies whether it restricts selection, equip, or action use.

## Reusable level progression

`progression` payload requires `axis` (`total_level` or `class_level` with explicit class reference), `maxLevel`, and ordered `entries`. Each entry has a positive `level` and `grants` list. Each grant has a globally unique local key within this progression, optional `requirements`, and optional `replaces` list of earlier grant keys. The grant kind uses the same contract as choices. Replacement removes only that progression source's entitlement, preserving other independent grants.

```json
{
  "axis":{"kind":"class_level","class":{"id":"example.class.guardsman"}},
  "maxLevel":5,
  "entries":[
    {"level":1,"grants":[{"id":"steady_hands","kind":"feature","feature":{"id":"example.feature.steady_hands"}}]},
    {"level":2,"grants":[{"id":"training","kind":"choice","choice":{"id":"example.choice.training"}}]},
    {"level":3,"grants":[{"id":"specialization","kind":"choice","choice":{"id":"example.choice.subclass"}}]},
    {"level":4,"grants":[{"id":"improvement","kind":"choice","choice":{"id":"example.choice.improvement"}}]},
    {"level":5,"grants":[{"id":"steady_hands_veteran","kind":"feature","feature":{"id":"example.feature.steady_hands_veteran"},"replaces":["steady_hands"]}]}
  ]
}
```

These levels are illustrative. Resources scale through NumberValue tables; feature potency can scale without granting duplicate copies each level. Explicit replacement handles genuine upgrades. A subclass has its own progression and parent-class reference; its progression axis declares whether level is parent-class level or another reviewed profile axis, never inferred from the word “subclass.” This version supports parent-class/total-level axes only; other axes require a contract revision.

On level increase, process newly crossed entries once, open their choice occurrences, and apply approved state initialization. On level decrease/respec, show revoked features/choices/resources and reconcile owned state explicitly. Skipping from 1 to 4 must process levels 2, 3 and 4; replaying the same advancement request must not duplicate grants.

## Review projection

Return available options with eligibility reasons, unresolved questions, effects preview, conflicts, newly granted choices and a before/after sheet projection. Editing clients never decide legality from hidden UI options. A future admin can edit progression rows, choice groups, bundles and prerequisite trees with typed pickers rather than raw executable expressions.

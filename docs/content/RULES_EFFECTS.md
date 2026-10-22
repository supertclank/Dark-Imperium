# Declarative rules and effects

This is a bounded proposed interpreter contract. It does not assert how the actual Dark Imperium dice, stacking, defence or action economy work. Those policies require source review. Named content supplies data; only reviewed, versioned primitives execute.

## Rule classification

| `automation` | Evaluation | UI obligation |
| --- | --- | --- |
| `automatic` | Uses complete deterministic character/content inputs; invalid if it depends on runtime facts | Show the applied contribution and its source |
| `conditional` | Needs contextual facts such as an attack weapon, target trait, health ratio or worn armour | Show applied/inactive/unknown separately; disclose missing facts |
| `manual` | Narrative adjudication or unsupported mechanic; no automatic contribution | Show full text, scope, usage and an explicit human decision affordance |

Classification applies to each effect/manual entry, so a single feature may contain an automatic stat bonus and a manual narrative benefit. A feature is not entirely “automated” merely because one clause is executable. The engine returns `applied`, `inactive`, `unresolved` or `manual` with a reason. Unknown is never silently false or true.

## Effect contract

An effect is embedded in a feature, property, condition, action outcome, power outcome or rule definition. Its identity is `(owner ContentId, local effect id)`.

| Field | Required / meaning |
| --- | --- |
| `id` | Required local stable key |
| `automation` | Required `automatic` or `conditional`; manual entries use ManualRule below |
| `activation` | Required `continuous`, `triggered` or `action` |
| `target` | Required typed Target with scope; see matrix |
| `operation` | Required allowed operation for target/value type |
| `value` | Required typed NumberValue, Dice or ContentRef; only `sense/remove` omits it because the target key identifies the removed sense. Grant removals still identify the exact referenced entitlement. |
| `when` | Optional Predicate; absent means true |
| `trigger` | Required only for `triggered`; otherwise prohibited |
| `duration` | Required Duration; continuous defaults must still be explicit |
| `stacking` | Required `{group, mode}`; group is a stable namespaced policy key, mode from the table below |
| `priority` | Required bounded integer -1000..1000; resolves precedence only within its phase |
| `label` | Optional short explanation; never interpreted as rules |

`Target.scope` is `self`, `action_target` or `attack_weapon`. `action_target` is legal only in a resolved action/trigger context. `attack_weapon` refers to the current attack's item instance, not any weapon in inventory. A calculated character may have many contextual attacks; it must not collapse weapon-specific bonuses into an unconditional actor-wide total.

### Targets and operations

| Target `kind` / extra fields | Value | Allowed operations |
| --- | --- | --- |
| `stat`, `key` from profile stat registry | NumberValue with matching unit | `base`, `add`, `multiply`, `minimum`, `maximum` |
| `roll`, `rollKind`, optional `attributeKey`/`skill`/`tags` | NumberValue for modifier, or integer one for advantage token | `add`, `advantage`, `disadvantage` |
| `damage`, optional `damageType` | NumberValue for flat bonus or Dice for `add_dice` | `add`, `multiply`, `add_dice` |
| `sense`, `key` from profile | Distance converted to profile unit | `maximum`, `remove` |
| `proficiency` | ContentRef to proficiency | `grant`, `remove` |
| `action` | ContentRef to action | `grant`, `remove` |
| `mitigation` | ContentRef to mitigation | `grant`, `remove` |
| `resource_max`, `resource` | NumberValue | `base`, `add`, `minimum`, `maximum` |
| `resource_current`, `resource` | NumberValue | `spend`, `restore` in actions/triggers only |
| `condition` | ContentRef to condition | `apply`, `remove` in actions/triggers only |

A stat target cannot spend a resource; a continuous effect cannot repeatedly heal or apply conditions on each recalculation. Features with common grants may use `grants` references as sugar for explicit while-source grants with provenance; the import compiler normalizes them to the same typed grant semantics. There are no arbitrary target paths or reflection accessors.

Profile registers units for movement/senses, wounds/hull, defence, attributes and resources. Defence and AC are presentation aliases of a chosen statistic, not two independently accumulating values unless the approved ruleset defines both. Technical integer bounds do not establish game limits.

## Number values and dice

`NumberValue` is exactly one of:

```json
{"kind":"constant","value":2}
```

```json
{"kind":"stat","key":"attribute.strength.modifier","scope":"self"}
```

```json
{"kind":"scale","axis":{"kind":"class_level","class":{"id":"example.class.guardsman"}},"rows":[{"at":1,"value":1},{"at":5,"value":2}],"outside":"clamp"}
```

Allowed axes are `total_level`, `class_level` with class reference, and `resource_spent` in an action context. Rows are strictly increasing, unique nonnegative thresholds. Use the greatest threshold <= input. `outside` is explicitly `clamp` or `error`; clamp uses the first/last value at the ends. Unknown input is unresolved, not zero. Statistic references must be declared, correctly typed and acyclic. Expressions cannot recursively embed other expressions; complex calculations require an approved profile derivation or manual handling.

Property definitions additionally permit `{"kind":"parameter","name":"declared_parameter"}` for a numeric parameter declared by that same property. It is invalid outside a property or when the parameter is not numeric. Parameter substitution happens before type/unit checks; it does not enable arbitrary field access.

Dice are structured `{count,sides,bonus}`. Adding dice preserves independent components and damage types; never replace a random roll by its average. Display notation such as `1d10+2` is derived. Critical, reroll, explosion, failure and success policies are separate reviewed roll rules, not magic strings in a weapon field.

## Predicates and requirements

A Predicate is one of `all`/`any` (nonempty list of predicates), `not` (one predicate), or a typed leaf. Maximum nesting 8 and maximum 100 nodes per predicate are proposed technical limits. No arbitrary expression strings.

| Leaf `kind` | Fields and meaning |
| --- | --- |
| `selected` | `content: ContentRef`; actor has an active selection/grant of that identity |
| `level` | `axis`, `operator`, `value`; total/class level with explicit class if relevant |
| `stat` | `key`, `operator`, `value`; compare a whitelisted pre-grant statistic |
| `proficient` | `proficiency: ContentRef`; valid source-granted entitlement |
| `equipped` | `itemKind?`, `property?`, `slot?`; tests the stated scope, at least one selector required |
| `attack_property` | `property: ContentRef`; current attack weapon has this property |
| `tagged` | `scope`, `tag: ContentRef`; explicit registered classification |
| `has_condition` | `scope`, `condition: ContentRef` |
| `health_ratio` | `scope`, `operator`, `numerator`, `denominator`; exact comparison of current/max wounds, denominator > 0 |
| `fact` | `key`, `equals`; known boolean/enumerated fact from the profile/runtime vocabulary |
| `resource_available` | `resource`, `atLeast`; validated current resource in action preflight |

Numeric operators are `eq`, `lt`, `lte`, `gt`, `gte`. Ratios compare by cross-multiplication; max wounds <= 0 is invalid/unresolved, not a divide-by-zero shortcut. All/any/not use three-valued logic: false dominates all; true dominates any; otherwise unknown propagates. Unknown grants no benefit and never satisfies an eligibility gate. The UI explains what information or human decision is missing.

`requirements` gates acquiring an option; `when` controls an already-owned effect. A feat can be legally acquired and later temporarily inactive. A strength requirement must explicitly say whether it restricts acquisition, equipping or grants a penalty; the importer must not guess. Eligibility uses the pre-grant snapshot, excluding the candidate's own grants. A feature cannot grant the proficiency that it requires to justify its own selection. Choice dependency cycles are invalid.

## Triggers, costs and action resolution

Trigger is `{event, timing, filter?, limit?}`. Initial event vocabulary: `turn_started`, `turn_ended`, `action_resolved`, `damage_received`, `rest_completed`. Timing is `before` or `after`, allowed only where the profile exposes that event boundary. Filters use the predicate vocabulary. A trigger requiring a target or combat context is conditional. Events have occurrence IDs; duplicate delivery cannot spend twice.

Action resolution is: validate actor/target/context → resolve selected mode → check prerequisites, slots and budgets → reserve costs → resolve test/roll → apply the declared success/failure outcomes and trigger phases → commit changes atomically. No side effects occur during a sheet recalculation.

Cost is `{resource: ContentRef, amount: NumberValue, timing:"attempt"|"success", source:"actor"|"item", refundOnCancel:boolean}`. Item costs resolve against the selected item's resource binding (such as its magazine). Unknown or insufficient resources block execution. Attempt costs remain spent after a failed roll; success costs are reserved in advance but only debited on success. Cancelled/invalid actions follow explicit refund policy, never a UI assumption. Costs shared across a transaction cannot overspend under concurrent requests; use state-version checks/locking.

Recharge rules name a `rest` rule/event, scope, amount/restore-to-max policy and optional usage cap. Once-per-rest is a resource with maximum one, an action cost of one, and an explicit recharge rule. Once-per-session is a resource renewed by a recorded session-boundary adjudication; opening/reloading a page does not reset it. No clock-based inference of a game rest.

Triggered chains have a hard event budget (proposed 64 generated effects per root event), per-root deduplication and cycle validation. Exhaustion stops resolution with an explicit diagnostic and no partial commit; never silently drop the remaining costs or effects. These are future runtime obligations, not an event-sourcing requirement.

## Durations

Duration tagged union: `{kind:"instant"}`, `{kind:"while_source"}`, `{kind:"permanent"}`, `{kind:"rounds",count,anchor:"source_turn_end"|"target_turn_end"}`, `{kind:"until_rest",rest:ContentRef}`, or `{kind:"until_condition_removed",condition:ContentRef}`. Permanent does not make a removed source's grant survive unless it was an explicit acquired state change. `while_source` continuously retracts when the source is no longer active/equipped. Turn-based expiry requires runtime context; outside combat it remains unresolved until adjudicated, not converted to wall-clock seconds.

## Stacking and deterministic phases

1. Resolve immutable lock, selected sources and active inventory instances.
2. Establish profile/base state and eligible progression/feature grants.
3. Validate stat dependency DAG and evaluate in topological order.
4. For each numeric target: choose `base`, then sum `add`, apply `multiply`, then lower bounds (`minimum`), then upper bounds (`maximum`), then profile rounding/clamp.
5. Resolve grants/removals and roll/mitigation policies.
6. Return results, contextual variants and provenance; no resource mutation.

For a target, competing `base` effects require an explicit group policy; absent or tied conflicting bases fail publication. Priority is evaluated within a phase, never used to place multiplication before additions. `minimum` establishes a floor; `maximum` establishes a ceiling; contradictory bounds are invalid. Multipliers use rational arithmetic; rounding occurs only at the profile's declared boundary.

Stacking modes: `sum` (all distinct eligible instances), `highest`/`lowest` (numeric comparison within group), `unique_source` (one application per acquisition/item instance), `replace` (highest priority; equal conflicting values rejected). A group includes target identity and context in addition to its declared key. Distinct copies of a weapon do not automatically stack: equipment scope and property rules decide eligibility first. Repeated same-source grants are deduplicated by source instance/local effect, not display name.

Advantage/disadvantage cancellation, mitigation order and rounding are **profile policies requiring human approval**. The demonstration profile uses cancel-opposites with one remaining benefit/penalty, and immunity before resistance/vulnerability. Those are examples, not claimed Dark Imperium rules. Never infer a resistance fraction merely from the word “resistant”; mitigation definitions supply a factor or flat reduction and a policy group. Save/attack/skill roll modifiers use the same roll targets with distinct selectors.

## Source tracking and manual escape hatch

Each contribution records definition ID/revision, local effect ID, owning actor, acquisition/item instance, grant path, condition result, input values, selected scaling row, stacking decision and final contribution. Removing/replacing a grant can therefore retract exactly its effects, actions and resources without removing a duplicate grant from another source.

ManualRule is `{id, automation:"manual", text, adjudicator:"player"|"gm", context, usageResource?, suggestedAction?, reason}`. It never contributes a numeric effect on its own. If an adjudicator awards a bonus, store a separately authorized temporary effect instance using the same approved primitives, with reason, approver and expiry. A narrative rule can remain text forever without being “failed automation.” Unsupported specials must be marked manual or excluded from a calculable lock, never executed as supplied Kotlin/JavaScript.

Security: no eval, templates with code, arbitrary JSONPath, dynamic classes, external network lookups or executable imports. Content does not authorize state mutation, permission grants or disclosure of hidden GM text. Engine capability names are an allowlist mapped to installed reviewed code; they are not module URLs or script paths.

## Integrated dice extension

Roll compilation evaluates typed modifiers and conditions using the same provenance/stacking phases. Advantage is resolved once into concrete keep groups. Critical-threshold/policy changes require registered capability operations; they are not implicitly new legal operations in the current effect whitelist. Calculation never draws randomness or spends costs. Action execution owns idempotent reservations and outcome commits across attack and damage. See [Integrated dice rolling](DICE_ROLLING.md).

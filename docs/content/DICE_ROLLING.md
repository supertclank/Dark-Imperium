# Integrated dice rolling — proposed v1

This is an architecture contract, not an implemented dice engine, character sheet, animation system or multiplayer service. All numerical examples are synthetic placeholders. In particular, a d20 attack, +6 modifier and critical threshold 20 are not established Dark Imperium rules. The existing Lasgun fixture remains manual. Authoritative test, advantage and critical policies require source review.

## Boundaries and data flow

Selected content + actor state + equipment + proficiency + attributes + class/species/feat features + temporary effects + explicit context → deterministic rules evaluation → resolved RollDefinition → execution request → dice engine → DiceRollResult → text presentation → optional animation.

Calculation never rolls dice or spends resources. UI buttons submit action intents; they never calculate attack modifiers. The rules engine exposes available roll intents with labels, eligibility, unresolved requirements and provenance. Unresolved predicates or missing rules block automatic resolution; users may use an explicitly labelled manual procedure. Recalculation alone cannot repeat an action.

The dice engine consumes resolved integers and policy identifiers, not arbitrary content scripts. It has no dependency on React, WebGL, physics, database persistence or campaign transport. Separate interfaces cover definition compilation, random uint32 generation, pure result reduction, authorization, action transactions and presentation. A future server runs the same versioned calculation contract with its own secure RNG.

## Dice data and expressions

Retain the existing Dice leaf `{count,sides,bonus}` unchanged for damage and tables. An adapter produces a dice group and one literal modifier; it adds a separate DamageComponent.bonus exactly once. No catalog rewrite is required.

An executable DiceGroup is `{id,count,sides,keep?}`. IDs are unique local keys. Count is an integer 1–100; sides is an integer 2–1000; standard supported displays include d4, d6, d8, d10, d12, d20 and d100. Keep, when present, is `{mode:"highest"|"lowest",count}` with integer count 1–group.count. Omission keeps all. Equal faces are selected in ascending original die-index order, then kept/discarded index arrays are sorted ascending. No exploding, reroll-until or script expressions are implied.

A roll contains 1–16 components and at most 100 generated dice in total. Each component has at most 32 modifiers; each signed integer modifier is bounded to ±1,000,000. Arithmetic must remain in the shared exact safe-integer range. Reject nonintegers, unsupported operations, unknown policy versions and excessive work before drawing randomness. Negative totals are valid unless the approved outcome policy explicitly clamps them.

Expressions are derived displays: `1d20`, `2d6`, `1d8 + 4`, `3d10 - 2`, `2d20 keep highest 1`. A component sums its kept faces and modifiers; dice groups add, never multiply. Zero modifiers are omitted and negative modifiers render with a minus sign. Multi-type damage displays separate component expressions. Strings are never executed or accepted as authoritative definitions. A future input parser may accept only this finite grammar and normalize into the same bounded schema.

## RollTemplate and RollDefinition

RollTemplate is an optional embedded content structure, not a new top-level entity kind. It has `{id,category,label,groups,modifiers,naturalGroupId?,criticalRule?}`. Groups use DiceGroup. Modifiers are `{id,value:NumberValue,source:ContentRef,when?:Predicate}`; use the existing typed NumberValue and predicate vocabulary. A template is resolved in its owning action/test and ruleset context, and unknown facts remain unresolved. CriticalRule references a rule with role test or damage as appropriate.

The resolved immutable RollDefinition has these fields:

| Field | Contract |
| --- | --- |
| schemaVersion, id | Version 1; unique opaque roll ID, distinct from content IDs and action-execution IDs |
| category | attribute, skill, save, attack, damage, psychic, ability, table or generic |
| label | Plain accessible text; no executable markup |
| source | `{kind:"content",ref:ContentRef,localId?}` or `{kind:"generic",label}` |
| actor? | `{kind:"character"|"creature"|"vehicle",instanceId}`; character is an actor variant, not a second identity |
| action? | `{ref:ContentRef,executionId,stageId,modeId?}`; attack and damage share executionId but use distinct stageId/roll IDs |
| snapshot | `{rulesetLockDigest,engineVersion,stateVersion,contextDigest}`; stateVersion is an integer; generic actorless rolls use 0 and a pinned generic policy package |
| components | Nonempty `{id,groups:DiceGroup[],modifiers:ResolvedModifier[],damageType?:ContentRef}[]`; a component may have zero groups for flat damage |
| advantage | `{state:"normal"|"advantage"|"disadvantage",policyId,appliedGroupIds}`; explicit normal for damage/generic rolls without such a mechanic |
| natural? | `{componentId,groupId}` selecting exactly one kept die; absent means no natural roll |
| critical | `{policyId,status:"disabled"|"enabled",threshold?:integer,comparison?:"at_least"|"at_most"}` |

ResolvedModifier is `{id,value:integer,source,label,contextual:boolean}`. Source has the RollDefinition source shape; contextual modifiers retain their context provenance through snapshot.contextDigest. Modifier IDs are unique per component and source contributions are deduplicated by the compiler. A damage roll requires a damageType on each component; other categories prohibit it. Additional damage is another identified component, preserving type and origin; do not merge types before mitigation. Result totals across types are informational only.

RollDefinition is fully resolved: no NumberValue, pending context, script or UI formula survives compilation. Its canonical digest is included in the request/result. Editing a compiled definition requires a new ID/digest. Ruleset and definition digests use the canonicalization contract in CONTENT_VERSIONING.

## Actions and generated roll intents

Actions gain optional `rolls:RollTemplate[]`. Attribute, skill and save intents bind an actor plus the profile's test rule; they need no duplicate persistent action content for each sheet cell. Class actions, species abilities and feats expose ordinary actions through features. Bestiary actors use their declared fixed bonuses or derivation policy, never both. Vehicle actions bind the mount and authorized crew actor; the vehicle is the roll actor and crew identity is part of the context. GM generic rolls use the same definition with generic source and optional actor.

Weapon modes retain complete alternative mode definitions. `delivery:attack_roll` needs a resolved test rule/template; target_test delegates the test to the target actor, automatic has no attack roll, and manual exposes a manual procedure. Each DamageComponent becomes a typed damage result component; conditional extra damage is compiled only when its predicate is resolved. Mode ID, ammunition resource and relevant item instance are bound to the action execution context.

ROLL ATTACK and ROLL DAMAGE are intent labels generated from available stages, not hardcoded weapon names. Damage depends on an accepted attack outcome or an explicitly recorded manual outcome where the rule requires a hit. Damage stages refer to the parent attack result ID. Multiple targets get explicit stage/target identities; one target's outcome cannot silently stand in for all targets. The profile declares whether damage is shared or rolled per target.

Psychic actions reuse power action templates for tests and costs, and power outcomes for effects, preserving the no-duplicate-outcomes rule. Perils/random tables use table Dice and a table rule to look up the total; no roll occurs while rendering the sheet. Random results propose an outcome; applying it follows the action transaction and any required GM adjudication.

## Advantage and critical policies

Advantage state is computed from effects, with a pinned policy defining stacking/cancellation, eligible groups, count and keep direction. Do not assume cancellation or d20 mechanics. The compiler expands the approved state into concrete groups once and records appliedGroupIds. The executor uses those groups without applying advantage a second time. Explicit keep groups that conflict with the selected policy are rejected, not silently expanded again. Missing policy means manual/unresolved, not a guessed default.

Natural is the retained unmodified face of the designated one-kept-die group, never a modified total, a damage sum or an arbitrary die. Natural may be absent for pools/tables. Threshold is checked with the explicit comparison; threshold must be within die bounds. A future source requiring pool-based critical logic needs an additional versioned, allowlisted policy before automation.

Critical policies specify detection and damage separately. Supported design primitives are normal damage, multiply dice counts, multiply selected component totals, add specified components, or manual adjudication. A policy declares affected component IDs/types, integer factor 1–10 where applicable, whether modifiers are included, rounding/clamping order and a bounded final dice count. These are alternative typed operations, not a formula language. The resolved damage definition records the transformed groups/modifiers; its parent critical decision and policy version remain auditable. Features may modify the threshold or select a permitted policy through registered rule-effect capabilities; unknown critical-effect operations cannot execute. Multiple conflicting replacements are unresolved unless the profile defines precedence.

Critical result status is not_applicable, none, critical or unresolved. A critical hit does not imply automatic success unless the test policy says so. An unknown test target may leave success unresolved even with a known natural face. No critical damage is inferred from the displayed total alone.

## Requests, results and physical dice

RollRequest is `{id,definitionId,definitionDigest,executionMode,visibility,retention,clientRequestId,campaignId?,parentResultId?,manualInput?}`. ExecutionMode is local_secure, server_secure or manual; retention is ephemeral or campaign_history. Requester identity comes from the authenticated session, never a trusted userId in client JSON. The trusted execution layer retrieves/validates the definition and authorizes actor, action, mode, visibility and retention. Local mode has no campaign authority.

DiceRollResult is `{schemaVersion:1,id,requestId,definitionId,definitionDigest,label,category,source,actor?,action?,snapshot,components,staticModifier,total,natural?,critical,visibility,authority,createdAt,parentResultId?,campaignId?,testOutcome?}`. CreatedAt is an ISO 8601 UTC timestamp generated by the resolver; local timestamps are untrusted. Authority is `{mode:"local_secure"|"server_secure"|"manual",verification:"client_claim"|"server_resolved"|"user_reported"}` with only the corresponding pair permitted. Source/actor/action/snapshot copy the validated definition.

For the synthetic Lasgun Attack illustration, faces [17], keptIndices [0], discardedIndices [], staticModifier 6 and total 23 produce natural.value 17. Under the illustrative threshold-20 policy, critical.status is none. This is not derived from the existing Lasgun fixture or a confirmed game rule.

Each result component is `{id,groups,staticModifier,total,damageType?}`. Each group is `{id,sides,faces,keptIndices,discardedIndices}`. Faces retain generation order. Kept and discarded indices partition every face exactly once; face bounds, group sizes and keep ordering must match the definition. Component staticModifier is the sum of its resolved modifiers; total is kept faces plus staticModifier. Top-level modifier/total sum component values. Natural is `{componentId,groupId,dieIndex,value}` and matches that retained face. Critical is `{status,policyId,reason}`. Optional testOutcome is success, failure or unresolved, evaluated by the rule evaluator rather than generic dice arithmetic.

Physical dice entry is a separate result variant: common identity/visibility/provenance fields plus `manual:{kind:"faces"|"total",reportedBy,values}`, with authority manual/user_reported. Faces mode supplies all group faces and can run the ordinary reducer; total mode supplies per-component totals and omits groups, staticModifier and natural when unknown. Critical is unresolved unless not applicable or independently adjudicated; an adjudication records user, reason and decision separately from computed evidence. Never invent raw faces to explain a reported total. UI must distinguish reported and computed results. A user may ignore digital rolls entirely and still use the character sheet; externally resolved action outcomes/costs use the same explicit action-execution ledger.

## Randomness and reproducibility

The future browser adapter uses Web Crypto getRandomValues on Uint32Array. If secure randomness is unavailable, fail digital resolution clearly and offer physical entry; never fall back silently to Math.random. For sides s, set limit = floor(4294967296 / s) * s. Draw unsigned x; reject x >= limit, otherwise return (x mod s) + 1. Rejection removes modulo bias. Draw each die independently. Cap a request at 10,000 uint32 draws and return an execution failure without publishing a partial roll if exceeded; transaction failure/retry follows the ledger.

Inject a uint32 source into the pure sampler for deterministic tests, isolated from production configuration. Use a CSPRNG on the future server. Test boundary/rejection values for every supported die and selection/arithmetic independently from animation. Statistical tests are supplementary, not proof of uniformity. Secure client randomness does not prevent a modified client from fabricating, suppressing or rerolling results; only server_resolved results carry server authority. Do not publish reusable server seeds or random streams.

d100 is one logical uniform result from 1 through 100. If shown as percentile dice, 1→00 and 1, 10→10 and 0, 99→90 and 9, and 100→00 and 0. The two visuals represent an already sampled value; they are not additional random draws or a sum.

## Visibility and history

| Visibility | Authorized audience and creator |
| --- | --- |
| player_private | Requesting player only; no automatic GM access; actor access still required |
| campaign_visible | Current authorized campaign members; authorized member may request |
| gm_public | Current campaign members; only a campaign GM may request |
| gm_private | Current campaign GMs only; only a campaign GM may request |

Campaign modes require campaignId and membership authorization. A local ephemeral roll is player_private; requesting shared visibility requires the campaign execution path. The server authorizes subscriptions, storage reads and every result event. Private faces, modifiers, labels, source metadata and even roll existence must not enter unauthorized event payloads, history pages, indexes or notifications. CSS hiding is insufficient. Audience filtering applies to animation too. Membership is rechecked on later history reads; changing visibility later is an explicit authorized disclosure, never an automatic UI toggle.

Future RollHistory is a separate runtime entity, not a catalog content kind: `{id,campaignId,rollerUserId,actor?,source,expression,result,total,visibility,createdAt}`. Expression and total are validated projections of the embedded structured result; immutable definition/snapshot data must remain retrievable for audit. Manual totals use an honest reported-total label rather than a fabricated dice expression. Store campaign history only when retention and authorization permit it. Local/private rolls may remain memory-only; no database row is mandatory. Retention/deletion/export policy is a later campaign product decision and must respect visibility.

## Server execution, retries and resource costs

Future flow: intent → authenticate/authorize → load authoritative state and pinned content → compile → reserve action costs → resolve → commit result, outcome and cost ledger → deliver audience-filtered event. Client-provided bonuses, critical flags and totals are never accepted as server-resolved evidence. Reject stale stateVersion and return an explicit recompile requirement.

Use one action execution ID across attack/damage and an idempotency key scoped to requester/campaign/stage. Retrying an identical request returns the stored result, not fresh randomness; reusing a key with different payload fails. Ammo and attempt costs belong to the action attempt, not each roll. Success costs commit at the specified successful outcome. Reservations, results, state changes and event publication records commit atomically; reliable publication may later use an outbox, but no queue implementation is required now. A crash before commit rolls back the reservation; after commit, retry retrieves that committed result. Cancellation follows the declared refundOnCancel policy and never erases an already revealed outcome to enable free rerolls. Multi-stage reservations have a bounded expiration and explicit recovery/cancel status. Damage resolution and duplicate events cannot spend ammo or apply damage twice.

## Presentation and accessibility

Present text immediately when a result is accepted. Animation receives the already-generated faces and result ID; cancellation, tab hiding, replay or reduced motion cannot change the result or reapply effects. An optional future renderer supports the seven standard die shapes and percentile mapping; unsupported shapes use text. Physics only animates a predetermined outcome.

All intents are keyboard-operable labelled controls with predictable focus. A concise screen-reader live announcement gives label, dice, modifier, total and critical/manual status; detailed per-die kept/discarded information is available as text without repeated animation announcements. Respect reduced motion, offer instant display, and never communicate success, visibility or critical status through colour or motion alone.

## Conformance and open decisions

[Synthetic roll fixtures](examples/dice-rolls.json) exercise positive/negative modifiers, keep ties, natural-versus-total critical detection, typed damage and percentile bounds. They are independent of the existing placeholder character/catalog and do not claim a calculated Lasgun attack. Implementation must additionally test malformed inputs, stale state, unauthorized visibility/history, duplicate requests, cancellation, concurrent resource use, delivery retries, physical entry and inaccessible animation environments.

Source review must establish each test die/pool, modifier derivation, success rule, critical policy, advantage cancellation, target damage sharing and table ranges. Campaign policy must establish retention and acceptance of manual/client claims. Until then, generic dice can be designed independently, but automated game-specific attacks remain unresolved.

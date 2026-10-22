# Character runtime contract — validated narrow path

This is the minimum future application contract for the Human / Schola Progenium / Veteran level-1 proof with Twitchy and its reviewed selections and kit. The content is playable with manual rules; this document does not claim that a production runtime, persisted ruleset lock, encounter engine or authorization service has been implemented. Unsupported options remain visibly unavailable. Full-catalogue publication remains blocked.

## Data boundaries

| Layer | Owns | Must not own or imply |
| --- | --- | --- |
| Canonical content | Versioned IDs/revisions/digests, prerequisites, grants, weapon modes, action rules, explicit save outcomes and approval provenance | Character identity, current HP, ammunition or permission to act |
| Persisted character | ID, owner/campaign access, revision, pinned content selection, species, Origin, class/level, pre-species scores, choice answers/occurrence provenance, Universal Trait, selected equipment package and inventory instance identities | Client-calculated trusted bonuses, caller-supplied eligibility approvals |
| Calculated profile | Final scores/modifiers, maximum HP, AC, Speed, saves, skills, PB, proficiencies, features, available action descriptors and eligible roll intents | Mutable HP/ammo, automatic dice rolls, resource expenditure |
| Runtime state | Current HP, each firearm's magazine/reload state, remaining grenade/item quantities, limited-use counters, temporary effects, conditions, state version | A second copy of canonical mechanics |
| Action request | Actor, owned item instance/mode, targets/placement, explicit choices, expected state version, unique idempotency key | An authoritative modifier, fabricated roll outcome or permission inferred from the UI |
| RollDefinition | Immutable resolved dice/components/modifiers, actor/source/action/execution/stage, policy IDs and snapshot/context digest | Authorization to attack or spend resources |
| DiceRollResult | Accepted definition ID/digest, faces/kept dice, totals, natural/critical interpretation, provenance/authority and execution/stage links | A new rule inferred from a displayed expression |
| Transactions/events | Exactly-once resource changes and accepted action/result transitions with audit/version checks | Repeated expenditure on retries, page refresh or recalculation |

Persist the original standard-array assignment and species choices; derive final scores. Persist the exact selected item IDs/quantities and selection provenance; do not trust a client `proficient` flag. Starting-package proficiency applies only to actually granted weapons/shields, separately from class weapon groups. The present fixture's inventory rows use definition references; production persistence must allocate stable item-instance IDs and bind actions to those instances.

The current proof's snapshot hash pins canonical records, approvals and the reviewed kit. It is an offline conformance pin, **not a production RulesetLock**. Before the production builder saves a character, a server-owned narrow profile must pin the supported content closure and policy versions, validate the submitted selections, and store a character revision and lock. General catalogue incompleteness must not silently broaden that profile. A later migration is explicit and audited; it must not retroactively alter existing characters or accepted roll definitions.

## Calculation versus state

Recalculate from the pinned content, persisted selections and applicable state/context without side effects. Do not reset current HP to maximum, refill a magazine, restore limited uses or consume a grenade when calculating or rendering. Unknown optional context yields a manual/blocked action, not a guessed zero modifier. Changes to maximum HP never invent a reconciliation policy.

Source-defined manual procedures remain visible: Human's failed-save reroll, Schola fear-save circumstances and education, Tactical Aim's target/turn restriction, Med-Pack use, ordinary reload and resource tracking. Manual handling must retain the actor, rule and any user-reported outcome as such; it must not masquerade as a server-generated result. The current proof uses baseline normal range/no advantage/no Tactical Aim/no critical-damage context. These constraints describe its generated rolls, not global game-rule limitations.

Magazine capacity comes from each Reload property. PHB PDF 31 abstracts ordinary spare ammunition unless mission scarcity applies; it does not authorize recalculation to refill a magazine. Establish and persist initial loaded state through a deliberate creation/encounter setup event. Grenade quantity starts from the validated kit (two) and thereafter belongs to inventory state. Initial and spent limited-use resources need explicit state transitions. No current state is inferred from an old offline projection.

## Weapon attack protocol

1. The authenticated player requests, for example, a Lasgun attack using an owned item instance, target, mode, expected state version and idempotency key.
2. The backend verifies actor/campaign ownership, pinned content, item possession/readiness, hand/equipment constraints, range/visibility, action economy, conditions, remaining ammunition and selected context. Unsupported interactions fail closed or enter an explicit manual procedure.
3. Load/recalculate the available action from trusted inputs. Resolve all modifier and advantage/critical context. Generate a fresh immutable attack RollDefinition whose snapshot includes actor/state/content/context versions and item identity.
4. Resolve the dice through an authorized resolver and accept the attack result once. A client-origin result is labelled with its actual authority; it is not a server-verified hit. Record target defence/manual adjudication needed to determine the hit.
5. Only an accepted hit (or an explicitly authorized manual hit outcome) makes the matching damage stage eligible. Bind that stage to the parent attack result, same execution/item/target and accepted critical decision. Never reuse another target's hit.
6. Resolve and accept the damage roll once. The future encounter system applies damage under the applicable mitigation/condition rules. Unresolved mitigation remains manual/blocked rather than importing defaults.

Validate ammunition and action expenditure and commit them exactly once at the accepted action-use boundary, including misses, using source-defined costs. A roll retry retrieves the existing execution/result; it is not a second attack. If resolution fails after use is committed, preserve the pending execution for completion/adjudication. Do not silently refund or repeat the shot. Reservation/commit details are an implementation protocol, not a new game rule.

The offline RollDefinitions validate arithmetic and structure only. The frontend must never submit one as proof that its owner was allowed to attack. The server must bind accepted definitions to its own actor state and execution records.

## Frag Grenade protocol

1. Verify ownership, selected Frag Grenade instance/quantity, permitted action use and placement context. Validate the 30/90-ft throwing rules. Within 30 ft, placement requires no attack roll; the existing longer-range placement check remains distinct from target saves.
2. Commit one grenade expenditure transactionally for the accepted use. Never consume separately for each target, damage roll, retry or save. Failure to place it as intended does not manufacture a replacement grenade.
3. Determine the final point and the creatures in the **15-ft radius** through encounter geometry or explicit GM adjudication. Freeze or version the target set for that execution.
4. Targets make Dexterity saves against the source actor's snapshotted grenade DC: **8 + PB + Dexterity modifier**. The proof DC is 12. Each target's own save bonus and authority must be resolved separately; the thrower's modifier is not the target's save bonus.
5. Resolve a **3d6 piercing base-damage RollDefinition with no ability modifier** independently of whether a target succeeds. Link the accepted damage result to the grenade execution.
6. For each accepted target save, use the explicit weapon-mode outcome: failure = full rolled damage; success = floor(rolled damage / 2). For example, 11 becomes 11 on failure and 5 on success. This scaling is before any separately governed target mitigation or HP change.

**Deferred encounter detail:** the approved rules do not establish whether one damage roll is shared by all targets or a separate roll is made per target. The implementation must require an explicit adjudicated execution policy before automatically processing multiple targets. Do not default to either policy. Record the selected policy and result-to-target associations when authorized. This does **not** block creation or ordinary manual play of the narrow character.

The outcome model applies only where a content record explicitly supplies it. PHB-RULE-059 resolves Frag Grenade; PHB-RULE-018 remains unresolved. Never attach half-on-success to another grenade, Blast property or area attack through a schema default.

## Atomicity, replay and audit requirements

Use character/runtime optimistic versions and an atomic compare-and-update or database transaction for state changes. A stable execution ID/idempotency key identifies one requested use. Uniqueness constraints prevent multiple ammo/grenade debits or accepted damage applications for the same execution/stage/target. Reuse of the same key with different payload must fail. Concurrent requests against the final grenade cannot both commit.

Separate planned, committed-use, awaiting-result, result-accepted and applied states. Retain content/approval digests, submitted context, authorization result and expenditure/result event links. An encounter application also needs its own idempotency boundary so retrying an accepted damage result cannot subtract HP twice. Cancellation/refund after commitment requires an explicit authorized correction event; no hidden reversal occurs on timeout or disconnect.

## First production implementation boundary

Implement the narrow data-driven creation and persistence flow first: server-validated choices, supported-option filtering, a server-owned narrow content lock, persisted character/inventory identities, calculated read model and clear manual-feature presentation. Unsupported PHB options must remain visibly unavailable. This work need not implement encounter automation, general Blast rules, animated dice or the whole runtime engine. Action execution can follow behind the authorization and transaction boundaries defined above.

See [dice contract](DICE_ROLLING.md), [character model](CHARACTER_MODEL.md), [minimum-rulings capability](PHB_MINIMUM_RULINGS_CAPABILITY.md) and [Frag gate report](../import/PHB_FRAG_GATE_REPORT.md).

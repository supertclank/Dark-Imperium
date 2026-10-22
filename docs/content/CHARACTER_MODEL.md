# Character and actor state

Definitions describe possibilities; selections and instances describe this particular actor. Character UUID and owner/account permissions remain application concerns. Content IDs are not user identities.

## Persisted selections

Required fields for a saved player character: `id` (UUID), `ownerId` (server-derived UUID), `stateVersion` (positive optimistic-concurrency integer), `name`, `rulesetLock` (`id`, `revision`, `sha256`), `selections`, `inventory`, `resources`, `conditions`, `temporaryEffects`, `notes`, `currency` and timestamps.

`selections` contains:

- `species`, optional `background`, and `classes` entries `{class:ContentRef,level,subclass?}`. Multiclassing is representable but MUST be disabled unless a reviewed profile permits it. Total level is the sum; do not persist an independently editable conflicting total.
- `attributes`: values keyed by profile attribute IDs; optionally record allocation method and point/roll evidence. The engine derives modifiers, not the form.
- `answers`: `{occurrenceId,origin,choice:ContentRef,optionIds,allocations?,status}`. Origin is `{kind:"creation_step",stepId}`, `{kind:"progression_grant",progression:ContentRef,grantId,advancementOccurrenceId}`, or `{kind:"feature_grant",feature:ContentRef,grantId,acquisitionInstanceId}`. It binds the answer to a specific grant/creation step. Status is `valid` or `stale`, never quietly discarded.
- `advancement`: ordered level-acquisition records with stable occurrence UUID, class reference, from/to levels, answer references, chosen feature/feat/power grants and acquisition provenance. This is selection history, not every combat event.

Species/background/class/feat/skill/power/equipment picks use the same validated choice contract. The character may store a normalized selected-feature/power index for querying, but its source of truth is the acquisition/answer record. Do not let both lists be independently edited. Character name and authored notes are ordinary owned fields, not content entities.

## Owned inventory

Each item instance requires `instanceId` UUID, `definition` ContentRef, `quantity` positive integer, `equipped` boolean, `slots` string array, `stateVersion`, and optional `customName`, `provenance`, `resources`, `loadedAmmunition`, `attachments` and `notes`.

Only identical, unmodified, unequipped items with equal condition/resource state may share a quantity stack. Weapons with distinct loaded magazines, augmetics, charged consumables and equipment with attachments normally have quantity one. An equipped item must exist in owned inventory. Slot/hands compatibility is profile-driven, not a UI-only check. Buying, consuming, equipping and reloading are explicit state mutations; recalculation does not duplicate grants or items.

Loaded ammunition records ammunition ContentRef, quantity, magazine capacity binding and any source inventory instance. Reload consumes loose ammunition and fills the magazine in a single transaction. Infinite ammunition must be an explicit capability/rule, not a missing quantity. Attachments point to owned system/augmetic instances with defined compatibility and one active host; cycles and double ownership are invalid.

## Mutable state

| State | Contract |
| --- | --- |
| Wounds/hull | Current integer owned value, keyed resource/stat convention from profile; maximum is calculated. The profile defines whether it represents remaining health or accumulated injury; examples use remaining wounds only. |
| Resources | Entries `{resource:ContentRef,scopeInstanceId?,current,lastRechargeOccurrence?}`; maximum derived; spending is transactional |
| Conditions | Instance UUID, condition reference, source actor/item, applied time, stack count, duration binding and recorded save/test state if relevant |
| Temporary effects | Instance UUID, pinned source/local effect, parameters allowed by its declaration, duration, adjudicator/authorization and reason |
| Currency | Integer balances per currency reference; conversions are explicit rules, not implicit floating arithmetic |
| Notes | Authored text with player/private/GM visibility controlled by application permissions |
| Advancement | Player selections with provenance; changes must revalidate downstream grants |

Current wounds do not automatically increase when max wounds increases unless an approved advancement rule says so. Values above a new maximum produce a reconciliation issue; never silently overwrite them on read. Resource removal preserves an audit/recovery record if a migration revokes the source. The character cannot manufacture arbitrary temporary effects by posting an untrusted numeric modifier.

## Runtime state is separate

Encounter/scene state references actor UUIDs and pins their lock/state snapshot: turn position, target/distance facts, cover, prepared reactions, pending roll results, initiative, marked targets and duration anchors. Some ongoing conditions/resources are persisted with the character so they survive leaving an encounter. There is one authoritative condition/resource instance, not independent sheet and combat copies. Runtime projections reference that instance/version.

Creature and vehicle definitions instantiate the same broad actor-state concepts without pretending every creature has player creation choices. A creature template is reusable immutable content; a spawned creature has its own current wounds, condition instances and ammunition. A vehicle's crew assignments are runtime/owned state, while required crew roles belong to its definition.

## Calculated projection

Return `{actorId, stateVersion, lockDigest, engineVersion, values, attacks, actions, proficiencies, mitigations, passiveFeatures, explanations, unresolved}`. Values include maximum wounds/hull, movement modes, defence, attribute modifiers, saves and skill bonuses. Attacks include weapon instance and selected firing mode; contextual inputs/unknowns are explicit. Available actions are definitions plus availability/reason/cost preview, not permission to execute without server revalidation.

Do not persist these as independently editable authoritative values. A cache may persist the projection for performance if its key includes actor state version, lock digest, engine version and normalized runtime context digest. Invalidate on any changed dependency, including equipping, resource threshold, conditions, advancement or migration. Never use a stale projection to authorize spending. Snapshots attached to an audit/export/encounter are legitimate historical records with exact input/version identifiers, not a second truth for current play.

The complete state fixture is [examples/character.json](examples/character.json). Its player/account IDs are synthetic examples and are never trusted as request ownership.

## Integrated dice extension

Rolls derive from the calculated actor snapshot, equipped item instances and explicit context. Results/history are separate runtime records, not persisted derived character truth. Physical dice and external outcomes remain valid; digital rolling is optional. State version, lock digest, engine version and context digest bind every compiled roll. See [Integrated dice rolling](DICE_ROLLING.md).

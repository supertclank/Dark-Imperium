# Design review and unresolved rules

## Architecture review

| Review question | Decision / evidence | Remaining risk |
| --- | --- | --- |
| Are current names hard-coded? | Identities and references are data; effect vocabulary, targets and profile policy are generic. Examples contain names, interpreter operations do not. | Overusing per-content “special handlers” would regress this boundary; manual clauses are preferred. |
| Can new content be added through data? | All requested entity families map to 40 registered kinds, with reusable feature/action/property/choice structures. | Entirely new mechanics may need a reviewed capability; no claim of universal automation. |
| Can content change safely? | Immutable revisions, exact lock closure, explicit migration and preserved old identities. | Storage/adapters are not implemented yet; mutable foundation behavior must not be confused with this proposal. |
| Are rules and presentation separated? | Engine returns values, provenance and unresolved/manual state; UI renders and submits choices. | Client-only eligibility or damage calculations must be rejected in implementation review. |
| Can builders be generic? | Typed choices, bundles, allocation, prerequisites, exclusions and grant occurrence IDs. | Actual creation sequence and allowed respec/multiclass rules are unknown. |
| Can common effects execute generically? | Typed target/operation matrix, bounded predicates/scaling and explicit deterministic phases. | Stacking, rounding, dice and mitigation policy need real source confirmation. |
| Do manual rules fit? | First-class ManualRule with adjudicator, context, usage resource and reason; no pretend numeric result. | UI must clearly label manual/unresolved, not merely omit it. |
| Can Bestiary reuse rules? | Creature templates reference weapons, actions, traits and typed overrides; current wounds belong to instances. | Fixed statblock bonuses must replace rather than accidentally stack with player derivations. |
| Can Astartes fit? | Ordinary classes + affiliations, feature pools, requirements and armour systems. | Complex origin/service/chapter eligibility needs source clarification. |
| Can admin tools edit it? | Strict field contracts and curated choice/effect/progression editors; publication separate from editing. | Raw JSON alone is not a friendly admin UI; forms remain a later task. |

## Refinements made during review

- Kept content identity separate from revision, source edition, runtime UUID and local grant/effect key.
- Distinguished ordinary reference cycles from invalid calculation/unlock cycles.
- Defined unknown conditional facts as unresolved rather than silently granting/denying bonuses.
- Prevented double application of armour defence and power/action outcomes.
- Made item instances and acquisition grants explicit, so re-evaluating a sheet cannot create equipment or refill ammunition.
- Restricted statblock overrides to named replacement fields rather than arbitrary JSON patches.
- Added shared item identity, species slot-capacity overrides and system attachment concepts without a new weapon schema for vehicles/Astartes.
- Made placeholder packages editorial-preview-only; all sample statistics remain non-authoritative.

## Expansion compatibility assessment

| Material | Representation | Limit/clarification |
| --- | --- | --- |
| Angels of Death | Additional package with classes, affiliations, equipment, systems, features and exact dependencies | Full book unavailable; no claim all its mechanics fit existing primitives |
| Astartes Chapters | Affiliation category `chapter`, faction relationship, features and restrictions | Confirm required chapter choice and what it mechanically grants |
| Deathwatch | Separate service affiliation plus prerequisites and features | Confirm coexistence with original chapter, replacement/retention and permitted equipment |
| Custom Chapters | Homebrew affiliation + feature choices under a unique namespace | Publication permissions and permitted trait budgets require group policy |
| Unknown Founding | Origin affiliation opening a trait choice with cardinality/exclusions | Demonstration choose-two is not authoritative; confirm pools and restrictions |
| New species | Species + features, size/anatomy and choices | New senses or locomotion semantics may require a profile capability |
| New classes/subclasses | Class, parented subclass, progression, grants and choices | Confirm level axes and multiclassing before enabling it |
| New/exotic weapons | Shared modes, property arguments, requirements, costs and special manual clauses | Unsupported targeting/roll procedures remain manual until implemented |
| New psychic disciplines | Discipline/power/action/rule/resource references | Actual tests, sustain, costs and Perils rules unknown |
| New factions | Faction relations + tags/lore; affiliations for selectable membership | Do not automatically convert lore attitudes into mechanics |
| New creatures | Creature/NPC templates reusing action/weapon/feature contracts | Threat scale and fixed-vs-derived statistics need agreement |
| Vehicles | Vehicle templates, mounts, systems, roles and common actor resources | Facing, damage locations, collisions and catastrophic procedures may remain manual |
| Homebrew/future books | Namespaced packages, validation and locked campaign selection | Homebrew cannot overwrite publisher identities or introduce executable code |

## Human decisions required before authoritative content publication

| Priority | Question | Why it matters |
| --- | --- | --- |
| Blocking | Which exact Player's Handbook/other source versions are current, and who approves interpretations? | Establishes authority, source identities and review ownership |
| Blocking | Actual creation sequence, attribute set/ranges/generation and skill/save formulas? | Defines profile inputs, derivations and builder constraints |
| Blocking | Wounds convention, maximum-wounds calculation, defence/AC model, movement units and rounding? | Avoids importing incompatible health/damage/unit assumptions |
| Blocking | Attack/test/damage dice procedures, advantage cancellation, stacking and mitigation ordering? | Required for trustworthy automatic projections |
| Blocking | Class progression, subclass gates, feat/attribute improvement levels and replacement rules? | Prevents invented advancement entitlements |
| Before equipment automation | Proficiency penalties vs hard gates; hands/slots; ammo/capacity/reload; alternate fire modes? | Determines legal use and resource transactions |
| Before psychic automation | Disciplines/power access, activation tests, warp costs, sustaining, failure and Perils triggers? | Unknown procedures cannot be safely inferred |
| Before Astartes import | Chapter/Unknown Founding/Deathwatch selections, trait budgets, equipment and anatomy restrictions? | Confirms general affiliation/choice representation and any new capabilities |
| Before Bestiary/vehicle automation | Threat scale, fixed statblock bonuses, crew actions, transport constraints and damage procedures? | Defines template/base-value and runtime policies |
| Before campaigns migrate | Who selects locks, whether mixed locks are allowed, and what respec/migration policies apply? | Preserves player state and consistent campaign rules |

## Risks and boundaries

The primary risk is mistaking a well-formed example for an official rule. Every fixture carries placeholder provenance and stays outside authoritative locks. A second risk is expanding the effect language into a general programming language; limit predicates, axes, operations and supported capabilities, and leave genuinely narrative rules manual. A third is ambiguous dual sources of truth: normalize grants and derived values centrally, retain immutable locks, and require explicit state transactions.

No application implementation, full rulebook import, new database migration, search service, admin UI or combat runtime was added in this task. The proposed specification is ready for rules-owner review and a focused validation implementation, not a claim of production rules conformance.

## Integrated dice extension

The integrated dice requirement is covered by a bounded model with separate compiler, sampler, reducer, action transaction and renderer. No game-specific test or critical default is inferred. Source approval of roll/critical/advantage policies and campaign decisions on history/manual trust remain open. Secure client RNG is not multiplayer anti-cheat. See [Integrated dice rolling](DICE_ROLLING.md).

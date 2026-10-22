# Entity catalog

Every row inherits the required envelope and optional envelope fields in CONTENT_MODEL. Fields below belong to `data`; required lists may be empty unless stated. All reference slots have the expected kind indicated. “Example key” means the complete record `example.<kind>.<key>` in [examples/catalog.json](examples/catalog.json), not a prose-only sketch. Domain-specific details are normative in DOMAIN_SCHEMAS; effects and grants use RULES_EFFECTS/CHARACTER_BUILDER.

## Character content

| Kind / purpose | Required payload | Optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `species`: biological/character origin | `features`, `size` profile size key | `choices`, `requirements`, `movementModes`, `slotCapacities`, `languages` proficiency refs | Feature/choice refs; size registered; movement values have units | `human`, `ogryn`; new species are new records, not branches |
| `background`: previous life | `features` | `choices`, `requirements`, `factions` | Features/choices; faction relations explicit | `frontier`; narrative benefits may be manual features |
| `class`: advancement path | `features`, `progression` | `choices`, `requirements`, `allowedSubclasses`, `powerAccess` | Progression axis agrees with class; powerAccess is discipline refs, not a class-name flag | `guardsman`; Astartes classes reuse it |
| `subclass`: class specialization | `parentClass`, `features`, `progression` | `choices`, `requirements` | Parent is class; eligibility does not bypass parent; progression level axis explicit | `line_veteran`; no embedded parent rules copy |
| `progression`: level-granted entitlements | `axis`, `maxLevel`, `entries` | `requirements` | Increasing valid levels, unique grant IDs, backwards-only replacement, no dependency cycles | `guardsman`; shared typed grant engine |
| `feature`: reusable trait/feat/benefit | `flavor`, `effects`, `grants`, `manualRules` | `choices`, `requirements`, `repeatable`, `usageResources`, `exclusiveGroup` | Flavor is `species_trait`, `background_feature`, `class_feature`, `subclass_feature`, `feat`, `chapter_trait`, `creature_trait`, `vehicle_trait`, `passive` or `general`; all use the same mechanics | `steady_hands`, `field_training`, `two_handed_focus`, `local_contacts`; specialization is eligibility/source, not separate engines |
| `skill`: named competency | `attributeKey` | `testRule`, `proficiencies` | Attribute declared in profile; optional rule role `test`; no assumed bonus formula | `awareness`; new skills extend data/profile vocabulary |
| `proficiency`: entitlement | `category`, `appliesTo` | `rank`, `effects`, `requirements` | category `skill`, `weapon`, `armour`, `tool`, `save`, `language` or `other`; appliesTo selector is explicit IDs or registered kind/tag selection | `las_weapons`; rank semantics require profile policy |
| `affiliation`: chapter/order/organization option | `category`, `features` | `faction`, `choices`, `requirements`, `exclusions` | Faction is not a chapter trait; choice pools and exclusions express membership rules | `chapter`, `unknown_founding`, `deathwatch`; custom chapters use homebrew namespace |
| `choice`: reusable player decision | `purpose`, `selectionMode`, `cardinality`, `repeatScope`, `options` | `pool`, `allocation`, `requirements`, `exclusions`, `presentationGroup`, `helpMarkdown` | See builder; required cardinality must have a satisfiable valid option set | `starting_loadout`, `chapter_traits`; choices can grant child choices with acyclic dependencies |

Level progression is its own entity, not an unstructured paragraph. A class can also grant level-independent features through `features`; granting the same feature through both that list and level-one progression is invalid unless explicitly independent/repeatable. A feat is a feature with `flavor: feat`; species/background/class/subclass/chapter/creature traits use that same feature structure. Source relationships and prerequisite policies distinguish them.

## Equipment

All item kinds support optional `requirements`, `properties`, `features`, `cost`, `availability`, `weight`, `variantOf` and `equip` where meaningful. Acquisition requirements and equip/use requirements are distinct. `variantOf` is editorial lineage; it does not inherit fields implicitly. Common item data and complete weapon/armour contracts are in DOMAIN_SCHEMAS.

| Kind / purpose | Required payload | Additional optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `weapon`: player/creature/vehicle weapon | `category`, `subcategory`, `modes`, `hands`, `properties`, `features` | `proficiencies`, `ammunition`, `reload`, `rate`, `specialRules`, common item fields | At least one unique mode; damaging mode has valid dice/type/ranges; properties accept declared arguments | `lasgun`, `combat_knife`, `shotgun`, `sidearm`; all exotic families reuse modes |
| `armour`: worn protection | `category`, `equip`, `properties`, `features`, `defence` | `proficiencies`, `shieldCompatibility`, `systems`, `augmeticCompatibility`, common fields | Defence is NumberValue/base policy; slots registered; penalties/resistances are features/properties | `flak`; Astartes systems attach through system refs |
| `shield`: carried protection | `equip`, `properties`, `features`, `defence` | `proficiencies`, common fields | Occupied hands/slots and armour compatibility checked together | `field`; shares protection primitives with armour |
| `ammunition`: consumable ammunition definition | `category`, `compatibleWeaponTags`, `unitsPerItem`, `features` | `properties`, common fields | Units > 0; weapon tag IDs known; compatibility checked both ways | `charge_pack`; charge packs can be capacity/resource-bearing variants |
| `equipment`: general gear | `category`, `features` | `equip`, `properties`, common fields | No weapon damage fields unless it is also a referenced weapon action | `field_pack`; add typed specialization only when needed |
| `consumable`: finite-use item | `category`, `uses`, `useResource`, `useAction`, `features` | `properties`, common fields | Uses positive; useResource has item scope; action must declare that matching item resource cost; cannot duplicate consumption | `medicae`; replenishment requires explicit rule |
| `augmetic`: installed modification | `installationSlots`, `features`, `compatibility` | `removalRule`, `properties`, common fields | Slots/capacity, anatomy/host compatibility explicit; installation is not ordinary wielding | `ocular`; manual surgical requirements allowed |
| `tool`: task equipment | `category`, `features` | `proficiencies`, `useActions`, common fields | Tool proficiency and action refs valid | `repair_kit`; reuse action/test models |
| `currency`: accounting unit | `minorUnitName`, `minorUnitsPerMajor`, `symbol` | `conversionRule` | Positive integer scale; no floats; no assumed galactic universal currency | `scrip`; campaign-specific currencies use separate IDs |

Vehicle weapons are ordinary `weapon` definitions mounted with mount/crew context. A mounted weapon may also be usable by a character if requirements allow it. Do not create an incompatible vehicle-damage schema.

## Rules, actions and resources

| Kind / purpose | Required payload | Optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `property`: reusable weapon/armour/item property | `appliesToKinds`, `parameters`, `effects`, `manualRules` | `features`, `requirements` | Parameters have local names, type, required/default and bounds; usage arguments reject unknown keys | `two_handed`, `reliable`, `heavy_armour`; applicable kinds constrain usage, not separate engines |
| `condition`: applied status definition | `effects`, `manualRules`, `stackPolicy`, `defaultDuration` | `removalRule`, `grantedActions` | Stack policy `unique`, `counted`, `independent`; counted needs cap; removal/expiry explicit | `suppressed`; instances carry source/expiry separately |
| `damage_type`: named damage vocabulary | `category` | `parent`, `interactionRule` | Optional hierarchy acyclic; interactions are explicit rules, not inferred from names | `energy`; extensible damage types |
| `mitigation`: resistance/immunity/vulnerability | `mode`, `damageTypes`, `policyGroup` | `factor`, `flatAmount`, `when` | Mode `resistance`, `immunity`, `vulnerability`; immunity has neither factor nor amount; other modes require exactly one. Resistance subtracts flatAmount or uses factor 0..1; vulnerability adds flatAmount or uses factor >= 1. Fractions have positive denominators. | `energy_resistance`; category-specific factors verified by rules owner |
| `action`: action/reaction/special action | `economy`, `target`, `costs`, `outcomes` | `requirements`, `test`, `range`, `trigger`, `frequencyResource`, `manualRules` | Economy key registered in profile; reaction needs trigger; outcomes resolved through declared test; costs atomic | `aim`, `brace_reaction`, `command_special`; special actions use an explicit budget/resource |
| `resource`: charges, effort, warp or other pool | `scope`, `max`, `initial`, `recharge` | `minimum`, `overflowPolicy`, `visibility` | Scope actor/item; max NumberValue; initial `maximum` or explicit value; recharge refers to rest rule or recorded adjudication event | `focus`, `warp`, `magazine`, `special_budget`; meaning comes from referenced rules |
| `rule`: bounded reusable rule policy/manual procedure | `role`, `automation`, `effects`, `manualRules` | `trigger`, `table`, `recharge`, `testPolicy`, `requirements` | Role `rest`, `test`, `psyker`, `perils`, `damage`, `conversion`, `installation` or `general`; executable fields must match installed capability | `rest`, `perils`, `psyker`, `vehicle_damage`; unsupported clauses remain manual |
| `profile`: locked game vocabulary/policies | `attributeKeys`, `stats`, `units`, `sizes`, `slots`, `actionEconomy`, `capabilities`, `policies`, `creationPlan` | `levelBounds`, `rollRules`, `multiclassing` | Exactly one profile per lock; all target/stat/economy keys declared; policies supported by capabilities | `demo`; profile changes are ruleset revisions, not app-name conditionals |

Passive effects are continuous effects or `feature` flavor `passive`, not a second effect language. Rest mechanics are rule role `rest`. Resistance, immunity and vulnerability are one typed mitigation family. Resource costs/recharges are shared across mundane, psychic and vehicle systems.

## Psyker content

| Kind / purpose | Required payload | Optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `discipline`: psychic-power grouping | `features` | `requirements`, `powerPool`, `faction` | Power pool restricted to power kind; powers explicitly reference discipline | `warding`; no discipline-specific code |
| `power`: psychic action definition | `discipline`, `action`, `duration`, `outcomes` | `requirements`, `scaling`, `failureRule`, `perilsRule`, `sustainCost`, `manualRules` | Discipline/action/rule refs checked; costs/test/target/range use action contract; outcomes applied once, not duplicated in action and power | `ward`; complete contract in DOMAIN_SCHEMAS |

Warp-related pools use `resource`; psyker-specific procedures use `rule` role `psyker`; perils tables use `rule` role `perils` with nonoverlapping outcome ranges or manual adjudication. No assumption is made about the actual warp/perils roll procedure or recharge cadence.

## Vehicles and Bestiary

| Kind / purpose | Required payload | Optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `vehicle`: reusable vehicle statblock | `vehicleType`, `size`, `movement`, `defence`, `hull`, `crew`, `mounts`, `systems`, `features`, `transportCapacity` | `damageRule`, `requirements`, `resources`, `factions`, `lore`, `actions` | Crew role refs, positive capacities, mount/system compatibility, typed weapon overrides | `scout_carrier`; locomotion modes allow very different vehicles |
| `system`: armour/vehicle/augmetic subsystem | `hostKinds`, `slot`, `features` | `requirements`, `actions`, `resources`, `powerDemand`, `compatibility` | Valid host kinds and slots, resource dependencies explicit, no installation cycles | `autosenses`, `drive`; same model for Astartes armour systems |
| `crew_role`: station responsibilities | `minOccupants`, `maxOccupants`, `actions` | `requirements`, `controls`, `features` | 0 <= min <= max; controlled mount/system keys must exist in owning vehicle | `gunner`; occupancy is runtime state |
| `creature`: NPC/creature statblock | `actorKind`, `creatureType`, `size`, `movement`, `defence`, `wounds`, `attributes`, `skills`, `saves`, `mitigations`, `features`, `actions`, `equipment`, `factions` | `threat`, `lore`, `resources`, `requirements`, `specialRules` | ActorKind `creature` or `npc`; registered attributes/skills; typed weapon overrides; no assumed CR formula | `renegade`; NPCs share creature schema; reactions and special actions reference action economy |

Threat is `{scale, value, label?}`; a number without a named scale is invalid. Creature traits use feature flavor `creature_trait`; creature actions/reactions share `action`. A named NPC may add lore and narrative faction relationships without duplicating its entire mechanical family. Definitions do not store initiative, current wounds or a particular crew member's UUID.

## Taxonomy and campaign content

| Kind / purpose | Required payload | Optional payload | Relationships and validation | Example key / extension |
| --- | --- | --- | --- | --- |
| `tag`: controlled classification | `category` | `parent`, `synonyms` | Acyclic hierarchy; normalized aliases do not grant mechanics | `imperium`, `las`, `heavy_armour`; supports search/restriction selectors |
| `faction`: organization identity | `relationships` | `parent`, `affiliations`, `lore` | Explicit relation `{faction,kind}` with kind `ally`, `enemy`, `neutral` or `unspecified`; hierarchy acyclic | `imperium`; do not infer attitude rules from a label |
| `location`: reusable place | `locationType` | `parent`, `factions`, `mapAsset`, `lore`, `encounters` | Reference kinds and acyclic containment; asset is safe content asset ID | `outpost`; actual campaign visits are runtime state |
| `handout`: player-facing document | `audience`, `bodyMarkdown` | `asset`, `relatedContent` | Audience `player` or `gm`; delivery authorization enforced server-side | `orders`; safe rendering, no scripts |
| `lore`: reference prose | `audience`, `bodyMarkdown` | `relatedContent` | References valid; indexing respects access controls | `frontier`; no mechanical parsing of prose |
| `adventure`: reusable scenario | `sections`, `encounters`, `locations`, `handouts` | `factions`, `requirements`, `recommendedThreat` | Sections have unique local IDs and references; do not store party progress | `patrol`; reusable publication content only |
| `encounter`: encounter template | `participants`, `environment`, `objectives` | `location`, `rewards`, `tacticsMarkdown`, `requirements` | Participants reference creature/vehicle templates with quantity > 0; environment facts declared; instantiated HP/turns absent | `checkpoint`; future encounter runtime consumes it |

Source registry entries and package/lock manifests are editorial/release structures rather than game content kinds. See CONTENT_MODEL and CONTENT_VERSIONING for their required/optional fields, relationships and examples.

## General extension rule

Add a record when a new item/species/discipline/chapter fits a defined kind. Add a field or kind only when it captures a genuinely different invariant and receives a schema-version migration. Do not hide mechanical payload in `extensions`, tags, names or Markdown. Unrecognized mechanical fields/capabilities fail validation; non-mechanical editorial metadata can survive round-tripping under its namespaced extension key.

## Integrated dice extension

Dice rolling adds no canonical content kinds. Actions/test rules carry optional RollTemplate structures; features grant actions; creatures and vehicles bind the common actor/action interface. RollDefinition, DiceRollResult and RollHistory are runtime contracts. See [Integrated dice rolling](DICE_ROLLING.md).

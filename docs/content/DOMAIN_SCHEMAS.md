# Detailed domain contracts

All fields use the common envelope and ContentRefs. This document expands the entity catalog; it does not replace the common rules language with special weapon/psyker/vehicle code.

## Profile and vocabulary

`attributeKeys` is a unique string list. `stats` is a list of `{key,unit,base,rounding,minimum?,maximum?,derivation?}`; stat keys are immutable within a profile lineage. `units` maps measurement families to supported units; `sizes` is a unique key list; `slots` maps slot keys to nonnegative capacities; `actionEconomy` is a unique key list. Species may optionally override default slot capacities through `slotCapacities`; this is structural anatomy, not a species-name check. `policies` contains explicitly declared policy identifiers/parameters and controlled taxonomies such as movement modes, equipment categories, availability scales and arcs. A policy registry rejects unknown keys/values.

An optional derivation is one of the installed profile capabilities: `attribute_modifier` with source attribute, offset, divisor and rounding; `sum` with a finite list of stat keys; or `table` with a declared input stat and finite threshold rows. No nested formula strings. The demonstration profile intentionally supplies modifier bases of zero rather than asserting an actual attribute formula. Exactly one owner (profile derivation, explicit creature base or selected base effect) supplies each base according to declared precedence.

Resource `initial` is `"maximum"` or a constant NumberValue within its bounds. Item ammunition is never replenished by a generic actor rest unless an explicit ammunition rule permits it. The demonstration magazine begins empty; acquisition/reload must supply real owned ammunition.

## Equipment common fields

`properties` is a list of PropertyUse; `features` is a list of feature references. `requirements` is `{acquire?,equip?,use?}`, each a Predicate. `equip` is `{slots:string[],hands:nonnegative integer,exclusiveGroups?:string[]}`. A definition states the slots it consumes; an instance states where it is actually fitted. Profile anatomy/slot capacities decide legality, so “two hands” does not assume every species has exactly two hands.

Optional `cost` is an Amount, `availability` is `{scale:registered key,rating:integer,label?:string}`, `weight` is Weight, and `variantOf` is a same-family ContentRef. Missing cost/weight means unrecorded/not used, not zero. An editorial import issue explains whether the source omits it or it is pending review. Faction/chapter restrictions use explicit affiliation/faction/feature prerequisites, not the word “Astartes” in a name.

A consumable's `useResource` explicitly binds its per-instance charges; `uses` supplies that binding's maximum, and `useAction` must spend the same item-scoped resource. Reaching zero marks that instance depleted; deleting/merging it is an inventory policy, not a second consumption cost. Do not infer the resource binding from the item's name or the order of action costs.

### Weapons

Required `category` and `subcategory` are controlled taxonomy keys from the package/profile, not fixed branches for las/bolt/plasma/etc. `hands` is a nonnegative integer; `properties`/`features` required lists; `modes` is a nonempty array of AttackMode. Optional `proficiencies` lists proficiency references; it must specify use semantics through requirements/policy rather than imply that owning a weapon grants proficiency.

AttackMode required fields: `id`, `name`, `attackKind` (`melee`, `ranged`, `area`), `delivery` (`attack_roll`, `target_test`, `automatic`, `manual`), `damage` list, `range`, and `costs` list. Optional fields: `action`, `test`, `properties`, `features`, `requirements`, `rate`, `target`, `manualRules`.

- DamageComponent: `{id,dice?,bonus: NumberValue,damageType: ContentRef}`. At least dice or a nonzero/variable bonus is required for a damaging component. `damage: []` is permitted only for a genuinely nondamaging mode with explicit effects/manual description. Damage type always required on a component.
- `dice.bonus` is the literal bonus printed with the base dice; component `bonus` is the separately declared variable/scaling addition. Both are included once. Importers must not transcribe the same printed bonus into both fields.
- Range: melee `{kind:"reach",distance:Distance}`; ranged `{kind:"distance",normal:Distance,long?:Distance}`; area `{kind:"area",shape:"cone"|"line"|"sphere"|"burst",size:Distance,origin:"self"|"target",placementRange?:Distance}`. Long >= normal after unit normalization. Omitting long means no long-range band, not unlimited range. Range penalties are policy, not embedded in display strings.
- Rate: optional `{shotsPerUse:positive integer,burstSize?:positive integer,rule?:ContentRef}`. Additional attack rolls, hits or ammo use must be defined through the action/rule; shotsPerUse alone does not imply them. Reconcile declared ammunition cost with the chosen rate.
- Ammunition: optional `{accepted:ContentRef[],capacity:positive integer,resource:ContentRef}`. Resource scope must be item. Capacity maps to the instance maximum; its resource binding overrides the reusable resource template's default maximum explicitly. Accepted refs are ammunition entities. Energy weapons may still use this structure if the real rules use charge accounting.
- Reload: optional `{action:ContentRef,amount:"full"|positive integer,source:"inventory"|"external",requirements?:Predicate}`. Requires ammunition/capacity and an explicit time/action cost. External replenishment needs adjudication rather than manufactured inventory.
- `specialRules`: optional rule references; generic mechanics go through effects/properties. Truly unsupported interactions use a manual rule entry with scope and reason.

Alternate firing modes are complete mode records, each with its own cost, damage, range and prerequisites. A profile/weapon can expose several modes without cloning the whole weapon. Heavy or vehicle-mounted versions use hands/slots, proficiency, crew and property data. Flame/area delivery uses a target test or manual adjudication; do not force it through a ranged attack roll. Melta/plasma/bolt/exotic rules require reviewed effects or manual clauses, not new top-level weapon schemas.

### Armour and shields

Armour requires `category`, `equip`, `properties`, `features`, and `defence` `{value:NumberValue,mode:"base"|"add",stackGroup:string}`. Shields use the same defence structure. This normalizes into the stat-effect pipeline; the armour field is the source of truth, so do not also duplicate the same defence effect in a feature.

Optional `shieldCompatibility` is `allowed`, `forbidden` or `{requires:Predicate}`. Strength requirements use `requirements.equip` or a feature penalty, as the source actually states. Movement changes, resistance, stealth penalties and special protection use feature/property effects. Optional `systems` references system definitions with `{system,quantity,slot}`. Optional `augmeticCompatibility` has allowed/excluded slots/tags and requirements; it cannot override the actor's anatomy without an explicit rule.

Astartes armour is armour plus systems/features and requirements. Autosenses, power supply and interfaces can be system entities. Runtime damage to a system belongs to its installed instance; whether deactivation suppresses its features is an explicit while-source policy. No fictional value or compatibility rule is assumed authoritative here.

## Features and properties

Feature payload required `flavor`, `effects`, `grants`, `manualRules`; optional choices, prerequisites, resources and repeatability. Feats/traits/features differ in acquisition and classification, not mechanical interpreter. Property parameters are named typed declarations `{name,type,required,default?,min?,max?,enum?,referenceKind?}` where type is integer, rational, boolean, enum or reference. Omitted required parameters, unknown arguments or wrong reference kinds are invalid. Defaults must themselves validate. Parameter references in effects use an explicit `{kind:"parameter",name}` NumberValue available only inside a property definition; arbitrary field access is forbidden.

## Actions, reactions, psychic powers

Action `economy` is a profile key; `target` is `{kind:"self"|"single"|"multiple"|"area",scope:"actor"|"object"|"point",maxTargets?:NumberValue,requirements?:Predicate}`. Target count for multiple targets is required and positive. Range may be self-only or one of the weapon range types. Optional `test` is `{rule:ContentRef,actor:"source"|"target",attributeKey?,skill?,difficulty?:NumberValue}`; the referenced test rule declares required fields. Never assume an attack/save/DC system from a name.

`outcomes` contains unique `{id,on:"success"|"failure"|"always",effects,manualRules,rule?}`. For no test, only always is valid. An action with no automatic mechanics may have a manual outcome. A reaction additionally requires a declared trigger/event; special actions require a budget/resource or explicit profile entitlement. Costs, triggered rules and frequency resources use RULES_EFFECTS.

Psychic power `discipline` references discipline; `action` references an action template supplying economy, target, range, test and costs. `duration` states the power's default effect duration. `outcomes` are the power-specific success/failure effects. **The action template used by a power must have no mechanical outcome effects**; its outcomes provide event labels only, avoiding double application. Power effects explicitly declare durations; a validator checks consistency with the power's default unless an exception is documented.

Optional `scaling` uses approved NumberValue tables; `sustainCost` uses resource costs with a declared turn/event boundary; `failureRule` and `perilsRule` reference rule roles psyker/general and perils respectively. Perils rule `table` is `{dice:Dice,entries:[{id,min,max,outcomeAction?,manualText?}]}`. Entries must cover the supported roll range without overlap unless an explicit fallback is given; at least one outcomeAction/manualText per entry. A power may instead use a fully manual perils rule if the source procedure is unknown. Tables do not themselves authorize random rolls during sheet calculation.

## Creature/NPC statblocks

Required fields listed in ENTITY_TYPES separate a template from actor state. `attributes` is a map of profile keys to base numbers; `skills` is a list `{skill:ContentRef,bonus:NumberValue}`; `saves` is `{attributeKey,bonus:NumberValue}[]`. A source may provide a fixed bonus without player-class derivation: annotate the value's source and do not derive a second bonus on top. The profile declares whether explicit statblock bases replace player derivations.

`movement` lists `{mode:profile key,speed:Distance}`. `defence` and `wounds` are NumberValue bases. `mitigations`, `features`, `actions`, `factions` are typed reference arrays. Actions include reaction/special economies; no duplicate reaction engine. Optional `threat` carries named scale and value. `lore` is a lore reference or safe inline Markdown with separate visibility. Equipment is `{id,item:ContentRef,quantity,equipped,overrides?}`.

Permitted weapon overrides are an explicit object of **replacement** fields: `{modeId,damage?,range?,costs?,name?}`. Only an existing mode can be changed; provided arrays replace that field rather than ambiguously concatenate. Override records have provenance and do not mutate the shared weapon. They cannot replace arbitrary effects or reference permissions. Reuse a separate variant weapon if several templates share the change. Other statblock-specific attack bonuses are contextual creature effects or action data, not copied weapon rules.

## Vehicles, mounts and crew

Vehicle `vehicleType` and `size` are profile taxonomy keys; `movement`, `defence` and `hull` are typed bases. `crew` is `{role:ContentRef,count:nonnegative integer}[]`; crew role definitions specify per-role minimum/maximum occupants. Total crew/transport capacities are separate. `transportCapacity` is `{occupants:nonnegative integer,cargo?:Weight,restrictions?:Predicate}`.

Mount is `{id,weapon:ContentRef,quantity:positive integer,slot,crewRole?:ContentRef,arc?:registered key,overrides?}`. Overrides use the creature weapon override contract. Mount IDs are stable local keys; crew `controls` refers to those keys in this host's context. Validate required crew roles exist and quantities fit capacity. Optional firing arcs are capabilities with declared semantics; an unknown arc is not automatically treated as unrestricted.

`systems` is `{id,system:ContentRef,slot,quantity}[]`, `features` are ordinary vehicle-trait features, `damageRule` references a rule role damage and `resources` are resource refs. Mobility, power demand and disabled-system effects use common features/requirements. A vehicle may have multiple movement modes and weapons. Current hull, occupied seats, crew assignments, ammunition and damaged systems belong to an instance. Catastrophic damage procedures remain manual when not represented by approved primitives.

## Taxonomy and campaign metadata

Tags have registered IDs and optional parent hierarchy. Example faction labels may include Imperium, Astra Militarum, Adeptus Astartes, Chaos, Aeldari, Drukhari, Orks, T'au, Necrons and Tyranids, but their canonical identities/relationships require source review. Content may reference multiple factions/tags. Search expansion filters use package/source metadata, not a tag pretending to be a release dependency.

Location/adventure/encounter content references templates; it contains no active campaign party, initiative or session progress. Encounter rewards are optional typed item/currency grants pending GM confirmation, not auto-issued merely because a template was viewed. GM-only prose must be filtered before transmission/index exposure, not merely hidden with CSS.

## Integrated dice extension

Actions may expose optional rolls:RollTemplate[]; test rules supply roll templates for attribute/skill/save/attack procedures. Weapon modes bind their existing test and damage components to distinct action stages. Existing Dice and DamageComponent fields retain their meaning. Profiles may opt into a versioned core.rolls.v1 capability with registered advantage/critical policies; absence does not imply D&D defaults. This additive proposal does not alter the current catalog fixtures. See [Integrated dice rolling](DICE_ROLLING.md).

## Implemented v8 Attack-action capacity

`action.attack.capacity` is a registered stat target for continuous automatic constant `base` effects with max stacking; validated integer range 1–20. v8 grants 2 only through canonical Extra Attack features. `spec.attackActionVersion=1` enables `calculated.attackAction` with `attacksPerAttackAction`, source feature IDs, eligible owned weapon action IDs, scope and `turnTracking=false`. This additive output is absent from historical profiles. Capacity does not generate extra actions or duplicate bonus/reaction/consumable actions. Each attack and linked damage has its own roll definition/session/result. Frontend sequence state is optional and not authoritative.

# Human ruling checklist

Fifteen approved decisions are integrated; **21 of the original 36 remain unresolved**. PHB-RULE-059 remains separate. See the [current readiness report](LEVEL4_ADVANCEMENT_REPORT.md).

## PHB-RULE-001 — RESOLVED

# Approved PHB-RULE-001 — Hiveborn

The detailed Origin `Allowed Species` entry is authoritative over the summary Origin matrix when they conflict.

Hiveborn eligibility:

- Human: allowed normally
- Ratling: allowed normally
- Ogryn: allowed as `RARE`
- Skitarii: not allowed
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entry suggesting Rare Squat/Kin does not apply.

Mark PHB-RULE-001 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-002 — RESOLVED

# Approved PHB-RULE-002 — Penal Worlder

The detailed Origin `Allowed Species` entry is authoritative.

Penal Worlder eligibility:

- Human: allowed normally
- Ogryn: allowed normally
- Ratling: allowed normally
- Skitarii: not allowed
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entry suggesting Rare Squat/Kin does not apply.

Mark PHB-RULE-002 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-003 — RESOLVED

# Approved PHB-RULE-003 — Voidborn

The detailed Origin `Allowed Species` entry is authoritative.

Voidborn eligibility:

- Human: allowed normally
- Ratling: allowed normally
- Ogryn: allowed as `RARE`
- Skitarii: not allowed
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entries permitting Squat/Kin or Rare Aeldari do not apply.

Mark PHB-RULE-003 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-004 — RESOLVED

# Approved PHB-RULE-004 — Forge World

The detailed Origin `Allowed Species` entry is authoritative.

Forge World eligibility:

- Human: allowed normally
- Skitarii: allowed normally
- Ogryn: not allowed
- Ratling: not allowed
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entry suggesting Rare Squat/Kin does not apply.

Mark PHB-RULE-004 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-005 — RESOLVED

# Approved PHB-RULE-005 — Militarum Regiment

The detailed Origin `Allowed Species` entry is authoritative.

Militarum Regiment eligibility:

- Human: allowed normally
- Ogryn: allowed normally
- Ratling: allowed normally
- Skitarii: allowed as `LIMITED`
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entry suggesting Rare Squat/Kin does not apply.

Mark PHB-RULE-005 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-006 — RESOLVED

# Approved PHB-RULE-006 — Underhive

The detailed Origin `Allowed Species` entry is authoritative.

Underhive eligibility:

- Human: allowed normally
- Ratling: allowed normally
- Ogryn: not allowed
- Skitarii: not allowed
- Squat / Kin: not allowed
- Aeldari: not allowed

The previous matrix entry suggesting Rare Squat/Kin does not apply.

Mark PHB-RULE-006 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-007 — RESOLVED

# Approved PHB-RULE-007 — Rare / Limited Origin Availability

Origin availability uses three production-relevant states.

## NORMAL

The Species/Origin combination is legal without additional approval, assuming all other prerequisites are satisfied.

## RARE

The Species/Origin combination is a legal player option but requires explicit GM approval.

Rare does NOT mean:

- invalid
- NPC-only
- automatically selectable

Until the application has a trusted GM/campaign approval mechanism, Rare combinations may be displayed but must not be available for ordinary self-service character creation.

## LIMITED

The Species/Origin combination is an exceptional player option.

It requires explicit GM/campaign approval for the specific combination and appropriate narrative justification.

Limited approval must be specific to the affected Species/Origin combination.

A generic `allow rare content` permission is not sufficient for Limited options.

Until a trusted campaign approval mechanism exists, Limited combinations may be displayed but must remain unavailable for ordinary self-service character creation.

Represent these states structurally.

Do not hard-code approval behaviour into React.

Mark PHB-RULE-007 RESOLVED.

Provenance: `review/approved-origin-rulings.txt`; exact digest and UTC timestamp are recorded in both ruling ledgers.

## PHB-RULE-009 — RESOLVED

Ability modifier:

`floor((abilityScore - 10) / 2)`

Rules:

- Use mathematical floor.

- Ability scores must be positive integers.

- Do not impose a generic maximum score of 20.

- Explicit feature-specific maximums or minimums take precedence.

- Species modifiers are applied according to existing character-creation rules.

- The engine must support legitimate scores above 20.

Update calculation policies, validation and tests.

Mark PHB-RULE-009 RESOLVED.

## PHB-RULE-010 — UNRESOLVED

Define resistance/vulnerability arithmetic, rounding, duplicate stacking, bypasses and their order with reductions, saves and immunity.

## PHB-RULE-011 — UNRESOLVED

Define expertise contribution and interaction with proficiency or repeated grants.

## PHB-RULE-012 — UNRESOLVED

If alternate methods are required, supply point costs/budget or dice/reroll procedure.

## PHB-RULE-014 — RESOLVED

Current Constitution applies once to every attained class level; each class Hit Die contribution has a minimum of 1 before separate feature HP. Maximum HP changes do not heal current HP; clamp only when current HP exceeds the new maximum.

Exact approval and provenance: [approved level-4 brief](../../content/packages/di_phb_1_0/review/approved-level4-rulings.txt), [ledger](../../content/packages/di_phb_1_0/review/decisions.json).

## PHB-RULE-015 — RESOLVED

Choose +2 to one ability, +1 to two different abilities, or one eligible Talent. ASI-specific maximum 20; no partial or wasted increases. PHB-RULE-009 remains unchanged.

Exact approval and provenance: [approved level-4 brief](../../content/packages/di_phb_1_0/review/approved-level4-rulings.txt), [ledger](../../content/packages/di_phb_1_0/review/decisions.json).

## PHB-RULE-016 — RESOLVED

A Talent is owned at most once unless its own explicit text says otherwise. Universal Traits are separate. No general stacking policy is introduced.

Exact approval and provenance: [approved level-4 brief](../../content/packages/di_phb_1_0/review/approved-level4-rulings.txt), [ledger](../../content/packages/di_phb_1_0/review/decisions.json).

## PHB-RULE-017 — UNRESOLVED

Specify Overheat damage amount/type and any weapon-specific exceptions.

## PHB-RULE-018 — UNRESOLVED

For each Blast weapon lacking an area, supply shape/range/size/save procedure or explicitly keep it GM-adjudicated.

## PHB-RULE-020 — UNRESOLVED

How much ammunition does personal Burst consume and which mixed-damage die is added?

## PHB-RULE-022 — UNRESOLVED

Specify trigger, chosen target, save ability and frequency for personal Suppression.

## PHB-RULE-024 — RESOLVED

## Default Weapon Ability Binding

Normal melee weapon:

- Attack ability: Strength

- Damage ability: Strength

Normal ranged weapon:

- Attack ability: Dexterity

- Damage ability: Dexterity

Finesse:

- Strength or Dexterity

- The same selected ability is used for attack and damage

Thrown:

- Uses the ability the weapon would normally use for its melee attack unless an explicit rule overrides it

Spirit Weapon:

- May substitute the user's psychic ability for Strength/Dexterity for attack and damage

Explicit weapon-specific rules override all defaults.

## Save-Based Weapons

Save-based weapon effects do not automatically add an ability modifier to their listed damage.

Only add an ability modifier when a rule explicitly says to do so.

Grenades and similar fixed-damage save effects therefore use their listed damage dice.

## Hands

Defaults:

- Pistol: 1

- Light melee weapon: 1

- Shield: 1

- Normal melee weapon: 1

- Heavy melee weapon: 2

- Versatile: 1 or 2

- Basic firearm: 2

- Shotgun: 2

- Sniper weapon: 2

- Heavy ranged weapon: 2

Add explicit overrides where required.

Force Staff is explicitly 2-handed.

## Reach

- Default melee reach: 5 ft

- Ranged weapons have no melee reach unless a rule gives them one

- Thrown melee weapons retain normal melee reach as well as their throwing range

## Proficiency Groups

Canonical weapon entities must have explicit `proficiencyGroups`.

Support groups including at minimum:

- simple_melee

- martial_melee

- pistol

- basic_firearm

- shotgun

- sniper

- heavy

- grenade

- flamer

- chain

- shock

- plasma

- melta

- force

- shield

- ogryn

- kin

- aeldari

- mechanicus

- rad_weapon

- advanced_firearm

- improvised

- mining_tool

Weapons may belong to more than one group.

Properties may help derive initial group membership, but canonical records must store membership explicitly.

## Starting Equipment Proficiency

A class is proficient with every weapon or shield granted directly by its own level-1 starting-equipment package.

For a package choice, this applies to the selected option.

Do not use this rule to grant unrelated weapon-group proficiency.

## Emplaced Weapons

Emplaced is a deployment restriction, not a proficiency.

Represent conceptually as:

- deployment: emplaced

- requires mount, brace, rig, feature or GM-approved setup

Do not create an `emplaced proficiency`.

Mark PHB-RULE-024 RESOLVED.

## PHB-RULE-026 — UNRESOLVED

Does slash mean choice, split damage or simultaneous types? Specify amounts and mitigation handling for each affected profile.

## PHB-RULE-028 — UNRESOLVED

Specify the exact AC formula for Powered Carapace.

## PHB-RULE-029 — UNRESOLVED

Specify the exact AC formula for Exo-Frame Plate.

## PHB-RULE-030 — UNRESOLVED

Specify the exact AC formula for Ogryn Flak Plate.

## PHB-RULE-032 — UNRESOLVED

Define unarmoured AC, legal protection combinations and stacking of shields/fields/base armour.

## PHB-RULE-035 — UNRESOLVED

Specify concentration maintenance, interruption, limits and check procedure before automating it.

## PHB-RULE-037 — UNRESOLVED

For odd pressure, what remains after Perils? Is pressure floored at zero after all reductions?

## PHB-RULE-038 — UNRESOLVED

Does Warp Step require one ordinary Perils check, an additional check, or another trigger override?

## PHB-RULE-046 — UNRESOLVED

Specify generic stack/removal rules only where needed, or approve manual per-application handling.

## PHB-RULE-047 — UNRESOLVED

Define these statuses or explicitly designate them narrative injury labels with GM adjudication.

## PHB-RULE-049 — RESOLVED

`medkit` in starting equipment is an alias for the canonical Med-Pack.

Do not create a separate Medkit entity.

Update all starting-package references to use the canonical Med-Pack entity while retaining "medkit" as a recognised display/source alias if useful.

Mark PHB-RULE-049 RESOLVED.

## PHB-RULE-050 — RESOLVED

Riot Shield uses the generic Shield profile:

- +2 AC

- requires one hand

Add appropriate tags such as:

- shield

- riot

- arbites

It qualifies for features that require or reference using a shield.

Do not duplicate the full Shield rules in a separate incompatible entity.

Mark PHB-RULE-050 RESOLVED.

## PHB-RULE-051 — RESOLVED

## Generic Starting Light Armour Pool

The starting-equipment option `light armour` contains:

- Armoured Bodyglove

- Mesh Armour

Do not include:

- Heavy Clothing

- Flak armour

- Species-pattern armour

Heavy Clothing remains a separately selectable item where explicitly offered.

## Minor Augmetic Pool

`minor augmetic` means a Controlled-Availability Augmetic Upgrade.

The current approved pool is:

- Optical Implant

- Respirator Implant

- Data-Jack

- Vox Implant

- Mag-Lock Palm

- Dermal Insulation

- Internal Chrono

- Mechadendrite, Utility

- Black-Iron Jaw

- Vocal Coder

Scarce and Rare augmetics do not belong to the generic Minor Augmetic pool.

## Narrative / Utility Starting Items

Canonicalise the following without inventing automatic mechanical bonuses:

- Symbol of Faith: narrative item

- Sanctioning brands/restraints: narrative item

- Psychic Focus: tagged functional item `psychic_focus`, no inherent numerical bonus

- Rations: general/narrative supply

- Lucky Charm: narrative trinket

- Manacles: utility/manual adjudication

- Black-market contact: character contact, not inventory

- Camo cloak: equipment; manual effect until explicitly defined

- Maintenance tools: utility/tool item

- Oath-token: narrative item; does not grant Relic-Bearer

- Survey auspex: scanner/auspex variant with manual utility

- Climbing kit: utility/tool item

- Claim marker: narrative/feature prop

- Spirit-token: narrative item

- Rune stones: Psychic Focus variant

- Spirit charm: narrative item

A canonical inventory item may legitimately have no automated combat mechanics.

Mark PHB-RULE-051 RESOLVED.

## PHB-RULE-055 — UNRESOLVED

Specify generic Aim action/effect or confirm Optic is restricted to Tactical Aim.

## PHB-RULE-056 — UNRESOLVED

Which cover category does half cover mean for personal Armour-Breaking?

## PHB-RULE-057 — UNRESOLVED

For odd total Hit Dice, round long-rest recovery up or down?

## PHB-RULE-058 — UNRESOLVED

Define same/different-source flat bonus, multiplier, temporary effect and duplicate equipment stacking where the PHB is silent.

## PHB-RULE-059 — RESOLVED (additional item-specific ruling)

Frag Grenade only: failed Dexterity save takes full rolled 3d6 piercing; successful save takes half rounded down; no ability modifier; 15-ft radius; existing grenade DC; expend one on use. Generic PHB-RULE-018 remains unresolved. The exact approval, timestamp, source relationship and affected IDs are in [item rulings](../../content/packages/di_phb_1_0/review/item-rulings.json).

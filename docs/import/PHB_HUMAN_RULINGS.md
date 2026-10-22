# Human ruling checklist

Five approved decisions are integrated; **31 of the original 36 remain unresolved**. The separate Frag Grenade save-success gap is recorded in the [current report](PHB_MINIMUM_RULINGS_REPORT.md).

## PHB-RULE-001 — UNRESOLVED

For Hiveborn, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-002 — UNRESOLVED

For Penal Worlder, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-003 — UNRESOLVED

For Voidborn, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-004 — UNRESOLVED

For Forge World, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-005 — UNRESOLVED

For Militarum Regiment, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-006 — UNRESOLVED

For Underhive, does the eligibility matrix or the Allowed Species list govern? State permitted species.

## PHB-RULE-007 — UNRESOLVED

What approval or prerequisite makes a Rare/Limited Origin selectable?

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

## PHB-RULE-014 — UNRESOLVED

How do Constitution changes affect prior HP gains, and is there a minimum per-level gain? How does a max-HP change affect current HP?

## PHB-RULE-015 — UNRESOLVED

Specify ASI amount, allocation, score cap and exceptions.

## PHB-RULE-016 — UNRESOLVED

Can a Talent be selected repeatedly, and which selections/benefits stack?

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

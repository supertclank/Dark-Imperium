# Tier-1 rules engine coverage

Release `di-phb-1.0-tier1-v2`; adapter `phb-tier1-kotlin-v1`. AUTOMATED means baseline values are calculated, not that combat outcomes or feature conditions are adjudicated. No unresolved ruling is resolved by this release.

| Mechanic | Classification | Behaviour / boundary |
|---|---|---|
| Human attributes, movement, class HP, PB, saves, selected skills, equipped Flak AC | AUTOMATED | Pinned policies; Veteran d10 levels 1–3, Hive Scum d8 level 1. No advancement or retroactive Constitution decisions. |
| Initiative / Twitchy | AUTOMATED | Dexterity modifier +2 only; excludes conditional Origin/doctrine bonuses. |
| Weapon attacks/damage, attributes, skills, saves | PARTIAL | 35 baseline RollDefinitions per fixture; authoritative dice and history. Targets, range, hits, critical damage and HP remain manual. |
| Frag Grenade | PARTIAL | Existing approved 3d6/DC/outcome profile; confirmed use consumes inventory. Targets and damage allocation manual. |
| Knife | PARTIAL | Melee plus server-selected Strength/Dexterity for finesse. Thrown use needs GM-approved improvised range under PHB PDF 35; no fabricated fixed range. |
| Autogun / Autopistol | PARTIAL | Single attack/damage available; Burst/Suppression unavailable (020/022). |
| Conditions | BLOCKED | No new condition execution engine or PHB-RULE-046 resolution. |
| Resources | MANUAL | Only applicable calculated resources are initialised on creation; reopen retains owned state. Human failed-save reroll and relevant Origin uses shown. Feature conditions govern availability; Field Discipline is unavailable pending 022 despite its recorded once/short-rest allowance. |
| Contacts | MANUAL | Source-linked package contact separate from inventory; identity agreed with GM. |
| Dirty Fighter | MANUAL | Apply the conditional extra damage manually, once per turn. Baseline damage excludes it. Conditions and combined-source stacking are not automated. PHB-RULE-046, PHB-RULE-058 |
| Streetwise | PARTIAL | The two selected skill proficiencies are calculated. Finding contacts is manual.  |
| Suppressing Fire | BLOCKED | Unavailable: the Suppression procedure is awaiting a ruling. No save DC, condition or automatic roll is supplied. Other character actions remain available. PHB-RULE-022 |
| Forge World benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Hiveborn benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Militarum Regiment benefits | PARTIAL | Choose an eligible ally before initiative to apply Squad Drill manually. Baseline initiative excludes that conditional +1. Field Discipline is unavailable until Suppression is resolved. PHB-RULE-022 |
| Penal Worlder benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Schola Progenium benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Shrine Worlder benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Underhive benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Voidborn benefits | PARTIAL | Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.  |
| Marksman 3 | MANUAL | Apply this feature only when its stated condition occurs. It is not included in baseline rolls. Combined-source stacking requires adjudication; no stacking policy is assumed. PHB-RULE-058 |
| Sergeant 3 | MANUAL | Apply this feature only when its stated condition occurs. It is not included in baseline rolls. Combined-source stacking requires adjudication; no stacking policy is assumed. PHB-RULE-058 |
| Shock Trooper 3 | MANUAL | Apply this feature only when its stated condition occurs. It is not included in baseline rolls. Combined-source stacking requires adjudication; no stacking policy is assumed. PHB-RULE-058 |

## Classes not published

Zealot (Human only, d10, Strength/Charisma saves; primary Strength or Dexterity, Charisma or Wisdom): Fury of Faith is MANUAL once/turn PB radiant/fire; Martyr’s Endurance is PARTIAL in principle (+1 AC below half HP plus manual fear advantage), but selected-state AC is not implemented/certified. Martyr’s Mercy is MANUAL in source (1d6 + Wisdom or Charisma, PB uses/long rest); resource, ability-selection and healing execution remain unimplemented. No corruption/fear/healing interaction was inferred. Training and source armour/weapon groups remain in the class audit. Mandatory Firebomb candidate prevents package certification.

Arbites Enforcer (Human only, d10, Strength/Wisdom saves; primary Strength or Dexterity, Wisdom; light/medium/flak/carapace/riot armour; pistols/shotguns/shock weapons/mauls/shields/grenades): Enforcer Training is BLOCKED for creation until its two-skill choice is mapped. Authority is MANUAL source-defined Wisdom save DC 8 + PB + Wisdom, PB uses/long rest, with three manual outcomes; no condition automation is inferred. Core armour/shield/equipment compatibility is unimplemented. Stun/Smoke remain candidates, not fake canonical manual items. Manacles and Symbol of Faith are already canonical utility/narrative equipment; they need no invented inherent bonus.

## Real package compilation

Veteran and Hive Scum compile in production. The prepared Zealot and Arbites package files map every named item, one-of branch and explicit one-grenade count; tests intentionally reject their mandatory candidate items. They are not releasable inventory. Riot Shield resolves to the approved Shield ID. Compiler tests cover canonical shield grants/equipping separately; this does not certify wielding a two-handed shotgun simultaneously with a shield. One instance is explicitly encoded for each singular named kit entry (PHB PDF 100); no runtime quantity default or text parser exists. Optional/nested choices, narratives, contacts, proficiencies, fixed items and consumables have regression coverage.

## Non-Human preparation

The regenerated machine audit retains each Species size, source, granted features, structured mechanical effects, complete manual core text and class access. No non-Human is published. Ratling Stealth is canonical; Small size, movement/other traits and equipment compatibility still need production projection. Ogryn Big Lad, Dexterity reduction, HP effects, frame restrictions, weapon groups and armour remain certification gates; PHB-RULE-030 blocks Ogryn Flak Plate. Skitarii augmetics/armour compatibility, Kin traits/equipment, and Aeldari movement/vision/core traits require certified projection. See `level-1-3-catalogue.json` species entries for exact source mechanics rather than guessed defaults.

Psyker/Warlock remain blocked: 52 power candidates, 38 required tier-1 Minor/Standard and 14 deferred Major; canonical schemas/pools/resources/execution boundaries incomplete. No manual power placeholders.

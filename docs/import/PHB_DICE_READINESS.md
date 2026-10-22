# Dice readiness after canonicalisation

**PARTIAL**. No 3D UI, RNG runtime or complete RollDefinition compiler implemented in this pass. Base dice are not final actor-resolved rolls.

| Intent | Status | Dependency |
| --- | --- | --- |
| Attribute rolls | BLOCKED | Score-to-modifier derivation absent; explicit modifier inputs can exercise a sum only. |
| Skill checks | PARTIAL | Known d20+ability+PB; entitlements/expertise/context compiler incomplete. |
| Saving throws | PARTIAL | Known formula; modifier and granted-save mapping needed. |
| Initiative | PARTIAL | Quick reference gives Dex formula; modifier/conditional source compilation needed. |
| Weapon attacks | BLOCKED | Canonical weapon/proficiency/mode/context closure incomplete. |
| Damage rolls | PARTIAL | Two typed base-dice templates; not complete actor attack damage or mitigation. |
| Psychic tests | BLOCKED | Known attack/DC/Perils arithmetic but full power/context/resource binding missing. |
| Healing | PARTIAL | Source dice/formulas retained; no action transaction/target/cap policy compiler. |
| Random tables | PARTIAL | Perils band function and source d6/d8 tables; typed outcomes/open-ended schema and context needed. |
| Narrative adjudicated outcomes | MANUAL | GM decisions remain external explicit outcomes, never fabricated random faces. |

## Additive binding extension implemented for draft validation

`phb.roll_bindings.v1` adds optional `damageBindings` to RollTemplate: each row `{groupId, componentId, damageType: ContentRef}`. For the supported one-group-per-component subset, every group binds exactly once, component IDs are unique and types resolve to damage_type. Other group/component arrangements fail until their schema is implemented. Existing unbound templates can still be inspected as base dice, but cannot be called typed damage RollDefinitions. Both PHB templates now bind explicitly.

Future compilation: validate locked source and known context; resolve typed groups and modifiers with provenance; attach immutable actor/action/item/mode/crew/target and state/lock/engine/context snapshot; resolve advantage/critical policy; reject every unresolved dependency; only then produce the DICE_ROLLING RollDefinition. No arbitrary expression, guessed modifier, costs or random outcomes may appear during sheet recalculation. Full schema conformance and authority tests remain part of runtime implementation.

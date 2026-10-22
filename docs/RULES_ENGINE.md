# Content and rules

For the proposed broader canonical content contract, see [docs/content](content/README.md). This document describes the **currently implemented foundation**; the proposal is not yet supported by the application and does not change existing behavior.

## Five distinct layers

1. **Content data:** Human, Guardsman and Lasgun are database rows, not special cases in the application. Their descriptions and mechanics arrive through the content API.
2. **Rules/effects:** Versioned JSON effects express mechanics using generic operations and targets. Weapon properties have stable keys, display labels and structured parameters.
3. **Character state:** Owner, selected content IDs, level, attributes, current wounds and equipment selections are persisted facts.
4. **Calculated values:** Movement and maximum wounds are deterministic outputs of the current selected content's effects. They are not frontend rules or duplicated saved totals.
5. **Presentation:** React renders returned content, state and calculated values. It does not check names, roll damage, grant bonuses or infer weapon rules.

## Implemented vocabulary

```json
{
  "schemaVersion": 1,
  "effects": [{ "operation": "add", "target": "movement", "value": 6 }]
}
```

The engine supports `add` on `movement` and `maxWounds`. It sums effects from the selected species and class. Movement is bounded below by zero; maximum wounds by one. Unknown schema versions, operations and targets fail explicitly. Integer overflow fails instead of wrapping. No arbitrary expressions, executable scripts, reflection or dynamic evaluation are accepted.

The seed Human contributes movement 6; Guardsman contributes maximum wounds 10. These are editable content values, not content-name branches. All six placeholder base attributes begin at 30 under a generic character-creation policy; current wounds initially equal calculated maximum wounds. These provisional policies belong to the engine/service layer rather than UI components.

The Lasgun uses `1d10` Energy damage, ranges 100/300 m and structured properties such as:

```json
{ "key": "two-handed", "label": "Two-handed", "parameters": { "hands": 2 } }
```

Damage dice and properties are displayed, not executed. The engine does not yet interpret reliability, ammunition, hands, attack bonuses, criticals, progression or features. Class progression is a structured level-one placeholder and is not evaluated.

## Next steps

Before expanding mechanics, agree the authoritative rule vocabulary with the group. Introduce a content validation/publishing boundary with schemas, allowed targets, numeric bounds and useful author errors. Define stacking, operation ordering, prerequisites, conditional predicates and calculation provenance explicitly, with unit tests for each rule primitive.

Add immutable content revisions and pin character selections before allowing live content editing. Today sheets recalculate from the current content; changing existing rules would change older sheets. Current wounds are saved state, so a future rules update also needs an explicit policy for values above a newly reduced maximum. Do not silently rewrite character state during reads.

An eventual pipeline can be: load pinned content → gather selected effects → validate predicates → apply deterministic phases → return calculated values and explanations. No event sourcing or generic scripting system is required. Expand a small, typed interpreter only as actual game rules demand it.

# Dice readiness after creation pass

**PARTIAL**, not READY_FOR_ROLL_DEFINITIONS. Two canonical base-damage templates retain validated type bindings. There are **zero complete actor-resolved PHB RollDefinitions** from the representative drafts.

| Intent | Status | Dependency |
| --- | --- | --- |
| Attribute checks |BLOCKED|009 modifier policy and profile binding|
| Skill checks |PARTIAL|Known formula; modifier/entitlement/context missing|
| Saving throws |PARTIAL|Known class save attributes/formula; final modifiers missing|
| Initiative |PARTIAL|Dex formula explicit; 009 and source modifiers missing|
| Weapon attacks |BLOCKED|Weapon/taxonomy/ability/context closure|
| Weapon damage |PARTIAL|Raw typed base templates exist; complete actor damage and critical context absent|
| Psychic tests |PARTIAL|Known formulas/counts/Perils bands; power/action/resource bindings absent|

The draft adapter returns empty action/roll arrays alongside explicit unresolvedFields, not a statement that the character has no actions. It never substitutes0 for an unknown modifier or calls a raw template a RollDefinition. Future compiler requirements remain those in DICE_ROLLING: immutable actor/action/item/mode/snapshot, resolved modifiers with provenance, complete typed components, policy and context. Neither3D dice nor a production compiler was implemented.

> **Current Frag gate pass:** [Results](../import/PHB_FRAG_GATE_REPORT.md). Narrow profile PLAYABLE_WITH_MANUAL_RULES; narrow builder data READY_WITH_MANUAL_RULES. 93 tests; 948 drafts; 310 candidates. Generic Blast and 31 original rulings remain unresolved. Earlier pass statements below are historical.

# Minimum-rulings import capability

`phb.equipment.minimum_rulings.v1` is an explicitly bounded offline import capability. It extends the emitted subset, not the production database schema. All new fields are validated; unsupported fields fail closed.

Weapons retain the domain AttackMode/DamageComponent model and add explicit `proficiencyGroups` from the approved vocabulary, `abilityBinding` for attack and damage, and optional `deployment: emplaced`. The imported subset supports integer hands, source properties, typed damage, ranges, action references and source availability labels. Availability is a controlled PHB label in this import capability; mapping to the general profile's scale/rating object remains a publication task. No ordered numeric availability rating is invented. Grenade save metadata explicitly retains `successOutcome: unresolved`.

Armour adds `dexterityBonus: {enabled,cap?}` to its source base. It is counted once and does not duplicate a feature effect. Equipment/tool/augmetic records retain manual clauses and `functionalTags`, including shared `psychic_focus`; no text is executed. Shield aliases reuse one mechanical profile. Proficiencies can target exact weapons or explicit weapon-group keys. Emplaced never appears in that vocabulary. Starting item provenance is the reviewed package, not a user-supplied proficient flag.

Human Broad Training's one-option reviewed weapon choice exists only to support this proof; other valid weapon/tool/language options are not declared illegal, but remain outside the supported subset. Veteran's four specialist groups are all represented. General choice occurrence provenance remains a runtime implementation task.

`narrow_character.project` validates a fixed supported level-1 configuration and exact kit before calculating the core. The package's approval document and canonical record digests are pinned. This proof pin is not a published ruleset lock. `compile_rolls` accepts an explicit baseline conformance context, emits distinct immutable roll IDs/stages and validates them against DICE_ROLLING. It rejects unsupported critical/advantage/Tactical Aim contexts. Each new execution nonce changes roll identity. Actual hit acceptance, item instance state, resource expenditure and authority are not implemented here and must precede real gameplay execution.

Policy IDs: `phb.advantage.v1` follows PDF 18 cancellation; `phb.critical.v1` follows PDF 31 natural 20, dice twice/modifiers once; `phb.grenade_dc.v1` follows PDF 47 (8 + PB + Dexterity). This baseline compiler emits normal rolls only; it does not silently resolve other policies.

Run `python -B -m unittest discover -s tests/content`. See the [current readiness report](../import/PHB_MINIMUM_RULINGS_REPORT.md).


## Explicit save outcomes capability

`phb.save_outcomes.v1` adds optional mode `area`, `consumption` and `save.outcomes`. Outcomes require explicit success and failure records, each with `damageMultiplier: {numerator, denominator}` and `rounding: floor`. Integers preserve exact arithmetic; denominator must be positive. No scripts or floating-point multipliers are accepted. The existing unresolved representation remains supported; the two forms are mutually exclusive. There is no generic default. Only Frag Grenade currently supplies these approved outcomes. `save_damage` scales an accepted base total without rolling, adding abilities, mutating resources or applying target mitigation. The independent damage RollDefinition retains the unscaled base dice.

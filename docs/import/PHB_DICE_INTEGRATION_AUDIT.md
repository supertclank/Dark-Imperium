> Historical intake report. Current counts, dispositions and readiness are in [PHB_CANONICALISATION_REPORT](PHB_CANONICALISATION_REPORT.md); machine-readable review ledgers have been updated.

# PHB dice integration audit

The source establishes d20 tests, advantage/disadvantage and natural20 critical rules. Earlier design examples remain placeholders; source evidence now supplies these particular policies. These classifications assess representability, not deployed engine support.

| Roll family | Source | Classification | Mapping / blocker |
| --- | --- | --- | --- |
| Skill/ability checks |2.5,22 | CONDITIONAL | d20 + ability modifier + proficiency if applicable; ability derivation needsPHB-002 |
| Saving throws |2.5,22 | CONDITIONAL | Same structure; source grants determine proficiency |
| Initiative |22 | CONDITIONAL | d20 + Dexterity modifier; feature contributions/context required |
| Personal attack |22, weapon properties | CONDITIONAL | d20 + applicable proficiency + relevant ability; hands/categories/attribute choice need mapping |
| Simple weapon base damage |8.1 Lasgun | READY | 1d8 radiant and80/240ft verified; isolated base-dice template only |
| Multiple additive damage types |8.1 Bolter | READY | 1d10 piercing and1d4 thunder are separate components; actor bonus allocation still pending |
| Slash damage |8,14 | AMBIGUOUS | PHB-006; no inferred split/choice |
| Advantage/disadvantage |2.5 | READY | Two d20 keep higher/lower; multiple same sources do not stack; opposites cancel |
| Critical |6.6 | READY | Natural20 attack; double damage dice, modifiers once; Brutal/Chain extra dice separately |
| Forced critical / rerolls |Class features | CONDITIONAL | Kill Confirmed and other exceptions need action/context lineage; no hardcoded weapon names |
| Psychic attack/save |14 | CONDITIONAL | Psychic attribute is Intelligence or Wisdom; access/cost/pressure procedure required |
| Healing |14,17,19 | CONDITIONAL | Dice and modifier refs fit the sampler; application, restrictions and durations need mapping |
| Death saves |6.7 | READY | d20 thresholds10+, natural1/two failures, natural20/1HP; state changes are transactional |
| Hit Dice recovery |6.13 | CONDITIONAL | Class Hit Die + Constitution; spending/recovery separate from random sampling |
| Perils trigger/severity |15 | AMBIGUOUS | d20 <= currentPressure; severity d20+Pressure; open31+band and Warp Step wording need review |
| Injury table |19 | READY | d8 lookup; optional GM-announced campaign procedure |
| Breakdown |21.5 | CONDITIONAL | d6 lookup, deduplicated triggers and repeated-result substitution |
| Mounted attack |21.3 | CONDITIONAL | d20+driver/gunnerDex+proficiency if trained; actor/crew binding required |
| Battle cannon |21.11 | CONDITIONAL | TargetDex save,3d10piercing+3d10thunder; no attack roll, crit orDexdamage; one shell |
| Vehicle driving/chase |21.2,21.7 | CONDITIONAL | Dexterity(Vehicles)+Handling; speed modifier and contest context |
| Requisition |18.2 | CONDITIONAL | d20+proficiency+relevant modifier+GMStanding/circumstance; no assumed price economy |
| Random target/power chosen by GM |15.4.6 | MANUAL | Need a validated target/power pool or explicit adjudication, not guessed dice sizes |

Exactly two isolated RollTemplates are staged inside canonical manual actions (Lasgun and Warp Spark base damage). **Zero actor-resolved RollDefinitions are emitted:** they require a real actor snapshot, approved profile and context. No final attack bonus is stored in weapon content. No RNG/3D/realtime interface is implemented in this task. See PHB-015 for the narrow template-binding gap.

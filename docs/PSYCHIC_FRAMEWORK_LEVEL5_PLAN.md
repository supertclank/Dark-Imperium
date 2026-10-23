# Shared psychic framework preparation through level 5

Status: plan only, no psychic class publication. Canonical evidence: PHB PDF pages 56–58 (Psyker), 83–84 (Warlock), 91–93 (powers), 95–96 (Pressure/Perils). The roster contains exactly two psychic classes and nine psychic subclasses. Zealot's faith features are not psychic mechanics.

## Required shared contracts

1. Pin psychic ability and source-defined overrides. Psychic attack = proficiency + psychic ability; save DC = 8 + proficiency + psychic ability. Do not change fixed martial weapon ability policy. Warlock Witchblade Training needs its own canonical psychic-ability weapon override.
2. Validate known-power choices, uniqueness, allowed discipline tags and tiers. Both class tables have Minor/Standard/Major counts 2/2/0 at 1, 2/3/0 at 2, 3/3/0 at 3, 3/4/0 at 4–5. No Major access before its source level. Psyker chooses discipline at level 1 and gets the discipline feature at 3; Warlock selects its path at 3. Universal access, discipline restrictions and replacement rules require explicit representation.
3. Generic power Action/RollDefinition data: action/bonus action/reaction, range/area, attack or save, damage/healing/temporary HP and manual target effects. Targetless UI must not claim a hit or mutate another creature. Ownership/eligibility checked by server before each session.
4. Warp Pressure starts at 0; source costs are Minor +1, Standard +2, Major +3, Empowered +1. Resolve the power and then physically roll d20 against current pressure. Keep the pressure mutation, roll session, cancellation and retry boundary transactional and idempotent. Never re-spend pressure during replay.
5. Perils triggers on raw d20 <= pressure. Severity is a separate d20 + pressure roll. Preserve each result, source table and links. Standard table is the default; optional Aeldari/Malefic tables need explicit campaign configuration/GM choice, not an automatic species switch. Narrative/GM-selected consequences stay manual and inspectable.
6. Rest metadata: short/long rest pressure reset 0. Vent uses an action and DC 12 Wisdom save; source success reduces 1d4+proficiency, failure reduces 1 and causes 1d6 psychic damage. Implement only after pressure-floor/rounding decisions are supplied. No arbitrary truncation or negative-pressure assumption.
7. Empowered options are canonical mutually exclusive per casting. Check applicability and costs; do not stack cost reductions. Level-5 Psyker Empowered Manifestation and Warlock Empowered Rune each provide a once-per-short-rest source-limited cost exemption. Warlock exemption applies only to Warlock/Divination/Telekinesis powers. Generic resource maxima/recovery and per-use state must be persisted.
8. Psychic Ward and Rune Ward: reaction, range 30 ft, reduction 1d8 + psychic modifier, pressure +1. Do not assume whether a non-power ward triggers an ordinary manifestation Perils check without source support. Keep unresolved procedure explicit.
9. Reuse generic Level-4 improvement policy and PHB-RULE-014 HP; d6 class HD, INT/WIS saves. Validate mandatory starting psychic equipment, forces/witchblades, armour, focus and powers before publication.
10. Inspector and shared manual labels must show source, action cost, trigger, uses, recovery, tier, tags, range and automation status. No bespoke class-specific React request endpoints.

## Decisions and approval gates

- PHB-RULE-035: concentration maintenance, interruption, limits and checks.
- PHB-RULE-037: odd-pressure post-Perils reduction interpretation and lower bounds after reductions. Existing ledger remains authoritative; do not decide it from wording during implementation.
- PHB-RULE-038: Warp Step's Perils timing/check count.
- PHB-RULE-046/058: conditions/stacking remain explicitly manual where a complete baseline power is otherwise executable.
- Blank / Null-Bound requires trusted GM approval; Universal/Null only, no Malefic. Warlock Pyromancy access requires GM approval. Origin RARE/LIMITED restrictions persist independently.
- Investigate equipment and optional Perils-table selections separately; do not label normal attacks plus incomplete powers a playable psychic class.

## Acceptance before publication

Validate every legal discipline/path and level-1–5 transition, forbidden power tags/tiers, explicit campaign approvals, ability forging, pressure/uses exactly-once finalisation, concurrent requests, cancellation/recovery, concentration gating, Perils boundary values and post-Perils arithmetic, both level-5 exemptions, same-profile history/replay and immutable migration. Test each class through the actual builder and progression UI; verify physical raw values against persisted results at mobile widths. Do not expand to level 6.

## Sequencing

The smallest immediate blocker-clearing milestone is **Mandatory Starting Equipment Rulings for Zealot and Arbites**: Firebomb success outcome/burning ground, Stun/Smoke use contracts, shield/base-armour combinations, plus each affected subclass's existing blocker. Once those non-psychic gates are answered, certify those classes through 5 using shared resource/action infrastructure. The next substantial engine milestone is **Shared Psychic Framework & Psychic Class Certification Through Level 5**.

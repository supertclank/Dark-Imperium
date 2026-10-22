# Frag Grenade ruling and narrow playability gate

**Narrow character: PLAYABLE_WITH_MANUAL_RULES. Narrow builder data: READY_WITH_MANUAL_RULES.** The existing Human / Schola Progenium / Veteran level-1 proof now has no unresolved mandatory creation dependency. These are content/data readiness results, not a claim that a production runtime or published full-catalogue lock exists.

## Approved ruling and scope

Recorded **PHB-RULE-059**, resolving PHB-GAP-FRAG-SAVE-SUCCESS for **Frag Grenade only**. The exact approval document is preserved with SHA-256, user provenance, UTC recording timestamp, PHB PDF 47 relationship and both affected entity IDs. Five earlier approvals remain intact. **31 of the original 36 rulings remain unresolved; generic PHB-RULE-018 is still unresolved.** The new item ruling is tracked separately rather than silently changing the original checklist denominator.

The weapon mode now owns explicit per-save rational damage multipliers: failure 1/1; success 1/2 with floor rounding. It also stores Dexterity save, grenade DC policy, 15-ft radius, 3d6 piercing, no ability damage binding, and consumption of one item at committed use. The action points to that mode instead of duplicating the mechanics in another effect. The reusable schema has no implicit half-damage default.

| Measure | Result |
| --- | --- |
| Canonical drafts | **948**; two existing records revised |
| Remaining candidates | **310** |
| Manual entries | **692** |
| Passing content tests | **93** (81 existing, 12 new; previous gap expectations updated for the approval) |
| Original unresolved rulings | **31** |
| Baseline RollDefinitions | Existing 8 retained; Laspistol attack/damage and grenade base damage added: **11 total** |
| Narrow proof | **PLAYABLE_WITH_MANUAL_RULES** |
| Narrow builder data | **READY_WITH_MANUAL_RULES** |
| Full level 1–3 catalogue | **BLOCKED** |
| Rules Engine / Dice Engine | **PARTIAL / PARTIAL** |
| Docker | **UNVERIFIED**; prior environmental failure retained |

## Revalidated proof

The selections and starting equipment are unchanged: Human, Schola, Veteran 1, Twitchy, standard array with the existing species increases, recorded skill/specialist/Broad Training choices, Lasgun, Laspistol, Combat Blade, equipped Flak Armour, two Frag Grenades and Med-Pack. Selection and exact-kit validation pass. Invalid or incomplete configurations remain rejected/incomplete.

Core output remains STR 17 / DEX 15 / CON 13 / INT 12 / WIS 10 / CHA 8; modifiers +3 / +2 / +1 / +1 / 0 / −1; PB +2; HP 11; AC 14; Speed 30 ft; initiative +4. Existing skills and saves remain unchanged. Lasgun is +4 to attack and 1d8+2 radiant; Combat Blade using Strength is +5 to attack and 1d6+3 piercing. Laspistol is +4 to attack and 1d6+2 radiant.

Frag Grenade intent is DC **12 Dexterity**, **15-ft radius**, **3d6 piercing**, **zero ability modifier**. Its base damage RollDefinition is independent of target save results. Explicit outcome evaluation proves failure 11 → 11, success 10 → 5 and success 11 → 5; tests cover every possible 3d6 total. No roll compilation or projection consumes a grenade or mutates the persisted draft.

Source-defined manual procedures remain visible and do not block ordinary manual play: conditional fear advantage, Human's failed-save reroll, Tactical Aim target/turn tracking, Med-Pack use and action/reload/resource adjudication. The production engine has not automated all of these procedures.

## Dependencies and runtime boundaries

**Remaining mandatory narrow creation blockers: none.** The resolved item gap was removed from creation diagnostics. Missing structured save data still re-blocks validation; the test suite prevents a missing outcome from silently inheriting a default.

**Deferred encounter detail:** whether grenade damage is rolled once for the whole area or separately per target remains unapproved. The intent explicitly says DEFERRED. This is an encounter execution question, not a reason to re-block character creation. The runtime contract requires an explicit adjudicated sharing policy before automatic multi-target execution.

**Full catalogue:** Origin/rarity rulings 001–007 and all other unanswered original rulings remain blocked in their applicable scopes; 310 candidates and broader class/power/resource/conditional mappings remain incomplete. No unsupported options are certified by the narrow result.

**Runtime implementation:** backend ownership/context validation, a production narrow RulesetLock, persisted character/item identity, accepted hit/parent-result linkage, authoritative dice resolution and atomic/idempotent resource transactions remain future work. An offline RollDefinition is never authorization to act. See the new [Character Runtime Contract](../content/CHARACTER_RUNTIME_CONTRACT.md), including separate Lasgun and grenade protocols.

## Verification and next task

The full content suite passes **93 tests**. Coverage includes the structured save schema, malformed/unknown outcomes, modifier exclusion, scope protection for Blast and other grenades/area attacks, exact preserved approval provenance, all mandatory starting-weapon roll structures, immutable projection and the narrow readiness gate. Existing generic content/dice design fixtures are checked separately.

Docker was not rerun because the preceding buildx access denial and absent Docker Desktop Linux-engine pipe are environmental. The existing **UNVERIFIED** state remains; no application failure or Docker success is inferred. The runtime and frontend/backend application source were not redesigned.

Recommended next task: **Implement the first production data-driven character builder and character persistence flow for the validated narrow Human / Schola Progenium / Veteran path, while keeping unsupported PHB options visibly unavailable.** Include server-side validation and a narrowly pinned profile; do not expose the rest of the catalogue as playable.

Artifacts: [proof input](../../tests/fixtures/narrow/veteran-level-1.json), [calculated profile and 11 rolls](../../content/packages/di_phb_1_0/review/narrow-character-result.json), [item ruling ledger](../../content/packages/di_phb_1_0/review/item-rulings.json), [readiness gate](../../content/packages/di_phb_1_0/review/narrow-playability-gate.json), [exact approval](../../content/packages/di_phb_1_0/review/approved-frag-grenade-ruling.txt).

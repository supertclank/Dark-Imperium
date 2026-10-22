# Minimum PHB rulings and narrow character proof

Applied exactly the five user-approved rulings **009, 024, 049, 050, 051**. **31 of the original 36 remain UNRESOLVED**, including all seven Origin/rarity decisions 001–007. The approval text is preserved byte-for-byte with SHA-256 provenance in the review ledger. No other ruling was resolved by implication.

| Measure | Result |
| --- | --- |
| Canonical drafts | 948 (previously 874) |
| Remaining candidates | 310 (previously 333) |
| Candidates promoted | 23; original evidence retained |
| New canonical records | 74, including promotions and new choices/proficiencies/items/actions |
| Manual entries | 692 |
| Content regression tests | **81 pass**, including all 61 prior tests updated for the approved state and 20 new tests |
| Narrow calculated core | **PASS** |
| Structured baseline RollDefinitions | **8**, deterministic and validated |
| Narrow playable character | **BLOCKED** |
| Full level 1–3 catalogue | **BLOCKED** |
| Rules Engine / Dice Engine | **PARTIAL / PARTIAL** |
| Docker | **UNVERIFIED**, commands attempted |

## Integrated content

Ability modifiers use mathematical floor with positive integer scores, no generic cap of 20, and explicit feature-specific bounds. Weapon policy covers Strength melee, Dexterity ranged, same-ability Finesse, melee-based Thrown, optional psychic Spirit Weapon substitution and explicit overrides. Save-based damage receives no automatic ability modifier. Hands/reach defaults, Force Staff's two-hand override, explicit proficiency groups, exact starting-item proficiency and emplaced deployment are tested.

Promoted common profiles include Lasgun, Laspistol, Autogun, Autopistol, Stub Pistol, Combat Blade and Trench Club. Frag Grenade has its explicit dice, type, range, save/DC and an unresolved successful-save outcome. Four armour profiles use their exact source base + Dexterity expression. The ten approved Controlled augmetics are canonical with visible manual effects. Medkit is an alias of Med-Pack; Riot Shield uses the single Shield profile (+2 AC, one hand). Narrative/utility items introduce no invented numerical bonuses; black-market contact remains outside inventory. Psychic Focus and Rune stones share the functional tag `psychic_focus`.

The two-member light-armour pool and ten-member minor-augmetic pool reference canonical records. Every affected starting token has an explicit alias/pool/contact binding. This does not certify all other class kit choices: the Veteran proof selects Med-Pack, while the unreviewed auspex alternative remains unavailable. Exotic weapons and ambiguous mechanics remain candidates or blocked contexts.

## Narrow proof

Human, Schola Progenium, Veteran level 1, Twitchy. Standard array STR 15 / DEX 14 / CON 13 / INT 12 / WIS 10 / CHA 8; Human +2 STR / +1 DEX. Human adaptability: Acrobatics. Origin: History and Intimidation. Veteran skills: Athletics and Insight. Specialist weapon group: sniper. Broad Training explicitly records Trench Club proficiency; this narrow supported option is not a new restriction on the PHB's broader weapon/tool/language choice.

Starting kit: Lasgun, Laspistol, Combat Blade, equipped Flak Armour, **two** Frag Grenades, Med-Pack. The validator checks exact selected-package membership and quantities. Starting-kit proficiency grants only its actual weapon/shield IDs, not their whole groups. Class groups are recorded separately.

| Value | Calculated result |
| --- | --- |
| Final scores | STR 17, DEX 15, CON 13, INT 12, WIS 10, CHA 8 |
| Modifiers | +3, +2, +1, +1, +0, −1 |
| Proficiency | +2 |
| Maximum HP | 11 (d10 first-level maximum +1 CON) |
| AC | 14 (Flak Armour 12 +2 DEX) |
| Speed | 30 ft |
| Initiative | +4 (+2 DEX, +2 Twitchy) |
| Saves | STR +3, DEX +4 proficient, CON +1, INT +1, WIS +2 proficient, CHA −1 |
| Proficient skills | Acrobatics +4, Athletics +5, History +3, Insight +2, Intimidation +1 |

Known source features and manual clauses remain visible, including Human's failed-save reroll, Schola conditional fear advantage and Imperial Education, Tactical Aim and Med-Pack usage. Baseline roll context explicitly excludes Tactical Aim, advantage/disadvantage and critical damage; it does not discard those mechanics globally. Level 2–3 is intentionally not certified, since Suppressing Fire introduces a different dependency.

## Eight validated baseline rolls

| Roll | Expression |
| --- | --- |
| Strength check | 1d20 +3 |
| Athletics check | 1d20 +5 |
| Dexterity save | 1d20 +4 |
| Initiative | 1d20 +4 |
| Lasgun attack | 1d20 +4 |
| Lasgun damage | 1d8 +2 radiant |
| Combat Blade attack (Strength Finesse choice) | 1d20 +5 |
| Combat Blade damage | 1d6 +3 piercing |

Lasgun explicitly belongs to basic_firearm, requires two hands and uses Dexterity for both rolls. Attack and damage use distinct roll IDs/stages with a shared execution identity. Definitions retain actor, canonical source, policy IDs, content snapshot, state version, inventory/context digest and typed components. Changed context produces new identities. These are **offline conformance definitions**, not permission to attack or apply damage; production ownership/context checks, accepted hit/parent results, ammunition transactions and persistent ruleset locking remain implementation work. No animated dice or builder UI was added.

The Frag save intent separately validates **DC 12 Dexterity, 15-ft radius, 3d6 piercing, ability damage bonus 0**. It does not fabricate the result of a successful save.

## Exact remaining blockers

**Narrow source blocker:** PDF 47 lists a Frag Grenade Dexterity save and 3d6 piercing damage but never states the successful-save consequence. Unlike Frag Bomb, it does not explicitly say half damage. Generic Blast says “usually” and does not supply an unconditional default; ruling 018 remains unresolved. The Veteran kit requires two Frag Grenades, so the selected dependency cannot be silently excluded or relabelled manual-by-design. See `review/narrow-source-gaps.json`. This newly isolated gap does not change the honest count of **31 unanswered original rulings**.

**Full catalogue blockers:** unresolved 001–007 Origin/rarity gates; conditional expertise, advancement/repetition, HP reconciliation, equipment/stacking and other selected-context rules; 310 candidates; incomplete power, resource, action and higher-level mappings. The reviewed starting branch does not make the rest available. Every original unresolved ruling retains its prior ID and decision=null.

**Implementation boundaries:** the conformance adapter does not replace backend authorization, complete occurrence validation, runtime state transactions, the general-purpose compiler or a published profile. The content package remains a private draft with publication blocked. The core proof can be reproduced independently of those runtime services.

Next task: obtain an explicit Frag Grenade successful-save ruling (or a precise source citation), then close and retest the narrow gate and runtime contract. **Do not yet recommend the full builder UI as ready for implementation against a playable PHB profile.**

## Verification and artifacts

`python -B -m unittest discover -s tests/content` — 81 passing tests. Structural validation still covers all 45 subclass progressions, canonical references/digests, source identity, candidate closure and existing policies. Regressions cover every requested minimum-ruling area, incomplete kits, missing specialist choices, invalid characters, malformed equipment/roll fields and approval provenance.

Docker build fails opening the buildx lock (access denied); startup fails because the Docker Desktop Linux engine pipe is missing. Frontend tests fail on pnpm's project-store symlink (EPERM); backend tests fail connecting to the Gradle daemon. These are **not** application-suite passes. See [infrastructure details](PHB_DOCKER_VERIFICATION.md).

The exact draft/context is in [proof input](../../tests/fixtures/narrow/veteran-level-1.json); calculated output and all roll definitions are in [proof result](../../content/packages/di_phb_1_0/review/narrow-character-result.json). See [ruling checklist](PHB_HUMAN_RULINGS.md), [promotion list](../../content/packages/di_phb_1_0/review/minimum-rulings-promotions.json), [starting bindings](../../content/packages/di_phb_1_0/review/starting-reference-bindings.json) and [schema capability](../content/PHB_MINIMUM_RULINGS_CAPABILITY.md).

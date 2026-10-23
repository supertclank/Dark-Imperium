# Dice rolling UX overhaul — completion report

Verified 23 October 2026 against the local PostgreSQL-backed application. No PHB rulings, progression data, pinned profile snapshots, attack adjudication, or damage application rules changed.

| # | Requirement | Implementation / evidence |
|---|---|---|
| 1 | Presentation state | IDLE, REQUESTING, ROLLING, SETTLING, REVEALED, DISMISSED in DicePresentation. Cross-panel coordinator prevents concurrent character/free presentations. |
| 2 | Delayed result | Completed server response stays outside result markup until renderer completion; reveal is bound to the specific presentation event. |
| 3 | History/latest masking | Character and free history are masked throughout requests, animation and convergence, including replay. Fresh history fetches cannot bypass the gate. |
| 4 | Page overlay | Transparent fixed viewport surface, safe margins, preserved scroll, no focus trap; compact floating result, dismiss, automatic hold/fade. |
| 5 | Physics | Lazy Three.js + @dimforge/rapier3d-compat 0.21.0. WASM physics is presentation-only. |
| 6 | Boundaries | Fixed floor plus four tall wall colliders, CCD, bounded catch-up, viewport resize containment. |
| 7 | Dice collision | Dynamic convex hull bodies share one Rapier world; real contact impulses transfer momentum. |
| 8 | Tuning | Central dice-physics.ts: gravity -25, friction .7, restitution .32, linear damping .8, angular damping .9, timestep 1/60, maximum natural phase 3200 ms, convergence 700 ms. |
| 9 | Dice models | d4 with truncated resting caps, cube d6, octahedron d8, kite-faced trapezohedron d10, dodecahedron d12 and icosahedron d20. Dark rough bodies and bone numerals. |
| 10 | Numerals | Transparent canvas textures with no rectangular background; oriented face planes, centred type, 6/9 disambiguation. |
| 11 | Face mapping | Explicit numbered face index/value/normal/numeral quaternion from dieFaceMap. d4 resting caps are unnumbered. |
| 12 | Landing | Final quaternion maps the server-selected face to world +Y, independent of camera. Geometry support height keeps vertices above the floor. Smooth convergence ends in an exact fixed pose. |
| 13 | Completion barrier | No callback until the entire physical pool finishes convergence. Skip places every die first, then invokes completion. |
| 14 | Multiple dice | Varied velocities, spin and spawn height. Natural positions retained when sufficiently separated; dense pools use spaced final positions to keep faces readable. |
| 15 | Percentiles | One stored d100 becomes two visual d10 bodies with separate stable identities: tens 00–90 and units 0–9. 00 + 0 represents 100. Both participate in the barrier. |
| 16 | Ability controls | All six backend-exposed ability checks use RollActionButton. |
| 17 | Skills | Every executable skill option remains accessible in the skill group. |
| 18 | Saves | All six backend-exposed saving throws. |
| 19 | Initiative | Prominent expanded initiative control. |
| 20 | Attacks | Backend-supported weapon attacks; only backend-permitted Finesse ability substitutions. |
| 21 | Damage | Direct damage plus linked damage after attack reveal. No automatic hit claim, critical damage or target HP update. |
| 22 | Consumables | Existing confirmation, transaction, optimistic state version and idempotency retained. Quantity can update on commit; damage/save outcomes wait for reveal. |
| 23 | Shared control | RollActionButton consumes server RollOption metadata and availability. |
| 24 | Launcher | Persistent authenticated Dice button in the shared application header. |
| 25 | Pool | Click a die to add; explicit plus/minus, quantities, summary, clear, roll; seven supported types. |
| 26 | Free API/history | POST/GET /api/rolls/free. Strict pool request, secure server dice, zero modifier, FREE_ROLL category, server-built definition, private owner history, request digest/advisory lock idempotency; migration V8. |
| 27 | Replay / again | Replay uses stored values locally and does not POST or consume. Roll Again creates a fresh request UUID. Replaying an old free roll preserves history ordering. |
| 28 | Accessibility | Reduced motion places final dice, then reveals after 150 ms; text mode reveals upon response. Initialization/context-loss fallback preserves the stored result. Optional sound retained. Settings synchronize across page controls. |
| 29 | Physics tests | 17 tests: floor/wall/corner containment, energy loss for all six shapes, die-to-die momentum, percentile identities and planar supporting faces for every authoritative orientation. |
| 30 | Reveal tests | Presentation + panel + free tests cover hidden completed responses, settling, history masking, linked-damage gating, skip, replay, stale callbacks, text/reduced modes and fallback. |
| 31 | Frontend | All 95 tests pass in the final full regression run. TypeScript passes. |
| 32 | Backend | 98 tests, zero failures. Free-roll test exercises authentication, owner isolation, persisted replay, conflicting UUID, invalid/duplicate/empty pools, forbidden modifier and 100d100 limit. |
| 33 | Content | All 152 integrity/regression tests pass. |
| 34 | Single die browser | Free d20: held text/history while tumbling, then revealed stored 7. |
| 35 | Multi-die browser | 4d6: hidden values/history while rolling; final values 5,5,4,5 and total 19. Replay kept values unchanged; skip placed matching faces. |
| 36 | Mixed browser | 1d20 + 1d12 + 1d8 + 2d6: hidden result during animation, grouped reveal; fresh Roll Again produced 16,11,5,2,6 total 40. Screenshot retained. |
| 37 | Free browser | Pool editing, server resolution, post-reveal history, local replay and fresh Roll Again verified; percentile 67 visually landed 60 + 7. |
| 38 | Spoiler browser | Explicit DOM checks while rolling for ability, skill, save, initiative, attack (including natural 20), linked damage and confirmed grenade. No Total, Latest result or new history row during animation. Evidence JSON retained. |
| 39 | Production build | Compilation, TypeScript and all eight static pages pass. Standalone traced-file packaging fails with the pre-existing Windows EPERM mkdir restriction. Deployable production bundle NOT certified. |
| 40 | Docker | Compose configuration validates. Docker Desktop Linux engine pipe absent. Startup remains UNVERIFIED, per user instruction. |
| 41 | Performance | Lazy physics/3D imports, cached WASM module, shared geometry/textures within each pool, pixel ratio capped at 1.5, maximum 20 physical bodies. Per-presentation world/GPU resources are disposed after hold/dismiss; no persistent idle animation loop. No console errors/warnings during checked browser rolls. No formal frame-rate benchmark claimed. |
| 42 | Limits | Above 20 physical dice (d100 counts as two) uses complete text presentation. Final convergence is controlled visual steering, not a second physics-based rules decision. Small-screen/device coverage is not exhaustive. Docker/standalone packaging limitations remain as above. |
| 43 | Next milestone | Non-human advancement through 2–4 and Ratling Sharpshooter certification were already completed in v6 before this task. Review the v6 and dice acceptance reports, resolve deployment verification, and seek explicit scope before any level-5/Extra Attack work. |

## Browser evidence

- [Final overlay over the character sheet](verification/dice-ux/dice-overhaul-final.png)
- [Seven character action checks](verification/dice-ux/dice-character-acceptance.json)
- [Mixed pool final faces and total](verification/dice-ux/dice-overhaul-mixed.png)
- [Percentile final pair](verification/dice-ux/dice-percentile.png)

The character checks used local acceptance fixtures, not a live campaign. One Frag Grenade was consumed by the confirmed test transaction (2 → 1). Stored replay did not consume another item.

## Authority and scope

Free rolls are intentionally independent of character profile snapshots and have no automatic modifiers. The client submits only a request UUID and supported count/sides groups; server-generated values, totals and persistence are authoritative. Physical motion never writes back a die value. Character rolls retain their original backend authorization and transactional logic.

Rapier integration reference: https://rapier.rs/docs/user_guides/javascript/getting_started_js/

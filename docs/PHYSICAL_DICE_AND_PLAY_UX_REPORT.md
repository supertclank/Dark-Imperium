# Physics-determined dice and character-sheet play UX

Verified locally on 23 October 2026. This milestone supersedes the predetermined-result animation model documented in DICE_UX_OVERHAUL_REPORT.md. No game rulings, character levels, content profiles, or progression rules changed.

## Completion checklist

| # | Requirement | Implementation and verification |
|---|---|---|
| 1 | Sheet layout | Compact PlaySheet replaces the long calculated-summary presentation. Existing advancement and deletion remain secondary controls. |
| 2 | Header/combat | Identity, class/subclass/level, current/max HP, defence, initiative, movement, proficiency, and expandable pinned profile. |
| 3 | Abilities | Six prominent modifier buttons, with scores secondary. Values come from saved server calculations. |
| 4 | Saves | Compact rows, proficiency marks, and direct server-authorized roll controls. |
| 5 | Skills | Dedicated compact column, proficiency markers and direct modifier buttons. |
| 6 | Actions | Default tab with attack/damage buttons, range, type, quantity, manual flags and expandable details. Finesse alternatives are supplied by the backend, not recalculated in React. |
| 7 | Inventory | Compact quantities/equipped markers and expandable item actions. No new equipment mutation rules. |
| 8 | Features/Traits | Grouped by species/origin/class/subclass/talent/other; expandable descriptions and source locators, with calculated/manual/conditional/unavailable labels. |
| 9 | Context panel | Optional context panel not added. Existing explicit Finesse choice and linked attack damage remain supported. |
| 10 | Responsive | Three columns on desktop; Actions moves above supporting columns at tablet/narrow sizes. Mobile abilities use a 3×2 grid, buttons at least 44px tall. |
| 11 | Shared controls | RollActionButton and the shared coordinator cover character/free rolls, duplicate prevention, and accessible names. |
| 12 | Old predetermined presentation | Removed production settledOrientation, target quaternion/convergence and forced-result renderer. Ordinary UI flows no longer POST to immediate server-RNG endpoints. Legacy API endpoints remain compatible for existing clients/tests; server RNG also supplies explicit fallback. |
| 13 | Sessions | V9 physical_roll_sessions stores owner/request, authorized specification, seed, expiry, reservation, status, submission digest and accepted result. Authorization returns no raw values or total. |
| 14 | Server seed | SecureRandom generates a fresh 256-bit seed. Seeded launch conditions derive from seed + die identity + retry number. Expiry is five minutes. |
| 15 | Physics | Rapier 0.21.0 rigid-body simulation at fixed 1/60s steps; seeded positions, uniform rotations, velocities/spin; gravity, friction, restitution, damping and CCD. |
| 16 | Colliders | Convex hulls match displayed d4/d6/d8/d10/d12/d20 geometry. d4 uses a truncated tetrahedron with paired opposite-cap labels; d10 uses a polar-dual antiprism. |
| 17 | Boundaries | Fixed floor and four tray walls. Camera adapts to viewport; the physical tray does not change when resized or when presentation mode changes. |
| 18 | Dice collisions | Bodies collide with each other. Accepted dice retain their physical pose and remain colliders while unresolved dice finish. |
| 19 | Settlement | Contact plus low linear/angular velocity for 24 steps; per-attempt timeout 600 steps. |
| 20 | Top face | Face normals transformed by the actual body quaternion; highest world-up dot must be at least .985 and exceed runner-up by .04. |
| 21 | Cocked dice | Only ambiguous/timed-out/escaped dice relaunch with their next derived seed. Three retries maximum, then one fallback submission. Browser 4d6 exercised this path. |
| 22 | No final flip | No final target rotation, slerp, convergence or face correction. Valid body pose is frozen unchanged after detection. Regression tests verify pose remains unchanged. |
| 23 | Checks/saves/attacks | Direct sheet buttons authorize, simulate, submit physical values, then reveal accepted server result. Initiative and skills use the same pipeline. |
| 24 | Damage | Backend applies existing modifier/type/pinned policies after validating raw faces. Hits, critical application and targets remain manual. |
| 25 | d100 | Two physical d10 bodies, tens 00–90 and units 0–9. 00+0 becomes 100; browser 10+6 persisted 16. |
| 26 | Free roller | Persistent launcher; raw pools only; quantity controls and private FREE_ROLL history; no arbitrary modifiers. Up to 100 logical dice, visual tray up to 20 physical dice, larger pools use the same headless simulation. |
| 27 | Consumables | Authorization reserves availability without decrement. Character locks serialize reservations. Final result/history/decrement/session completion share one DB transaction. Cancel/expiry release availability; duplicates do not consume again. |
| 28 | History | Compact collapsed character history; free history inside its popover. Stored accepted results remain canonical. No partial result shown before acceptance. |
| 29 | Replay/Again | Matching-version physical replay reruns recorded seed locally, with no session/history/resource mutation. Divergent/unavailable replay preserves canonical text. Legacy/fallback records display stored text. Roll Again authorizes a new UUID/seed; consumables require their explicit action confirmation. |
| 30 | Accessible modes | Reduced Motion accelerates the same world then shows settled geometry; Text Only runs it headlessly. Skip accelerates the existing simulation. Both modes browser-tested and unit-tested. |
| 31 | Security | Authentication/ownership, same-origin writes, strict request parsing, exact counts/ranges, supported versions, expiry/cancellation, idempotency and stale character context enforced. Legacy request-ID reuse cannot bypass an existing session. Client physical values are trusted within the authorized specification; PvP anti-cheat is out of scope. |
| 32 | Physics tests | 31 tests across physical simulation and rigid-body geometry/contact suites: face normals, edge/corner/wall/die cocking, selective retry, retry cap, collisions, deterministic step batching, percentile reconstruction, and unchanged accepted pose. |
| 33 | Frontend tests | 105 tests pass, including five PlaySheet tests, session/reveal separation, retrying identical submissions, cancellation callbacks, replay, free pool controls, and existing builder/advancement regressions. TypeScript passes. |
| 34 | Backend tests | 101 tests pass. New integration cases cover owned sessions, invalid shapes/ranges/versions, concurrent duplicate finalization, cancellation/expiry/fallback and grenade reservation/consumption. Existing Finesse test also checks server display alternatives. |
| 35 | Content regressions | 152 tests pass. v6 profile digest and all unresolved ruling gates unchanged. |
| 36 | Desktop browser | Compact sheet inspected at 1101px viewport; direct controls and tabs verified. No page-level horizontal overflow. |
| 37 | Single-die proof | Strength check: observed physical d20 10, stored raw 10, +2, total 12. Replay reproduced face 10. See physical-d20.png. |
| 38 | Multi-die proof | 4d6 observed 2,6,2,6; stored raw [2,6,2,6], total 16. Cocked reroll occurred; accepted replay reproduced those faces. See physical-4d6.png. |
| 39 | Mixed-pool proof | d20=8, d12=2, d8=5, d6=2,5; stored groups match, total 22. See physical-mixed.png. |
| 40 | Character action proof | Ability 10+2=12; Acrobatics 2+4=6; STR save 14+2=16; initiative 12+6=18; Long-Las attack 3+6=9; damage 6+4=10. Frag Grenade 4+4+5=13, existing successful-save policy 6, quantity 1→0. |
| 41 | Free-roll proof | Browser stayed on character URL throughout; add/remove/clear/pool roll worked; accepted raw arrays match persisted physical metadata. Percentile 16 verified. See persistence JSON and screenshots. |
| 42 | Narrow acceptance | 390×844 browser viewport: document scrollWidth 375, no horizontal overflow, six ability controls ≥44px, Actions immediately below abilities, inventory/features tabs usable, launcher remains available without covering tab navigation. Narrow DEX roll 1+3=4 succeeded. See physical-mobile-actions.png. |
| 43 | Production build | Optimized compilation, TypeScript and all eight static pages pass. Standalone traced-file packaging still fails with Windows EPERM mkdir under .next/standalone. Deployable production bundle NOT certified. See physical-build.log. |
| 44 | Docker | Compose configuration validates with a test-only password supplied through the environment. Docker Desktop Linux engine pipe is absent. Container startup remains UNVERIFIED, as previously accepted by the user. Native API started successfully and applied migration V9. |
| 45 | Limitations | Physics values are not server-re-simulated; a malicious client could submit in-range faces. Cross-browser/device bit-identical replay is not certified; stored values remain authoritative on mismatch. Physical fairness/distribution has not been statistically certified. No audio UI in the new presenter. Production packaging/Docker limitations above remain. |
| 46 | Next milestone | Non-human levels 2–4 and Ratling Sharpshooter certification are already recorded in the preceding v6 milestone; retain those gates before level 5/Extra Attack. Next practical work is deployment verification on a working Docker/Linux environment and broader device/performance testing, without inventing new rules. |

## Evidence and operating notes

Evidence files are under [verification/physical-dice](verification/physical-dice). Browser checks used local verification characters, not a live campaign. The veteran fixture's last grenade was intentionally consumed during acceptance. Its canonical profile and other inventory were unchanged.

Session endpoints: POST /api/characters/{id}/roll-sessions, POST /api/roll-sessions/free, POST /api/roll-sessions/{id}/finalize and POST /api/roll-sessions/{id}/cancel. Finalization accepts only values, fallback flag and version identifiers; it never accepts a client modifier/total/resource amount. No trajectory is stored.

The previous dice reports are historical and describe superseded outcome authority. The v6 content profile remains di-phb-1.0-tier1-v6, digest fc78eebe9eab846b96aecf4823f88185e6d9818a1cde59bf255368be37db7769.

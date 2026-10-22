# Production narrow character builder

Implementation pass: 22 October 2026. Project: `C:\Users\tgccl\OneDrive\Documents\localdev\dark-imperium`.

The authenticated narrow creation flow is implemented and was exercised in a browser against Ktor and PostgreSQL: list → nine-step builder → server validation → review → create → sheet → list → reopen. This is a **PLAYABLE_WITH_MANUAL_RULES** release. Full PHB publication remains **BLOCKED**; Rules Engine and Dice Engine remain **PARTIAL**.

## Pages and supported choices

- `/characters`: owner-only summaries, Species, Origin, Class, level, updated date, creation link and empty state.
- `/characters/new`: Identity, Species, Origin, Ability Scores, Class, Universal Trait, Proficiencies & Skills, Equipment, Review. Back navigation preserves local draft state. No server character exists until confirmation.
- `/characters/{id}`: persisted identity and current HP, calculated scores/modifiers/saves/skills, AC, speed, initiative, PB, proficiencies, inventory, weapon actions, source-linked feature text and manual-rule indicators. Delete requires an explicit confirmation; name-only PATCH remains available through the API. No respec UI.

Only Human / Schola Progenium / Veteran level 1 / Twitchy is published. Standard-array assignments and Human +2/+1 increases use canonical choices. Imperial Adaptability, both Schola skill pools, Veteran's two skills and specialist weapon groups use their canonical pools. Broad Training deliberately exposes only the reviewed Trench Club proficiency. Equipment is Lasgun, Laspistol, Combat Blade, Flak Armour, two Frag Grenades and Med-Pack. Auspex, Autogun and other alternatives are rejected. No new game-design rulings were made.

The profile supplies SUPPORTED, UNSUPPORTED, BLOCKED and COMING LATER messages. Source descriptions can mention other PHB content, but do not create selectable options. The legacy seed compendium remains separately labelled development reference data. Legacy foundation character rows are retained, not silently certified or migrated into the production list.

## Data flow and lock

`content/profiles/di-phb-1.0-narrow-v1.json` is a publication allowlist. `tools/export_narrow_profile.py` exports canonical records, reviewed equipment/class inputs, PB evidence and approval ledger verbatim into a server resource. `--check` detects drift. The profile endpoint returns only the allowlisted selector/choice/kit views, never the unrestricted record map.

Profile ID: `di-phb-1.0-narrow-v1`; calculation adapter: `narrow-kotlin-v1`.

Snapshot SHA-256: `3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af`.

`NarrowRules` owns validation and calculation; routes and React contain no Human/Veteran formulas. React renders backend projections and submits selections. Canonical grants supply attribute increases, skills and weapon proficiencies; progression supplies level-1 features; automatic effects supply speed/initiative; the approved policies and reviewed class/armour/weapon inputs supply baseline statistics. The adapter is deliberately limited to this release. Expanding content requires review and adapter support, not merely adding an ID to a list.

Startup registers the immutable snapshot in PostgreSQL. Reusing a profile ID with a different digest fails. Every character references the profile ID and digest, and retrieval recalculates against the stored snapshot rather than today's source files. New releases require new IDs and retention of the calculation adapter needed by old characters. No automatic ruleset migration is implemented.

## Persistence and migration

`V4__production_narrow_characters.sql` is additive and preserves V1–V3 tables:

| Table | Stored information |
| --- | --- |
| `ruleset_profiles` | Profile identity, digest, engine version and immutable canonical snapshot |
| `player_characters` | UUID, authenticated owner FK, profile FK, name, canonical selectors, level, base attributes, kit choices, timestamps and owner-scoped idempotency key/hash |
| `player_character_choices` | One row per canonical choice with bounded selected option IDs |
| `player_character_inventory` | Stable instance UUID, canonical definition ID, initial and current quantity, equipped state and nullable ammunition state |
| `player_character_runtime` | Current HP, state version, limited-use resources, conditions and temporary effects |

Derived maximum HP, modifiers, AC and attack bonuses are recalculated, not persisted. Starting HP equals calculated maximum HP. The Human failed-save reroll starts at one use per long rest and is marked manual. Ammunition is null, not inferred full. Definition IDs are checked against the pinned canonical snapshot by the service; the database enforces owner/profile/character relationships, unique choices/items/request keys and quantity constraints. Child rows cascade on character deletion.

Creation validates first, then inserts selections, choices, inventory and runtime in one transaction. A repeated `(owner, requestId)` with the same payload returns the original character. Reusing that key with another payload returns 409 `IDEMPOTENCY_CONFLICT`. Browser requests retain one UUID for retries. A draft refresh begins a new local draft; cross-refresh draft recovery is not implemented.

## API and validation

All routes require the existing HttpOnly session cookie; mutations require the configured Origin. Owner identity comes from the authenticated session. Foreign owners receive 404 for reads, rename and delete. Unknown JSON fields, including client owner/calculated fields, are rejected.

| Method | Route | Result |
| --- | --- | --- |
| GET | `/api/character-builder/profile` | Restricted profile, canonical choices, class features and reviewed kit |
| POST | `/api/characters/validate` | 200 `VALID` or `INVALID`, field issues, optional ability preview and full calculation only when valid |
| POST | `/api/characters` | 201 saved sheet and Location; 422 field validation errors; 409 conflicting retry key |
| GET | `/api/characters` | Owner-only summary array |
| GET | `/api/characters/{id}` | Persisted selections, current runtime/inventory and pinned calculated projection |
| PATCH | `/api/characters/{id}` | Name-only owner update |
| DELETE | `/api/characters/{id}` | Owner-only deletion with cascades |

Request shape: `profileId`, `profileDigest`, UUID `requestId`, `name`, `speciesId`, `originId`, `classId`, `level`, `traitId`, `attributes`, `answers`, `packageChoices`, `inventory`. See `backend/src/test/resources/production-draft.json` for a complete valid example.

Validation covers profile/digest, supported selectors, eligibility predicates, exact standard-array allocation, legal canonical Human increases, required choices, counts and within-choice uniqueness, valid skills/proficiencies/Broad Training, exact kit, quantities and equipped armour. Stable codes include MISSING_CHOICE, CONTENT_NOT_SUPPORTED, INVALID_ELIGIBILITY, INVALID_ABILITY_ALLOCATION, INVALID_SKILL_SELECTION, INVALID_EQUIPMENT_SELECTION, INVALID_QUANTITY, RULESET_MISMATCH and STALE_PROFILE. No unresolved rule is filled with an inferred decision.

## Calculations and dice boundary

The golden selections produce STR/DEX/CON/INT/WIS/CHA **17/15/13/12/10/8**, modifiers **+3/+2/+1/+1/+0/−1**, PB **+2**, HP **11**, AC **14**, speed **30 ft**, initiative **+4**. Tests compare against the independent prior proof fixture.

Baseline actions are Lasgun, Laspistol, Combat Blade and Frag Grenade. Grenade damage is 3d6, DC 12 for the proof, 15-foot radius, half damage on success rounded down under PHB-RULE-059. Generic PHB-RULE-018 remains unresolved.

The projection contains 35 display-only RollDefinitions: six attributes, fifteen skills, six saves, initiative, three weapon attack/damage pairs and grenade damage. Existing wire-shape conformance is checked with the production engine's distinct identity. These are not 35 newly authorized executable actions, and do not replace the earlier eleven offline proof definitions. Finesse displays the Strength baseline; contextual ability choices, advantage, target legality, range, ammunition and consumption still require manual adjudication.

`RollDefinition != authorization to act`. Rendering/retrieval never consumes inventory or resets HP. No active roll buttons or resource-mutation endpoints are added. A future runtime executor must revalidate owner, current state, action and target; the baseline projection cannot be submitted as authority.

## Verification

- **Backend: 25 tests pass**, including nine narrow calculation/validation tests, twelve PostgreSQL API/integrity tests and four retained foundation tests. Coverage includes altered selectors, ability/skill/proficiency/kit/quantity validation, golden projection, ownership, retrieval, retry safety, profile locking, forced failure of the final child insert with rollback, and read-only current state.
- **Frontend: 14 tests pass** across builder navigation, required-field/API errors, score assignment payloads, allowed selectors, review, creation redirect, list, sheet and delete confirmation; retained API client tests also pass.
- **Content: 95 tests pass**: all existing 93 unchanged in scope plus two production snapshot/wire-contract checks. Export `--check` passes. Canonical counts remain 948 drafts, 310 candidates and 692 manual entries.
- **Backend build/installDist: PASS** on JDK 21 / Gradle 8.14.3. Native compilation used the in-process compiler to avoid an environment-specific stale daemon/temp-directory issue.
- **Migrations: PASS** on an empty PostgreSQL 17.6 test database (V1–V4), and on an existing V3 development database upgraded to V4.
- **Browser flow: PASS** using the real Next proxy, cookie authentication, Ktor and PostgreSQL. Created `Cassian UI verification`, returned to list and reopened the saved sheet. Desktop visual inspection completed. Responsive CSS and keyboard-labelled controls are implemented; a separate physical mobile/tablet-device acceptance run was not performed.
- **Frontend production build: UNVERIFIED (environment).** Optimized compilation and TypeScript pass. The first run generated all pages but failed copying standalone output; subsequent retries, including after renewing project write permission, failed creating prerender directories with Windows EPERM. No fully successful production package is claimed. Browser acceptance used the compiled application before the final packaging retry; source/component tests cover the final UI changes.
- **Docker: UNVERIFIED**. `docker info` cannot connect to `dockerDesktopLinuxEngine` because its named pipe is absent. No successful Compose startup is claimed.

Cached dependency files were recovered locally because this environment rejects pnpm's project symlink registration. Package versions and lockfile were not changed to bypass verification. Normal installations should continue to use the committed frozen pnpm lockfile.

## Remaining scope and next task

This release has no full catalogue, level-up/respec, campaign/encounter management, runtime combat mutation, authoritative dice rolling, 3D dice or persisted builder drafts. The 31 original unanswered rulings remain blocked. Manual feature prose is visible with its source; display does not imply automation. The separate legacy reference catalogue is not a production eligibility source.

Recommended next task: implement production browser dice rolling for the validated sheet, with server-authoritative roll execution, current-state/action validation, idempotent consumption and roll results/history. Keep 3D presentation as a later layer.

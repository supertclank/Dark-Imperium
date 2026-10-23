Current sheet/weapon-ability milestone: [40-point completion and acceptance report](docs/CHARACTER_SHEET_V7_REPORT.md).

Current dice and play UX: [physics-determined dice and compact sheet report](docs/PHYSICAL_DICE_AND_PLAY_UX_REPORT.md) — physical outcomes, server validation, transactional reservations, and browser evidence.

Previous dice UX milestone: [overhaul completion report](docs/DICE_UX_OVERHAUL_REPORT.md) — overlay physics, delayed reveal, free pools and verification limits.

## Non-Human advancement release (v6)

Eight non-Human martial class contexts now have certified paths through level 4, including Ratling Sharpshooter. The release has 220 certified family rows and 40 individually filtered Talent alternatives. Existing v4 non-Humans use an explicit atomic upgrade; earlier profiles remain pinned. Validation: 152 content, 97 backend and 72 frontend tests pass, plus TypeScript and eight-class browser acceptance. Frontend standalone packaging remains blocked by Windows EPERM; Docker startup remains unverified.

See the [30-point completion report](docs/import/NONHUMAN_ADVANCEMENT_V6_REPORT.md), [browser evidence](docs/import/NONHUMAN_V6_BROWSER_EVIDENCE.json), and [current publication matrix](content/packages/di_phb_1_0/review/nonhuman-v6-publication-matrix.json).

## Level 4 advancement release

Human Veteran level-4 advancement is available for 24 certified families through an explicit v4-to-v5 upgrade, with ASI or 18 audited Talents. Older profiles stay pinned. Validation: 146 content, 88 backend and 69 frontend tests pass; TypeScript passes. Frontend production packaging is blocked by Windows EPERM; Docker startup is unverified. See the [full release report](docs/import/LEVEL4_ADVANCEMENT_REPORT.md).

> **Builder UX pass:** [Presentation and ability-score verification](docs/BUILDER_PRESENTATION_REPORT.md). Structured choices, immediate doctrine details and an initially unassigned unique Standard Array. 141 content / 77 backend / 63 frontend tests pass; v4 snapshot unchanged. Mobile browser verification and Windows standalone packaging remain unverified.

> **Current v4 release:** [Non-Human certification and verification](docs/import/NONHUMAN_V4_REPORT.md). Six species, 64 restricted certified families; Ogryn, Skitarii, Kin and Aeldari now have reviewed level-one paths. Open tool/vehicle and equipment alternatives remain unavailable. Existing profiles stay pinned. Earlier reports below are historical.

> **Current release:** [Advancement and Ratling v3 report](docs/import/ADVANCEMENT_RATLING_V3_REPORT.md). Transactional Human Veteran advancement through level 3 and ten Ratling level-one families; 58 certified families total. Older profiles remain pinned. Prior release reports below are historical.

> **Current release:** [Human tier-1 v2 completion report](docs/import/HUMAN_TIER1_V2_REPORT.md). Eight NORMAL Human Origins; Veteran levels 1–3 (Shock Trooper, Marksman, Sergeant at level 3), Hive Scum level 1. Authoritative rolls/history/3D presentation; unresolved procedures explicitly manual or unavailable. Prior reports below are historical.

> **Production narrow builder:** [Implementation and verification](docs/PRODUCTION_CHARACTER_BUILDER.md). Human / Schola Progenium / Veteran, level 1, with Twitchy. Server validation, pinned ruleset, PostgreSQL persistence and sheet are implemented. Full catalogue and authoritative dice execution remain unavailable.

> **Current Frag gate pass:** [Results](docs/import/PHB_FRAG_GATE_REPORT.md). Narrow profile PLAYABLE_WITH_MANUAL_RULES; narrow builder data READY_WITH_MANUAL_RULES. 93 tests; 948 drafts; 310 candidates. Generic Blast and 31 original rulings remain unresolved. Earlier pass statements below are historical.

> **Current pass:** [Minimum rulings and narrow proof](docs/import/PHB_MINIMUM_RULINGS_REPORT.md). Five rulings approved, 31 unresolved. 948 canonical drafts; 310 candidates; 81 content tests pass. The narrow core calculates, but a mandatory Frag Grenade save outcome keeps playable readiness BLOCKED. Earlier sections below describe historical scope.

# Dark Imperium Web

The proposed [canonical content and rules-data specification](docs/content/README.md) documents future content imports, choices, progression, versioning and expansions. It is separate from the currently implemented foundation and contains explicitly non-authoritative examples.

A private tabletop companion: register, log in, complete the supported nine-step character builder, review server-calculated statistics, save and reopen your character. The production path uses canonical PHB content and an immutable ruleset snapshot. The separate seed compendium remains legacy development reference data.

## Stack and layout

- `frontend/`: Next.js App Router, React, TypeScript, responsive CSS, Vitest.
- `backend/`: Kotlin, Ktor, Gradle Kotlin DSL, JDBC/HikariCP, Argon2id authentication.
- `database/migrations/`: PostgreSQL schema and seed data managed by Flyway.
- `docs/`: architecture, schema, rules, API, contributor guide and verification report.

This is a modular monolith: a presentation server and one API application backed by one database. No Redis, queues, GraphQL or microservices.

## Start with Docker

Prerequisites: Docker Engine/Desktop running with Linux containers and Docker Compose v2 or later. Port 3000 must be free. Native Node/Java/Gradle installations are not required for Docker startup.

1. Copy `.env.example` to `.env` (PowerShell: `Copy-Item .env.example .env`; POSIX: `cp .env.example .env`).
2. Set `POSTGRES_PASSWORD` to a unique random password. An empty password deliberately prevents startup. Do not commit `.env`.
3. From this directory, run:

   ```sh
   docker compose up
   ```

4. Open <http://localhost:3000>, register using a 12–128 character password, then log in.
5. Select **Create character**, select a supported Human Origin, Veteran level 1–3 or Hive Scum level 1, and complete the steps, choose ability increases and proficiencies, review the starting kit and calculated sheet, then save. Return to **Characters** to reopen the sheet.

Compose builds both applications, waits for database readiness, runs Flyway at API startup, then starts the frontend after API readiness. PostgreSQL uses a named persistent volume. The default host binding is loopback-only. The API and database are not published to the host.

Use `docker compose up --build` after code changes. `docker compose down` stops the stack and preserves records. **`docker compose down -v` permanently deletes the development database.**

## Environment

| Setting                                              | Purpose                                                                      |
| ---------------------------------------------------- | ---------------------------------------------------------------------------- |
| `POSTGRES_DB` / `POSTGRES_USER`                      | Database identity; defaults supplied in `.env.example`                       |
| `POSTGRES_PASSWORD`                                  | Required secret; no default or seed account                                  |
| `APP_ORIGIN`                                         | Exact browser origin, no trailing slash; defaults to `http://localhost:3000` |
| `COOKIE_SECURE`                                      | `false` for local HTTP only; use `true` for HTTPS deployment                 |
| `FRONTEND_PORT`                                      | Published port; update `APP_ORIGIN` to match if changed                      |
| `DATABASE_URL`, `DATABASE_USER`, `DATABASE_PASSWORD` | API database settings; Compose supplies these                                |
| `BACKEND_URL`                                        | Frontend server's private API target; Compose sets `http://backend:8080`     |

Use the configured hostname consistently: `localhost` and `127.0.0.1` are different origins. Production requires TLS termination, `COOKIE_SECURE=true`, the exact HTTPS origin, private database networking, backup/restore procedures and appropriately restricted access to the deployment. Registration currently permits anyone who can reach the site; use a private network or access gateway for your private group. Invitation and account recovery workflows are not implemented.

## Tests and builds

With Node 22.13+ and pnpm 11.25.0:

```sh
cd frontend
pnpm install --frozen-lockfile
pnpm test
pnpm build
```

With JDK 21 and Docker running (Gradle is bootstrapped by the committed wrapper):

```sh
cd backend
./gradlew test installDist
```

On Windows use `gradlew.bat`. Backend integration tests start PostgreSQL 17 through Testcontainers. They **fail**, rather than silently skip, when neither Docker nor an explicit test database is available.

For an existing disposable PostgreSQL database, set `TEST_DATABASE_URL=jdbc:postgresql://localhost:5432/imperium_test`, `TEST_DATABASE_USER` and `TEST_DATABASE_PASSWORD` before running tests. Its name must end in `_test`. Tests apply the real migrations and create randomized accounts; do not point them at a production database.

Unit tests alone: `./gradlew test --tests imperium.RulesEngineTest`. Integration tests: `./gradlew test --tests imperium.ApiIntegrationTest`.

## Migrations

Flyway applies `database/migrations/V*.sql` in version order at API startup and validates checksums on subsequent starts. The Gradle resources configuration packages the same SQL into both local builds and the backend image. Do not edit an applied migration; add a new numbered migration. Back up deployed databases before migrating. There is no automatic schema creation or destructive reset endpoint.

## Documentation and status

- [Architecture](docs/ARCHITECTURE.md)
- [Database](docs/DATABASE.md)
- [Rules engine](docs/RULES_ENGINE.md)
- [Development](docs/DEVELOPMENT.md)
- [REST API](docs/API.md)
- [Verification and limitations](docs/VERIFICATION.md)

The frontend production build and real-PostgreSQL backend tests have been exercised locally. **Docker Compose startup remains unverified on the delivery machine because its Docker engine was unavailable; the owner explicitly accepted that verification limit.** See the verification report for exact checks. This is a tested foundation, not a completed implementation of the full RPG.

Recommended next milestone: formalize the initial game rules, add content validation/version pinning and calculated-value explanations, then implement a focused wounds/attributes editing flow with regression tests. Campaigns, encounters, combat tracking and advanced GM tools remain out of scope.

## PHB import status — 22 October 2026

The supplied Version 1.0 handbook is now registered and partially transcribed. See [PHB import report](docs/import/PHB_IMPORT_REPORT.md). The original example records remain historical placeholders and are not PHB data. Canonical drafts and incomplete candidates are separate; publication and full builder readiness remain blocked pending source review and mapping.


## Rules resolution pass — 2026-10-22

870 canonical drafts, 333 remaining candidates, 45 mapped subclasses and 44 passing content tests.15 concrete issues resolved; 36 human questions remain. Builder NOT_READY; rules/dice PARTIAL. See the [canonicalisation report](docs/import/PHB_CANONICALISATION_REPORT.md) and its exact-rulings checklist. Application behaviour remains unchanged.


## Human rulings integration pass — 2026-10-22

Current result: [Character creation readiness report](docs/import/CHARACTER_CREATION_READINESS_REPORT.md).874 canonical drafts; 333 candidates; 61 passing content tests. Human rulings 0 integrated/36 unresolved. Builder BLOCKED; rules/dice PARTIAL. Docker and native application test execution remain environment-blocked.

## Production dice rolling — 2026-10-22

The validated narrow sheet now supports server-authoritative checks, saves, initiative, weapon rolls, transactional Frag Grenade use and private persisted history. See [production dice completion report](docs/PRODUCTION_DICE_ROLLING.md) for API design, 43 backend / 28 frontend / 95 content passing tests, browser acceptance and explicit production-build/Docker verification limits. Earlier milestone sections above are historical.

## 3D dice presentation — 2026-10-22

Optional Three.js dice now present completed server results, with persistent reduced-motion/text-only preferences, optional sound, local-only animation replay and fresh-request Roll Again for non-consumables. See [3D dice completion report](docs/THREE_D_DICE_PRESENTATION.md) for 46 frontend / 43 backend / 95 content passing tests, browser evidence and remaining build/device verification limits.

## Level 1–3 independent catalogue audit — 2026-10-22

See the [catalogue readiness report](docs/import/LEVEL_1_3_CATALOGUE_REPORT.md), [full publication matrix](docs/import/LEVEL_1_3_PUBLICATION_MATRIX.md) and [Origin scenarios](docs/import/LEVEL_1_3_ORIGIN_SCENARIOS.md). PHB-RULE-001–007 remain unresolved. The 4,140-row inventory, calculation proofs and blocked-family fixtures prepare expansion; they publish no new paths. The existing narrow production profile is unchanged.

## Origin approvals and initial tier-1 publication — 2026-10-22

PHB-RULE-001–007 are integrated (12/36 resolved). The new immutable tier-1 profile supports Human / Hiveborn / Veteran level 1, with Twitchy and the reviewed kit. Rare/Limited paths remain approval-blocked. Existing narrow characters retain their snapshot and adapter. See the [current readiness and verification report](docs/import/LEVEL_1_3_CATALOGUE_REPORT.md) for the updated 4,140-row matrix, compiler/adapter scope, tests, browser evidence and remaining blockers. Earlier milestone sections are historical.

# Dark Imperium Web

The proposed [canonical content and rules-data specification](docs/content/README.md) documents future content imports, choices, progression, versioning and expansions. It is separate from the currently implemented foundation and contains explicitly non-authoritative examples.

A private tabletop companion with one complete vertical slice: create an account, log in, create a Human Guardsman with a Lasgun, save the character, and reopen their character sheet. Includes a searchable seed compendium and owner-only rename/delete. Rules and statistics are explicitly provisional.

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
5. Select **Create character**, enter a name, select Human, Guardsman and Lasgun, and save. Return to **Characters** to reopen the sheet.

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

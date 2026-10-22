# Development guide

## Local workflow

Use Docker Compose for the full reproducible environment. For faster source iteration, run PostgreSQL locally, then the API with JDK 21 and `backend/gradlew run`, then `pnpm dev` in `frontend`. Set API environment variables listed in the README; point `BACKEND_URL` at the API when it is not `http://localhost:8080`. Set `APP_ORIGIN` to the exact URL you open in the browser. Flyway runs before the API accepts requests.

For local PostgreSQL access through Compose, use a temporary development override publishing only `127.0.0.1:5432:5432` on the database service; the checked-in default deliberately keeps it internal. Do not publish the API or DB publicly.

The frontend image is a Next.js standalone production build; Compose rebuilds are explicit. Host-side `pnpm dev` provides hot reload. On Windows `gradlew.bat` is the wrapper command. If a restricted environment blocks the Kotlin daemon, use `-Pkotlin.compiler.execution.strategy=in-process`.

## Conventions for people and coding agents

- Preserve the requested stack and modular monolith boundaries.
- Keep game content in data; never branch on names such as Human, Guardsman or Lasgun in UI/routes.
- Perform every authorization check in the API. Every character query/mutation must be owner-scoped.
- Use prepared SQL, explicit transactions and new numbered migrations. Do not edit applied migrations or rely on ORM schema creation.
- Add rule vocabulary only when supported by a documented game requirement. Reject unsupported effects; do not silently ignore them.
- Keep base state and calculated values separate. Add regression tests at service/API boundaries for persistence and access control.
- Do not use localStorage for session tokens, passwords or authoritative character data.
- Keep `.env`, databases, logs, build output and dependency trees out of source control. Dependency lockfiles and the Gradle wrapper belong in source control.
- Use native labelled controls, visible focus, meaningful error states and responsive layouts. Content names and descriptions are rendered as text, not HTML.
- Avoid adding placeholder buttons for future features. Campaigns, encounters, combat tracking, GM tools and content management are not part of this release.

## Validation

Frontend: `pnpm test`, `pnpm build`. If an OS sandbox prevents esbuild's config discovery, `pnpm test --configLoader runner` uses Vite's alternate config loader; this was used for the delivery environment.

Backend: `./gradlew test installDist` with Docker running or explicit `TEST_DATABASE_*` settings. Integration tests use the actual PostgreSQL SQL/migrations and Ktor test host, not H2 or mocked repositories. They exercise cookies, origin checks, structured errors, all seed content, atomic character creation, owner-only reads/mutations and logout revocation.

Manual acceptance: register → log in → create character → select seeded options → save → return to list → reopen → reload → log out. Check a second account cannot see the first character. Inspect narrow/mobile layouts and keyboard navigation whenever UI layout changes.

## Adding content

For development, add seed content through a new migration. Insert shared `items` identity before weapon details. Use stable slugs and generated UUIDs. A content administration UI is intentionally absent. Validate rule JSON against the current typed interpreter. Do not change existing live content effects without addressing version pinning and migration policy first.

## Operational limits

Before external deployment, configure HTTPS and Secure cookies, private access, backups, resource limits, monitoring and a tested recovery procedure. Authentication throttles are process-local and reset on restart. Registration does not verify email or require an invitation. Account recovery and deletion are not implemented. Treat this as a private-group foundation, not an internet-scale identity platform.

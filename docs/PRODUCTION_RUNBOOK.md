# Production runbook

Validation date: 23 October 2026. **Production release gate: BLOCKED.** Backend distribution and fresh migrations are verified. A clean frontend artifact cannot currently be produced in this Windows execution environment. Host Docker build/runtime, Compose application startup and localhost application access are VERIFIED by the user. Detailed named-browser production acceptance remains pending. Codex-session Docker access is ENVIRONMENT_BLOCKED, not a host or repository defect. Do not treat the working development preview as deployment acceptance.

The frozen content release remains `di-phb-1.0-tier1-v7`, digest `af92705fc1a85b49a4e06c52999cfff335e8a9800f43608a30e540f391b4b6d5`. This milestone changes no rules, profiles or character migrations.

## Prerequisites and configuration

Use PostgreSQL 17, JDK 21, Gradle 8.14.3, and pnpm 11.25.0. Docker builds use Node 22 Alpine; the available native validation runtime was Node 24.22.1 with Next.js 16.4.2. Do not claim Node 22/Linux runtime validation from the native tests.

| Variable | Process | Requirement |
|---|---|---|
| DATABASE_URL | Backend | JDBC PostgreSQL URL, e.g. jdbc:postgresql://127.0.0.1:5432/dark_imperium. Do not put passwords in the URL. |
| DATABASE_USER / DATABASE_PASSWORD | Backend | Dedicated database account and secret injected by the runtime. No real secret in Git or command logs. |
| APP_ORIGIN | Backend | Exact browser origin, including scheme and non-default port. Writes with a different Origin are rejected. |
| COOKIE_SECURE | Backend | true for HTTPS deployments. Default is true; HTTPS APP_ORIGIN is then required. false only for loopback HTTP verification. |
| PORT | Backend | Optional validated integer 1–65535; default 8080. |
| BACKEND_URL | Frontend | Server-side API address; never NEXT_PUBLIC_. Default localhost:8080 for native use. Compose uses http://backend:8080. |
| HOSTNAME / PORT | Standalone frontend | Bind address and port, normally 0.0.0.0 / 3000 in a container; 127.0.0.1 for native loopback. |
| POSTGRES_DB / USER / PASSWORD | Compose | .env.example documents names. Supply a unique password; Compose refuses an empty/missing password. |
| FRONTEND_PORT | Compose | Published loopback port; default 3000. Backend and database are not host-published. |
| TEST_DATABASE_URL / USER / PASSWORD | Backend tests | A disposable separate database whose name ends in _test. Never point tests at campaign data. Without this setting, tests require Docker/Testcontainers. |

Sessions use HttpOnly, SameSite=Lax cookies with seven-day expiry; logout revokes them. Same-origin API proxying is intentional; there is no broad CORS allowance. Place a production HTTPS reverse proxy in front of the frontend and leave backend/database private. Changing APP_ORIGIN requires matching the public frontend origin, not the internal backend URL.

## Clean native build procedure

Start from a clean checkout of the intended reviewed commit, outside sync-managed folders. Install the versions above. Do not copy node_modules, .next, backend/build or local .env from another checkout.

```sh
git clone <your-repository-url> dark-imperium
cd dark-imperium
git checkout <reviewed-commit>
# Create PostgreSQL role/database with your normal administrative tooling.
createuser --pwprompt imperium
createdb --owner=imperium dark_imperium
createdb --owner=imperium dark_imperium_validation_test
# Inject DATABASE_* and TEST_DATABASE_* through your shell/secret manager.
gradle -p backend test installDist
cd frontend
pnpm install --frozen-lockfile
pnpm exec tsc --noEmit
pnpm build
```

Native Windows commands use the equivalent PowerShell environment assignments and gradle.bat. In this sandbox pnpm's default project-registry symlink was denied. A clean install from the existing lockfile succeeded using:

```powershell
pnpm install --frozen-lockfile --store-dir .pnpm-store --node-linker=hoisted --config.enable-global-virtual-store=false
node node_modules/next/dist/bin/next build
```

This is a supported alternative dependency layout, not a successful deployment recipe: the later Next build still hit EPERM. Direct invocation avoids pnpm's automatic dependency-status install reverting the per-command layout. The diagnostic project was `C:\Users\tgccl\Documents\Codex\di-prod-validation`, outside OneDrive, with fresh dependencies and no pre-existing .next. The original source checkout is under OneDrive. Neither antivirus involvement nor the exact Windows permission subsystem has been proven; no protections were disabled.

## Start generated artifacts

Only proceed after a successful build. Copy `backend/build/install/dark-imperium-api` as a complete directory. Its bin launcher and lib JARs include migrations and profiles and need no source checkout. With runtime environment set, start:

```sh
/path/to/dark-imperium-api/bin/dark-imperium-api
```

Flyway applies V1–V10 automatically at startup. On migration failure startup must fail; correct the cause from logs and restore/test a backup if necessary. Do not edit applied migration checksums or immutable profile JSON. Native validation copied the distribution to an unrelated folder, started against an empty database, observed all ten migrations, and checked `/api/health`.

For the frontend, copy `.next/standalone` to the release directory and copy `.next/static` to that directory's `.next/static`. If public assets are added later, copy public too. Set HOSTNAME, PORT and BACKEND_URL, then:

```sh
node /path/to/frontend-release/server.js
```

Do not use `next dev` for acceptance. Standard-node output and webpack were explored diagnostically but did not resolve the directory-creation errors; no alternate output mode or worker-count workaround was retained in repository configuration.

## Docker / Linux route

The user has verified this build/startup route on the Windows host with Docker Desktop using desktop-linux. Direct Docker runtime verification from inside Codex is NOT POSSIBLE DUE TO SESSION PERMISSIONS:

```sh
cp .env.example .env
# Set unique POSTGRES_PASSWORD, public APP_ORIGIN and HTTPS COOKIE_SECURE=true as appropriate.
docker compose config --quiet
docker compose up --build -d
docker compose ps
docker compose logs --tail=100 database backend frontend
```

Compose waits for PostgreSQL readiness, then backend readiness, then frontend readiness. Both final application images run as non-root users. Frontend uses generated standalone assets; backend uses only its distribution and JRE. Build caches/dependencies, sync artifacts and .env are excluded from build contexts. Lockfile dependency installation is deterministic; base image tags are not digest-pinned. After the user started Docker Desktop on 23 October, docker version found the desktop-linux endpoint but returned permission denied accessing npipe:////./pipe/dockerDesktopLinuxEngine from this execution session. WSL previously returned E_ACCESSDENIED. The user subsequently confirmed successful host Docker build/startup and localhost application access. Those host checks are VERIFIED; the session restriction does not invalidate them. Do not retry engine repair or alter host Docker security to accommodate this session. See verification/production/host-docker-verification.json for evidence provenance.

Do not use `docker compose down -v` on a database containing real characters. Back up PostgreSQL before deployment and verify restoration separately.

## Health and acceptance

```sh
curl --fail http://127.0.0.1:8080/api/health
curl --fail http://127.0.0.1:3000/api/health
curl --fail http://127.0.0.1:3000/
```

Backend readiness executes SELECT 1 and returns only status. Frontend's proxied health checks the frontend-to-API-to-database chain. Also check an actual static JS asset and authenticated hard-refresh of `/characters/<owned-id>`: HTTP 200 alone does not establish hydration, dice lazy-loading or authentication success. Complete the browser/device matrix before signing off production.

## Recovery and diagnostics

- Connection/migration errors: inspect startup logs, host/port, DB role permissions and migration history. Do not expose database details to users.
- Rejected requests: logs record HTTP method, route, status and error code, without request bodies, notes, cookies or seeds. Unexpected errors remain generic to clients. Explicit physics fallback logs only the session ID; persisted result metadata records SERVER_FALLBACK.
- Lost finalization response: keep the page open and use Retry. It resubmits the same session and raw values, never rerolls. After expiry, the server clearly rejects it. Reload/navigation currently loses the in-memory retry closure; inspect history before initiating another roll.
- Abandoned rolls: active reservations count only CREATED sessions whose expires_at is in the future. At five minutes they cease blocking inventory even if the historical session row remains. Cancellation releases immediately. Expiry is logical cleanup, not row deletion.
- Duplicate finalization: identical submission returns the stored result; changed submission is rejected. Resource use and history insert are transactional.
- WebGL unavailable/context loss: continue the same physical world headlessly. If physics/module loading fails, request the existing authorised server fallback once. Text mode needs no WebGL; it normally uses shared geometry math, and a missing module takes the same server fallback path.
- Replay: stored values remain canonical; mismatching trajectories cannot replace them. No cross-device deterministic trajectory claim.
- Notes conflict: preserve/copy the local draft before reload, review the saved version and merge deliberately. Limits are 20,000 UTF-16 code units, a 131,072-byte notes-only proxy/backend envelope and 16,384 bytes elsewhere. Direct backend access should remain private; the public proxy enforces streamed body limits.

## Remaining release gates

The host Docker build/startup gate is closed by user verification. Run real Chrome, Edge and Firefox production flows, mobile-width flows, cold deep links/static assets, WebGL fault cases and history/replay verification against the confirmed production URL. Native Windows sandbox EPERM is a separate environment limitation; it does not block use of the verified Docker deployment route. Safari and physical mobile hardware remain unverified. Level 5/Extra Attack certification should wait for these production gates.

## Local production verification alongside development

Port 3000 was occupied by the development server. Verified host production startup uses the following PowerShell overrides (repeat in a new shell, or persist equivalent values in the local uncommitted .env):

```powershell
$env:FRONTEND_PORT = "3100"
$env:APP_ORIGIN = "http://localhost:3100"
docker compose up --build -d --wait frontend
docker compose ps
```

Use http://localhost:3100 for browser acceptance. The origin must match for authenticated writes. This retains the database volume. The WASM CSP fix is build-time configuration: rebuild the frontend, then reload the page to retry physics initialization. Merely restarting the existing image does not apply it. Keep JavaScript unsafe-eval disabled in production; Rapier requires only wasm-unsafe-eval. Host engine access from Codex remains blocked and is not required for browser/API checks.

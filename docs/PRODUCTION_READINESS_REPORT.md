# Production Readiness & Cross-Device Validation

23 October 2026. **Release decision: NOT YET PRODUCTION-READY.** Independent hardening and automated validation are complete. Docker build, Compose startup and localhost application access are VERIFIED by the user on the host Windows machine. Detailed production browser/device acceptance remains pending; Codex Docker access is a session restriction, not an application or host Docker defect. Do not advance to level 5/Extra Attack on the strength of this pass alone.

| # | Requested result | Evidence / status |
|---|---|---|
| 1 | Windows build | Clean lockfile dependency install succeeds with a local store/hoisted layout. Next production compilation and TypeScript succeed, but clean prerender directory creation fails. No clean complete frontend artifact. |
| 2 | EPERM diagnosis | Reproduced outside OneDrive with fresh dependencies; single-worker and webpack diagnostics also fail. Failure is not limited to standalone trace copying. Exact permission subsystem/locking cause remains UNRESOLVED; no antivirus claim or security weakening. See diagnosis below. |
| 3 | Linux build | VERIFIED via user-reported host Docker Linux build using docker compose up --build. No separate WSL or clean no-cache build claim. |
| 4 | Standalone packaging | VERIFIED for the host Docker deployment route: the configured frontend Dockerfile packages standalone output and launches server.js, and the user confirms the stack built and ran. Native Windows sandbox packaging remains environment-blocked; no independent Codex image inspection. |
| 5 | Backend production | Clean source-copy compilation and installDist verified using cached locked-version build dependencies. Distribution copied to a source-independent folder and started on port 8081. |
| 6 | Docker build | VERIFIED by user on host Windows using docker compose up --build. Dockerfiles retain build/runtime separation, non-root runtime users and generated production artifacts. |
| 7 | Docker runtime | VERIFIED: host output shows database, backend and frontend healthy; frontend bound 127.0.0.1:3100. Codex browser confirms production UI at localhost:3100. Codex engine access remains ENVIRONMENT_BLOCKED; direct engine verification NOT POSSIBLE DUE TO SESSION PERMISSIONS. |
| 8 | Fresh database | Empty imperium_production_acceptance database applied all ten migrations sequentially. /api/health returned ok. Separate fresh _test database used for backend tests. |
| 9 | Chrome | UNVERIFIED: unavailable to current browser tooling; named-browser production flow pending. |
| 10 | Edge | UNVERIFIED: unavailable to current browser tooling; named-browser production flow pending. |
| 11 | Firefox | UNVERIFIED: unavailable to current browser tooling; named-browser production flow pending. |
| 12 | Browser limits | Codex IAB production checks now available on port 3100; exact version not exposed. Named Chrome/Edge/Firefox and real devices remain unverified. |
| 13 | Desktop | Production IAB: 1920×1080, 1440×900 and 1280×720; all six tabs, no horizontal overflow. Separate account and v7 Ratling Sharpshooter created through the builder. |
| 14 | Tablet | Production IAB 768×1024: all six tabs fit with scrollWidth 753. Physical tablet/touch unverified. |
| 15 | Mobile | Production IAB 390×844 and 320×740: all six tabs fit without horizontal overflow. At 320px feature inspector is modal, locks body scrolling and fits width. |
| 16 | Sheet fixes | Safe-area-aware launcher/page clearance and coarse-pointer roll-target minimums, without changing desktop density or calculated rules. |
| 17 | Inspector fixes | Mobile backdrop, modal semantics and body-scroll lock; focus wrapping/return and Escape retained. Owned pinned entity coverage tested, including progression-derived features/subclass. |
| 18 | Notes | Production notes save/reload passes. Two-tab conflict rejects stale save, preserves local draft and retains the accepted concurrent note. |
| 19 | Free launcher | Safe-area inset and bottom page clearance added. Development responsive rendering checked. Full production page/menu matrix remains unverified. |
| 20 | Fixed 60 Hz | Shared clock now explicitly clamps invalid/negative elapsed time and bounds catch-up to six fixed steps per animated frame. Ten seconds at 60 Hz produces 600 steps. |
| 21 | 120/144 Hz | Simulated timing tests produce 600 fixed steps per ten seconds and identical settled raw faces across 30/60/120/144 Hz. Not a physical monitor test. |
| 22 | Low FPS | Automated 30 FPS and intermittent 1.5-second stalls: bounded work, same results, valid final faces and no escaped bodies. Browser CPU-throttle control unavailable. |
| 23 | Viewport resize | Development live Knife attack resized 1440→320; settled 16, total 21. Camera reframes a fixed world; no physics teleport. Canvas bottom clearance avoids fixed controls. |
| 24 | WebGL failure | New renderer tests: init failure continues headlessly; context loss accelerates the same world and returns exactly one callback. Actual production context-loss injection unverified. |
| 25 | Rapier fallback | Production first Knife attack used one clearly labelled SERVER_FALLBACK, raw 17 + 5 = 22, preserved after reload. Found production CSP blocks Rapier WASM; narrow permission fix added and tested, host rebuild/retest pending. |
| 26 | Reduced motion | Existing preference/matchMedia implementation and tests retained; accelerated same-world path. Real OS/device setting and production flow remain unverified. |
| 27 | Text only | Headless test constructs no WebGL renderer and returns same authorised values. Shared geometry/math normally uses Three modules; unavailable module loading takes approved server fallback, so no WebGL is required to roll. |
| 28 | Distribution smoke | 400 deterministic diverse seeds for each d4/d6/d8/d10/d12/d20/d100: 2,800 rolls, zero exhausted retries. Broad catastrophic-bias thresholds pass; not fairness certification. Full histograms saved. |
| 29 | Seed diversity | Backend test verifies 40 unique 64-hex seeds; implementation uses 32 SecureRandom bytes, not incremental counters. |
| 30 | Abandoned sessions | Expiry tested with database-controlled clock boundary. Expired finalization rejects without history; page destruction cannot commit a late callback. Logical expiry releases reservations after five minutes. Rows retained for audit. |
| 31 | Reservation cleanup | Existing transactional reservation, cancellation/expiry and rollback tests pass. Expired CREATED rows are excluded from active reservation counts; no phantom item consumption. |
| 32 | Network recovery | Existing identical-submission retry test passes: no new simulation/session or resource use. In-memory settled values survive a lost response while page stays open. Reload/navigation retry restoration is not implemented; check history, then expiry/failure state. |
| 33 | History/replay | Production fallback history survives authenticated hard reload with raw values, modifier and label retained. Physics/replay production verification awaits CSP rebuild. |
| 34 | Historical profiles | All eight bundled profiles match baseline. New test reopens/rolls narrow-v1 and tier1-v1…v7, entering v5 via its legal explicit advancement contract. Historical Finesse tests remain historical. |
| 35 | Security/proxy | Added malformed dotted-ID/encoded separator rejection tests and scoped body-limit regression. Ownership, exact counts/ranges, action/context, expiry, duplicate submission and forged Knife ability tests pass. Health reveals no configuration. |
| 36 | Content tests | 155 pass. No canonical catalogue, ruling, immutable snapshot or progression changes. |
| 37 | Backend tests | 108 pass against separate test PostgreSQL; clean distribution built. |
| 38 | Frontend tests | 129 pass in 20 files after adding production CSP regression. Four targeted header/renderer tests pass; TypeScript passes. |
| 39 | TypeScript | Passes. Successful production compiler/TS stages do not imply a deployable artifact. |
| 40 | Runbook | docs/PRODUCTION_RUNBOOK.md: prerequisites, exact commands, configuration, migrations, artifacts, Docker, health, recovery and release gates. |
| 41 | Browser support | docs/BROWSER_SUPPORT.md: explicit tested/unverified browser matrix and required production flow. |
| 42 | Device validation | docs/DEVICE_VALIDATION.md and JSON/screenshots: development-only viewport matrix with outstanding production/device checks. |
| 43 | Production blockers | Rebuild frontend with WASM CSP fix and verify production physics, roll categories, free pools/d100 and replay. Complete named-browser and remaining failure/recovery/device acceptance. Docker build/startup itself is verified. |
| 44 | Limitations | No real device/monitor/CPU-throttle certification; no statistical fairness or cross-device trajectory guarantee; client faces are range-validated, not server re-simulated; durable browser retry after reload absent. No new rules or game features added. |
| 45 | Next milestone | Host rebuild of frontend, then production dice/replay acceptance and remaining browser matrix. No Level 5/Extra Attack work until readiness gates pass. |

## Windows diagnosis

Runtime: Node v24.22.1, pnpm 11.25.0, Next.js 16.4.2. Original source: `C:\Users\tgccl\OneDrive\Documents\localdev\Dark-Imperium`. Clean diagnostic copy: `C:\Users\tgccl\Documents\Codex\di-prod-validation`, outside OneDrive. No old node_modules or .next was copied into that clean project.

1. Default pnpm install failed creating its project-registry symlink under sandbox AppData. Local `.pnpm-store`, hoisted node linker and disabled global virtual store allowed a fresh frozen-lockfile install; 141 packages downloaded.
2. Direct clean `node node_modules/next/dist/bin/next build` compiled successfully and passed TypeScript, then failed `mkdir` at `C:\Users\tgccl\Documents\Codex\di-prod-validation\frontend\.next\server\app\login.segments\login`.
3. A separate fresh `.next-serial` output with one worker failed `mkdir` at `.next-serial\server\app\_not-found.segments\_not-found`.
4. A separate webpack diagnostic failed during compilation at `.next-webpack\types\app\register`.
5. Standard Node output in the earlier non-clean workspace also failed prerender directory creation. Neither output-mode nor worker-count workaround was retained.
6. The previously failing directory can be created by an isolated Node mkdir; 100 serial and 100 concurrent scratch mkdir operations succeeded. Inherited directory ACLs showed modify access. These observations do not prove a simple concurrency race, antivirus lock, path-length issue or a repository bug. Defender status inspection was unavailable. The exact interaction with the restricted Windows execution environment remains unresolved.

Earlier standalone trace-copy failure: `C:\Users\tgccl\Documents\Codex\2026-10-22\files-pasted-by-the-user-dark\work\advancement-build\.next\standalone\node_modules\next\dist\build\webpack\config\blocks\css`, operation mkdir, EPERM. This pass establishes that OneDrive and standalone tracing are not necessary conditions for failure, not that every ordinary Windows deployment fails.

## Evidence

All new logs, histograms, backend runtime/migration records, profile comparison and development viewport evidence are under [verification/production](verification/production). `production-api-startup.log` records the empty-schema migration sequence. `backend-runtime.json` records production API health, pinned v7 details, fallback metadata and duplicate idempotence. No credentials are included.

The independent production backend used port 8081 with loopback-only HTTP verification origin 3100; this did not establish a working production frontend on 3100. The user confirmed http://localhost:3000/ as the host Docker URL. Fresh Codex browser navigation at that URL still loads development React and Next dev HMR scripts; this session cannot yet establish that its browser reaches the host-verified production instance. Validation databases are separate from imperium_preview. No existing character was migrated.

## Host verification update — 23 October 2026

Evidence source: explicit user report in this chat, recorded in [host-docker-verification.json](verification/production/host-docker-verification.json). The host returns Docker Client and Server information, uses desktop-linux, has Compose available, successfully builds/starts the stack with docker compose up --build, and serves the working application over localhost. This closes the host Docker deployment gate. No image digest, fresh-volume migration run, browser version, or detailed browser acceptance matrix was supplied, so those details are not inferred. Prior session error logs remain historical evidence only. Do not attempt host Docker repairs from the restricted session.

## Production URL follow-up

The user explicitly confirmed `http://localhost:3000/` as the Docker-served application. Fresh navigation in a new Codex IAB tab, and a separate check of `http://127.0.0.1:3000/`, both showed **Open Next.js Dev Tools**. DOM script URLs included `react-dom-client_development` and `[turbopack]_browser_dev_hmr-client`. This is evidence of development runtime assets in the session browser, not evidence against the user’s host Docker verification. Production browser acceptance is pending resolution of this endpoint/runtime mismatch. No Docker engine calls, service stops or host repairs were attempted. Evidence: [runtime observation](verification/production/production-runtime-mismatch.json), [screenshot](verification/production/production-runtime-mismatch.png).

## Docker production acceptance on port 3100

The earlier endpoint mismatch is resolved: host logs showed the frontend could not bind occupied port 3000. With FRONTEND_PORT=3100 and APP_ORIGIN=http://localhost:3100, all three containers are healthy. Fresh IAB navigation at 3100 has no development tools. Creation, authenticated deep-link reload, six tabs at six sizes, weapon/feature inspection, notes persistence and conflict handling pass. Test character: 4cd99cd0-d353-4687-9908-2f96058216ff, isolated verification account. No existing character was modified.

The first physical roll exposed a real deployment defect: production script-src omitted WebAssembly permission, while Rapier calls RAPIER.init(). The served header was captured directly; it lacks both wasm-unsafe-eval and unsafe-eval. Added only wasm-unsafe-eval, retaining the production JavaScript eval prohibition and same-origin restrictions. This is required by [CSP WebAssembly integration](https://www.w3.org/TR/CSP/#wasm-integration) and the installed Next CSP guide. No physics algorithms or rules changed. All 129 frontend tests and TypeScript pass; running-container acceptance of the fix awaits the host rebuild. The saved fallback result remains canonical and must not be replaced. See docker-browser-acceptance.json and docker-production-history.png.

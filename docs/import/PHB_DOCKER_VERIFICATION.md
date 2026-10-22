# Infrastructure verification — minimum rulings pass

Docker remains **UNVERIFIED**. Commands ran from the relocated project, with process-local disposable POSTGRES_PASSWORD to satisfy Compose interpolation; no .env was written.

| Command | Result |
| --- | --- |
| `docker compose build` | Exit 1: `open C:\Users\tgccl\.docker\buildx\.lock: Access is denied.` |
| `docker compose up -d` | Exit 1: unable to get `postgres:17-alpine`; missing `//./pipe/dockerDesktopLinuxEngine` |
| `pnpm test` (frontend) | EPERM creating project-store symlink under AppData sandbox pnpm/store |
| Cached JDK 21 / Gradle 8.14.3 `gradle.bat test --offline --no-daemon` (backend) | Exit 1: `Could not connect to the Gradle daemon.` |

No container health, migration, seed, frontend-test or backend-test success is claimed. The Python content/conformance suite runs independently. Application architecture and Compose configuration were not changed to work around infrastructure access.

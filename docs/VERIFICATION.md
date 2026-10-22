# Delivery verification

Verified on 22 October 2026 in the delivery environment.

## Passed

- Next.js 16.4.2 optimized production build, including TypeScript checking and generation of all application routes.
- Frozen pnpm dependency installation.
- Five frontend tests: API structured errors, empty logout response, network failures, character submission/navigation and retained input after failed save.
- Kotlin compilation and `installDist` application packaging on JDK 21 / Gradle 8.14.3.
- Eleven backend tests: four rules/password/rate-limit unit tests and seven API integration tests.
- Integration tests used actual PostgreSQL 17.6, not an in-memory substitute. They cover registration, login, creation, committed retrieval, owner-only listing/reads/updates/deletes, all three seeded catalogs, logout revocation, invalid input/origin handling, atomic failure and equipment cascade cleanup.
- Flyway applied V1–V3. The final test run included the generic item-identity migration. A running preview database with a saved character also upgraded from V2 to V3 successfully.
- Browser acceptance walkthrough: register → login → empty archive → create named Human Guardsman → equip Lasgun → save → sheet → reload → archive list → reopen. The saved character and session also survived an API restart and V3 migration.
- Browser compendium navigation, weapon statistics, search empty state and logout.
- Desktop visual inspection of the landing page and character sheet. A screenshot is included alongside the source package.
- Docker Compose configuration parsed successfully with interpolation disabled. Dockerfiles, health checks, persistence, environment wiring and source packaging were reviewed.

The frontend tests used Vitest's `--configLoader runner` because the delivery OS sandbox blocked esbuild's directory traversal during its default configuration loading. The normal project test command remains available outside that restriction.

## Not verified

**`docker compose up` and container image builds were not executed successfully.** Docker CLI/Compose were installed but the Docker engine was unreachable. The owner explicitly requested finishing with Docker startup marked unverified. A temporary loopback-only native PostgreSQL instance was used for real database testing instead. This does not establish container-runtime compatibility; run the documented Compose acceptance test on a machine with a working engine.

Mobile/tablet media rules and keyboard-accessible native controls are implemented, but an exhaustive device, screen-reader, cross-browser or accessibility audit was not performed. No load test or production penetration test was performed.

## Known functional limits

- Game statistics are illustrative placeholders; properties and class progression are stored but not mechanically interpreted.
- Character creation starts at level one. Editing is limited to renaming and deletion; wounds, attributes, equipment changes and advancement are future work.
- Content versions are not immutable snapshots; existing sheets use current referenced content.
- There are no invitations, email verification, password recovery, MFA, account deletion or session-management screens. Private deployment access is currently an operational boundary.
- Authentication rate limiting is process-local. Character lists are unpaginated and hydrate full sheets, suitable for the initial small group.
- Campaigns, encounters, combat tracking and advanced GM/content tooling are deliberately absent.

## Next milestone

Agree the authoritative initial rules and introduce validated, immutable content revisions with calculated-value explanations. Then add a small, fully tested character-state editing flow for wounds/attributes. Keep advanced systems deferred until those foundations are stable.

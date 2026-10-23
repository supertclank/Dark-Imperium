# Browser support and validation

23 October 2026. **No named browser is certified for production in this pass.** The user has verified host Docker build, startup and localhost application access; this does not identify a browser/version or certify the detailed flows below. Only the Codex in-app browser is exposed by this session's browser tooling; it is not evidence of separate Chrome, Edge, Firefox or Safari acceptance.

| Browser | Version tested | Character sheet | Dice physics | Fallback | Limits |
|---|---|---|---|---|---|
| Codex in-app browser | Version not exposed by tool inventory | Development preview tested at six widths; all tabs, inspector, inventory search, notes conflict | Development resize during live d20 succeeded; existing v7 proofs remain historical | Automated WebGL-init/context-loss, headless and module-failure tests; no production browser fault injection | Not a production frontend; not a physical mobile device |
| Chrome | Not available to automation | UNVERIFIED | UNVERIFIED | UNVERIFIED | Full production flow pending |
| Edge | Not available to automation | UNVERIFIED | UNVERIFIED | UNVERIFIED | Full production flow pending |
| Firefox | Not available to automation | UNVERIFIED | UNVERIFIED | UNVERIFIED | Full production flow pending |
| Safari / mobile Safari | No available environment | UNVERIFIED | UNVERIFIED | UNVERIFIED | No WebKit/device acceptance |

The executable tests cover fixed-step outcomes at 30/60/120/144 Hz, long frames, top-face detection, collisions, bounded rerolls, physical/result submission separation, failed finalization retries, fallback, replay invariance and reduced/text modes. jsdom tests and Node-hosted Rapier are not browser/device certification.

## Required production acceptance sequence

For each actual browser, record its exact version and OS and use generated production frontend artifacts plus the production API configuration. Open root/list/saved v7 character; exercise every tab and weapon/feature inspection; roll ability, skill, save, initiative, attack and damage; exercise free pool controls, d100, mixed dice and replay; hard-refresh and compare raw values, labels, profile digest, timestamps and state. Repeat a mobile-width flow with notes save/reload and an optimistic conflict.

Verify static assets and lazy-loaded dice after a cold load. Inject WebGL unavailability/context loss and physics-module failure where tooling permits. Repeated finalization must not duplicate history/resources. Real device reduced-motion, background suspension, CPU throttling and touch scrolling remain pending. Never replace the canonical saved result because a replay trajectory differs.

Evidence: [device matrix](verification/production/device-matrix.json), [timing tests](../frontend/tests/SimulationTiming.test.ts), [renderer failure tests](../frontend/tests/RendererFailure.test.ts), and [release report](PRODUCTION_READINESS_REPORT.md).

Production URL follow-up: the user confirmed `http://localhost:3000/`. Fresh session browser navigation still loads Next Dev Tools and development/HMR scripts (also at IPv4 loopback). Host Docker verification stays VERIFIED; these browser observations cannot be counted as production acceptance. See [runtime evidence](verification/production/production-runtime-mismatch.json).

## Production follow-up, port 3100

The port-3000 development/production mismatch is resolved. Host Compose output confirms all three containers healthy at localhost:3100. Codex IAB now verifies creation, sheet deep-link reload, all six tabs at 1920/1440/1280/768/390/320 widths without overflow, weapon and mobile feature inspection, notes save/reload and stale-save draft preservation. Saved fallback history also survives reload. These are production IAB checks, not named-browser or physical-device certification. Physics and replay acceptance remain pending a host rebuild for the WASM CSP correction. Earlier development-only evidence above is retained as historical context. See [production browser evidence](verification/production/docker-browser-acceptance.json).

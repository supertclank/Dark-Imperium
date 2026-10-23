# Device validation

23 October 2026. These are **viewport-emulated development checks in the Codex in-app browser**, not production or real hardware certification. All six tabs were clicked at every size. Browser version is not exposed by the tool inventory.

| Viewport | Sheet/tabs | Inspector | Dice | Free roller | Notes | Issues/status |
|---|---|---|---|---|---|---|
| 1920×1080 | All tabs inside width; scrollWidth 1905 | Desktop panel retained | Automated timing tests, not per-size browser certification | Launcher rendered | Notes tab opens | Production flow pending |
| 1440×900 | All tabs inside width; scrollWidth 1425 | Desktop panel retained | Live throw started here then resized to 320 | Launcher rendered | Notes tab opens | Production flow pending |
| 1280×720 | All tabs inside width; scrollWidth 1265 | Existing desktop rules inspection | Not separately rerolled | Launcher rendered | Notes tab opens | Production flow pending |
| 768×1024 | All tabs inside width; scrollWidth 753 | Panel layout; no physical touch test | Not separately rerolled | Launcher rendered | Notes tab opens | Coarse-pointer controls now minimum 44px; physical tablet unverified |
| 390×844 | All tabs inside width; scrollWidth 375; 44px ability/tab controls | Mobile focus/scroll/backdrop semantics tested; prior v7 drawer proof | Prior v7 proof; current automated timing/fault tests | Launcher rendered | Tab retained | Real device and production acceptance pending |
| 320×740 | All tabs inside width; scrollWidth 305; 44px ability/tab controls | New modal backdrop/scroll lock prevents background interaction | Resize during throw completed with raw 16, +5, total 21 | Launcher rendered above safe-area margin | Actual stale save rejected, draft preserved | Dice are small at this width; physical touchscreen and production flow unverified |

## Hardening

- Mobile inspector now advertises aria-modal, blocks background pointer interaction with a backdrop, locks body scrolling, traps keyboard focus and restores the opener. Escape/Close work; the backdrop closes without saving or changing rules.
- Physical tray uses a fixed world. Viewport changes adjust only the camera projection; they do not teleport bodies or change canonical values. Bottom canvas clearance reserves space for fixed controls and device safe areas.
- Launcher/panel respect safe-area inset. Page bottom clearance allows final content to scroll above the launcher. Coarse-pointer roll controls are at least 44px without enlarging fine-pointer desktop density.
- Character tabs remain a deliberate two-row grid. Inspection is an intentional independent scroll surface. Notes stay mounted across tab changes.

[Machine-readable widths](verification/production/device-matrix.json), [320px sheet](verification/production/device-320.png), [live resize](verification/production/production-resize-development.png), [notes conflict](verification/production/production-notes-conflict.png).

Selected tab and inspector are intentionally ephemeral. Reload returns to Actions with the owned pinned character; saved notes remain persisted. A local unsaved draft or in-memory roll retry is not restored after page destruction. Copy the draft before resolving a conflict; check saved history before starting another roll after a lost connection/reload.

Host Docker production build/startup and localhost access are verified by the user. Remaining acceptance: full mobile free-roller menu/d100/replay checks on the final production artifact, cold reload on every route, Chrome/Edge/Firefox matrix, true reduced-motion OS settings, touch scrolling and physical-device performance. These are not waived by the development screenshots.

## Production follow-up, port 3100

The port-3000 development/production mismatch is resolved. Host Compose output confirms all three containers healthy at localhost:3100. Codex IAB now verifies creation, sheet deep-link reload, all six tabs at 1920/1440/1280/768/390/320 widths without overflow, weapon and mobile feature inspection, notes save/reload and stale-save draft preservation. Saved fallback history also survives reload. These are production IAB checks, not named-browser or physical-device certification. Physics and replay acceptance remain pending a host rebuild for the WASM CSP correction. Earlier development-only evidence above is retained as historical context. See [production browser evidence](verification/production/docker-browser-acceptance.json).

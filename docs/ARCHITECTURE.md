> **Current production pass:** [Narrow character builder](PRODUCTION_CHARACTER_BUILDER.md) describes the V4 schema, pinned calculation adapter, API and current verification. Foundation details below are historical where superseded.

# Architecture

## Boundaries

```text
Browser (React / App Router)
  -> same-origin /api/* proxy (Next.js server)
    -> Ktor REST API
       -> authentication / content / characters / rules calculator
          -> JDBC + HikariCP -> PostgreSQL
```

The API is a modular monolith with explicit service boundaries, not independently deployed domain services. Next.js owns presentation and an intentionally thin reverse proxy. Kotlin owns validation, sessions, ownership, transactions and calculations. PostgreSQL owns durable records and referential constraints. Flyway owns schema evolution.

The small modules are source files with one responsibility: `AuthService`, `ContentRepository`, `CharacterService`, `RulesEngine`, `Database`, API wiring and serializable models. No generic repository framework, ORM or speculative plugin runtime is needed for this slice. Extract feature packages when their size warrants it.

## Decisions

1. **Opaque database sessions, not browser tokens.** Random 256-bit tokens travel only in HttpOnly SameSite=Lax cookies. PostgreSQL stores SHA-256 digests, a seven-day absolute expiry and the user ID. Logout deletes the digest and clears the cookie. Expired sessions are rejected and cleaned on login. Sessions survive an API restart.
2. **Same-origin proxy.** The browser never needs the private API hostname or database secrets. Only a fixed backend URL and safe path segments are accepted; caller-supplied destinations and forwarding headers are not used. The proxy caps streamed request bodies at 16 KiB and has a 15-second upstream timeout. Neither the API nor database has a published Compose port.
3. **CSRF protection.** Every mutation, including registration/login/logout, requires an exact `Origin` match on the API. Missing origins are rejected. Cookies have SameSite=Lax, HttpOnly and configurable Secure. No permissive CORS configuration exists. Non-browser API clients must send the configured Origin explicitly.
4. **Password handling.** Argon2id v1 parameters: 19 MiB memory, two iterations, one lane, independent 16-byte salts, 32-byte outputs. Passwords accept 12–128 characters without trimming. Unknown accounts perform a dummy verification. Hash formats are versioned for later upgrades.
5. **Bounded authentication throttling.** A single-process limiter permits 15 attempts per normalized email and 150 combined auth attempts globally per 15-minute window, with a bounded key map. Keys are email digests. It resets at restart and intentionally avoids trusting forwarded client IPs. An edge limiter is appropriate before exposing the application beyond the private group. The global limit is conservative and can affect all users during abuse.
6. **Ownership from the session.** Character reads, updates and deletes scope SQL to `(id, user_id)`. The client cannot submit a user ID; strict DTO decoding rejects unknown fields. A foreign character returns the same 404 as a missing one. Listing uses only the authenticated user ID.
7. **Atomic creation.** Validate content IDs, calculate starting values, write the character and equipment inside one transaction. A failure rolls everything back. Rename is transactional; delete cascades only to owned equipment.
8. **Content-driven calculations.** Species and classes provide versioned structured effects. `RulesEngine` interprets a small allowlist of operations and targets. It never branches on a game-content name or ID. See the rules document.

## Errors and runtime

API errors have stable codes and useful messages, never exception text. Unexpected exceptions are logged server-side and return a generic 500. The browser handles network failures, service unavailability, unauthenticated sessions, missing records and invalid forms. Client route guards are a convenience only; API authorization is authoritative.

JDBC and hashing work run on the coroutine IO dispatcher. Hikari bounds database connections. Health checks execute a database query rather than simply checking the HTTP socket. There are no external services in the core flow.

The UI uses native controls, labelled fields, focus outlines, live error messages, semantic navigation, skip links, reduced-motion support and responsive grids. Presentation never calculates RPG-specific effects.

## Deliberate limits

No email delivery, password resets, MFA, invitations, roles, content administration, pagination or session management UI. No independent multi-node rate-limit coordination. Content reads follow current records rather than immutable revisions, and only level one creation is supported. These are explicit next-stage decisions, not simulated features.

## Proposed integrated dice boundary

[Integrated dice rolling](content/DICE_ROLLING.md) defines the future content-to-roll compiler, immutable result, secure unbiased sampler, action cost/idempotency ledger, visibility and optional presentation adapters. This is a proposal only: no dice engine, 3D renderer, campaign history or multiplayer transport is implemented. Existing character-sheet functionality must remain usable with physical dice.

# Database

PostgreSQL 17, UUID primary keys, UTC-aware `timestamptz` audit fields and explicit Flyway migrations. JDBC prepared statements bind user input; the only interpolated table name comes from a closed Kotlin enum.

| Entity                | Responsibility / relationships                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `users`               | Unique normalized email, password hash, creation timestamp                                                                       |
| `sessions`            | Hashed opaque token, user FK, absolute expiry; cascades on account removal                                                       |
| `species`             | Slug, display content, effect JSONB and content version                                                                          |
| `classes`             | Slug, display content, effect JSONB, progression JSONB and version                                                               |
| `items`               | Shared catalog identity and item kind; starting foundation for other item categories                                             |
| `weapons`             | Typed weapon record; composite FK to item identity/kind prevents non-weapon references; statistics and structured property JSONB |
| `characters`          | Owner, name, species/class FKs, level, base attribute JSONB, current wounds, timestamps                                          |
| `character_equipment` | Character FK, generic item FK, quantity and equipped flag; unique per character/item                                             |

## Migrations

- V1 defines accounts, sessions, content, characters and equipment.
- V2 inserts clearly labelled development Human, Guardsman and Lasgun records.
- V3 introduces shared item identity and migrates equipment's weapon reference to a generic item reference without losing data or foreign-key protection.

Seed IDs are stable for repeatable fixtures, but application behavior does not depend on them. Flyway history prevents reseeding on restart. No accounts or passwords are seeded.

## Constraints and transactions

Emails are lowercase and unique. Character names are nonblank and length-bounded. Level, wounds, range and quantity have database constraints. Equipment cascades on character deletion. Content references restrict deletion while in use. Owner/created-time and session-user/expiry indexes support the initial access patterns.

Creation inserts character and equipment in one transaction. The request cannot set owner, level, attributes or current wounds. Reopening a character loads the current referenced content and calculates derived values; there is no duplicated persisted max-wounds/movement field to drift out of sync.

## Extension path

- Add subclasses/backgrounds through new content tables and explicit nullable character FKs or join tables.
- Add skills, feats and feature choices through content catalogs and character-selection join tables, keeping selections separate from calculated effects.
- Add armour/gear by inserting an `items` identity plus a typed detail table with its own kind constraint. Existing equipment identity and ownership relationships remain intact. Extend the equipment response type and renderer when those categories actually exist; this release intentionally renders weapon equipment only.
- Version content immutably and pin character selections to revisions before editing live rules. Current integer versions document the direction but are not historical snapshots.
- Add pagination and consolidated list queries when the private group's record count warrants it; the current list hydrates complete sheets and is intentionally small-scale.

JSONB preserves structured rules and future parameters; it is not used instead of relational ownership or referential integrity. Application decoding currently enforces the effect schema; a content publishing validator is the next milestone.

Back up with PostgreSQL-native tooling and test restoration before relying on a production deployment. Never delete the Compose volume merely to apply a new migration.

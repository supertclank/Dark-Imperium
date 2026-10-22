# Dark Imperium content contract — proposed v1

This is a **design specification, not an implemented application feature**. It proposes the canonical contract for future importers, content tools, builders and rules evaluation. Editorial approval and rules-owner decisions are required before publishing authoritative game data. No application code, database migrations or gameplay features were changed for this task.

## Read in this order

1. [Content architecture and common envelope](CONTENT_MODEL.md)
2. [Permanent IDs](CONTENT_IDS.md) and [versioning](CONTENT_VERSIONING.md)
3. [Entity catalog](ENTITY_TYPES.md) and [detailed equipment, powers and statblocks](DOMAIN_SCHEMAS.md)
4. [Effects, predicates and evaluation](RULES_EFFECTS.md)
5. [Character state](CHARACTER_MODEL.md) and [builder/progression](CHARACTER_BUILDER.md)
6. [Validation](VALIDATION.md) and [import workflow](IMPORT_STRATEGY.md)
7. [Complete examples](EXAMPLE_CONTENT.md)
8. [Expansion/design review and open decisions](DESIGN_REVIEW.md)
9. [Integrated dice rolling](DICE_ROLLING.md)
10. [Bridge from the existing foundation](FOUNDATION_MAPPING.md)

## Evidence and authority

The repository was inspected on 22 October 2026. It contains application source, V1–V3 database migrations, and the existing architecture/rules documents. No Player's Handbook, Bestiary, GM Guide, Angels of Death book, PDF or DOCX rulebook was found in the repository. The supplied task briefs describe desired capabilities, not authoritative game mechanics.

The only available game data is the development seed migration: Human movement 6, Guardsman maximum wounds 10, and a Lasgun with 1d10 Energy damage, 100/300 m ranges and descriptive two-handed/reliable properties. The foundation explicitly labels these values placeholders. The six current attributes at 30 are also placeholders. This specification does not infer real rules from those values or from other Warhammer games.

All examples use the reserved `example` namespace and `verification: placeholder`. Their exact statistics, creation order, progression levels, chapter mechanics, resource costs, dice procedures and terminology need human confirmation. They demonstrate structure and relationships only. They must never enter an authoritative ruleset accidentally.

## Contract conventions

**MUST** identifies a validation or safety requirement. **SHOULD** is the recommended default with a documented exception. Field tables are normative proposed contracts; JSON examples instantiate them. A required array may be empty unless its table says otherwise. Optional absence means not supplied, never zero or unlimited. `null` is prohibited except where expressly allowed; unknown source facts are recorded as editorial issues instead of fabricated values.

Every entity inherits the envelope in CONTENT_MODEL. Every payload field is defined by its entity/family table. Examples are complete records in [examples/catalog.json](examples/catalog.json); the catalog is a compact review fixture, not an importer or full rulebook. [examples/ruleset-lock.json](examples/ruleset-lock.json) pins its records. [examples/character.json](examples/character.json) demonstrates owned state.

Machine-readable examples and repository-local checks are described in [VERIFICATION.md](VERIFICATION.md). No claim is made that the existing engine accepts this contract or that a production JSON Schema/compiler has been implemented.

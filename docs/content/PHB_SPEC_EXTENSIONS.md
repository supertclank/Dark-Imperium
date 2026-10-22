# Small PHB specification extensions

Implemented draft validator addition: `phb.roll_bindings.v1`, optional RollTemplate.damageBindings with one group per typed component. See PHB_DICE_READINESS. This is additive schemaVersion1 capability negotiation; an engine without it cannot publish/execute this package. No production engine support is claimed.

Other proposals remain unimplemented and cannot appear as executable draft payloads:

1. Power multilist membership: migrate single discipline to `powerLists: ContentRef[]` plus typed tier; one authority, explicit migration, class access selects intersection. Do not encode alternate membership as free-form names.
2. Duration: game-time minutes and explicit concentration owner/end events; never wall-clock expiry. Concentration rules require source ruling.
3. Resource: tagged bounded/unbounded maximum and transactional gain operation. Pressure has no inferred cap; underflow policy still requires ruling.
4. Random tables: resolved numeric modifier and one optional open-ended final band; nonoverlapping complete coverage of reachable totals. No magic sentinel game maximum.
5. Mounted-only weapon host context: model required host/crew without inventing actor hands; payload-bound weapon mode for grenade launcher. Treat as explicit schema migration, not null required fields.
6. Vehicle: register DT/Handling stats and reviewed damageRule in the existing profile. No new engine/service or independent dice system.
7. Missing execution primitives: exact actor-local class training/save entitlements, feature resources, damage reduction with critical context and explicit replacement upgrades. Reuse existing effects/requirements wherever possible; only add a primitive when a real invariant is missing.

`ACTIONS.md` was absent in the original architecture. Its new page is an index to the existing DOMAIN_SCHEMAS/DICE_ROLLING/RULES_EFFECTS contracts, not a competing action model.

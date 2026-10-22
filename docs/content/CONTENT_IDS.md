# Permanent IDs

## Convention

Use `<namespace>.<kind>.<key>[.<subkey>...]`, lowercase ASCII. Full regex:

```text
^[a-z][a-z0-9_]{1,31}\.[a-z][a-z0-9_]{1,31}\.[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$
```

Maximum 160 characters. Each component is nonempty; no whitespace, slash, percent, Unicode lookalikes or user-controlled SQL identifiers. Dots and underscores are safe path characters; use standard URL encoding nonetheless. A database UNIQUE constraint covers the entire case-sensitive canonical ID. Do not derive table/column names from it. UUID storage keys may coexist.

| Example proposed identity | Meaning |
| --- | --- |
| `di.species.human` | Publisher-owned Human identity |
| `di.class.guardsman` | Class identity |
| `di.subclass.guardsman.line_veteran` | Class-related option; relationship still explicitly stored |
| `di.weapon.lasgun` | Weapon identity |
| `di.weapon.lasgun.carbine` | Mechanically distinct variant, not a renamed display label |
| `di.property.weapon.two_handed` | Parameterized weapon property |
| `di.feature.guardsman.steady_hands` | Feature identity independent of grant level |
| `di.rule.rest.field_rest` | Rest/recharge policy |
| `di.choice.guardsman.starting_loadout` | Reusable choice definition |
| `di.power.discipline_a.ward` | Psychic power; discipline relationship is explicit |
| `di.creature.renegade_trooper` | Distinct statblock identity |
| `di.affiliation.blood_angels` | Chapter option represented by generic affiliation |
| `hb_7fa2c100.weapon.custom_carbine` | Homebrew namespace assigned by the registry |

These examples establish syntax, not official labels or real rulebook IDs. The complete sample catalog deliberately uses `example.*`, reserved for non-authoritative fixtures. A namespace registry prevents collisions; namespaces are assigned to publishers/owners, not merely trusted from uploaded files. Homebrew namespaces require a unique server-assigned suffix with collision checking. `di` is reserved for approved Dark Imperium content; it does not imply any external rights or endorsement.

## Stability rules

- A display-name correction, translation or book reorganization changes a revision, not the ID.
- Once allocated, an ID is never reassigned to unrelated content, even after withdrawal.
- Reparenting a subclass may leave its historically descriptive key unchanged; the `parentClass` reference is authoritative. Do not parse lineage out of keys.
- An expansion from the same publisher may continue using `di`; package/source identity describes its origin. Independent publishers use their own namespaces.
- Variants with independent mechanics get their own IDs and optional `variantOf` references. Avoid implicit inheritance/merge behavior. A variant contains its complete final fields; lineage is editorial unless an explicit typed override contract is used.
- Deprecation/replacement uses `replacedBy`, never silent aliases. An administrative identity redirect may support old URLs, but import/lock resolution must retain the original pinned identity or perform a reviewed migration.

## Nested stable IDs

Effects, action outcomes, progression grants, option bundles and manual-rule entries have local keys (regex `^[a-z][a-z0-9_]{0,63}$`). Their identity is the tuple `(owning ContentId, local key)`; revisions resolve through the lock. For display/logging, `di.feature.steady_hands#attack_bonus` is acceptable. The fragment is not itself a ContentRef.

A grant at level 3 uses a stable local key such as `choose_subclass`, not an array index. Moving that grant to a new level in a new revision preserves the key if its meaning is unchanged. Replacement creates a new grant key and explicitly names the old grant key. Choice answers are keyed by grant occurrence and choice local option key, not option label or array position.

Repeated sources require instance identity: `(actor UUID, acquisition UUID, owner ContentId, local key)`. Two copies of the same weapon retain separate item UUIDs. Deleting one instance retracts only that instance's grants. A progression grant ID identifies a rule entitlement; an owned inventory UUID identifies the actual object acquired from it.

Content revision, source/book version and ruleset lock identity never become suffixes in ContentIds. These are separate axes, allowing a character to use an old Lasgun revision without inventing a new weapon identity.

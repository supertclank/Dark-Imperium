# PHB damage vocabulary and interaction

Canonical DAMAGE_TYPE identities: acid, bludgeoning, fire, force, lightning, necrotic, piercing, poison, psychic, radiant, radiation, slashing, thunder. Acid is added from Hazard Plate (printed29/PDF42). No hierarchy links or universal energy/physical parent are inferred. Radiant and radiation remain distinct; poison damage and Poisoned condition are distinct; psychic damage and psychic origin are distinct.

| Term | Classification in the cited PHB context | Relationship |
| --- | --- | --- |
| Plasma | WEAPON_CATEGORY | Profiles commonly say radiant/fire; slash unresolved |
| Melta | WEAPON_CATEGORY | Profiles supply actual damage labels separately |
| Flame / flamer | WEAPON_CATEGORY or descriptive delivery | Fire is the actual damage type where printed |
| Las | WEAPON_CATEGORY | Lasgun lists radiant; no inferred energy parent |
| Bolt | WEAPON_CATEGORY | Bolter explicitly has piercing plus thunder |
| Energy | descriptive TAG candidate, not canonical DAMAGE_TYPE | No general PHB energy resistance family established; old example.energy is not PHB |
| Physical | descriptive TAG candidate, not canonical DAMAGE_TYPE | No automatic bludgeoning/piercing/slashing grouping |
| Psychic | DAMAGE_TYPE when damage column says psychic; TAG when describing origin/access | Context must distinguish source of a power from its damage |
| Explosive | DELIVERY_METHOD/description | Blast is RULE_KEYWORD/property; actual typed damage comes from item |
| Power Field | RULE_KEYWORD/property | Resistance bypass wording, not force damage conversion |
| Poisoned / Bleeding Eyes | condition / Perils outcome name | Not new damage types |

Source: weapons PDF35–40, Hazard Plate42, grenades47, powers91–93, Perils95, vehicle116/121. Term occurrence evidence is in review/damage-terminology.json; a text occurrence is not an automatic taxonomy assignment. No unsupported DAMAGE_SUBTYPE is created.

## Components and mitigation order

Preserve each explicit `+` component with its own dice and damage type. `or` means a source-stated choice, not simultaneous damage; action choice still needs binding. Slash semantics require a ruling. Do not split one die pool in half, double it or assign an umbrella type.

Ordinary critical: double attack damage dice, modifiers once, then specific critical extra dice (6.6). Mounted area/battle cannon has no attack roll, critical or Dex damage modifier (21.11). This does not settle how all extra damage interacts with criticals.

General creature path is deliberately incomplete: base components → source-approved damage/critical transformation → **unresolved ordering of save fractions, resistance/vulnerability, flat reductions and other mitigation** → committed HP change. AC determines attack defence, not universal damage subtraction. Shields add their printed AC or provide a particular reaction; fields do not contribute zero AC as armour.

The explicit vehicle subsequence is usable once per-component mitigation is resolved: one hit/effect, after resistance → sum its components → compare with DT (halve DT rounded down for Armour-Breaking) → below threshold0, otherwise full total. Never combine separate attacks; do not subtract DT. Battle cannon applies save then Armour-Breaking/DT. Hull poison/radiation immunity and object/mind targeting restrictions apply; crew resolve separately. This establishes only a partial order, not an invented global resistance algorithm.

Same-type resistance stacking, vulnerability interaction, reductions versus resistance and general rounding remain human rulings. Unknown mitigation blocks final damage, even if a raw damage roll can be generated. Ordinary immunity is not inherited by source taxonomy or crew membership.

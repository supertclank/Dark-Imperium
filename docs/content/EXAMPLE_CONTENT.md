# Complete representative content

All values below are **placeholders**, not authoritative Dark Imperium rules. No rulebook was available. Human/Guardsman/Lasgun examples retain representative numbers from the foundation where useful; all additional mechanics demonstrate the proposed contract only. IDs use the reserved `example` namespace, every record is a draft, and verification remains `placeholder`.

The complete linked fixture is [examples/catalog.json](examples/catalog.json): 100 records covering all 40 proposed entity kinds, including every reference used below. These are complete envelopes and payloads, not snippets intended to be imported without their dependencies. [examples/ruleset-lock.json](examples/ruleset-lock.json) pins exact revisions/digests and allows draft/placeholders **only for editorial preview**. It is not a production ruleset. [examples/character.json](examples/character.json) demonstrates selections, choice origins, owned inventory and state; it deliberately stores no calculated totals and its Lasgun magazine starts empty.

## Relationship map

- Human → movement trait; Ogryn → frame trait.
- Guardsman → starting wounds feature + progression → weapon proficiency, starting-loadout choice, skill choice, subclass choice and upgrade.
- Lasgun → Energy damage, weapon properties, proficiency, magazine resource, ammunition and reload action.
- Ward → Warding discipline + psychic action template → warp resource, test procedure, failure and Perils rules.
- Creature → shared Lasgun with a typed range/name override, reusable traits/reaction/special action and mitigation.
- Vehicle → shared weapon mount, crew role, drive system, trait and damage procedure.
- Astartes example class → chapter-origin choice → chapter/Unknown Founding affiliations → chapter traits/choose-two choice; Deathwatch is a separate eligible service affiliation. Powered armour references an armour system and an explicit class requirement.

Examples deliberately include manual test/Perils/vehicle procedures rather than inventing executable rules for unavailable sources. Per-entity purpose, optional fields, validation and extension points are in [ENTITY_TYPES](ENTITY_TYPES.md); full family contracts are in [DOMAIN_SCHEMAS](DOMAIN_SCHEMAS.md).

## Expected fixture behavior

Human + level-one Guardsman yields movement 6 and maximum wounds 10. Ogryn + Guardsman yields movement 5 and maximum wounds 14. Base attribute modifier values are zero only because the demo profile intentionally does not assert a real formula. A two-handed attack gains a conditional +2 damage contribution when its actual attack weapon qualifies; without attack context the contribution is unresolved. Manual contacts contributes no numeric modifier. The sample character owns an unloaded Lasgun, so an ammo-spending attack is unavailable until an explicit reload/acquisition supplies ammunition.

The remaining catalog records supply complete examples for backgrounds, skills/proficiencies, shield/ammunition/gear/consumables/augmetics/tools/currency, properties/conditions/mitigation/actions/resources/rest, disciplines/psyker/Perils, systems/crew, factions/tags and campaign content. Each ENTITY_TYPES example key resolves in the catalog.

## Human species

```json
{
  "schemaVersion": 1,
  "id": "example.species.human",
  "kind": "species",
  "revision": 1,
  "name": "Human",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Human is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.human",
        "heading": "Human"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "size": "medium",
    "features": [
      {
        "id": "example.feature.human_movement"
      }
    ]
  }
}
```

## Ogryn species

```json
{
  "schemaVersion": 1,
  "id": "example.species.ogryn",
  "kind": "species",
  "revision": 1,
  "name": "Ogryn",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Ogryn is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.ogryn",
        "heading": "Ogryn"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "size": "large",
    "features": [
      {
        "id": "example.feature.ogryn_frame"
      }
    ]
  }
}
```

## Guardsman class

```json
{
  "schemaVersion": 1,
  "id": "example.class.guardsman",
  "kind": "class",
  "revision": 1,
  "name": "Guardsman",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Guardsman is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.guardsman",
        "heading": "Guardsman"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "features": [
      {
        "id": "example.feature.guardsman_wounds"
      }
    ],
    "progression": {
      "id": "example.progression.guardsman"
    },
    "allowedSubclasses": [
      {
        "id": "example.subclass.line_veteran"
      }
    ]
  }
}
```

## Example subclass

```json
{
  "schemaVersion": 1,
  "id": "example.subclass.line_veteran",
  "kind": "subclass",
  "revision": 1,
  "name": "Example Line Veteran",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Example Line Veteran is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.line_veteran",
        "heading": "Example Line Veteran"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "parentClass": {
      "id": "example.class.guardsman"
    },
    "features": [],
    "progression": {
      "id": "example.progression.line_veteran"
    },
    "requirements": {
      "kind": "level",
      "axis": {
        "kind": "class_level",
        "class": {
          "id": "example.class.guardsman"
        }
      },
      "operator": "gte",
      "value": 3
    }
  }
}
```

## Lasgun

```json
{
  "schemaVersion": 1,
  "id": "example.weapon.lasgun",
  "kind": "weapon",
  "revision": 1,
  "name": "Lasgun",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Lasgun is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.lasgun",
        "heading": "Lasgun"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [
    {
      "id": "example.tag.las"
    }
  ],
  "data": {
    "category": "ranged",
    "subcategory": "las",
    "hands": 2,
    "properties": [
      {
        "property": {
          "id": "example.property.two_handed"
        },
        "arguments": {
          "hands": 2
        }
      },
      {
        "property": {
          "id": "example.property.reliable"
        },
        "arguments": {}
      }
    ],
    "features": [],
    "modes": [
      {
        "id": "standard",
        "name": "Standard",
        "attackKind": "ranged",
        "delivery": "manual",
        "damage": [
          {
            "id": "primary",
            "dice": {
              "count": 1,
              "sides": 10,
              "bonus": 0
            },
            "bonus": {
              "kind": "constant",
              "value": 0
            },
            "damageType": {
              "id": "example.damage_type.energy"
            }
          }
        ],
        "range": {
          "kind": "distance",
          "normal": {
            "value": 100,
            "unit": "m"
          },
          "long": {
            "value": 300,
            "unit": "m"
          }
        },
        "costs": [
          {
            "resource": {
              "id": "example.resource.magazine"
            },
            "amount": {
              "kind": "constant",
              "value": 1
            },
            "timing": "attempt",
            "source": "item",
            "refundOnCancel": true
          }
        ],
        "rate": {
          "shotsPerUse": 1
        }
      }
    ],
    "cost": {
      "currency": {
        "id": "example.currency.scrip"
      },
      "units": 100
    },
    "weight": {
      "value": 4,
      "unit": "kg"
    },
    "availability": {
      "scale": "example_supply",
      "rating": 1,
      "label": "Illustrative"
    },
    "equip": {
      "slots": [
        "hands"
      ],
      "hands": 2
    },
    "proficiencies": [
      {
        "id": "example.proficiency.las_weapons"
      }
    ],
    "requirements": {
      "use": {
        "kind": "proficient",
        "proficiency": {
          "id": "example.proficiency.las_weapons"
        }
      }
    },
    "ammunition": {
      "accepted": [
        {
          "id": "example.ammunition.charge_pack"
        }
      ],
      "capacity": 30,
      "resource": {
        "id": "example.resource.magazine"
      }
    },
    "reload": {
      "action": {
        "id": "example.action.reload"
      },
      "amount": "full",
      "source": "inventory"
    }
  }
}
```

## Example armour

```json
{
  "schemaVersion": 1,
  "id": "example.armour.flak",
  "kind": "armour",
  "revision": 1,
  "name": "Example flak armour",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Example flak armour is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.flak",
        "heading": "Example flak armour"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "category": "light",
    "equip": {
      "slots": [
        "body"
      ],
      "hands": 0
    },
    "properties": [],
    "features": [],
    "defence": {
      "value": {
        "kind": "constant",
        "value": 12
      },
      "mode": "base",
      "stackGroup": "example.worn_defence"
    },
    "shieldCompatibility": "allowed",
    "weight": {
      "value": 5,
      "unit": "kg"
    }
  }
}
```

## Example feat

```json
{
  "schemaVersion": 1,
  "id": "example.feature.field_training",
  "kind": "feature",
  "revision": 1,
  "name": "Field training",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Field training is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.field_training",
        "heading": "Field training"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "flavor": "feat",
    "effects": [
      {
        "id": "field_movement",
        "automation": "automatic",
        "activation": "continuous",
        "target": {
          "kind": "stat",
          "scope": "self",
          "key": "movement"
        },
        "operation": "add",
        "value": {
          "kind": "constant",
          "value": 1
        },
        "duration": {
          "kind": "while_source"
        },
        "stacking": {
          "group": "example.field_movement",
          "mode": "unique_source"
        },
        "priority": 0
      }
    ],
    "grants": [],
    "manualRules": [],
    "requirements": {
      "kind": "level",
      "axis": {
        "kind": "total_level"
      },
      "operator": "gte",
      "value": 1
    },
    "repeatable": false
  }
}
```

## Example class feature

```json
{
  "schemaVersion": 1,
  "id": "example.feature.steady_hands",
  "kind": "feature",
  "revision": 1,
  "name": "Steady hands",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Steady hands is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.steady_hands",
        "heading": "Steady hands"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "flavor": "class_feature",
    "effects": [],
    "grants": [
      {
        "id": "weapon_training",
        "kind": "proficiency",
        "proficiency": {
          "id": "example.proficiency.las_weapons"
        }
      }
    ],
    "manualRules": []
  }
}
```

## Example conditional feature

```json
{
  "schemaVersion": 1,
  "id": "example.feature.two_handed_focus",
  "kind": "feature",
  "revision": 1,
  "name": "Two-handed focus",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Two-handed focus is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.two_handed_focus",
        "heading": "Two-handed focus"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "flavor": "class_feature",
    "effects": [
      {
        "id": "two_handed_damage",
        "automation": "conditional",
        "activation": "continuous",
        "target": {
          "kind": "damage",
          "scope": "attack_weapon"
        },
        "operation": "add",
        "value": {
          "kind": "constant",
          "value": 2
        },
        "duration": {
          "kind": "while_source"
        },
        "stacking": {
          "group": "example.two_handed_damage",
          "mode": "unique_source"
        },
        "priority": 0,
        "when": {
          "kind": "attack_property",
          "property": {
            "id": "example.property.two_handed"
          }
        }
      }
    ],
    "grants": [],
    "manualRules": []
  }
}
```

## Example manual feature

```json
{
  "schemaVersion": 1,
  "id": "example.feature.local_contacts",
  "kind": "feature",
  "revision": 1,
  "name": "Local contacts",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Local contacts is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.local_contacts",
        "heading": "Local contacts"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "flavor": "background_feature",
    "effects": [],
    "grants": [],
    "manualRules": [
      {
        "id": "information",
        "automation": "manual",
        "text": "Once in a qualifying scene, ask the GM for local information; no automatic success is granted.",
        "adjudicator": "gm",
        "context": "scene",
        "reason": "Narrative context or unverified rules require human adjudication."
      }
    ]
  }
}
```

## Example psychic power

```json
{
  "schemaVersion": 1,
  "id": "example.power.ward",
  "kind": "power",
  "revision": 1,
  "name": "Example ward",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Example ward is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.ward",
        "heading": "Example ward"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "discipline": {
      "id": "example.discipline.warding"
    },
    "action": {
      "id": "example.action.psychic_activation"
    },
    "duration": {
      "kind": "rounds",
      "count": 1,
      "anchor": "source_turn_end"
    },
    "outcomes": [
      {
        "id": "warded",
        "on": "success",
        "effects": [
          {
            "id": "ward_defence",
            "automation": "conditional",
            "activation": "action",
            "target": {
              "kind": "stat",
              "scope": "self",
              "key": "defence"
            },
            "operation": "add",
            "value": {
              "kind": "constant",
              "value": 1
            },
            "duration": {
              "kind": "rounds",
              "count": 1,
              "anchor": "source_turn_end"
            },
            "stacking": {
              "group": "example.ward_defence",
              "mode": "unique_source"
            },
            "priority": 0
          }
        ],
        "manualRules": []
      },
      {
        "id": "failed",
        "on": "failure",
        "effects": [],
        "manualRules": [],
        "rule": {
          "id": "example.rule.psyker"
        }
      }
    ],
    "perilsRule": {
      "id": "example.rule.perils"
    },
    "requirements": {
      "kind": "selected",
      "content": {
        "id": "example.discipline.warding"
      }
    }
  }
}
```

## Example creature

```json
{
  "schemaVersion": 1,
  "id": "example.creature.renegade",
  "kind": "creature",
  "revision": 1,
  "name": "Example renegade trooper",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Example renegade trooper is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.renegade",
        "heading": "Example renegade trooper"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "actorKind": "npc",
    "creatureType": "humanoid",
    "size": "medium",
    "movement": [
      {
        "mode": "walk",
        "speed": {
          "value": 6,
          "unit": "m"
        }
      }
    ],
    "defence": {
      "kind": "constant",
      "value": 12
    },
    "wounds": {
      "kind": "constant",
      "value": 10
    },
    "attributes": {
      "strength": 30,
      "agility": 30,
      "toughness": 30,
      "intellect": 30,
      "willpower": 30,
      "presence": 30
    },
    "skills": [
      {
        "skill": {
          "id": "example.skill.awareness"
        },
        "bonus": {
          "kind": "constant",
          "value": 2
        }
      }
    ],
    "saves": [
      {
        "attributeKey": "willpower",
        "bonus": {
          "kind": "constant",
          "value": 1
        }
      }
    ],
    "mitigations": [
      {
        "id": "example.mitigation.energy_resistance"
      }
    ],
    "features": [
      {
        "id": "example.feature.creature_watchful"
      }
    ],
    "actions": [
      {
        "id": "example.action.brace_reaction"
      },
      {
        "id": "example.action.command_special"
      }
    ],
    "resources": [
      {
        "id": "example.resource.special_budget"
      }
    ],
    "equipment": [
      {
        "id": "primary",
        "item": {
          "id": "example.weapon.lasgun"
        },
        "quantity": 1,
        "equipped": true,
        "overrides": {
          "modeId": "standard",
          "name": "Worn lasgun",
          "range": {
            "kind": "distance",
            "normal": {
              "value": 80,
              "unit": "m"
            },
            "long": {
              "value": 200,
              "unit": "m"
            }
          }
        }
      }
    ],
    "factions": [
      {
        "id": "example.faction.imperium"
      }
    ],
    "threat": {
      "scale": "example_threat",
      "value": 1,
      "label": "Placeholder"
    },
    "lore": {
      "id": "example.lore.frontier"
    }
  }
}
```

## Example vehicle

```json
{
  "schemaVersion": 1,
  "id": "example.vehicle.scout_carrier",
  "kind": "vehicle",
  "revision": 1,
  "name": "Example scout carrier",
  "summary": "Non-authoritative schema example; values require rules-owner review.",
  "descriptionMarkdown": "Example scout carrier is an illustrative fixture, not a transcription of an approved rulebook.",
  "lifecycle": "draft",
  "verification": "placeholder",
  "sources": [
    {
      "sourceId": "example.source.design",
      "sourceVersion": "proposal-1",
      "locator": {
        "sectionKey": "examples.scout_carrier",
        "heading": "Example scout carrier"
      },
      "verificationNote": "No authoritative source book was available."
    }
  ],
  "tags": [],
  "data": {
    "vehicleType": "ground",
    "size": "huge",
    "movement": [
      {
        "mode": "drive",
        "speed": {
          "value": 20,
          "unit": "m"
        }
      }
    ],
    "defence": {
      "kind": "constant",
      "value": 15
    },
    "hull": {
      "kind": "constant",
      "value": 30
    },
    "crew": [
      {
        "role": {
          "id": "example.crew_role.gunner"
        },
        "count": 1
      }
    ],
    "mounts": [
      {
        "id": "primary",
        "weapon": {
          "id": "example.weapon.lasgun"
        },
        "quantity": 1,
        "slot": "turret",
        "crewRole": {
          "id": "example.crew_role.gunner"
        },
        "arc": "front"
      }
    ],
    "systems": [
      {
        "id": "drive",
        "system": {
          "id": "example.system.drive"
        },
        "slot": "engine",
        "quantity": 1
      }
    ],
    "features": [
      {
        "id": "example.feature.vehicle_rugged"
      }
    ],
    "transportCapacity": {
      "occupants": 4,
      "cargo": {
        "value": 100,
        "unit": "kg"
      }
    },
    "damageRule": {
      "id": "example.rule.vehicle_damage"
    },
    "factions": [
      {
        "id": "example.faction.imperium"
      }
    ],
    "resources": [
      {
        "id": "example.resource.focus"
      }
    ]
  }
}
```

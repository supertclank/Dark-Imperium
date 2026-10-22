# PHB content inventory

This is the first full-book inventory pass for the selected **Version 1.0** PDF, not a certified line-by-line source review or a claim that all rules are executable. All 22 chapters were included in text/table extraction. Front matter and TOC are evidence, not duplicate entities. Section and table occurrences intentionally overlap; their count is not a count of unique game entities. Per-page text and all extracted table cells are retained privately with the original PDF.

The immutable source is registered in [sources.json](../../content/packages/di_phb_1_0/sources.json). Printed pages 1–112 correspond to PDF pages 14–125 (offset 13). Current means the file supplied by the user; global newest-version status is unverified. `(2)` is a download suffix, not an edition. Source SHA-256: `a58335b1264ac40e30ff0b310626d306fc88f7003e0c3af345e0d55c978e94b7`.

The existing content contracts were followed: JSON, `di.<kind>.<key>` permanent IDs, one entity per file, embedded effects/ManualRule, generic choices/progressions and source citations. There is no ACTIONS.md in the existing specification; action contracts are in DOMAIN_SCHEMAS and DICE_ROLLING. Existing `example.*` fixtures and development seed data remain separate and unchanged.

## Category coverage

| Category | Discovered content / inspection outcome | Conversion state |
| --- | --- | --- |
| Character creation | 9 ordered steps; default standard array 15,14,13,12,10,8; usually start level3; supported levels1–20; HP fixed values; proficiency table | Source rules transcribed; missing foundational policies block playable profile |
| Species | Human, Ogryn, Ratling, Skitarii, Kin, Aeldari | All 6 draft species; fixed bonuses/speed and some choices structured; remaining traits/manual restrictions retained |
| Origins/backgrounds | Hiveborn, Shrine Worlder, Penal Worlder, Voidborn, Forge World, Schola Progenium, Militarum Regiment, Underhive, Craftworld/Outcast, Mining Hold/Guild | All10 draft backgrounds and skill choices; six eligibility conflicts |
| Classes | All12 classes in sections11.1–11.12 | All12 draft classes; 240 level rows; class training/complex features mostly manual |
| Subclasses | 45 named specializations across twelve classes, including 6 Psyker disciplines and 6 Skitarii protocols | Veteran3 mapped; remaining42 reserved candidates |
| Skills | 15 named skills in2.5; Vehicles separately defined as a proficiency in21.1 | 15 skills and corresponding skill proficiencies; Vehicles remains source procedure |
| Universal Traits | 20 creation traits | All transcribed as shared features; Twitchy +2 initiative is structured |
| Talents/feats | 20 general and30 species-restricted Talents | 50 feat-flavored features; prerequisites/complex mechanics manual pending mapping |
| Weapons | 84 chapter8 profiles; 13 mounted table rows, 3 reusing existing names; 7 chapter10 grenades; additional high-tier wargear in18.14 | Known dice/ranges/property references staged; unresolved required fields excluded from canonical entities |
| Armour/shields/fields | 31 chapter9 rows, including Shield/Slab Shield/Brute Shield Harness and reactive fields | Ogryn Leathers and Shield are explicit canonical slice; others quarantined |
| Armour modifications | 24 upgrades across general/Ogryn/Skitarii/Kin/Aeldari groups | System candidates; no fictional armour-property glossary invented |
| Equipment | 12 mission supplies,22 augmetics,7 specialist ammunition types,9 weapon modifications,9 masterwork traits,8 vehicle upgrades; exotic/archeotech/relic/unique entries retained | Named candidate IDs and exact source rows; class-issued narrative kit unresolved |
| Conditions/states | 15 named rows plus Exhaustion; Bloodied is explicitly a state | 16 candidates; source wording preserved |
| Damage types | Bludgeoning,piercing,slashing,radiant,fire,poison,thunder,force,psychic,lightning,radiation,necrotic | 12 vocabulary records; no invented mitigation semantics |
| Weapon properties | 31 glossary rows | 31 property records, Reload/Versatile parameters; special effects manual |
| Actions/reactions | 9 generic actions; opportunity attacks/grapple/shove; class/item/psyker reactions; 6 vehicle action rows plus ram/chase procedures | Inventory and source rules; only2 isolated base-damage templates in canonical actions |
| Rests | Short Rest >=1h, Long Rest >=8h; source recovery and limits | Manual rest rule preserved; no automatic recharge implemented |
| Psychic content | 14 Minor,18 Standard,12 Major,8 Warlock Rune powers; multiple access tags; two known-power progressions | 52 power candidates, costs/tables in evidence; no invented discipline assignments |
| Random tables | Standard/Aeldari/Malefic Perils, d8 injuries, d6 breakdowns, corruption track | Complete table evidence and manual rules; variable-roll/open-bound handling pending |
| Vehicles | 12 complete source profiles, crew/stations,DT,Handling,cargo,mounts,modifications | Numeric base candidates and exact full profile evidence |
| Core rules | Combat,cover,suppression,critical,death,healing,advancement,requisition,maintenance,corruption,vehicle procedures | Numbered section inventory and manual rule records; source gaps in review report |

## Status meaning

READY means the represented draft structure is ready for technical/source review, not published or fully automated. MANUAL_RULE preserves an adjudicated or not-yet-automated clause. AMBIGUOUS, MISSING_REFERENCE, DUPLICATE_OR_CONFLICT and SPEC_EXTENSION_REQUIRED identify open work. Coverage is separate: STRUCTURED, PARTIALLY_STRUCTURED, MANUAL_ONLY or NOT_YET_IMPORTED. Missing fields remain missing in review candidates; those files are not canonical entities and cannot be loaded by the importer.

Permanent identity allocations are in [CONTENT_MANIFEST.json](../../content/CONTENT_MANIFEST.json). The [machine inventory](../../content/packages/di_phb_1_0/review/inventory.json) contains source cells and exact locators. The following ledger includes every extracted section/table occurrence plus canonical draft/candidate records. It is intentionally repetitive so a future reviewer can reconcile source occurrences without silently merging duplicate-looking names.

## Item ledger

| Inventory identity | Category / name | Printed / PDF page | Status | Coverage |
| --- | --- | --- | --- | --- |
| section_1_1_p15 | section / Design Goals | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_1_2_p15 | section / Core System | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_1_3_p15 | section / Character Tiers | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_1_4_p15 | section / Proficiency Bonus | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_1_5_p15 | section / Rules Priority | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_1_p17 | section / Ability Scores | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_2_p17 | section / Hit Points | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_3_p17 | section / Species and Class Restrictions | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_3_1_p17 | section / Class at a Glance | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_p17 | section / Hard Restrictions | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_1_p17 | section / Ogryns | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_2_p17 | section / Skitarii | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_3_p17 | section / Psykers | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_4_p17 | section / Ratlings | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_5_p18 | section / Squats / Kin | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_4_6_p18 | section / Aeldari / Eldar | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_2_5_p18 | section / Skills and Ability Checks | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_1_p20 | section / Human | 7 / 20 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_1_p23 | section / Human | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_2_p20 | section / Ogryn Abhuman | 7 / 20 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_2_p23 | section / Ogryn Abhuman | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_3_p21 | section / Ratling Abhuman | 8 / 21 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_3_p23 | section / Ratling Abhuman | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_4_p21 | section / Skitarii Augmented Human | 8 / 21 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_4_p23 | section / Skitarii Augmented Human | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_5_p22 | section / Squat / Kin | 9 / 22 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_5_p24 | section / Squat / Kin | 11 / 24 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_6_p22 | section / Aeldari / Eldar | 9 / 22 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_6_p24 | section / Aeldari / Eldar | 11 / 24 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_1_1_p23 | section / Human Traits | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_2_1_p23 | section / Ogryn Traits | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_3_1_p23 | section / Ratling Traits | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_4_1_p23 | section / Skitarii Traits | 10 / 23 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_5_1_p24 | section / Squat / Kin Traits | 11 / 24 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_3_6_1_p24 | section / Aeldari Traits | 11 / 24 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_1_p26 | section / Hiveborn | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_2_p26 | section / Shrine Worlder | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_3_p26 | section / Penal Worlder | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_4_p26 | section / Voidborn | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_5_p26 | section / Forge World | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_6_p26 | section / Schola Progenium | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_7_p27 | section / Militarum Regiment | 14 / 27 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_8_p27 | section / Underhive | 14 / 27 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_9_p27 | section / Craftworld / Outcast | 14 / 27 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_4_10_p27 | section / Mining Hold / Guild | 14 / 27 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_1_p31 | section / Turns and Actions | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_2_p31 | section / Cover | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_3_p31 | section / Suppression | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_4_p31 | section / Reload | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_5_p31 | section / Close-Quarters Shooting | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_6_p31 | section / Critical Hits | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_7_p31 | section / Dropping to 0 Hit Points | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_8_p31 | section / Stabilising and Recovery | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_9_p31 | section / Ranged Attacks and Range | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_10_p32 | section / Opportunity Attacks | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_11_p32 | section / Grappling and Shoving | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_12_p32 | section / Two-Weapon Fighting | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_13_p32 | section / Rest and Recovery | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_6_14_p32 | section / Conditions and Battlefield States | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_1_p37 | section / Imperial Ranged Weapons | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_2_p38 | section / Imperial Melee Weapons | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_3_p38 | section / Ogryn Weapons | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_4_p40 | section / Squat / Kin Weapons | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_5_p40 | section / Aeldari Weapons | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_8_6_p40 | section / Mechanicus Weapons | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_1_p42 | section / General and Imperial Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_2_p42 | section / Ogryn Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_3_p42 | section / Squat / Kin Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_4_p42 | section / Aeldari Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_5_p44 | section / Armour Modifications | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_6_p44 | section / Ogryn Armour Modifications | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_7_p44 | section / Skitarii Armour Modifications | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_8_p45 | section / Kin Armour Modifications | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_9_9_p45 | section / Aeldari Armour Modifications | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_10_1_p47 | section / Throwing Grenades | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_p50 | section / Veteran | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_1_p50 | section / Guardsman Training | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_2_p50 | section / Tactical Aim | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_3_p50 | section / Suppressing Fire | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_4_p50 | section / Regimental Doctrine | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_5_p50 | section / Extra Attack | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_6_p50 | section / Fire Team Veteran | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_7_p50 | section / Doctrine Feature | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_9_p50 | section / Hold the Line | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_10_p50 | section / Killing Zone | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_11_p51 | section / Veteran’s Accuracy | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_13_p51 | section / Battlefield Instinct | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_14_p51 | section / Improved Doctrine | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_15_p51 | section / Kill Confirmed | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_17_p51 | section / Veteran’s Command | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_18_p51 | section / Dug-In Kill Team | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_1_20_p51 | section / Lord Castellan’s Moment | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_p53 | section / Zealot | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_1_p53 | section / Fury of Faith | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_2_p53 | section / Martyr’s Endurance | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_3_p53 | section / Martyr’s Mercy | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_4_p53 | section / Charge of Conviction | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_5_p53 | section / Sacred Path | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_6_p53 | section / Extra Attack | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_7_p53 | section / Blood and Benediction | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_8_p53 | section / Sacred Path Feature | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_9_p53 | section / Refuse the Dark | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_10_p53 | section / Sainted Fury | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_11_p53 | section / Martyr’s Renewal | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_13_p53 | section / Unbroken Creed | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_14_p54 | section / Sacred Path Feature | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_15_p54 | section / Living Saint’s Shadow | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_17_p54 | section / Martyrdom Unending | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_18_p54 | section / Sacred Path Ascendant | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_2_20_p54 | section / Living Icon of Wrath | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_p56 | section / Psyker | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_1_p56 | section / Psychic Discipline | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_2_p56 | section / Psychic Ward | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_3_p56 | section / Discipline Feature | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_5_p57 | section / Empowered Manifestation | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_6_p57 | section / Disciplined Channel | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_7_p57 | section / Discipline Feature | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_9_p57 | section / Warp Anchor | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_10_p57 | section / Mastered Manifestation | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_11_p57 | section / Major Power Access | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_13_p57 | section / Sanctioned Focus | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_14_p57 | section / Discipline Feature | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_15_p57 | section / Alpha-Level Risk | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_17_p57 | section / Soul-Bound Discipline | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_18_p57 | section / Warp-Crowned Focus | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_3_20_p57 | section / Sanctioned Apex | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_p59 | section / Ogryn Skullbreaker | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_1_p59 | section / Big Lad | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_2_p59 | section / Loyal Protector | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_3_p59 | section / Brutal Impact | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_4_p59 | section / Ogryn Role | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_5_p59 | section / Extra Attack | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_6_p59 | section / Too Stubborn to Drop | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_7_p59 | section / Role Feature | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_9_p59 | section / Living Barricade | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_10_p59 | section / Thunderous Violence | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_11_p59 | section / Bigger and Meaner | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_13_p60 | section / Can’t Keep Him Down | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_14_p60 | section / Role Feature | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_15_p60 | section / Walking Fortress | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_17_p60 | section / Mountain of Muscle | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_18_p60 | section / Role Feature | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_4_20_p60 | section / Unkillable Big Lad | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_p62 | section / Arbites Enforcer | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_1_p62 | section / Enforcer Training | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_2_p62 | section / Authority | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_3_p62 | section / Breach and Clear | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_4_p62 | section / Enforcement Doctrine | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_5_p62 | section / Extra Attack | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_6_p62 | section / Lockdown Order | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_7_p62 | section / Doctrine Feature | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_9_p62 | section / No Escape | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_10_p62 | section / Judgement Protocol | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_11_p62 | section / Riot Control | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_13_p62 | section / Legal Terror | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_14_p63 | section / Doctrine Feature | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_15_p63 | section / Sentence Executed | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_17_p63 | section / Absolute Jurisdiction | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_18_p63 | section / Doctrine Feature | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_5_20_p63 | section / Final Sentence | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_p65 | section / Hive Scum | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_1_p65 | section / Dirty Fighter | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_2_p65 | section / Streetwise | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_3_p65 | section / Cunning Action | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_4_p65 | section / Gang Style | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_5_p65 | section / Backstabber | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_6_p65 | section / Low Cunning | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_7_p65 | section / Gang Style Feature | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_9_p65 | section / Vanish into Trouble | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_10_p65 | section / Knife-Edge Survivor | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_13_p65 | section / Underhive Reputation | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_14_p65 | section / Gang Style Feature | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_17_p66 | section / No Honour, No Problem | 53 / 66 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_18_p66 | section / Backstabber +6d6 | 53 / 66 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_6_20_p66 | section / King of the Underhive | 53 / 66 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_p68 | section / Ratling Sharpshooter | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_1_p68 | section / Small Target | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_2_p68 | section / Deadeye | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_3_p68 | section / Scamper | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_4_p68 | section / Ratling Trick | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_5_p68 | section / Killshot | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_6_p68 | section / Cameleoline Habits | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_7_p68 | section / Ratling Trick Feature | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_9_p68 | section / Impossible Angle | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_10_p68 | section / Perfect Shot | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_13_p68 | section / Gone Before the Shot | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_14_p68 | section / Ratling Trick Feature | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_15_p69 | section / Ghost Marksman | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_17_p69 | section / Deadeye +4d6 | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_18_p69 | section / Ratling Trick Feature | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_7_20_p69 | section / Impossible Little Legend | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_p71 | section / Skitarii Veteran | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_1_p71 | section / Machine Focus | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_2_p71 | section / Targeting Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_3_p71 | section / Augmetic Reflexes | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_4_p71 | section / Combat Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_5_p71 | section / Extra Attack | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_6_p71 | section / Doctrinal Subroutine | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_7_p71 | section / Protocol Feature | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_9_p71 | section / Blessed Autosenses | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_10_p72 | section / Omnissian Execution | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_11_p72 | section / Calculated Volley | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_13_p72 | section / Redundant Systems | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_14_p72 | section / Protocol Feature | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_15_p72 | section / Will of the Omnissiah | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_17_p72 | section / Perfect Targeting Logic | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_18_p72 | section / Protocol Feature | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_8_20_p72 | section / Living Instrument of the Omnissiah | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_p74 | section / Kin Armsman | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_1_p74 | section / Kin Training | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_2_p74 | section / Oath-Mark | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_3_p74 | section / Steady Advance | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_4_p74 | section / Hold Doctrine | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_5_p74 | section / Extra Attack | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_6_p74 | section / Grudge Settled | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_7_p74 | section / Doctrine Feature | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_9_p74 | section / Void-Hardened Line | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_10_p74 | section / Ancestral Wrath | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_11_p74 | section / Kinfire Drill | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_13_p74 | section / Iron Compact | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_14_p75 | section / Doctrine Feature | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_15_p75 | section / Holdfast Champion | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_17_p75 | section / Grudge-Bound Advance | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_18_p75 | section / Doctrine Feature | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_9_20_p75 | section / Ancestor-Core Champion | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_p77 | section / Hernkyn Prospector | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_1_p77 | section / Prospector Training | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_2_p77 | section / Claim Sight | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_3_p77 | section / Surveyor’s Step | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_4_p77 | section / Expedition Role | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_5_p77 | section / Extra Attack | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_6_p77 | section / Mark the Seam | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_7_p77 | section / Expedition Feature | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_9_p77 | section / Outrider’s Escape | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_10_p77 | section / Perfect Claim | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_11_p77 | section / Deep Scan | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_13_p77 | section / No Stone Unturned | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_14_p78 | section / Expedition Feature | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_15_p78 | section / Master Prospector | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_17_p78 | section / Legendary Claim-Staker | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_18_p78 | section / Expedition Feature | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_10_20_p78 | section / Claim the Horizon | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_p80 | section / Aeldari Outcast | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_1_p80 | section / Ranger Training | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_2_p80 | section / Shuriken Grace | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_3_p80 | section / Ghostwalk | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_4_p80 | section / Outcast Path | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_5_p80 | section / Extra Attack | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_6_p80 | section / Unseen Shot | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_7_p80 | section / Path Feature | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_9_p80 | section / Webway Instinct | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_10_p80 | section / Death from Elsewhere | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_11_p80 | section / Perfect Motion | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_13_p80 | section / Vanish Beyond Sight | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_14_p80 | section / Path Feature | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_15_p80 | section / Mythic Outcast | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_17_p81 | section / Pathless Perfection | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_18_p81 | section / Path Feature | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_11_20_p81 | section / Legend of the Wandering Path | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_p83 | section / Aeldari Warlock | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_1_p83 | section / Runes of Battle | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_2_p83 | section / Witchblade Training | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_3_p83 | section / Rune Ward | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_4_p83 | section / Warlock Path | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_5_p83 | section / Empowered Rune | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_6_p83 | section / Battle-Seer | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_7_p83 | section / Path Feature | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_9_p84 | section / Ghosthelm Discipline | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_10_p84 | section / War-Rune Mastery | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_11_p84 | section / Major Rune Access | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_13_p84 | section / Fate Splitter | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_14_p84 | section / Path Feature | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_15_p84 | section / Storm of Runes | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_17_p84 | section / Spirit-Rune Focus | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_18_p84 | section / Path Feature | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_11_12_20_p84 | section / Farseer’s Echo | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_12_1_p86 | section / General Talents | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_12_2_p87 | section / Species-Restricted Talents | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_1_p91 | section / Psychic Save DC | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_2_p91 | section / Psychic Attack Modifier | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_3_p91 | section / Known Powers | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_4_p91 | section / Psychic Power Cost and Empowered Powers | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_5_p91 | section / Minor Psychic Powers | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_6_p92 | section / Standard Psychic Powers | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_7_p93 | section / Major Psychic Powers | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_14_8_p93 | section / Warlock Rune Powers | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_1_p95 | section / Warp Pressure | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_2_p95 | section / Reducing Warp Pressure | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_3_p95 | section / Perils Severity | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_p95 | section / Perils Effects | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_1_p95 | section / Warp Static | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_2_p95 | section / Bleeding Eyes | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_3_p95 | section / Soul Echo | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_4_p95 | section / Warp Scream | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_5_p95 | section / Possession Pressure | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_6_p95 | section / Uncontrolled Manifestation | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_7_p95 | section / Reality Tear | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_4_8_p95 | section / Catastrophic Perils | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_5_p95 | section / After Perils | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_6_p96 | section / Aeldari Warlock Perils | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_15_7_p96 | section / Malefic-Touched Perils | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_16_1_p98 | section / Gaining Corruption | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_16_2_p98 | section / Corruption Track | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_16_3_p98 | section / Corruption Scars | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_16_4_p98 | section / Reducing Corruption | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_17_1_p100 | section / Class Equipment Packages | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_17_2_p101 | section / Mission Items and Supplies | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_1_p103 | section / Availability | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_2_p103 | section / Requisition Test | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_3_p103 | section / Requisition Outcomes | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_4_p103 | section / Xenos, Forbidden and Black-Market Gear | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_5_p103 | section / Provenance and Faction Access | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_6_p104 | section / Equipment by Character Tier | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_7_p104 | section / Weapon Modifications | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_8_p104 | section / Master-Crafted Wargear | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_9_p105 | section / Specialist Ammunition and Charges | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_10_p105 | section / Salvage and Captured Equipment | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_11_p105 | section / Item Condition and Repair | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_12_p106 | section / Replacing Lost or Destroyed Equipment | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_13_p106 | section / Trading, Gifts and Ownership | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_p106 | section / Exotic, Relic and Unique Wargear | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_1_p106 | section / Signature Wargear | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_2_p106 | section / Exotic Wargear | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_3_p107 | section / Archeotech | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_4_p107 | section / Faction Relics | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_5_p108 | section / Unique Wargear | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_18_14_6_p108 | section / Creating Additional Relics | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_19_1_p110 | section / When to Use a Lasting Injury | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_19_2_p110 | section / Lasting Injury Table | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_19_3_p110 | section / Medical Care | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_19_4_p110 | section / Augmetic Replacement | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_20_1_p112 | section / When You Gain a Level | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_20_2_p112 | section / Retraining | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_1_p114 | section / Profiles and Crew | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_2_p114 | section / Driving and Movement | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_3_p115 | section / Actions and Attacks | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_4_p115 | section / Collisions | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_5_p116 | section / Hull Damage and Breakdowns | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_6_p116 | section / Boarding and Disembarking | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_7_p117 | section / Chases | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_8_p117 | section / Repairs and Resupply | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_9_p118 | section / Requisition and Modifications | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_10_p119 | section / Civilian and Imperial Scouts | 106 / 119 | MANUAL_RULE | NOT_YET_IMPORTED |
| section_21_11_p121 | section / Weapon Profiles | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_001_row_001 | Tier / Tier 1 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_001_row_002 | Tier / Tier 2 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_001_row_003 | Tier / Tier 3 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_001_row_004 | Tier / Tier 4 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_002_row_001 | Levels / 1-4 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_002_row_002 | Levels / 5-8 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_002_row_003 | Levels / 9-12 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_002_row_004 | Levels / 13-16 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_002_row_005 | Levels / 17-20 | 2 / 15 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_001 | Species / Human | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_002 | Species / Ogryn | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_003 | Species / Ratling | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_004 | Species / Skitarii | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_005 | Species / Squat / Kin | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_003_row_006 | Species / Aeldari / Eldar | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_001 | Class / Veteran | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_002 | Class / Zealot | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_003 | Class / Psyker | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_004 | Class / Ogryn Skullbreaker | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_005 | Class / Arbites Enforcer | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_006 | Class / Hive Scum | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_007 | Class / Ratling Sharpshooter | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_008 | Class / Skitarii Veteran | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_009 | Class / Kin Armsman | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_010 | Class / Hernkyn Prospector | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_011 | Class / Aeldari Outcast | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_004_row_012 | Class / Aeldari Warlock | 4 / 17 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_005_row_001 | Skill / Survival | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_005_row_002 | Skill / Technology | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_001 | Skill / Acrobatics | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_002 | Skill / Athletics | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_003 | Skill / Investigation | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_004 | Skill / Medicine | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_005 | Skill / Perception | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_006_row_006 | Skill / Stealth | 5 / 18 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_001 | Origin / Hiveborn | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_002 | Origin / Shrine Worlder | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_003 | Origin / Penal Worlder | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_004 | Origin / Voidborn | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_005 | Origin / Forge World | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_006 | Origin / Schola Progenium | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_007 | Origin / Militarum Regiment | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_008 | Origin / Underhive | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_009 | Origin / Craftworld / Outcast | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_007_row_010 | Origin / Mining Hold / Guild | 13 / 26 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_001 | Trait / Faithful | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_002 | Trait / Jaded | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_003 | Trait / Twitchy | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_004 | Trait / Unnaturally Lucky | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_005 | Trait / Augmetic Scarred | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_006 | Trait / Chem-Hardened | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_007 | Trait / Devoted Servant | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_008 | Trait / Touched by the Warp | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_009 | Trait / Hive Survivor | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_010 | Trait / Munitorum Drilled | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_011 | Trait / Iron Nerves | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_012 | Trait / Faith in Steel | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_013 | Trait / Dirty Pragmatist | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_014 | Trait / Vox Familiar | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_015 | Trait / Grudge-Bearer | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_016 | Trait / Hard to Kill | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_017 | Trait / Knife in the Boot | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_018 | Trait / Field Chirurgeon | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_019 | Trait / Black-Market Eye | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_008_row_020 | Trait / Litany-Marked | 16 / 29 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_001 | Common Action / Attack | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_002 | Common Action / Dash | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_003 | Common Action / Disengage | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_004 | Common Action / Dodge | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_005 | Common Action / Help | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_006 | Common Action / Hide | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_007 | Common Action / Ready | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_008 | Common Action / Reload | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_009_row_009 | Common Action / Use Mission Gear | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_010_row_001 | Cover / Light Cover | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_010_row_002 | Cover / Heavy Cover | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_010_row_003 | Cover / Full Cover | 18 / 31 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_011_row_001 | Maneuver / Grapple | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_011_row_002 | Maneuver / Escape | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_011_row_003 | Maneuver / Move a Grappled Target | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_011_row_004 | Maneuver / Shove | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_012_row_001 | Rest / Short Rest | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_012_row_002 | Rest / Long Rest | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_001 | Condition / State / Blinded | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_002 | Condition / State / Bloodied | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_003 | Condition / State / Charmed | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_004 | Condition / State / Frightened | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_005 | Condition / State / Grappled | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_006 | Condition / State / Hidden | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_007 | Condition / State / Incapacitated | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_008 | Condition / State / Invisible | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_013_row_009 | Condition / State / Poisoned | 19 / 32 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_001 | Condition / State / Prone | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_002 | Condition / State / Restrained | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_003 | Condition / State / Stunned | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_004 | Condition / State / Suppressed | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_005 | Condition / State / Surprised | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_014_row_006 | Condition / State / Unconscious | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_001 | Level / 1 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_002 | Level / 2 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_003 | Level / 3 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_004 | Level / 4 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_005 | Level / 5 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_015_row_006 | Level / 6 | 20 / 33 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_001 | Property / Accurate | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_002 | Property / Armour-Breaking | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_003 | Property / Beam | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_004 | Property / Blast | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_005 | Property / Brutal | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_006 | Property / Burst | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_007 | Property / Chain | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_008 | Property / Close-Quarters | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_009 | Property / Emplaced | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_010 | Property / Entangling | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_011 | Property / Finesse | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_012 | Property / Focus | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_013 | Property / Heavy | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_014 | Property / Industrial | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_015 | Property / Light | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_016 | Property / Mechanicus | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_017 | Property / Monomolecular | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_018 | Property / Ogryn | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_019 | Property / Overheat | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_020 | Property / Power Field | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_021 | Property / Psyker | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_022 | Property / Reload X | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_023 | Property / Shield | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_024 | Property / Shock | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_025 | Property / Silent | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_026 | Property / Spray | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_027 | Property / Spirit Weapon | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_028 | Property / Suppression | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_029 | Property / Thrown | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_030 | Property / Twin-Linked | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_016_row_031 | Property / Versatile X | 22 / 35 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_001 | Weapon / Stub Pistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_002 | Weapon / Laspistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_003 | Weapon / Autopistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_004 | Weapon / Hand Cannon | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_005 | Weapon / Bolt Pistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_006 | Weapon / Plasma Pistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_007 | Weapon / Melta Pistol | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_008 | Weapon / Stub Rifle | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_009 | Weapon / Lascarbine | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_010 | Weapon / Lasgun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_011 | Weapon / Hot-Shot Lasgun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_012 | Weapon / Autogun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_013 | Weapon / Shotgun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_014 | Weapon / Combat Shotgun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_015 | Weapon / Long-Las | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_016 | Weapon / Needle Rifle | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_017 | Weapon / Bolter | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_018 | Weapon / Combi-Bolter | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_019 | Weapon / Flamer | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_020 | Weapon / Plasma Gun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_021 | Weapon / Meltagun | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_022 | Weapon / Grenade Launcher | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_023 | Weapon / Heavy Stubber | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_024 | Weapon / Heavy Bolter | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_017_row_025 | Weapon / Multi-Laser | 24 / 37 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_001 | Weapon / Knife | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_002 | Weapon / Combat Blade | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_003 | Weapon / Trench Club | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_004 | Weapon / Maul | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_005 | Weapon / Shock Maul | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_006 | Weapon / Chain Knife | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_007 | Weapon / Chainsword | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_008 | Weapon / Heavy Chainsword | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_009 | Weapon / Power Sword | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_010 | Weapon / Power Axe | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_011 | Weapon / Power Maul | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_012 | Weapon / Thunder Hammer | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_013 | Weapon / Force Sword | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_014 | Weapon / Force Staff | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_015 | Weapon / Omnissian Axe | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_016 | Weapon / Relic Blade | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_018_row_017 | Weapon / Heavy Axe | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_001 | Weapon / Ripper Gun | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_002 | Weapon / Kickback Shotgun | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_003 | Weapon / Grenadier Gauntlet | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_004 | Weapon / Twin-Linked Heavy Stubber | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_005 | Weapon / Ogryn Club | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_006 | Weapon / Big Friendly Rock | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_007 | Weapon / Brute Shield Bash | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_008 | Weapon / Power Maul, Ogryn Pattern | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_009 | Weapon / Industrial Cutter | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_019_row_010 | Weapon / Slab Hammer | 25 / 38 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_001 | Weapon / Autoch-Pattern Pistol | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_002 | Weapon / Bolt Revolver | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_003 | Weapon / Ion Pistol | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_004 | Weapon / Autoch-Pattern Bolter | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_005 | Weapon / Ion Blaster | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_006 | Weapon / Magna-Rail Rifle | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_007 | Weapon / Plasma Beamer | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_008 | Weapon / EtaCarn Mining Tool | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_009 | Weapon / Concussion Hammer | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_010 | Weapon / Kin Power Axe | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_011 | Weapon / Plasma Axe | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_020_row_012 | Weapon / Concussion Gauntlet | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_001 | Weapon / Shuriken Pistol | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_002 | Weapon / Shuriken Catapult | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_003 | Weapon / Ranger Long Rifle | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_004 | Weapon / Aeldari Lasblaster | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_005 | Weapon / Fusion Gun | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_006 | Weapon / Death Spinner | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_007 | Weapon / Witchblade | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_008 | Weapon / Singing Spear | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_009 | Weapon / Aeldari Power Sword | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_010 | Weapon / Monomolecular Blade | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_011 | Weapon / Corsair Sabre | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_012 | Weapon / Star Glaive | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_013 | Weapon / Ghostsword | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_014 | Weapon / Biting Blade | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_021_row_015 | Weapon / Executioner Blade | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_022_row_001 | Weapon / Galvanic Rifle | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_022_row_002 | Weapon / Radium Carbine | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_022_row_003 | Weapon / Arc Pistol | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_022_row_004 | Weapon / Arc Rifle | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_022_row_005 | Weapon / Taser Goad | 27 / 40 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_001 | Armour / Heavy Clothing | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_002 | Armour / Armoured Bodyglove | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_003 | Armour / Flak Vest | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_004 | Armour / Flak Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_005 | Armour / Flak Greatcoat | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_006 | Armour / Mesh Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_007 | Armour / Scout Carapace | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_008 | Armour / Carapace Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_009 | Armour / Riot Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_010 | Armour / Void Suit, Armoured | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_011 | Armour / Hazard Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_012 | Armour / Powered Carapace | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_013 | Armour / Shield | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_014 | Armour / Refractor Field | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_023_row_015 | Armour / Conversion Field | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_001 | Armour / Ogryn Leathers | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_002 | Armour / Ogryn Flak Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_003 | Armour / Ogryn Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_004 | Armour / Bullgryn Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_005 | Armour / Slab Shield | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_024_row_006 | Armour / Brute Shield Harness | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_025_row_001 | Armour / Kin Void Suit | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_025_row_002 | Armour / Kin Mesh | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_025_row_003 | Armour / Hearthkyn Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_025_row_004 | Armour / Exo-Frame Plate | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_025_row_005 | Armour / Prospector Rig | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_026_row_001 | Armour / Aeldari Mesh | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_026_row_002 | Armour / Ranger Weave | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_026_row_003 | Armour / Rune Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_026_row_004 | Armour / Aspect-Pattern Armour | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_026_row_005 | Armour / Holo-Field Cloak | 29 / 42 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_001 | Modification / Reinforced Plates | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_002 | Modification / Sealed System | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_003 | Modification / Camo Weave | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_004 | Modification / Shock Insulation | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_005 | Modification / Mag Boots / Anchor Rig | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_006 | Modification / Medicae Harness | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_007 | Modification / Servo Assist | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_027_row_008 | Modification / Hexagrammic Lining | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_028_row_001 | Modification / Reinforced Harness | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_028_row_002 | Modification / Slab-Lock Bracing | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_028_row_003 | Modification / Recoil Yoke | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_028_row_004 | Modification / Blast Baffles | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_029_row_001 | Modification / Ablative Ceramite | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_029_row_002 | Modification / Rad-Seal Shrouds | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_029_row_003 | Modification / Servo-Bracing | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_029_row_004 | Modification / Noospheric Armour Link | 31 / 44 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_030_row_001 | Modification / Void-Seal Redundancy | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_030_row_002 | Modification / Grav-Anchor Spurs | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_030_row_003 | Modification / Ancestor-Wrought Plating | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_030_row_004 | Modification / Exo-Servo Overdrive | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_031_row_001 | Modification / Holo-Weave Matrix | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_031_row_002 | Modification / Spirit-Stone Lattice | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_031_row_003 | Modification / Adaptive Weave | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_031_row_004 | Modification / Ghostplate Flexors | 32 / 45 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_001 | Grenade / Frag Grenade | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_002 | Grenade / Frag Bomb | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_003 | Grenade / Krak Grenade | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_004 | Grenade / Smoke Grenade | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_005 | Grenade / Stun Grenade | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_006 | Grenade / Firebomb | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_032_row_007 | Grenade / Rad Grenade | 34 / 47 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_001 | Level / 1 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_002 | Level / 2 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_003 | Level / 3 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_004 | Level / 4 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_005 | Level / 5 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_006 | Level / 6 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_007 | Level / 7 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_008 | Level / 8 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_009 | Level / 9 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_010 | Level / 10 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_011 | Level / 11 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_012 | Level / 12 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_013 | Level / 13 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_014 | Level / 14 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_015 | Level / 15 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_016 | Level / 16 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_017 | Level / 17 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_018 | Level / 18 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_019 | Level / 19 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_033_row_020 | Level / 20 | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_034_row_001 | Doctrine / Shock Trooper | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_034_row_002 | Doctrine / Marksman | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_034_row_003 | Doctrine / Sergeant | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_035_row_001 | Doctrine / Shock Trooper | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_035_row_002 | Doctrine / Marksman | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_035_row_003 | Doctrine / Sergeant | 37 / 50 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_036_row_001 | Doctrine / Shock Trooper | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_036_row_002 | Doctrine / Marksman | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_036_row_003 | Doctrine / Sergeant | 38 / 51 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_001 | Level / 1 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_002 | Level / 2 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_003 | Level / 3 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_004 | Level / 4 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_005 | Level / 5 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_006 | Level / 6 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_007 | Level / 7 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_008 | Level / 8 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_009 | Level / 9 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_010 | Level / 10 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_011 | Level / 11 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_012 | Level / 12 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_013 | Level / 13 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_014 | Level / 14 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_015 | Level / 15 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_016 | Level / 16 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_017 | Level / 17 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_018 | Level / 18 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_019 | Level / 19 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_037_row_020 | Level / 20 | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_038_row_001 | Sacred Path / Preacher | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_038_row_002 | Sacred Path / Flagellant | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_038_row_003 | Sacred Path / Purifier | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_039_row_001 | Path / Preacher | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_039_row_002 | Path / Flagellant | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_039_row_003 | Path / Purifier | 40 / 53 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_040_row_001 | Sacred Path / Preacher | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_040_row_002 | Sacred Path / Flagellant | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_040_row_003 | Sacred Path / Purifier | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_041_row_001 | Sacred Path / Preacher | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_041_row_002 | Sacred Path / Flagellant | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_041_row_003 | Sacred Path / Purifier | 41 / 54 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_001 | Level / 1 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_002 | Level / 2 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_003 | Level / 3 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_004 | Level / 4 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_005 | Level / 5 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_006 | Level / 6 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_007 | Level / 7 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_008 | Level / 8 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_009 | Level / 9 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_010 | Level / 10 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_011 | Level / 11 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_012 | Level / 12 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_013 | Level / 13 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_014 | Level / 14 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_015 | Level / 15 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_016 | Level / 16 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_017 | Level / 17 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_018 | Level / 18 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_019 | Level / 19 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_042_row_020 | Level / 20 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_001 | Discipline / Biomancer | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_002 | Discipline / Telekine | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_003 | Discipline / Diviner | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_004 | Discipline / Pyromancer | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_005 | Discipline / Malefic- Touched | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_043_row_006 | Discipline / Blank / Null- Bound | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_001 | Level / 1 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_002 | Level / 2 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_003 | Level / 3 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_004 | Level / 4 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_005 | Level / 5 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_006 | Level / 6 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_007 | Level / 7 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_008 | Level / 8 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_009 | Level / 9 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_010 | Level / 10 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_011 | Level / 11 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_012 | Level / 12 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_013 | Level / 13 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_014 | Level / 14 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_015 | Level / 15 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_016 | Level / 16 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_017 | Level / 17 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_018 | Level / 18 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_019 | Level / 19 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_044_row_020 | Level / 20 | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_045_row_001 | Discipline / Biomancer | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_045_row_002 | Discipline / Telekine | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_045_row_003 | Discipline / Diviner | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_045_row_004 | Discipline / Pyromancer | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_045_row_005 | Discipline / Malefic-Touched | 43 / 56 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_046_row_001 | Discipline / Blank / Null-Bound | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_001 | Discipline / Biomancer | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_002 | Discipline / Telekine | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_003 | Discipline / Diviner | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_004 | Discipline / Pyromancer | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_005 | Discipline / Malefic-Touched | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_047_row_006 | Discipline / Blank / Null- Bound | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_001 | Discipline / Biomancer | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_002 | Discipline / Telekine | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_003 | Discipline / Diviner | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_004 | Discipline / Pyromancer | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_005 | Discipline / Malefic-Touched | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_048_row_006 | Discipline / Blank / Null-Bound | 44 / 57 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_001 | Level / 1 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_002 | Level / 2 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_003 | Level / 3 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_004 | Level / 4 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_005 | Level / 5 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_006 | Level / 6 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_007 | Level / 7 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_008 | Level / 8 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_009 | Level / 9 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_010 | Level / 10 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_011 | Level / 11 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_012 | Level / 12 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_013 | Level / 13 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_014 | Level / 14 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_015 | Level / 15 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_016 | Level / 16 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_017 | Level / 17 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_018 | Level / 18 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_019 | Level / 19 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_049_row_020 | Level / 20 | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_050_row_001 | Ogryn Role / Bulwark | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_050_row_002 | Ogryn Role / Gun Lugger | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_050_row_003 | Ogryn Role / Bone ’ead | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_050_row_004 | Ogryn Role / Brute | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_051_row_001 | Role / Bulwark | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_051_row_002 | Role / Gun Lugger | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_051_row_003 | Role / Bone ’ead | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_051_row_004 | Role / Brute | 46 / 59 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_052_row_001 | Ogryn Role / Bulwark | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_052_row_002 | Ogryn Role / Gun Lugger | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_052_row_003 | Ogryn Role / Bone ’ead | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_052_row_004 | Ogryn Role / Brute | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_053_row_001 | Ogryn Role / Bulwark | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_053_row_002 | Ogryn Role / Gun Lugger | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_053_row_003 | Ogryn Role / Bone ’ead | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_053_row_004 | Ogryn Role / Brute | 47 / 60 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_001 | Level / 1 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_002 | Level / 2 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_003 | Level / 3 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_004 | Level / 4 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_005 | Level / 5 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_006 | Level / 6 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_007 | Level / 7 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_008 | Level / 8 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_009 | Level / 9 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_010 | Level / 10 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_011 | Level / 11 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_012 | Level / 12 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_013 | Level / 13 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_014 | Level / 14 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_015 | Level / 15 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_016 | Level / 16 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_017 | Level / 17 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_018 | Level / 18 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_019 | Level / 19 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_054_row_020 | Level / 20 | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_055_row_001 | Enforcement Doctrine / Riot Shield | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_055_row_002 | Enforcement Doctrine / Executioner | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_055_row_003 | Enforcement Doctrine / Investigator | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_056_row_001 | Doctrine / Riot Shield | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_056_row_002 | Doctrine / Executioner | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_056_row_003 | Doctrine / Investigator | 49 / 62 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_057_row_001 | Enforcement Doctrine / Riot Shield | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_057_row_002 | Enforcement Doctrine / Executioner | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_057_row_003 | Enforcement Doctrine / Investigator | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_058_row_001 | Enforcement Doctrine / Riot Shield | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_058_row_002 | Enforcement Doctrine / Executioner | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_058_row_003 | Enforcement Doctrine / Investigator | 50 / 63 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_001 | Level / 1 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_002 | Level / 2 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_003 | Level / 3 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_004 | Level / 4 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_005 | Level / 5 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_006 | Level / 6 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_007 | Level / 7 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_008 | Level / 8 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_009 | Level / 9 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_010 | Level / 10 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_011 | Level / 11 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_012 | Level / 12 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_013 | Level / 13 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_014 | Level / 14 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_015 | Level / 15 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_016 | Level / 16 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_017 | Level / 17 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_018 | Level / 18 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_019 | Level / 19 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_059_row_020 | Level / 20 | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_060_row_001 | Gang Style / Gunslinger | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_060_row_002 | Gang Style / Knife Rat | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_060_row_003 | Gang Style / Chem-User | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_060_row_004 | Gang Style / Sump Ghost | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_061_row_001 | Style / Gunslinger | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_061_row_002 | Style / Knife Rat | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_061_row_003 | Style / Chem-User | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_061_row_004 | Style / Sump Ghost | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_062_row_001 | Gang Style / Gunslinger | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_062_row_002 | Gang Style / Knife Rat | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_062_row_003 | Gang Style / Chem-User | 52 / 65 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_063_row_001 | Gang Style / Sump Ghost | 53 / 66 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_001 | Level / 1 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_002 | Level / 2 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_003 | Level / 3 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_004 | Level / 4 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_005 | Level / 5 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_006 | Level / 6 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_007 | Level / 7 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_008 | Level / 8 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_009 | Level / 9 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_010 | Level / 10 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_011 | Level / 11 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_012 | Level / 12 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_013 | Level / 13 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_014 | Level / 14 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_015 | Level / 15 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_016 | Level / 16 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_017 | Level / 17 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_018 | Level / 18 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_019 | Level / 19 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_064_row_020 | Level / 20 | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_065_row_001 | Ratling Trick / Long-Las Sniper | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_065_row_002 | Ratling Trick / Underhive Rat | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_065_row_003 | Ratling Trick / Spotter | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_065_row_004 | Ratling Trick / Black-Market Gremlin | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_066_row_001 | Trick / Long-Las Sniper | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_066_row_002 | Trick / Underhive Rat | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_066_row_003 | Trick / Spotter | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_066_row_004 | Trick / Black-Market Gremlin | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_067_row_001 | Ratling Trick / Long-Las Sniper | 55 / 68 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_068_row_001 | Ratling Trick / Underhive Rat | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_068_row_002 | Ratling Trick / Spotter | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_068_row_003 | Ratling Trick / Black-Market Gremlin | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_069_row_001 | Ratling Trick / Long-Las Sniper | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_069_row_002 | Ratling Trick / Underhive Rat | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_069_row_003 | Ratling Trick / Spotter | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_069_row_004 | Ratling Trick / Black-Market Gremlin | 56 / 69 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_001 | Level / 1 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_002 | Level / 2 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_003 | Level / 3 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_004 | Level / 4 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_005 | Level / 5 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_006 | Level / 6 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_007 | Level / 7 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_008 | Level / 8 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_009 | Level / 9 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_010 | Level / 10 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_011 | Level / 11 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_012 | Level / 12 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_013 | Level / 13 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_014 | Level / 14 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_015 | Level / 15 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_016 | Level / 16 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_017 | Level / 17 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_018 | Level / 18 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_019 | Level / 19 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_070_row_020 | Level / 20 | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_071_row_001 | Protocol / Ruststalker Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_001 | Combat Protocol / Ranger | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_002 | Combat Protocol / Vanguard | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_003 | Combat Protocol / Protector | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_004 | Combat Protocol / Data-Hunter | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_005 | Combat Protocol / Infiltrator | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_072_row_006 | Combat Protocol / Ruststalker | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_073_row_001 | Protocol / Ranger Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_073_row_002 | Protocol / Vanguard Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_073_row_003 | Protocol / Protector Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_073_row_004 | Protocol / Data-Hunter Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_073_row_005 | Protocol / Infiltrator Protocol | 58 / 71 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_074_row_001 | Combat Protocol / Ruststalker | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_001 | Combat Protocol / Ranger | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_002 | Combat Protocol / Vanguard | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_003 | Combat Protocol / Protector | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_004 | Combat Protocol / Data-Hunter | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_005 | Combat Protocol / Infiltrator | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_075_row_006 | Combat Protocol / Ruststalker | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_076_row_001 | Combat Protocol / Ranger | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_076_row_002 | Combat Protocol / Vanguard | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_076_row_003 | Combat Protocol / Protector | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_076_row_004 | Combat Protocol / Data-Hunter | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_076_row_005 | Combat Protocol / Infiltrator | 59 / 72 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_001 | Level / 1 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_002 | Level / 2 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_003 | Level / 3 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_004 | Level / 4 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_005 | Level / 5 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_006 | Level / 6 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_007 | Level / 7 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_008 | Level / 8 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_009 | Level / 9 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_010 | Level / 10 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_011 | Level / 11 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_012 | Level / 12 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_013 | Level / 13 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_014 | Level / 14 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_015 | Level / 15 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_016 | Level / 16 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_017 | Level / 17 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_018 | Level / 18 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_019 | Level / 19 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_077_row_020 | Level / 20 | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_078_row_001 | Hold Doctrine / Hearthguard | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_078_row_002 | Hold Doctrine / Ironhead | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_078_row_003 | Hold Doctrine / Guild-Militant | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_079_row_001 | Doctrine / Hearthguard | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_079_row_002 | Doctrine / Ironhead | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_079_row_003 | Doctrine / Guild-Militant | 61 / 74 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_080_row_001 | Hold Doctrine / Hearthguard | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_080_row_002 | Hold Doctrine / Ironhead | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_080_row_003 | Hold Doctrine / Guild-Militant | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_081_row_001 | Hold Doctrine / Hearthguard | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_081_row_002 | Hold Doctrine / Ironhead | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_081_row_003 | Hold Doctrine / Guild-Militant | 62 / 75 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_001 | Level / 1 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_002 | Level / 2 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_003 | Level / 3 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_004 | Level / 4 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_005 | Level / 5 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_006 | Level / 6 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_007 | Level / 7 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_008 | Level / 8 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_009 | Level / 9 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_010 | Level / 10 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_011 | Level / 11 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_012 | Level / 12 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_013 | Level / 13 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_014 | Level / 14 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_015 | Level / 15 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_016 | Level / 16 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_017 | Level / 17 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_018 | Level / 18 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_019 | Level / 19 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_082_row_020 | Level / 20 | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_083_row_001 | Expedition Role / Outrider | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_083_row_002 | Expedition Role / Claim-Staker | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_083_row_003 | Expedition Role / Trail Gunner | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_084_row_001 | Role / Outrider | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_084_row_002 | Role / Claim-Staker | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_084_row_003 | Role / Trail Gunner | 64 / 77 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_085_row_001 | Expedition Role / Outrider | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_085_row_002 | Expedition Role / Claim-Staker | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_085_row_003 | Expedition Role / Trail Gunner | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_086_row_001 | Expedition Role / Outrider | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_086_row_002 | Expedition Role / Claim-Staker | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_086_row_003 | Expedition Role / Trail Gunner | 65 / 78 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_001 | Level / 1 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_002 | Level / 2 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_003 | Level / 3 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_004 | Level / 4 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_005 | Level / 5 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_006 | Level / 6 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_007 | Level / 7 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_008 | Level / 8 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_009 | Level / 9 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_010 | Level / 10 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_011 | Level / 11 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_012 | Level / 12 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_013 | Level / 13 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_014 | Level / 14 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_015 | Level / 15 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_016 | Level / 16 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_017 | Level / 17 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_018 | Level / 18 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_019 | Level / 19 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_087_row_020 | Level / 20 | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_088_row_001 | Outcast Path / Shadow Guide | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_089_row_001 | Path / Ranger | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_089_row_002 | Path / Corsair | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_089_row_003 | Path / Shadow Guide | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_090_row_001 | Outcast Path / Ranger | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_090_row_002 | Outcast Path / Corsair | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_090_row_003 | Outcast Path / Shadow Guide | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_091_row_001 | Outcast Path / Ranger | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_091_row_002 | Outcast Path / Corsair | 67 / 80 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_092_row_001 | Outcast Path / Corsair | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_092_row_002 | Outcast Path / Shadow Guide | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_093_row_001 | Outcast Path / Ranger | 68 / 81 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_001 | Level / 1 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_002 | Level / 2 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_003 | Level / 3 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_004 | Level / 4 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_005 | Level / 5 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_006 | Level / 6 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_007 | Level / 7 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_008 | Level / 8 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_009 | Level / 9 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_010 | Level / 10 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_011 | Level / 11 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_012 | Level / 12 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_013 | Level / 13 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_014 | Level / 14 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_015 | Level / 15 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_016 | Level / 16 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_017 | Level / 17 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_018 | Level / 18 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_019 | Level / 19 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_094_row_020 | Level / 20 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_001 | Level / 1 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_002 | Level / 2 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_003 | Level / 3 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_004 | Level / 4 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_005 | Level / 5 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_006 | Level / 6 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_007 | Level / 7 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_008 | Level / 8 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_009 | Level / 9 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_010 | Level / 10 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_011 | Level / 11 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_012 | Level / 12 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_013 | Level / 13 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_014 | Level / 14 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_015 | Level / 15 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_016 | Level / 16 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_017 | Level / 17 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_018 | Level / 18 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_019 | Level / 19 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_095_row_020 | Level / 20 | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_096_row_001 | Path / Seer of Battle | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_096_row_002 | Path / Storm Warlock | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_096_row_003 | Path / Spirit Guardian | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_097_row_001 | Warlock Path / Seer of Battle | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_097_row_002 | Warlock Path / Storm Warlock | 70 / 83 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_098_row_001 | Warlock Path / Seer of Battle | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_098_row_002 | Warlock Path / Storm Warlock | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_098_row_003 | Warlock Path / Spirit Guardian | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_099_row_001 | Warlock Path / Seer of Battle | 71 / 84 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_001 | Talent / Rapid Reload | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_002 | Talent / Hip Fire | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_003 | Talent / Close-Quarters Killer | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_004 | Talent / Heavy Weapon Training | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_005 | Talent / Iron Discipline | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_006 | Talent / Combat Medic | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_007 | Talent / Grenadier | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_008 | Talent / Brawler | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_009 | Talent / Cybernetic Implant | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_010 | Talent / Point Blank Execution | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_011 | Talent / Suppressive Discipline | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_012 | Talent / Field Armourer | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_013 | Talent / Bayonet Fighter | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_014 | Talent / Breacher | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_015 | Talent / Crisis Runner | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_016 | Talent / Dead Calm | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_017 | Talent / Tactical Reposition | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_018 | Talent / Weapon Specialist | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_019 | Talent / Armour Familiarity | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_100_row_020 | Talent / Relic-Bearer | 73 / 86 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_001 | Talent / Ogryn Wall | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_002 | Talent / Bigger Gun | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_003 | Talent / Loyal as Stone | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_004 | Talent / Bone ’ead Implant | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_005 | Talent / Too Angry to Notice | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_006 | Talent / Ratling Vanish | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_007 | Talent / Impossible Shot | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_008 | Talent / Pocket Marksman | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_009 | Talent / Scavver’s Luck | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_010 | Talent / Cook’s Morale | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_011 | Talent / Machine Precision | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_012 | Talent / Sacred Augmetics | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_013 | Talent / Rad-Hardened | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_014 | Talent / Noospheric Burst | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_015 | Talent / Cold Logic | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_016 | Talent / Witch-Sight | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_017 | Talent / Imperial Flexibility | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_018 | Talent / Last Order Standing | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_019 | Talent / Sanctioning Scars | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_020 | Talent / Hive-Blooded | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_021 | Talent / Ancestor’s Grudge | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_022 | Talent / Hold-Born Engineer | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_023 | Talent / Void Stock | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_024 | Talent / Iron Stance | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_025 | Talent / Kin Weapon Master | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_026 | Talent / Aeldari Grace | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_027 | Talent / Path Discipline | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_028 | Talent / Ranger’s Cloak | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_029 | Talent / Witchblade Adept | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_101_row_030 | Talent / Alien Reflexes | 74 / 87 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_001 | Upgrade / Optical Implant | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_002 | Upgrade / Bionic Arm | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_003 | Upgrade / Bionic Legs | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_004 | Upgrade / Subdermal Plating | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_005 | Upgrade / Respirator Implant | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_006 | Upgrade / Data-Jack | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_007 | Upgrade / Vox Implant | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_008 | Upgrade / Pain Editor | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_009 | Upgrade / Recoil Bracing | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_010 | Upgrade / Targeting Lens | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_011 | Upgrade / Mag-Lock Palm | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_012 | Upgrade / Skeletal Reinforcement | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_013 | Upgrade / Dermal Insulation | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_014 | Upgrade / Chem Injector | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_015 | Upgrade / Internal Chrono | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_016 | Upgrade / Mechadendrite, Utility | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_017 | Upgrade / Mechadendrite, Medicae | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_018 | Upgrade / Mechadendrite, Combat | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_019 | Upgrade / Cranial Cogitator | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_020 | Upgrade / Augmetic Heart | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_021 | Upgrade / Black-Iron Jaw | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_102_row_022 | Upgrade / Vocal Coder | 76 / 89 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_103_row_001 | Power Type / Minor Power | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_103_row_002 | Power Type / Standard Power | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_103_row_003 | Power Type / Major Power | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_103_row_004 | Power Type / Empowered Power | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_001 | Empowered Option / Overcharged Damage | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_002 | Empowered Option / Brutal Manifestation | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_003 | Empowered Option / Extended Reach | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_004 | Empowered Option / Sustained Focus | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_005 | Empowered Option / Split Manifestation | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_104_row_006 | Empowered Option / Discipline Mastery | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_001 | Power / Warp Spark | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_002 | Power / Kinetic Push | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_003 | Power / Mind Lumen | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_004 | Power / Static Veil | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_005 | Power / Flesh Knit | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_006 | Power / Pain Spike | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_105_row_007 | Power / Ember Flicker | 78 / 91 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_001 | Power / Ashen Brand | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_002 | Power / Danger Sense | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_003 | Power / Echo Read | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_004 | Power / Whisper from Below | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_005 | Power / Warp Bite | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_006 | Power / Null Glare | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_106_row_007 | Power / Blank Sense | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_001 | Power / Focused Rupture | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_002 | Power / Assail | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_003 | Power / Psychic Shield | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_004 | Power / Soulfire | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_005 | Power / Dominate Nerve | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_006 | Power / Warp Step | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_007 | Power / Blood Surge | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_008 | Power / Toxic Bloom | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_009 | Power / Kinetic Bulwark | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_010 | Power / Crush Grip | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_011 | Power / Fate’s Nudge | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_012 | Power / Prescient Aim | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_013 | Power / Cleansing Wave | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_014 | Power / Burning Halo | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_015 | Power / Terror Echo | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_016 | Power / Baleful Rupture | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_017 | Power / Null Field | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_107_row_018 | Power / Silence the Witch | 79 / 92 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_001 | Power / Telekinetic Crush | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_002 | Power / Inferno Bloom | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_003 | Power / Prescient Execution | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_004 | Power / Biomantic Surge | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_005 | Power / Flesh Reforged | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_006 | Power / Hemorrhage | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_007 | Power / Force Dome | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_008 | Power / Foresight Cascade | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_009 | Power / Soulstorm | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_010 | Power / Malefic Door | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_011 | Power / Possession Spike | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_108_row_012 | Power / Pariah Zone | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_001 | Power / Conceal | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_002 | Power / Reveal | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_003 | Power / Protect | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_004 | Power / Jinx | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_005 | Power / Quicken | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_006 | Power / Restrain Fate | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_007 | Power / Destructor Rune | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_109_row_008 | Power / Fortune Thread | 80 / 93 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_110_row_001 | Method / Short rest | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_110_row_002 | Method / Long rest | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_110_row_003 | Method / Vent as an action | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_110_row_004 | Method / Kill with Focused Rupture | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_110_row_005 | Method / Stabilising Focus | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_001 | Result / 2-6 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_002 | Result / 7-10 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_003 | Result / 11-14 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_004 | Result / 15-18 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_005 | Result / 19-22 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_006 | Result / 23-26 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_007 | Result / 27-30 | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_111_row_008 | Result / 31+ | 82 / 95 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_001 | Severity / 2-6 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_002 | Severity / 7-10 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_003 | Severity / 11-14 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_004 | Severity / 15-18 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_005 | Severity / 19-22 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_006 | Severity / 23-26 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_007 | Severity / 27-30 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_112_row_008 | Severity / 31+ | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_001 | Severity / 2-6 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_002 | Severity / 7-10 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_003 | Severity / 11-14 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_004 | Severity / 15-18 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_005 | Severity / 19-22 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_006 | Severity / 23-26 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_007 | Severity / 27-30 | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_113_row_008 | Severity / 31+ | 83 / 96 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_001 | Corruption / 0 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_002 | Corruption / 1 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_003 | Corruption / 2 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_004 | Corruption / 3 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_005 | Corruption / 4 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_006 | Corruption / 5 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_114_row_007 | Corruption / 6 | 85 / 98 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_001 | Class / Veteran | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_002 | Class / Zealot | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_003 | Class / Psyker | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_004 | Class / Ogryn Skullbreaker | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_005 | Class / Arbites Enforcer | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_006 | Class / Hive Scum | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_007 | Class / Ratling Sharpshooter | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_008 | Class / Skitarii Veteran | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_009 | Class / Kin Armsman | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_010 | Class / Hernkyn Prospector | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_011 | Class / Aeldari Outcast | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_115_row_012 | Class / Aeldari Warlock | 87 / 100 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_001 | Item / Med-Stim | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_002 | Item / Med-Pack | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_003 | Item / Field Dressing | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_004 | Item / Ammo Pack | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_005 | Item / Specialist Ammo Pack | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_006 | Item / Grenade Bandolier | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_007 | Item / Weapon Maintenance Kit | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_008 | Item / Auspex Battery | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_009 | Item / Rebreather Filter | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_010 | Item / Void Patch Kit | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_011 | Item / Stimm Slug | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_116_row_012 | Item / Purity Seal Charm | 88 / 101 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_001 | Availability / Issued | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_002 | Availability / Controlled | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_003 | Availability / Scarce | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_004 | Availability / Rare | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_005 | Availability / Exceptional | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_006 | Availability / Near-Unique | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_117_row_007 | Availability / Unique | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_001 | Approach / Formal Request | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_002 | Approach / Locate Supply | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_003 | Approach / Mechanicus Petition | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_004 | Approach / Religious Petition | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_005 | Approach / Black Market | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_118_row_006 | Approach / Personal Leverage | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_119_row_001 | Result / Failure by 5+ | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_119_row_002 | Result / Failure by 1-4 | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_119_row_003 | Result / Success | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_119_row_004 | Result / Success by 5+ | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_119_row_005 | Result / Natural 20 | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_120_row_001 | Provenance / Imperial General | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_120_row_002 | Provenance / Mechanicus | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_120_row_003 | Provenance / Kin | 90 / 103 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_121_row_001 | Provenance / Aeldari | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_121_row_002 | Provenance / Proscribed / Heretical | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_121_row_003 | Provenance / Black Market | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_122_row_001 | Tier / Tier 1 | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_122_row_002 | Tier / Tier 2 | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_122_row_003 | Tier / Tier 3 | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_122_row_004 | Tier / Tier 4 | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_001 | Modification / Bayonet / Breaching Lug | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_002 | Modification / Extended Magazine / Charge Pack | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_003 | Modification / Reflex Sight | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_004 | Modification / Camo Wrap / Low-Signature Furniture | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_005 | Modification / Recoil Compensation | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_006 | Modification / Targeting Optic | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_007 | Modification / Reinforced Action | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_008 | Modification / Sanctified Fittings | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_123_row_009 | Modification / Archeotech Interface | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_124_row_001 | Masterwork Trait / Perfect Balance | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_124_row_002 | Masterwork Trait / Artificer Edge | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_124_row_003 | Masterwork Trait / Precision Barrel / Focusing Array | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_124_row_004 | Masterwork Trait / Rapid Feed | 91 / 104 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_125_row_001 | Masterwork Trait / Recoil Compensation | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_125_row_002 | Masterwork Trait / Compact Pattern | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_125_row_003 | Masterwork Trait / Artificer Armour | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_125_row_004 | Masterwork Trait / Responsive Plating | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_125_row_005 | Masterwork Trait / Sealed Systems | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_001 | Ammunition / Tracer / Target-Marking | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_002 | Ammunition / Manstopper | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_003 | Ammunition / Armour-Piercing | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_004 | Ammunition / Incendiary | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_005 | Ammunition / Hot-Shot Charge Pack | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_006 | Ammunition / Sanctified Ammunition | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_126_row_007 | Ammunition / Xenos / Exotic Magazine | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_127_row_001 | Step / 1. Secure | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_127_row_002 | Step / 2. Assess | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_127_row_003 | Step / 3. Restore | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_127_row_004 | Step / 4. Integrate | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_127_row_005 | Step / 5. Explain | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_128_row_001 | Condition / Pristine | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_128_row_002 | Condition / Serviceable | 92 / 105 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_129_row_001 | Condition / Worn | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_129_row_002 | Condition / Damaged | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_129_row_003 | Condition / Ruined | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_001 | Equipment Grade / Issued | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_002 | Equipment Grade / Controlled | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_003 | Equipment Grade / Scarce | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_004 | Equipment Grade / Rare | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_005 | Equipment Grade / Exceptional | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_130_row_006 | Equipment Grade / Near-Unique / Unique | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_131_row_001 | Item / Inferno Pistol | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_131_row_002 | Item / Grav-Pistol | 93 / 106 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_001 | Item / Grav-Gun | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_002 | Item / Digital Weapon | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_003 | Item / Null Rod | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_004 | Item / Rosarius | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_005 | Item / Displacer Field | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_006 | Item / Conversion Beamer | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_007 | Item / Teleport Homer | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_132_row_008 | Item / Stasis Grenade | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_001 | Item / Volkite Serpenta | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_002 | Item / Volkite Charger | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_003 | Item / Suspensor Harness | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_004 | Item / Archeotech Logic Engine | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_005 | Item / Phase-Shunt Field | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_133_row_006 | Item / Medicae Crucible | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_001 | Relic / The Last Light - Imperial | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_002 | Relic / Bulwark of Saint Drusus - Imperial | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_003 | Relic / Martyr's Censer - Imperial | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_004 | Relic / Arc of the Reductor - Mechanicus | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_005 | Relic / Omnissian Data-Relic - Mechanicus | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_134_row_006 | Relic / Big Lug's Door - Ogryn | 94 / 107 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_135_row_001 | Relic / Grutt's Lucky Club - Ogryn | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_135_row_002 | Relic / Ancestor-Wrought Rail Rifle - Kin | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_135_row_003 | Relic / Oathplate of the First Claim - Kin | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_135_row_004 | Relic / Ghosthelm of the Wandering Seer - Aeldari | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_135_row_005 | Relic / Starfall Long Rifle - Aeldari | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_001 | Unique Item / Halo of Saint Varro | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_002 | Unique Item / Heart-Key of the Red Vault | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_003 | Unique Item / The First Oathstone | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_004 | Unique Item / The Veiled Eye | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_005 | Unique Item / The Door That Would Not Break | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_136_row_006 | Unique Item / The Ghost's Coin | 95 / 108 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_001 | d8 / 1 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_002 | d8 / 2 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_003 | d8 / 3 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_004 | d8 / 4 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_005 | d8 / 5 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_006 | d8 / 6 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_007 | d8 / 7 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_137_row_008 | d8 / 8 | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_138_row_001 | Care / Improvised | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_138_row_002 | Care / Field Medicae | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_138_row_003 | Care / Hospital / Regimental | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_138_row_004 | Care / Specialist | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_138_row_005 | Care / Exceptional | 97 / 110 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_139_row_001 | Tier / Tier 1: Levels 1-4 | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_139_row_002 | Tier / Tier 2: Levels 5-10 | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_139_row_003 | Tier / Tier 3: Levels 11-16 | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_139_row_004 | Tier / Tier 4: Levels 17-20 | 99 / 112 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_140_row_001 | Difficulty / Routine | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_140_row_002 | Difficulty / Demanding | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_140_row_003 | Difficulty / Dangerous | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_140_row_004 | Difficulty / Extreme | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_140_row_005 | Difficulty / Exceptional | 101 / 114 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_001 | Action / Drive Hard | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_002 | Action / Evasive Driving | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_003 | Action / Fire a Mount | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_004 | Action / Reload a Mount | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_005 | Action / Spot or Assist | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_141_row_006 | Action / Damage Control | 102 / 115 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_001 | d6 / 1 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_002 | d6 / 2 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_003 | d6 / 3 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_004 | d6 / 4 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_005 | d6 / 5 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_142_row_006 | d6 / 6 | 103 / 116 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_001 | Band / 0 — Contact | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_002 | Band / 1 — Close | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_003 | Band / 2 — Near | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_004 | Band / 3 — Far | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_005 | Band / 4 — Distant | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_143_row_006 | Band / 5 — Lost | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_144_row_001 | Work / Damage Control | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_144_row_002 | Work / Field repair | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_144_row_003 | Work / Workshop repair | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_144_row_004 | Work / Rebuild a wreck | 104 / 117 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_001 | Upgrade / Reinforced plating | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_002 | Upgrade / Smoke launchers | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_003 | Upgrade / Auspex survey suite | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_004 | Upgrade / Recovery winch | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_005 | Upgrade / All-terrain running gear | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_006 | Upgrade / Sealed compartment | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_007 | Upgrade / Ogryn accommodation | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_145_row_008 | Upgrade / Spare-parts locker | 105 / 118 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_001 | Weapon / Heavy stubber | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_002 | Weapon / Heavy bolter | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_003 | Weapon / Multi-laser | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_004 | Weapon / Autocannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_005 | Weapon / Lascannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_006 | Weapon / Battle cannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_007 | Weapon / Bolt cannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_008 | Weapon / HYLas rotary cannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_009 | Weapon / Magna-coil autocannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_010 | Weapon / Scatter laser | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_011 | Weapon / Shuriken cannon | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_012 | Weapon / Twin shuriken catapults | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_146_row_013 | Weapon / Pulse laser | 108 / 121 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_001 | Rule / Attack roll | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_002 | Rule / Ability/skill check | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_003 | Rule / Saving throw | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_004 | Rule / Weapon save DC | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_005 | Rule / Psychic save DC | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_006 | Rule / Psychic attack | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_007 | Rule / Grenade save DC | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_008 | Rule / Initiative | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_147_row_009 | Rule / Proficiency bonus | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_148_row_001 | On Your Turn / Movement | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_148_row_002 | On Your Turn / Action | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_148_row_003 | On Your Turn / Bonus Action | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_148_row_004 | On Your Turn / Reaction | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_148_row_005 | On Your Turn / Object Interaction | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_001 | Rule / Normal/maximum range | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_002 | Rule / Close-quarters shooting | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_003 | Rule / Opportunity attack | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_004 | Rule / Grapple | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_005 | Rule / Shove | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_006 | Rule / Light / Heavy / Full Cover | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_007 | Rule / Suppressed | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_008 | Rule / Critical hit | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_009 | Rule / Reload X | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_149_row_010 | Rule / Two-weapon fighting | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_001 | Condition / State / Blinded | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_002 | Condition / State / Bloodied | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_003 | Condition / State / Frightened | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_004 | Condition / State / Grappled | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_005 | Condition / State / Hidden | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_006 | Condition / State / Incapacitated | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_007 | Condition / State / Invisible | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_008 | Condition / State / Poisoned | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_009 | Condition / State / Prone | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_010 | Condition / State / Restrained | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_011 | Condition / State / Stunned | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_012 | Condition / State / Suppressed | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_150_row_013 | Condition / State / Unconscious | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_001 | Property / Accurate | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_002 | Property / Armour-Breaking | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_003 | Property / Blast | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_004 | Property / Brutal | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_005 | Property / Burst | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_151_row_006 | Property / Close-Quarters | 110 / 123 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_001 | Property / Heavy | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_002 | Property / Overheat | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_003 | Property / Reload X | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_004 | Property / Shock | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_005 | Property / Spray | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_152_row_006 | Property / Suppression | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_001 | Rule / Item / Short rest | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_002 | Rule / Item / Long rest | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_003 | Rule / Item / Death saves | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_004 | Rule / Item / Stabilise | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_005 | Rule / Item / Med-Stim | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_006 | Rule / Item / Med-Pack | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_007 | Rule / Item / Field Dressing | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_153_row_008 | Rule / Item / Exhaustion | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_001 | Rule / Minor power | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_002 | Rule / Standard power | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_003 | Rule / Major power | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_004 | Rule / Empowered power | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_005 | Rule / Perils check | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_006 | Rule / Perils severity | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_007 | Rule / Vent | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_008 | Rule / Short/long rest | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_154_row_009 | Rule / Corruption | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_001 | Rule / Issued / Controlled / Scarce | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_002 | Rule / Rare / Exceptional / Near-Unique | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_003 | Rule / Unique | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_004 | Rule / Requisition test | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_005 | Rule / Standard ammunition | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_006 | Rule / Specialist ammunition | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_007 | Rule / Item Condition | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_155_row_008 | Rule / Signature Wargear | 111 / 124 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_001 | Rule / Normal driving | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_002 | Rule / Drive Hard / Evade | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_003 | Rule / Fire a Mount | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_004 | Rule / Mounted attack / DC | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_005 | Rule / Damage Threshold | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_006 | Rule / Breakdown | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_007 | Rule / Wrecked at 0 HP | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_008 | Rule / Damage Control | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_009 | Rule / Field repair | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_010 | Rule / Chase contest | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| table_156_row_011 | Rule / Passenger protection | 112 / 125 | MANUAL_RULE | NOT_YET_IMPORTED |
| di.skill.acrobatics | skill / Acrobatics | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.acrobatics | proficiency / Acrobatics proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.athletics | skill / Athletics | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.athletics | proficiency / Athletics proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.investigation | skill / Investigation | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.investigation | proficiency / Investigation proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.medicine | skill / Medicine | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.medicine | proficiency / Medicine proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.perception | skill / Perception | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.perception | proficiency / Perception proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.stealth | skill / Stealth | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.stealth | proficiency / Stealth proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.survival | skill / Survival | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.survival | proficiency / Survival proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.technology | skill / Technology | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.technology | proficiency / Technology proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.deception | skill / Deception | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.deception | proficiency / Deception proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.intimidation | skill / Intimidation | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.intimidation | proficiency / Intimidation proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.persuasion | skill / Persuasion | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.persuasion | proficiency / Persuasion proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.insight | skill / Insight | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.insight | proficiency / Insight proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.history | skill / History | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.history | proficiency / History proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.religion | skill / Religion | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.religion | proficiency / Religion proficiency | 5 / 18 | READY | STRUCTURED |
| di.skill.sleight_of_hand | skill / Sleight of Hand | 5 / 18 | READY | STRUCTURED |
| di.proficiency.skill.sleight_of_hand | proficiency / Sleight of Hand proficiency | 5 / 18 | READY | STRUCTURED |
| di.feature.species.human.traits | feature / Human traits | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.human.baseline | feature / Human fixed baseline | 10 / 23 | READY | STRUCTURED |
| di.choice.human.ability_scores | choice / Human ability score increases | 10 / 23 | READY | STRUCTURED |
| di.choice.human.imperial_adaptability | choice / Choose 1 skill proficiency | 10 / 23 | READY | STRUCTURED |
| di.species.human | species / Human | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.ogryn.traits | feature / Ogryn Abhuman traits | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.ogryn.baseline | feature / Ogryn Abhuman fixed baseline | 10 / 23 | READY | STRUCTURED |
| di.species.ogryn | species / Ogryn Abhuman | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.ratling.traits | feature / Ratling Abhuman traits | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.ratling.baseline | feature / Ratling Abhuman fixed baseline | 10 / 23 | READY | STRUCTURED |
| di.species.ratling | species / Ratling Abhuman | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.skitarii.traits | feature / Skitarii Augmented Human traits | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.skitarii.baseline | feature / Skitarii Augmented Human fixed baseline | 10 / 23 | READY | STRUCTURED |
| di.choice.skitarii.ability_scores | choice / Skitarii Augmented Human ability score choice | 10 / 23 | READY | STRUCTURED |
| di.species.skitarii | species / Skitarii Augmented Human | 10 / 23 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.kin.traits | feature / Squat / Kin traits | 11 / 24 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.kin.baseline | feature / Squat / Kin fixed baseline | 11 / 24 | READY | STRUCTURED |
| di.choice.kin.ability_scores | choice / Squat / Kin ability score choice | 11 / 24 | READY | STRUCTURED |
| di.species.kin | species / Squat / Kin | 11 / 24 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.aeldari.traits | feature / Aeldari / Eldar traits | 11 / 24 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.species.aeldari.baseline | feature / Aeldari / Eldar fixed baseline | 11 / 24 | READY | STRUCTURED |
| di.choice.aeldari.ability_scores | choice / Aeldari / Eldar ability score choice | 11 / 24 | READY | STRUCTURED |
| di.species.aeldari | species / Aeldari / Eldar | 11 / 24 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.choice.hiveborn.skills | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.feature.origin.hiveborn | feature / Hiveborn benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.hiveborn | background / Hiveborn | 13 / 26 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.choice.shrine_worlder.skills | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.feature.origin.shrine_worlder | feature / Shrine Worlder benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.shrine_worlder | background / Shrine Worlder | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.choice.penal_worlder.skills | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.feature.origin.penal_worlder | feature / Penal Worlder benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.penal_worlder | background / Penal Worlder | 13 / 26 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.choice.voidborn.skills | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.feature.origin.voidborn | feature / Voidborn benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.voidborn | background / Voidborn | 13 / 26 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.feature.origin.forge_world | feature / Forge World benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.forge_world | background / Forge World | 13 / 26 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.choice.schola_progenium.skills | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.choice.schola_progenium.skills_2 | choice / Choose 1 skill proficiency | 13 / 26 | READY | STRUCTURED |
| di.feature.origin.schola_progenium | feature / Schola Progenium benefits | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.schola_progenium | background / Schola Progenium | 13 / 26 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.choice.militarum_regiment.skills | choice / Choose 1 skill proficiency | 14 / 27 | READY | STRUCTURED |
| di.feature.origin.militarum_regiment | feature / Militarum Regiment benefits | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.militarum_regiment | background / Militarum Regiment | 14 / 27 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.choice.underhive.skills | choice / Choose 2 skill proficiency | 14 / 27 | READY | STRUCTURED |
| di.feature.origin.underhive | feature / Underhive benefits | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.underhive | background / Underhive | 14 / 27 | DUPLICATE_OR_CONFLICT | PARTIALLY_STRUCTURED |
| di.choice.craftworld_outcast.skills | choice / Choose 2 skill proficiency | 14 / 27 | READY | STRUCTURED |
| di.feature.origin.craftworld_outcast | feature / Craftworld / Outcast benefits | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.craftworld_outcast | background / Craftworld / Outcast | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.choice.mining_hold_guild.skills | choice / Choose 2 skill proficiency | 14 / 27 | READY | STRUCTURED |
| di.feature.origin.mining_hold_guild | feature / Mining Hold / Guild benefits | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.background.mining_hold_guild | background / Mining Hold / Guild | 14 / 27 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.faithful | feature / Faithful | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.jaded | feature / Jaded | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.twitchy | feature / Twitchy | 16 / 29 | READY | STRUCTURED |
| di.feature.universal.unnaturally_lucky | feature / Unnaturally Lucky | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.augmetic_scarred | feature / Augmetic Scarred | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.chem_hardened | feature / Chem-Hardened | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.devoted_servant | feature / Devoted Servant | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.touched_by_the_warp | feature / Touched by the Warp | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.hive_survivor | feature / Hive Survivor | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.munitorum_drilled | feature / Munitorum Drilled | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.iron_nerves | feature / Iron Nerves | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.faith_in_steel | feature / Faith in Steel | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.dirty_pragmatist | feature / Dirty Pragmatist | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.vox_familiar | feature / Vox Familiar | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.grudge_bearer | feature / Grudge-Bearer | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.hard_to_kill | feature / Hard to Kill | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.knife_in_the_boot | feature / Knife in the Boot | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.field_chirurgeon | feature / Field Chirurgeon | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.black_market_eye | feature / Black-Market Eye | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.universal.litany_marked | feature / Litany-Marked | 16 / 29 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.accurate | property / Accurate | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.armour_breaking | property / Armour-Breaking | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.beam | property / Beam | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.blast | property / Blast | 22 / 35 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.brutal | property / Brutal | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.burst | property / Burst | 22 / 35 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.chain | property / Chain | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.close_quarters | property / Close-Quarters | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.emplaced | property / Emplaced | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.entangling | property / Entangling | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.finesse | property / Finesse | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.focus | property / Focus | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.heavy | property / Heavy | 22 / 35 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.industrial | property / Industrial | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.light | property / Light | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.mechanicus | property / Mechanicus | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.monomolecular | property / Monomolecular | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.ogryn | property / Ogryn | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.overheat | property / Overheat | 22 / 35 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.power_field | property / Power Field | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.psyker | property / Psyker | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.reload | property / Reload X | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.shield | property / Shield | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.shock | property / Shock | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.silent | property / Silent | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.spray | property / Spray | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.spirit_weapon | property / Spirit Weapon | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.suppression | property / Suppression | 22 / 35 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.property.weapon.thrown | property / Thrown | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.twin_linked | property / Twin-Linked | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.property.weapon.versatile | property / Versatile X | 22 / 35 | MANUAL_RULE | MANUAL_ONLY |
| di.feature.talent.rapid_reload | feature / Rapid Reload | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.hip_fire | feature / Hip Fire | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.close_quarters_killer | feature / Close-Quarters Killer | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.heavy_weapon_training | feature / Heavy Weapon Training | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.iron_discipline | feature / Iron Discipline | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.combat_medic | feature / Combat Medic | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.grenadier | feature / Grenadier | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.brawler | feature / Brawler | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.cybernetic_implant | feature / Cybernetic Implant | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.point_blank_execution | feature / Point Blank Execution | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.suppressive_discipline | feature / Suppressive Discipline | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.field_armourer | feature / Field Armourer | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.bayonet_fighter | feature / Bayonet Fighter | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.breacher | feature / Breacher | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.crisis_runner | feature / Crisis Runner | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.dead_calm | feature / Dead Calm | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.tactical_reposition | feature / Tactical Reposition | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.weapon_specialist | feature / Weapon Specialist | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.armour_familiarity | feature / Armour Familiarity | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.relic_bearer | feature / Relic-Bearer | 73 / 86 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.ogryn_wall | feature / Ogryn Wall | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.bigger_gun | feature / Bigger Gun | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.loyal_as_stone | feature / Loyal as Stone | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.bone_ead_implant | feature / Bone ’ead Implant | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.too_angry_to_notice | feature / Too Angry to Notice | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.ratling_vanish | feature / Ratling Vanish | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.impossible_shot | feature / Impossible Shot | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.pocket_marksman | feature / Pocket Marksman | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.scavvers_luck | feature / Scavver’s Luck | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.cooks_morale | feature / Cook’s Morale | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.machine_precision | feature / Machine Precision | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.sacred_augmetics | feature / Sacred Augmetics | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.rad_hardened | feature / Rad-Hardened | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.noospheric_burst | feature / Noospheric Burst | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.cold_logic | feature / Cold Logic | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.witch_sight | feature / Witch-Sight | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.imperial_flexibility | feature / Imperial Flexibility | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.last_order_standing | feature / Last Order Standing | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.sanctioning_scars | feature / Sanctioning Scars | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.hive_blooded | feature / Hive-Blooded | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.ancestors_grudge | feature / Ancestor’s Grudge | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.hold_born_engineer | feature / Hold-Born Engineer | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.void_stock | feature / Void Stock | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.iron_stance | feature / Iron Stance | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.kin_weapon_master | feature / Kin Weapon Master | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.aeldari_grace | feature / Aeldari Grace | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.path_discipline | feature / Path Discipline | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.rangers_cloak | feature / Ranger’s Cloak | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.witchblade_adept | feature / Witchblade Adept | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.talent.alien_reflexes | feature / Alien Reflexes | 74 / 87 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_1_1 | rule / Design Goals | 2 / 15 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_1_2 | rule / Core System | 2 / 15 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_1_3 | rule / Character Tiers | 2 / 15 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_1_4 | rule / Proficiency Bonus | 2 / 15 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_1_5 | rule / Rules Priority | 2 / 15 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_1 | rule / Ability Scores | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_2 | rule / Hit Points | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_3 | rule / Species and Class Restrictions | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_3_1 | rule / Class at a Glance | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_1 | rule / Ogryns | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_2 | rule / Skitarii | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_3 | rule / Psykers | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_4 | rule / Ratlings | 4 / 17 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_5 | rule / Squats / Kin | 5 / 18 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_4_6 | rule / Aeldari / Eldar | 5 / 18 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_2_5 | rule / Skills and Ability Checks | 5 / 18 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_1 | rule / Turns and Actions | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_2 | rule / Cover | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_3 | rule / Suppression | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_4 | rule / Reload | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_5 | rule / Close-Quarters Shooting | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_6 | rule / Critical Hits | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_7 | rule / Dropping to 0 Hit Points | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_8 | rule / Stabilising and Recovery | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_9 | rule / Ranged Attacks and Range | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_10 | rule / Opportunity Attacks | 19 / 32 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_11 | rule / Grappling and Shoving | 19 / 32 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_12 | rule / Two-Weapon Fighting | 19 / 32 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_13 | rule / Rest and Recovery | 19 / 32 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_6_14 | rule / Conditions and Battlefield States | 19 / 32 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_1 | rule / Psychic Save DC | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_2 | rule / Psychic Attack Modifier | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_3 | rule / Known Powers | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_4 | rule / Psychic Power Cost and Empowered Powers | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_5 | rule / Minor Psychic Powers | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_6 | rule / Standard Psychic Powers | 79 / 92 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_7 | rule / Major Psychic Powers | 80 / 93 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_14_8 | rule / Warlock Rune Powers | 80 / 93 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_1 | rule / Warp Pressure | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_2 | rule / Reducing Warp Pressure | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_3 | rule / Perils Severity | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_1 | rule / Warp Static | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_2 | rule / Bleeding Eyes | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_3 | rule / Soul Echo | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_4 | rule / Warp Scream | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_5 | rule / Possession Pressure | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_6 | rule / Uncontrolled Manifestation | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_7 | rule / Reality Tear | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_4_8 | rule / Catastrophic Perils | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_5 | rule / After Perils | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_6 | rule / Aeldari Warlock Perils | 83 / 96 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_15_7 | rule / Malefic-Touched Perils | 83 / 96 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_16_1 | rule / Gaining Corruption | 85 / 98 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_16_2 | rule / Corruption Track | 85 / 98 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_16_3 | rule / Corruption Scars | 85 / 98 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_16_4 | rule / Reducing Corruption | 85 / 98 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_1 | rule / Availability | 90 / 103 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_2 | rule / Requisition Test | 90 / 103 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_3 | rule / Requisition Outcomes | 90 / 103 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_4 | rule / Xenos, Forbidden and Black-Market Gear | 90 / 103 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_5 | rule / Provenance and Faction Access | 90 / 103 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_6 | rule / Equipment by Character Tier | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_7 | rule / Weapon Modifications | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_8 | rule / Master-Crafted Wargear | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_9 | rule / Specialist Ammunition and Charges | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_10 | rule / Salvage and Captured Equipment | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_11 | rule / Item Condition and Repair | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_12 | rule / Replacing Lost or Destroyed Equipment | 93 / 106 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_13 | rule / Trading, Gifts and Ownership | 93 / 106 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14 | rule / Exotic, Relic and Unique Wargear | 93 / 106 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_1 | rule / Signature Wargear | 93 / 106 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_2 | rule / Exotic Wargear | 93 / 106 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_3 | rule / Archeotech | 94 / 107 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_4 | rule / Faction Relics | 94 / 107 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_5 | rule / Unique Wargear | 95 / 108 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_18_14_6 | rule / Creating Additional Relics | 95 / 108 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_19_1 | rule / When to Use a Lasting Injury | 97 / 110 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_19_2 | rule / Lasting Injury Table | 97 / 110 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_19_3 | rule / Medical Care | 97 / 110 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_19_4 | rule / Augmetic Replacement | 97 / 110 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_20_1 | rule / When You Gain a Level | 99 / 112 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_20_2 | rule / Retraining | 99 / 112 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_1 | rule / Profiles and Crew | 101 / 114 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_2 | rule / Driving and Movement | 101 / 114 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_3 | rule / Actions and Attacks | 102 / 115 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_4 | rule / Collisions | 102 / 115 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_5 | rule / Hull Damage and Breakdowns | 103 / 116 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_6 | rule / Boarding and Disembarking | 103 / 116 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_7 | rule / Chases | 104 / 117 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_8 | rule / Repairs and Resupply | 104 / 117 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_9 | rule / Requisition and Modifications | 105 / 118 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_10 | rule / Civilian and Imperial Scouts | 106 / 119 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.rule.phb_21_11 | rule / Weapon Profiles | 108 / 121 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.training | feature / Veteran training and hit die | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_1.guardsman_training | feature / Guardsman Training | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_1.tactical_aim | feature / Tactical Aim | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_2.suppressing_fire | feature / Suppressing Fire | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_3.regimental_doctrine | feature / Regimental Doctrine | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_5.extra_attack | feature / Extra Attack | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_6.fire_team_veteran | feature / Fire Team Veteran | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_7.doctrine_feature | feature / Doctrine Feature | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_9.hold_the_line | feature / Hold the Line | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_10.killing_zone | feature / Killing Zone | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_11.veterans_accuracy | feature / Veteran’s Accuracy | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_13.battlefield_instinct | feature / Battlefield Instinct | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_14.improved_doctrine | feature / Improved Doctrine | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_15.kill_confirmed | feature / Kill Confirmed | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_17.veterans_command | feature / Veteran's Command | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_18.dug_in_kill_team | feature / Dug-In Kill Team | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.veteran.level_20.lord_castellans_moment | feature / Lord Castellan's Moment | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.veteran | progression / Veteran progression | 37 / 50 | READY | PARTIALLY_STRUCTURED |
| di.class.veteran | class / Veteran | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.training | feature / Zealot training and hit die | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_1.fury_of_faith | feature / Fury of Faith | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_1.martyrs_endurance | feature / Martyr’s Endurance | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_1.martyrs_mercy | feature / Martyr’s Mercy | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_2.charge_of_conviction | feature / Charge of Conviction | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_3.sacred_path | feature / Sacred Path | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_5.extra_attack | feature / Extra Attack | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_6.blood_and_benediction | feature / Blood and Benediction | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_7.sacred_path_feature | feature / Sacred Path Feature | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_9.refuse_the_dark | feature / Refuse the Dark | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_10.sainted_fury | feature / Sainted Fury | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_11.martyrs_renewal | feature / Martyr’s Renewal | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_13.unbroken_creed | feature / Unbroken Creed | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_14.sacred_path_feature | feature / Sacred Path Feature | 41 / 54 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_15.living_saints_shadow | feature / Living Saint’s Shadow | 41 / 54 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_17.martyrdom_unending | feature / Martyrdom Unending | 41 / 54 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_18.sacred_path_ascendant | feature / Sacred Path Ascendant | 41 / 54 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.zealot.level_20.living_icon_of_wrath | feature / Living Icon of Wrath | 41 / 54 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.zealot | progression / Zealot progression | 40 / 53 | READY | PARTIALLY_STRUCTURED |
| di.class.zealot | class / Zealot | 40 / 53 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.training | feature / Psyker training and hit die | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_1.psychic_discipline | feature / Psychic Discipline | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_1.warp_pressure | feature / Warp Pressure | 82 / 95 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_2.psychic_ward | feature / Psychic Ward | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_3.discipline_feature | feature / Discipline Feature | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_5.empowered_manifestation | feature / Empowered Manifestation | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_6.disciplined_channel | feature / Disciplined Channel | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_7.discipline_feature | feature / Discipline Feature | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_9.warp_anchor | feature / Warp Anchor | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_10.mastered_manifestation | feature / Mastered Manifestation | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_11.major_power_access | feature / Major Power Access | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_13.sanctioned_focus | feature / Sanctioned Focus | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_14.discipline_feature | feature / Discipline Feature | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_15.alpha_level_risk | feature / Alpha-Level Risk | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_17.soul_bound_discipline | feature / Soul-Bound Discipline | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_18.warp_crowned_focus | feature / Warp-Crowned Focus | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.psyker.level_20.sanctioned_apex | feature / Sanctioned Apex | 44 / 57 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.psyker | progression / Psyker progression | 43 / 56 | READY | PARTIALLY_STRUCTURED |
| di.class.psyker | class / Psyker | 43 / 56 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.training | feature / Ogryn Skullbreaker training and hit die | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_1.big_lad | feature / Big Lad | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_1.loyal_protector | feature / Loyal Protector | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_2.brutal_impact | feature / Brutal Impact | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_3.ogryn_role | feature / Ogryn Role | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_5.extra_attack | feature / Extra Attack | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_6.too_stubborn_to_drop | feature / Too Stubborn to Drop | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_7.role_feature | feature / Role Feature | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_9.living_barricade | feature / Living Barricade | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_10.thunderous_violence | feature / Thunderous Violence | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_11.bigger_and_meaner | feature / Bigger and Meaner | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_13.cant_keep_him_down | feature / Can’t Keep Him Down | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_14.role_feature | feature / Role Feature | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_15.walking_fortress | feature / Walking Fortress | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_17.mountain_of_muscle | feature / Mountain of Muscle | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_18.role_feature | feature / Role Feature | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ogryn_skullbreaker.level_20.unkillable_big_lad | feature / Unkillable Big Lad | 47 / 60 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.ogryn_skullbreaker | progression / Ogryn Skullbreaker progression | 46 / 59 | READY | PARTIALLY_STRUCTURED |
| di.class.ogryn_skullbreaker | class / Ogryn Skullbreaker | 46 / 59 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.training | feature / Arbites Enforcer training and hit die | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_1.enforcer_training | feature / Enforcer Training | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_1.authority | feature / Authority | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_2.breach_and_clear | feature / Breach and Clear | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_3.enforcement_doctrine | feature / Enforcement Doctrine | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_5.extra_attack | feature / Extra Attack | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_6.lockdown_order | feature / Lockdown Order | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_7.doctrine_feature | feature / Doctrine Feature | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_9.no_escape | feature / No Escape | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_10.judgement_protocol | feature / Judgement Protocol | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_11.riot_control | feature / Riot Control | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_13.legal_terror | feature / Legal Terror | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_14.doctrine_feature | feature / Doctrine Feature | 50 / 63 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_15.sentence_executed | feature / Sentence Executed | 50 / 63 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_17.absolute_jurisdiction | feature / Absolute Jurisdiction | 50 / 63 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_18.doctrine_feature | feature / Doctrine Feature | 50 / 63 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.arbites_enforcer.level_20.final_sentence | feature / Final Sentence | 50 / 63 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.arbites_enforcer | progression / Arbites Enforcer progression | 49 / 62 | READY | PARTIALLY_STRUCTURED |
| di.class.arbites_enforcer | class / Arbites Enforcer | 49 / 62 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.training | feature / Hive Scum training and hit die | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_1.dirty_fighter | feature / Dirty Fighter | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_1.streetwise | feature / Streetwise | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_2.cunning_action | feature / Cunning Action | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_3.gang_style | feature / Gang Style | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_5.backstabber_3d6 | feature / Backstabber +3d6 | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_6.low_cunning | feature / Low Cunning | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_7.gang_style_feature | feature / Gang Style Feature | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_9.vanish_into_trouble | feature / Vanish into Trouble | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_10.knife_edge_survivor | feature / Knife-Edge Survivor | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_11.backstabber_4d6 | feature / Backstabber +4d6 | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_13.underhive_reputation | feature / Underhive Reputation | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_14.gang_style_feature | feature / Gang Style Feature | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_15.backstabber_5d6 | feature / Backstabber +5d6 | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_17.no_honour | feature / No Honour | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_17.no_problem | feature / No Problem | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_18.backstabber_6d6 | feature / Backstabber +6d6 | 53 / 66 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hive_scum.level_20.king_of_the_underhive | feature / King of the Underhive | 53 / 66 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.hive_scum | progression / Hive Scum progression | 52 / 65 | READY | PARTIALLY_STRUCTURED |
| di.class.hive_scum | class / Hive Scum | 52 / 65 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.training | feature / Ratling Sharpshooter training and hit die | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_1.small_target | feature / Small Target | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_1.deadeye | feature / Deadeye | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_2.scamper | feature / Scamper | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_3.ratling_trick | feature / Ratling Trick | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_5.killshot | feature / Killshot | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_6.cameleoline_habits | feature / Cameleoline Habits | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_7.ratling_trick_feature | feature / Ratling Trick Feature | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_9.impossible_angle | feature / Impossible Angle | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_10.perfect_shot | feature / Perfect Shot | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_11.deadeye_3d6 | feature / Deadeye +3d6 | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_13.gone_before_the_shot | feature / Gone Before the Shot | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_14.ratling_trick_feature | feature / Ratling Trick Feature | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_15.ghost_marksman | feature / Ghost Marksman | 56 / 69 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_17.deadeye_4d6 | feature / Deadeye +4d6 | 56 / 69 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_18.ratling_trick_feature | feature / Ratling Trick Feature | 56 / 69 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.ratling_sharpshooter.level_20.impossible_little_legend | feature / Impossible Little Legend | 56 / 69 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.ratling_sharpshooter | progression / Ratling Sharpshooter progression | 55 / 68 | READY | PARTIALLY_STRUCTURED |
| di.class.ratling_sharpshooter | class / Ratling Sharpshooter | 55 / 68 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.training | feature / Skitarii Veteran training and hit die | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_1.machine_focus | feature / Machine Focus | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_1.targeting_protocol | feature / Targeting Protocol | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_2.augmetic_reflexes | feature / Augmetic Reflexes | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_3.combat_protocol | feature / Combat Protocol | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_5.extra_attack | feature / Extra Attack | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_6.doctrinal_subroutine | feature / Doctrinal Subroutine | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_7.protocol_feature | feature / Protocol Feature | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_9.blessed_autosenses | feature / Blessed Autosenses | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_10.omnissian_execution | feature / Omnissian Execution | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_11.calculated_volley | feature / Calculated Volley | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_13.redundant_systems | feature / Redundant Systems | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_14.protocol_feature | feature / Protocol Feature | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_15.will_of_the_omnissiah | feature / Will of the Omnissiah | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_17.perfect_targeting_logic | feature / Perfect Targeting Logic | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_18.protocol_feature | feature / Protocol Feature | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.skitarii_veteran.level_20.living_instrument_of_the_omnissiah | feature / Living Instrument of the Omnissiah | 59 / 72 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.skitarii_veteran | progression / Skitarii Veteran progression | 58 / 71 | READY | PARTIALLY_STRUCTURED |
| di.class.skitarii_veteran | class / Skitarii Veteran | 58 / 71 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.training | feature / Kin Armsman training and hit die | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_1.kin_training | feature / Kin Training | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_1.oath_mark | feature / Oath-Mark | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_2.steady_advance | feature / Steady Advance | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_3.hold_doctrine | feature / Hold Doctrine | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_5.extra_attack | feature / Extra Attack | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_6.grudge_settled | feature / Grudge Settled | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_7.doctrine_feature | feature / Doctrine Feature | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_9.void_hardened_line | feature / Void-Hardened Line | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_10.ancestral_wrath | feature / Ancestral Wrath | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_11.kinfire_drill | feature / Kinfire Drill | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_13.iron_compact | feature / Iron Compact | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_14.doctrine_feature | feature / Doctrine Feature | 62 / 75 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_15.holdfast_champion | feature / Holdfast Champion | 62 / 75 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_17.grudge_bound_advance | feature / Grudge-Bound Advance | 62 / 75 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_18.doctrine_feature | feature / Doctrine Feature | 62 / 75 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.kin_armsman.level_20.ancestor_core_champion | feature / Ancestor-Core Champion | 62 / 75 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.kin_armsman | progression / Kin Armsman progression | 61 / 74 | READY | PARTIALLY_STRUCTURED |
| di.class.kin_armsman | class / Kin Armsman | 61 / 74 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.training | feature / Hernkyn Prospector training and hit die | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_1.prospector_training | feature / Prospector Training | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_1.claim_sight | feature / Claim Sight | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_2.surveyors_step | feature / Surveyor’s Step | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_3.expedition_role | feature / Expedition Role | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_5.extra_attack | feature / Extra Attack | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_6.mark_the_seam | feature / Mark the Seam | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_7.expedition_feature | feature / Expedition Feature | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_9.outriders_escape | feature / Outrider’s Escape | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_10.perfect_claim | feature / Perfect Claim | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_11.deep_scan | feature / Deep Scan | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_13.no_stone_unturned | feature / No Stone Unturned | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_14.expedition_feature | feature / Expedition Feature | 65 / 78 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_15.master_prospector | feature / Master Prospector | 65 / 78 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_17.legendary_claim_staker | feature / Legendary Claim-Staker | 65 / 78 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_18.expedition_feature | feature / Expedition Feature | 65 / 78 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.hernkyn_prospector.level_20.claim_the_horizon | feature / Claim the Horizon | 65 / 78 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.hernkyn_prospector | progression / Hernkyn Prospector progression | 64 / 77 | READY | PARTIALLY_STRUCTURED |
| di.class.hernkyn_prospector | class / Hernkyn Prospector | 64 / 77 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.training | feature / Aeldari Outcast training and hit die | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_1.ranger_training | feature / Ranger Training | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_1.shuriken_grace | feature / Shuriken Grace | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_2.ghostwalk | feature / Ghostwalk | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_3.outcast_path | feature / Outcast Path | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_5.extra_attack | feature / Extra Attack | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_6.unseen_shot | feature / Unseen Shot | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_7.path_feature | feature / Path Feature | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_9.webway_instinct | feature / Webway Instinct | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_10.death_from_elsewhere | feature / Death from Elsewhere | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_11.perfect_motion | feature / Perfect Motion | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_13.vanish_beyond_sight | feature / Vanish Beyond Sight | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_14.path_feature | feature / Path Feature | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_15.mythic_outcast | feature / Mythic Outcast | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_17.pathless_perfection | feature / Pathless Perfection | 68 / 81 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_18.path_feature | feature / Path Feature | 68 / 81 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_outcast.level_20.legend_of_the_wandering_path | feature / Legend of the Wandering Path | 68 / 81 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.aeldari_outcast | progression / Aeldari Outcast progression | 67 / 80 | READY | PARTIALLY_STRUCTURED |
| di.class.aeldari_outcast | class / Aeldari Outcast | 67 / 80 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.training | feature / Aeldari Warlock training and hit die | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_1.runes_of_battle | feature / Runes of Battle | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_1.witchblade_training | feature / Witchblade Training | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_2.rune_ward | feature / Rune Ward | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_3.warlock_path | feature / Warlock Path | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_4.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_5.empowered_rune | feature / Empowered Rune | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_6.battle_seer | feature / Battle-Seer | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_7.path_feature | feature / Path Feature | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_8.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_9.ghosthelm_discipline | feature / Ghosthelm Discipline | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_10.war_rune_mastery | feature / War-Rune Mastery | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_11.major_rune_access | feature / Major Rune Access | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_12.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_13.fate_splitter | feature / Fate Splitter | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_14.path_feature | feature / Path Feature | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_15.storm_of_runes | feature / Storm of Runes | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_16.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_17.spirit_rune_focus | feature / Spirit-Rune Focus | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_18.path_feature | feature / Path Feature | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_19.ability_score_improvement_talent | feature / Ability Score Improvement / Talent | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.class.aeldari_warlock.level_20.farseers_echo | feature / Farseer's Echo | 71 / 84 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.aeldari_warlock | progression / Aeldari Warlock progression | 70 / 83 | READY | PARTIALLY_STRUCTURED |
| di.class.aeldari_warlock | class / Aeldari Warlock | 70 / 83 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.shock_trooper.level_3 | feature / Shock Trooper 3 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.shock_trooper.level_7 | feature / Shock Trooper 7 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.shock_trooper.level_14 | feature / Shock Trooper 14 | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.subclass.veteran.shock_trooper | progression / Shock Trooper progression | 37 / 50 | READY | PARTIALLY_STRUCTURED |
| di.subclass.veteran.shock_trooper | subclass / Shock Trooper | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.marksman.level_3 | feature / Marksman 3 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.marksman.level_7 | feature / Marksman 7 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.marksman.level_14 | feature / Marksman 14 | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.subclass.veteran.marksman | progression / Marksman progression | 37 / 50 | READY | PARTIALLY_STRUCTURED |
| di.subclass.veteran.marksman | subclass / Marksman | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.sergeant.level_3 | feature / Sergeant 3 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.sergeant.level_7 | feature / Sergeant 7 | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.subclass.veteran.sergeant.level_14 | feature / Sergeant 14 | 38 / 51 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.progression.subclass.veteran.sergeant | progression / Sergeant progression | 37 / 50 | READY | PARTIALLY_STRUCTURED |
| di.subclass.veteran.sergeant | subclass / Sergeant | 37 / 50 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.choice.veteran.subclass | choice / Regimental Doctrine | 37 / 50 | READY | STRUCTURED |
| di.choice.veteran.starting_skills | choice / Choose 2 skill proficiency | 37 / 50 | READY | STRUCTURED |
| di.damage_type.bludgeoning | damage_type / Bludgeoning | 25 / 38 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.fire | damage_type / Fire | 24 / 37 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.force | damage_type / Force | 27 / 40 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.lightning | damage_type / Lightning | 27 / 40 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.necrotic | damage_type / Necrotic | 80 / 93 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.piercing | damage_type / Piercing | 24 / 37 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.poison | damage_type / Poison | 24 / 37 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.psychic | damage_type / Psychic | 80 / 93 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.radiant | damage_type / Radiant | 24 / 37 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.radiation | damage_type / Radiation | 27 / 40 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.slashing | damage_type / Slashing | 25 / 38 | READY | PARTIALLY_STRUCTURED |
| di.damage_type.thunder | damage_type / Thunder | 24 / 37 | READY | PARTIALLY_STRUCTURED |
| di.armour.ogryn_leathers | armour / Ogryn Leathers | 29 / 42 | READY | PARTIALLY_STRUCTURED |
| di.shield.shield | shield / Shield | 29 / 42 | READY | PARTIALLY_STRUCTURED |
| di.action.lasgun.base_damage | action / Lasgun base damage | 24 / 37 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.warp_spark.base_damage | action / Warp Spark base damage | 78 / 91 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.weapon.stub_pistol | weapon / Stub Pistol | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.laspistol | weapon / Laspistol | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.autopistol | weapon / Autopistol | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.hand_cannon | weapon / Hand Cannon | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.bolt_pistol | weapon / Bolt Pistol | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.plasma_pistol | weapon / Plasma Pistol | 24 / 37 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.melta_pistol | weapon / Melta Pistol | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.stub_rifle | weapon / Stub Rifle | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.lascarbine | weapon / Lascarbine | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.lasgun | weapon / Lasgun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.hot_shot_lasgun | weapon / Hot-Shot Lasgun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.autogun | weapon / Autogun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.shotgun | weapon / Shotgun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.combat_shotgun | weapon / Combat Shotgun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.long_las | weapon / Long-Las | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.needle_rifle | weapon / Needle Rifle | 24 / 37 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.bolter | weapon / Bolter | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.combi_bolter | weapon / Combi-Bolter | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.flamer | weapon / Flamer | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.plasma_gun | weapon / Plasma Gun | 24 / 37 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.meltagun | weapon / Meltagun | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.grenade_launcher | weapon / Grenade Launcher | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.heavy_stubber | weapon / Heavy Stubber | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.heavy_bolter | weapon / Heavy Bolter | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.multi_laser | weapon / Multi-Laser | 24 / 37 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.knife | weapon / Knife | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.combat_blade | weapon / Combat Blade | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.trench_club | weapon / Trench Club | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.maul | weapon / Maul | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.shock_maul | weapon / Shock Maul | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.chain_knife | weapon / Chain Knife | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.chainsword | weapon / Chainsword | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.heavy_chainsword | weapon / Heavy Chainsword | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.power_sword | weapon / Power Sword | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.power_axe | weapon / Power Axe | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.power_maul | weapon / Power Maul | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.thunder_hammer | weapon / Thunder Hammer | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.force_sword | weapon / Force Sword | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.force_staff | weapon / Force Staff | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.omnissian_axe | weapon / Omnissian Axe | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.relic_blade | weapon / Relic Blade | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.heavy_axe | weapon / Heavy Axe | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ripper_gun | weapon / Ripper Gun | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.kickback_shotgun | weapon / Kickback Shotgun | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.grenadier_gauntlet | weapon / Grenadier Gauntlet | 25 / 38 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.twin_linked_heavy_stubber | weapon / Twin-Linked Heavy Stubber | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ogryn_club | weapon / Ogryn Club | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.big_friendly_rock | weapon / Big Friendly Rock | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.brute_shield_bash | weapon / Brute Shield Bash | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.power_maul_ogryn_pattern | weapon / Power Maul, Ogryn Pattern | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.industrial_cutter | weapon / Industrial Cutter | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.slab_hammer | weapon / Slab Hammer | 25 / 38 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.autoch_pattern_pistol | weapon / Autoch-Pattern Pistol | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.bolt_revolver | weapon / Bolt Revolver | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ion_pistol | weapon / Ion Pistol | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.autoch_pattern_bolter | weapon / Autoch-Pattern Bolter | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ion_blaster | weapon / Ion Blaster | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.magna_rail_rifle | weapon / Magna-Rail Rifle | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.plasma_beamer | weapon / Plasma Beamer | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.etacarn_mining_tool | weapon / EtaCarn Mining Tool | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.concussion_hammer | weapon / Concussion Hammer | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.kin_power_axe | weapon / Kin Power Axe | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.plasma_axe | weapon / Plasma Axe | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.concussion_gauntlet | weapon / Concussion Gauntlet | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.shuriken_pistol | weapon / Shuriken Pistol | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.shuriken_catapult | weapon / Shuriken Catapult | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ranger_long_rifle | weapon / Ranger Long Rifle | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.aeldari_lasblaster | weapon / Aeldari Lasblaster | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.fusion_gun | weapon / Fusion Gun | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.death_spinner | weapon / Death Spinner | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.witchblade | weapon / Witchblade | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.singing_spear | weapon / Singing Spear | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.aeldari_power_sword | weapon / Aeldari Power Sword | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.monomolecular_blade | weapon / Monomolecular Blade | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.corsair_sabre | weapon / Corsair Sabre | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.star_glaive | weapon / Star Glaive | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.ghostsword | weapon / Ghostsword | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.biting_blade | weapon / Biting Blade | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.executioner_blade | weapon / Executioner Blade | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.galvanic_rifle | weapon / Galvanic Rifle | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.radium_carbine | weapon / Radium Carbine | 27 / 40 | AMBIGUOUS | PARTIALLY_STRUCTURED |
| di.weapon.arc_pistol | weapon / Arc Pistol | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.arc_rifle | weapon / Arc Rifle | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.taser_goad | weapon / Taser Goad | 27 / 40 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.heavy_clothing | armour / Heavy Clothing | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.armoured_bodyglove | armour / Armoured Bodyglove | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.flak_vest | armour / Flak Vest | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.flak_armour | armour / Flak Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.flak_greatcoat | armour / Flak Greatcoat | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.mesh_armour | armour / Mesh Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.scout_carapace | armour / Scout Carapace | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.carapace_armour | armour / Carapace Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.riot_armour | armour / Riot Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.void_suit_armoured | armour / Void Suit, Armoured | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.hazard_plate | armour / Hazard Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.powered_carapace | armour / Powered Carapace | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.refractor_field | equipment / Refractor Field | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.conversion_field | equipment / Conversion Field | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.ogryn_flak_plate | armour / Ogryn Flak Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.ogryn_plate | armour / Ogryn Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.bullgryn_plate | armour / Bullgryn Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.shield.slab_shield | shield / Slab Shield | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.shield.brute_shield_harness | shield / Brute Shield Harness | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.kin_void_suit | armour / Kin Void Suit | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.kin_mesh | armour / Kin Mesh | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.hearthkyn_plate | armour / Hearthkyn Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.exo_frame_plate | armour / Exo-Frame Plate | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.prospector_rig | armour / Prospector Rig | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.aeldari_mesh | armour / Aeldari Mesh | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.ranger_weave | armour / Ranger Weave | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.rune_armour | armour / Rune Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.aspect_pattern_armour | armour / Aspect-Pattern Armour | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.holo_field_cloak | equipment / Holo-Field Cloak | 29 / 42 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.warp_spark | power / Warp Spark | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.kinetic_push | power / Kinetic Push | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.mind_lumen | power / Mind Lumen | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.static_veil | power / Static Veil | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.flesh_knit | power / Flesh Knit | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.pain_spike | power / Pain Spike | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.ember_flicker | power / Ember Flicker | 78 / 91 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.ashen_brand | power / Ashen Brand | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.danger_sense | power / Danger Sense | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.echo_read | power / Echo Read | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.whisper_from_below | power / Whisper from Below | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.warp_bite | power / Warp Bite | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.null_glare | power / Null Glare | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.blank_sense | power / Blank Sense | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.focused_rupture | power / Focused Rupture | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.assail | power / Assail | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.psychic_shield | power / Psychic Shield | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.soulfire | power / Soulfire | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.dominate_nerve | power / Dominate Nerve | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.warp_step | power / Warp Step | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.blood_surge | power / Blood Surge | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.toxic_bloom | power / Toxic Bloom | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.kinetic_bulwark | power / Kinetic Bulwark | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.crush_grip | power / Crush Grip | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.fates_nudge | power / Fate’s Nudge | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.prescient_aim | power / Prescient Aim | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.cleansing_wave | power / Cleansing Wave | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.burning_halo | power / Burning Halo | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.terror_echo | power / Terror Echo | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.baleful_rupture | power / Baleful Rupture | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.null_field | power / Null Field | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.silence_the_witch | power / Silence the Witch | 79 / 92 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.telekinetic_crush | power / Telekinetic Crush | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.inferno_bloom | power / Inferno Bloom | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.prescient_execution | power / Prescient Execution | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.biomantic_surge | power / Biomantic Surge | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.flesh_reforged | power / Flesh Reforged | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.hemorrhage | power / Hemorrhage | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.force_dome | power / Force Dome | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.foresight_cascade | power / Foresight Cascade | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.soulstorm | power / Soulstorm | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.malefic_door | power / Malefic Door | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.possession_spike | power / Possession Spike | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.pariah_zone | power / Pariah Zone | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.conceal | power / Conceal | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.reveal | power / Reveal | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.protect | power / Protect | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.jinx | power / Jinx | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.quicken | power / Quicken | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.restrain_fate | power / Restrain Fate | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.destructor_rune | power / Destructor Rune | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.power.fortune_thread | power / Fortune Thread | 80 / 93 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.autocannon | weapon / Autocannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.lascannon | weapon / Lascannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.battle_cannon | weapon / Battle cannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.bolt_cannon | weapon / Bolt cannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.hylas_rotary_cannon | weapon / HYLas rotary cannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.magna_coil_autocannon | weapon / Magna-coil autocannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.scatter_laser | weapon / Scatter laser | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.shuriken_cannon | weapon / Shuriken cannon | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.twin_shuriken_catapults | weapon / Twin shuriken catapults | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.pulse_laser | weapon / Pulse laser | 108 / 121 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.action.attack | action / Attack | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.dash | action / Dash | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.disengage | action / Disengage | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.dodge | action / Dodge | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.help | action / Help | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.hide | action / Hide | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.ready | action / Ready | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.reload | action / Reload | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.action.use_mission_gear | action / Use Mission Gear | 18 / 31 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.vehicle.civilian_autocar | vehicle / Civilian Autocar | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.cargo_hauler | vehicle / Cargo Hauler | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.hive_outrider_bike | vehicle / Hive Outrider Bike | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.armoured_utility_truck | vehicle / Armoured Utility Truck | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.scout_sentinel | vehicle / Scout Sentinel | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.taurox | vehicle / Taurox | 106 / 119 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.chimera | vehicle / Chimera | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.leman_russ_battle_tank | vehicle / Leman Russ Battle Tank | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.sagitaur | vehicle / Sagitaur | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.hernkyn_pioneer_bike | vehicle / Hernkyn Pioneer Bike | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.aeldari_vyper | vehicle / Aeldari Vyper | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.vehicle.falcon_grav_tank | vehicle / Falcon Grav-tank | 107 / 120 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.blinded | condition / Blinded | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.bloodied | condition / Bloodied | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.charmed | condition / Charmed | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.frightened | condition / Frightened | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.grappled | condition / Grappled | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.hidden | condition / Hidden | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.incapacitated | condition / Incapacitated | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.invisible | condition / Invisible | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.poisoned | condition / Poisoned | 19 / 32 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.prone | condition / Prone | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.restrained | condition / Restrained | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.stunned | condition / Stunned | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.suppressed | condition / Suppressed | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.surprised | condition / Surprised | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.unconscious | condition / Unconscious | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.reinforced_plates | system / Reinforced Plates | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.sealed_system | system / Sealed System | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.camo_weave | system / Camo Weave | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.shock_insulation | system / Shock Insulation | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.mag_boots_anchor_rig | system / Mag Boots / Anchor Rig | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.medicae_harness | system / Medicae Harness | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.servo_assist | system / Servo Assist | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.hexagrammic_lining | system / Hexagrammic Lining | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.reinforced_harness | system / Reinforced Harness | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.slab_lock_bracing | system / Slab-Lock Bracing | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.recoil_yoke | system / Recoil Yoke | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.blast_baffles | system / Blast Baffles | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.ablative_ceramite | system / Ablative Ceramite | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.rad_seal_shrouds | system / Rad-Seal Shrouds | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.servo_bracing | system / Servo-Bracing | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.noospheric_armour_link | system / Noospheric Armour Link | 31 / 44 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.void_seal_redundancy | system / Void-Seal Redundancy | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.grav_anchor_spurs | system / Grav-Anchor Spurs | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.ancestor_wrought_plating | system / Ancestor-Wrought Plating | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.exo_servo_overdrive | system / Exo-Servo Overdrive | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.holo_weave_matrix | system / Holo-Weave Matrix | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.spirit_stone_lattice | system / Spirit-Stone Lattice | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.adaptive_weave | system / Adaptive Weave | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.armour.ghostplate_flexors | system / Ghostplate Flexors | 32 / 45 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.frag_grenade | weapon / Frag Grenade | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.frag_bomb | weapon / Frag Bomb | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.krak_grenade | weapon / Krak Grenade | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.smoke_grenade | weapon / Smoke Grenade | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.stun_grenade | weapon / Stun Grenade | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.firebomb | weapon / Firebomb | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.rad_grenade | weapon / Rad Grenade | 34 / 47 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.optical_implant | augmetic / Optical Implant | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.bionic_arm | augmetic / Bionic Arm | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.bionic_legs | augmetic / Bionic Legs | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.subdermal_plating | augmetic / Subdermal Plating | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.respirator_implant | augmetic / Respirator Implant | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.data_jack | augmetic / Data-Jack | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.vox_implant | augmetic / Vox Implant | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.pain_editor | augmetic / Pain Editor | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.recoil_bracing | augmetic / Recoil Bracing | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.targeting_lens | augmetic / Targeting Lens | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.mag_lock_palm | augmetic / Mag-Lock Palm | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.skeletal_reinforcement | augmetic / Skeletal Reinforcement | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.dermal_insulation | augmetic / Dermal Insulation | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.chem_injector | augmetic / Chem Injector | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.internal_chrono | augmetic / Internal Chrono | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.mechadendrite_utility | augmetic / Mechadendrite, Utility | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.mechadendrite_medicae | augmetic / Mechadendrite, Medicae | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.mechadendrite_combat | augmetic / Mechadendrite, Combat | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.cranial_cogitator | augmetic / Cranial Cogitator | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.augmetic_heart | augmetic / Augmetic Heart | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.black_iron_jaw | augmetic / Black-Iron Jaw | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.augmetic.vocal_coder | augmetic / Vocal Coder | 76 / 89 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.med_stim | equipment / Med-Stim | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.med_pack | equipment / Med-Pack | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.field_dressing | equipment / Field Dressing | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.ammo_pack | equipment / Ammo Pack | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.specialist_ammo_pack | equipment / Specialist Ammo Pack | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.grenade_bandolier | equipment / Grenade Bandolier | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.weapon_maintenance_kit | equipment / Weapon Maintenance Kit | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.auspex_battery | equipment / Auspex Battery | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.rebreather_filter | equipment / Rebreather Filter | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.void_patch_kit | equipment / Void Patch Kit | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.stimm_slug | equipment / Stimm Slug | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.purity_seal_charm | equipment / Purity Seal Charm | 88 / 101 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.bayonet_breaching_lug | system / Bayonet / Breaching Lug | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.extended_magazine_charge_pack | system / Extended Magazine / Charge Pack | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.reflex_sight | system / Reflex Sight | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.camo_wrap_low_signature_furniture | system / Camo Wrap / Low-Signature Furniture | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.recoil_compensation | system / Recoil Compensation | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.targeting_optic | system / Targeting Optic | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.reinforced_action | system / Reinforced Action | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.sanctified_fittings | system / Sanctified Fittings | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.weapon.archeotech_interface | system / Archeotech Interface | 91 / 104 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.feature.masterwork.perfect_balance | feature / Perfect Balance | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.artificer_edge | feature / Artificer Edge | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.precision_barrel_focusing_array | feature / Precision Barrel / Focusing Array | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.rapid_feed | feature / Rapid Feed | 91 / 104 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.recoil_compensation | feature / Recoil Compensation | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.compact_pattern | feature / Compact Pattern | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.artificer_armour | feature / Artificer Armour | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.responsive_plating | feature / Responsive Plating | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.feature.masterwork.sealed_systems | feature / Sealed Systems | 92 / 105 | MANUAL_RULE | PARTIALLY_STRUCTURED |
| di.ammunition.tracer_target_marking | ammunition / Tracer / Target-Marking | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.manstopper | ammunition / Manstopper | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.armour_piercing | ammunition / Armour-Piercing | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.incendiary | ammunition / Incendiary | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.hot_shot_charge_pack | ammunition / Hot-Shot Charge Pack | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.sanctified_ammunition | ammunition / Sanctified Ammunition | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.ammunition.xenos_exotic_magazine | ammunition / Xenos / Exotic Magazine | 92 / 105 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.inferno_pistol | weapon / Inferno Pistol | 93 / 106 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.grav_pistol | weapon / Grav-Pistol | 93 / 106 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.grav_gun | weapon / Grav-Gun | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.digital_weapon | equipment / Digital Weapon | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.null_rod | equipment / Null Rod | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.rosarius | equipment / Rosarius | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.displacer_field | equipment / Displacer Field | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.conversion_beamer | weapon / Conversion Beamer | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.teleport_homer | equipment / Teleport Homer | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.consumable.wargear.stasis_grenade | consumable / Stasis Grenade | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.volkite_serpenta | weapon / Volkite Serpenta | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.volkite_charger | weapon / Volkite Charger | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.suspensor_harness | equipment / Suspensor Harness | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.archeotech_logic_engine | equipment / Archeotech Logic Engine | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.phase_shunt_field | equipment / Phase-Shunt Field | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.medicae_crucible | equipment / Medicae Crucible | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.the_last_light_imperial | equipment / The Last Light - Imperial | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.bulwark_of_saint_drusus_imperial | equipment / Bulwark of Saint Drusus - Imperial | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.martyrs_censer_imperial | equipment / Martyr's Censer - Imperial | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.arc_of_the_reductor_mechanicus | equipment / Arc of the Reductor - Mechanicus | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.omnissian_data_relic_mechanicus | equipment / Omnissian Data-Relic - Mechanicus | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.big_lugs_door_ogryn | equipment / Big Lug's Door - Ogryn | 94 / 107 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.grutts_lucky_club_ogryn | weapon / Grutt's Lucky Club - Ogryn | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.ancestor_wrought_rail_rifle_kin | weapon / Ancestor-Wrought Rail Rifle - Kin | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.armour.wargear.oathplate_of_the_first_claim_kin | armour / Oathplate of the First Claim - Kin | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.ghosthelm_of_the_wandering_seer_aeldari | equipment / Ghosthelm of the Wandering Seer - Aeldari | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.weapon.wargear.starfall_long_rifle_aeldari | weapon / Starfall Long Rifle - Aeldari | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.halo_of_saint_varro | equipment / Halo of Saint Varro | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.heart_key_of_the_red_vault | equipment / Heart-Key of the Red Vault | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.the_first_oathstone | equipment / The First Oathstone | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.the_veiled_eye | equipment / The Veiled Eye | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.the_door_that_would_not_break | equipment / The Door That Would Not Break | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.equipment.wargear.the_ghosts_coin | equipment / The Ghost's Coin | 95 / 108 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.reinforced_plating | system / Reinforced plating | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.smoke_launchers | system / Smoke launchers | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.auspex_survey_suite | system / Auspex survey suite | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.recovery_winch | system / Recovery winch | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.all_terrain_running_gear | system / All-terrain running gear | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.sealed_compartment | system / Sealed compartment | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.ogryn_accommodation | system / Ogryn accommodation | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.system.vehicle.spare_parts_locker | system / Spare-parts locker | 105 / 118 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.condition.exhaustion | condition / Exhaustion | 20 / 33 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.zealot.preacher | subclass / Preacher | 40 / 53 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.zealot.flagellant | subclass / Flagellant | 40 / 53 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.zealot.purifier | subclass / Purifier | 40 / 53 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.biomancer | subclass / Biomancer | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.telekine | subclass / Telekine | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.diviner | subclass / Diviner | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.pyromancer | subclass / Pyromancer | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.malefic_touched | subclass / Malefic-Touched | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.psyker.blank_null_bound | subclass / Blank / Null-Bound | 43 / 56 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ogryn_skullbreaker.bulwark | subclass / Bulwark | 46 / 59 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ogryn_skullbreaker.gun_lugger | subclass / Gun Lugger | 46 / 59 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ogryn_skullbreaker.bone_ead | subclass / Bone ’ead | 46 / 59 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ogryn_skullbreaker.brute | subclass / Brute | 46 / 59 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.arbites_enforcer.riot_shield | subclass / Riot Shield | 49 / 62 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.arbites_enforcer.executioner | subclass / Executioner | 49 / 62 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.arbites_enforcer.investigator | subclass / Investigator | 49 / 62 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hive_scum.gunslinger | subclass / Gunslinger | 52 / 65 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hive_scum.knife_rat | subclass / Knife Rat | 52 / 65 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hive_scum.chem_user | subclass / Chem-User | 52 / 65 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hive_scum.sump_ghost | subclass / Sump Ghost | 52 / 65 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ratling_sharpshooter.long_las_sniper | subclass / Long-Las Sniper | 55 / 68 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ratling_sharpshooter.underhive_rat | subclass / Underhive Rat | 55 / 68 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ratling_sharpshooter.spotter | subclass / Spotter | 55 / 68 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.ratling_sharpshooter.black_market_gremlin | subclass / Black-Market Gremlin | 55 / 68 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.ruststalker | subclass / Ruststalker Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.ranger | subclass / Ranger Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.vanguard | subclass / Vanguard Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.protector | subclass / Protector Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.data_hunter | subclass / Data-Hunter Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.skitarii_veteran.infiltrator | subclass / Infiltrator Protocol | 58 / 71 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.kin_armsman.hearthguard | subclass / Hearthguard | 61 / 74 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.kin_armsman.ironhead | subclass / Ironhead | 61 / 74 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.kin_armsman.guild_militant | subclass / Guild-Militant | 61 / 74 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hernkyn_prospector.outrider | subclass / Outrider | 64 / 77 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hernkyn_prospector.claim_staker | subclass / Claim-Staker | 64 / 77 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.hernkyn_prospector.trail_gunner | subclass / Trail Gunner | 64 / 77 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_outcast.ranger | subclass / Ranger | 67 / 80 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_outcast.corsair | subclass / Corsair | 67 / 80 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_outcast.shadow_guide | subclass / Shadow Guide | 67 / 80 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_warlock.seer_of_battle | subclass / Seer of Battle | 70 / 83 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_warlock.storm_warlock | subclass / Storm Warlock | 70 / 83 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |
| di.subclass.aeldari_warlock.spirit_guardian | subclass / Spirit Guardian | 70 / 83 | SPEC_EXTENSION_REQUIRED | PARTIALLY_STRUCTURED |

For every non-READY record, machine inventory `reason` and `issues` explain its status; [review issues](PHB_REVIEW_REQUIRED.md) provide the action needed. Section/table-only entries are retained evidence with mapping not yet asserted, not alleged missing rules.

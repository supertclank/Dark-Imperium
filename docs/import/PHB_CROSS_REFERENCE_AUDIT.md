# PHB cross-reference audit

This is a source-and-import audit, not a completed certification of every prose reference. All canonical draft ContentRefs resolve in the draft package; incomplete mappings stay outside it. The source-to-ID review is broader than the runtime reference validator.

| Reference / comparison | Finding | Disposition |
| --- | --- | --- |
| Origins table vs prose | Six differing eligibility lists | PHB-001; no preferred list silently chosen |
| Frag Bomb in Ogryn kit | Complete entry exists in10, printed34/PDF47 | Not missing; do not repeat the task brief's illustrative missing-item example as fact |
| Ogryn Club in kit | Listed in8.3, printed25/PDF38 | Same weapon identity |
| Hernkyn equipment | Ion Blaster/Magna-Rail Rifle in8.4 | Preserve GM approval wording; no invented rifle |
| Skitarii kit | Galvanic Rifle/Radium Carbine/Taser Goad in8.6 | Defined; slash damage semantics unresolved |
| medkit / Med-Pack | Different names; only Med-Pack has located mission stat entry | PHB-014; no automatic alias |
| riot shield / Shield / Slab Shield | No explicit statement that riot shield equals either entry | PHB-014 |
| light armour / concrete armour rows | Category is not an equipment identity | PHB-014; choose a reviewed pool later |
| survey auspex, focus, tools, tokens, brands, charms | Named starting kit lacks a dedicated full stat definition for every term | Preserve narrative text; do not fabricate charges, costs or actions |
| Force Sword vs Spirit Weapon | Force Sword has Psyker/Power Field, not Spirit Weapon | Do not automatically grant psychic attack substitution |
| Mounted heavy stubber/bolter/multi-laser | Chapter21 explicitly retains chapter8 profiles with mounting context | Shared reserved IDs, multiple source evidence locators; do not double-import three weapons |
| Mounted Burst | Chapter21 says three shots and first-listed extra damage die | Retain mounted scope; PHB-004 for personal weapons |
| Armour-Breaking | Chapter21 explicitly extends it to halving hull DT | Specific extension, not a rebalance or AC reduction |
| Class tables | 12 tables each have levels1–20 | 240 ordered rows; exact level source labels preserved |
| Repeated subclass table headings | Split tables and repeated Feature labels require level mapping | Veteran3 mapped; other42 candidates PHB-012 |
| Small Target / Path Discipline / Recoil Compensation | Repeated labels can have different owners/mechanics | Do not merge by display name; namespace keys include context |
| Psyker/Warlock known-power tables vs kit | Both level-one tables show2 Minor/2 Standard, matching equipment text | Known-power counts preserved as evidence; no double grant from kit |
| Psyker Major access | Class prose and allowed-tag tables need precise interpretation for Universal Major powers | Keep access manual pending reviewed pool |
| Aeldari Warlock access vs chapter14 intro | Specific Warlock class and Rune power section explicitly grant access | Record specific exception; do not remove Warlock powers |
| Diseased/bleeding/crippled/concentration | Referenced, but complete uniform condition/procedure definitions not located | PHB-013/009 |
| Twin-Linked | Rerolls a damage die after a miss sets up the next hit | Preserve the unusual text exactly; do not substitute tabletop40k mechanics |
| Half cover / Aim | Not aligned to complete generic definitions located here | PHB-016 |
| Old development seeds | Human/Guardsman/Lasgun samples use different values and units | Excluded entirely from PHB identities and source truth |

No class-table/prose mismatch has been declared resolved just because an automated name match failed. Such failures are explicitly mapping backlog until a human source comparison establishes a true conflict. This distinction prevents manufacturing missing rules.

The canonical validator checks IDs, exact source versions, reference closure/types, class-parent/progression links, choices, supported effects, base dice bounds and hashes. It does not prove every prose clause is mapped. See [review issues](PHB_REVIEW_REQUIRED.md) and [import report](PHB_IMPORT_REPORT.md).

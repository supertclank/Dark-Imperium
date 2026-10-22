# Prerequisite contract and PHB audit

This clarifies the existing RULES_EFFECTS Predicate union, not a second rule language. `all`/`any` use `predicates: Predicate[]`; `not` uses `predicate: Predicate`. Depth <=8 and total nodes <=100. Numeric comparisons are eq/lt/lte/gt/gte. Arrays are nonempty. References must resolve to the required canonical kind. Unknown input produces unresolved, never eligible.

| Requirement | Existing representation |
| --- | --- |
| Minimum/maximum level | level, explicit total_level or class_level axis, gte/lte |
| Required species/class/subclass/Origin/feature/feat | selected ContentRef; feat is feature flavor feat |
| Excluded species/other selection | not(selected) |
| Required attribute | stat key from profile registry, pre-grant snapshot |
| Proficiency | proficient with proficiency ContentRef |
| Psychic capability | registered fact derived from source grants and hard restrictions; no string class-name test |
| Equipped kind/property/slot | equipped selector; only currently equipped instances |
| Equipment tag | tagged attack_weapon or item context; registered tag and explicit context |
| Faction/chapter | selected faction/affiliation or registered tag, according to actual source semantics |
| Conditional health | health_ratio with exact cross-multiplication, lte for Bloodied, lt for below half |
| AND/OR/exclusion | all/any/not with three-valued logic |

Evaluation uses the pre-grant snapshot. selected includes existing active source grants, not the candidate being evaluated. A subclass must satisfy its own requirements AND parent-class eligibility AND the parent level/choice entitlement; having a selected subclass ID cannot bypass that relationship. The generic offline evaluator validates logic, not a complete builder or campaign approval service.

Canonical changes: all 30 species-restricted Talents now have explicit prerequisites, including Human AND Psyker, Human OR Ratling, Aeldari AND Outcast/Warlock. Three Origins have matching matrix/prose prerequisites; the other seven have unresolved `phb.origin_eligibility.<key>` gates. These are issue-resolution gates, not authority for clients to declare legality. Only a reviewed campaign ruling can populate one. Null-Bound additionally uses the source-required `phb.null_bound_approved` gate. Facts are not arbitrary code.

The existing12 classes preserve the species eligibility matrix. Ogryn and Skitarii class locks remain; Ratling Zealot is a GM-approved alternate requiring modified features, outside the core selectable data. Touched by the Warp must not bypass explicit Skitarii psychic prohibition. Warlock is an explicit specific access exception, not an Imperial Psyker class.

Equipment acquire/equip/use gates remain distinct. A weapon training requirement does not automatically forbid ownership. Source restrictions with exceptions (Ogryn modified users, Mechanicus interface/GM approval, Heavy training) require registered entitlements and contextual gates; unresolved taxonomy must not be converted to blanket bans.

Astartes is future content: no PHB species, chapter or eligibility IDs are fabricated. New species/classes/affiliations can use the same Predicate and choice model. Publication checks must validate requirement reference kinds, rule vocabulary, self-grant/circular unlocks and satisfiable choices against a complete profile; this pass does not claim that solver exists.

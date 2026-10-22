-- Representative development content, not authoritative Dark Imperium rules.
INSERT INTO species (id, slug, name, description, rules) VALUES
('10000000-0000-0000-0000-000000000001', 'human', 'Human', 'Resilient citizens of a fractured imperium. Development rules; subject to revision.',
'{"schemaVersion":1,"effects":[{"operation":"add","target":"movement","value":6}]}');
INSERT INTO classes (id, slug, name, description, rules, progression) VALUES
('20000000-0000-0000-0000-000000000001', 'guardsman', 'Guardsman', 'A trained soldier holding the line against the darkness. Development progression.',
'{"schemaVersion":1,"effects":[{"operation":"add","target":"maxWounds","value":10}]}',
'[{"level":1,"features":[]}]');
INSERT INTO weapons (id, slug, name, description, category, damage_dice, damage_type, normal_range, long_range, properties) VALUES
('30000000-0000-0000-0000-000000000001', 'lasgun', 'Lasgun', 'A dependable infantry energy weapon. All statistics are representative placeholders.', 'Ranged', '1d10', 'Energy', 100, 300,
'[{"key":"two-handed","label":"Two-handed","parameters":{"hands":2}},{"key":"reliable","label":"Reliable","parameters":{}}]');

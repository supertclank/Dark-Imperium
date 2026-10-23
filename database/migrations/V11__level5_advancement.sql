ALTER TABLE character_advancements DROP CONSTRAINT character_advancements_to_level_check;
ALTER TABLE character_advancements ADD CONSTRAINT character_advancements_to_level_check CHECK (to_level BETWEEN 2 AND 5);

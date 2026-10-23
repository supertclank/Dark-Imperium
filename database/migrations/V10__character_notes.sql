ALTER TABLE player_characters ADD COLUMN notes TEXT NOT NULL DEFAULT '';
ALTER TABLE player_characters ADD COLUMN notes_version BIGINT NOT NULL DEFAULT 0;

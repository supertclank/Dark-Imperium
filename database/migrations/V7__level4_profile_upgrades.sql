ALTER TABLE character_advancements DROP CONSTRAINT character_advancements_to_level_check;
ALTER TABLE character_advancements ADD CONSTRAINT character_advancements_to_level_check CHECK (to_level BETWEEN 2 AND 4);
CREATE TABLE character_profile_upgrades (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 character_id uuid NOT NULL REFERENCES player_characters(id) ON DELETE CASCADE,
 from_profile text NOT NULL REFERENCES ruleset_profiles(id),
 from_digest char(64) NOT NULL,
 to_profile text NOT NULL REFERENCES ruleset_profiles(id),
 to_digest char(64) NOT NULL,
 request_id uuid NOT NULL,
 contract_version text NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(character_id,request_id)
);

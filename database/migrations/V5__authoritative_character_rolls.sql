-- Roll records are append-only through the application. Character deletion cascades
-- its private history; there is no result-update or result-delete API.
ALTER TABLE player_characters ADD CONSTRAINT player_character_owner_identity UNIQUE(id,user_id);
CREATE TABLE character_rolls (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    character_id uuid NOT NULL,
    request_id uuid NOT NULL,
    request_digest char(64) NOT NULL,
    profile_id text NOT NULL,
    profile_digest char(64) NOT NULL,
    roll_definition_id uuid NOT NULL,
    action_id text,
    roll_type text NOT NULL,
    visibility text NOT NULL, -- application currently permits PRIVATE only; extensible
    parent_result_id uuid,
    state_version_before bigint NOT NULL CHECK(state_version_before >= 0),
    state_version_after bigint NOT NULL CHECK(state_version_after >= state_version_before),
    result jsonb NOT NULL CHECK(jsonb_typeof(result) = 'object'),
    created_at timestamptz NOT NULL,
    UNIQUE(user_id,request_id),
    UNIQUE(id,character_id),
    FOREIGN KEY(character_id,user_id) REFERENCES player_characters(id,user_id) ON DELETE CASCADE,
    FOREIGN KEY(profile_id,profile_digest) REFERENCES ruleset_profiles(id,digest),
    FOREIGN KEY(parent_result_id,character_id) REFERENCES character_rolls(id,character_id)
);
CREATE INDEX character_rolls_history_idx ON character_rolls(character_id,created_at DESC,id DESC);
-- Conceptual rollback: export history, drop character_rolls, then owner identity constraint.

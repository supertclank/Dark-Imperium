CREATE TABLE character_advancements (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    character_id uuid NOT NULL REFERENCES player_characters(id) ON DELETE CASCADE,
    request_id uuid NOT NULL,
    request_digest char(64) NOT NULL,
    from_level integer NOT NULL,
    to_level integer NOT NULL CHECK (to_level BETWEEN 2 AND 3),
    state_version_before bigint NOT NULL,
    state_version_after bigint NOT NULL,
    result jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(user_id, request_id),
    CHECK (to_level = from_level + 1)
);

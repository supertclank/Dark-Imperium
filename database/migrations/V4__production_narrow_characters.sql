-- Additive: foundation characters remain intact, not silently migrated to PHB rules.
CREATE TABLE ruleset_profiles (
    id text PRIMARY KEY,
    digest char(64) NOT NULL,
    engine_version text NOT NULL,
    snapshot jsonb NOT NULL CHECK (jsonb_typeof(snapshot) = 'object'),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (id, digest)
);
CREATE TABLE player_characters (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    profile_id text NOT NULL,
    profile_digest char(64) NOT NULL,
    name varchar(80) NOT NULL CHECK (length(trim(name)) > 0),
    species_id text NOT NULL,
    origin_id text NOT NULL,
    class_id text NOT NULL,
    trait_id text NOT NULL,
    level integer NOT NULL CHECK (level BETWEEN 1 AND 20),
    base_attributes jsonb NOT NULL CHECK (jsonb_typeof(base_attributes) = 'object'),
    package_choices jsonb NOT NULL CHECK (jsonb_typeof(package_choices) = 'object'),
    request_id uuid NOT NULL,
    request_digest char(64) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (profile_id, profile_digest) REFERENCES ruleset_profiles(id, digest),
    UNIQUE(user_id, request_id)
);
CREATE INDEX player_characters_owner_idx ON player_characters(user_id, created_at DESC);
CREATE TABLE player_character_choices (
    character_id uuid NOT NULL REFERENCES player_characters(id) ON DELETE CASCADE,
    choice_id text NOT NULL,
    option_ids jsonb NOT NULL CHECK (jsonb_typeof(option_ids) = 'array'),
    PRIMARY KEY (character_id, choice_id)
);
CREATE TABLE player_character_inventory (
    id uuid PRIMARY KEY,
    character_id uuid NOT NULL REFERENCES player_characters(id) ON DELETE CASCADE,
    definition_id text NOT NULL,
    initial_quantity integer NOT NULL CHECK(initial_quantity > 0),
    quantity integer NOT NULL CHECK(quantity >= 0),
    equipped boolean NOT NULL,
    ammunition jsonb, -- null = not initialised; never inferred as a full magazine
    UNIQUE(character_id, definition_id)
);
CREATE TABLE player_character_runtime (
    character_id uuid PRIMARY KEY REFERENCES player_characters(id) ON DELETE CASCADE,
    current_hp integer NOT NULL CHECK(current_hp >= 0),
    state_version bigint NOT NULL DEFAULT 0 CHECK(state_version >= 0),
    resources jsonb NOT NULL DEFAULT '{}',
    conditions jsonb NOT NULL DEFAULT '[]',
    temporary_effects jsonb NOT NULL DEFAULT '[]'
);
-- Conceptual rollback: drop the four player_character* tables first, then profiles.
-- Do not run rollback against retained user characters without an explicit export.

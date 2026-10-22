CREATE TABLE users (
    id uuid PRIMARY KEY,
    email varchar(254) NOT NULL UNIQUE CHECK (email = lower(email)),
    password_hash text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE sessions (
    token_hash char(64) PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX sessions_user_idx ON sessions(user_id);
CREATE INDEX sessions_expiry_idx ON sessions(expires_at);
CREATE TABLE species (
    id uuid PRIMARY KEY,
    slug text NOT NULL UNIQUE,
    name text NOT NULL,
    description text NOT NULL,
    rules jsonb NOT NULL DEFAULT '{}',
    version integer NOT NULL DEFAULT 1
);
CREATE TABLE classes (
    id uuid PRIMARY KEY,
    slug text NOT NULL UNIQUE,
    name text NOT NULL,
    description text NOT NULL,
    rules jsonb NOT NULL DEFAULT '{}',
    progression jsonb NOT NULL DEFAULT '[]',
    version integer NOT NULL DEFAULT 1
);
CREATE TABLE weapons (
    id uuid PRIMARY KEY,
    slug text NOT NULL UNIQUE,
    name text NOT NULL,
    description text NOT NULL,
    category text NOT NULL,
    damage_dice text NOT NULL,
    damage_type text NOT NULL,
    normal_range integer NOT NULL CHECK(normal_range >= 0),
    long_range integer NOT NULL CHECK(long_range >= normal_range),
    properties jsonb NOT NULL DEFAULT '[]',
    version integer NOT NULL DEFAULT 1
);
CREATE TABLE characters (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name varchar(80) NOT NULL CHECK(length(trim(name)) > 0),
    species_id uuid NOT NULL REFERENCES species(id),
    class_id uuid NOT NULL REFERENCES classes(id),
    level integer NOT NULL DEFAULT 1 CHECK(level BETWEEN 1 AND 20),
    attributes jsonb NOT NULL,
    current_wounds integer NOT NULL CHECK(current_wounds >= 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX characters_owner_idx ON characters(user_id, created_at DESC);
CREATE TABLE character_equipment (
    id uuid PRIMARY KEY,
    character_id uuid NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    weapon_id uuid NOT NULL REFERENCES weapons(id),
    quantity integer NOT NULL DEFAULT 1 CHECK(quantity > 0),
    equipped boolean NOT NULL DEFAULT true,
    UNIQUE(character_id, weapon_id)
);

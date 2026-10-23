CREATE TABLE physical_roll_sessions (
 id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 character_id uuid REFERENCES player_characters(id) ON DELETE CASCADE,
 request_id uuid NOT NULL, request_digest text NOT NULL, request jsonb NOT NULL,
 specification jsonb NOT NULL, presentation_seed text NOT NULL,
 reserved_item text, status text NOT NULL DEFAULT 'CREATED' CHECK(status IN ('CREATED','COMPLETED','CANCELLED')),
 created_at timestamptz NOT NULL DEFAULT now(), expires_at timestamptz NOT NULL,
 submission_digest text, result jsonb, UNIQUE(user_id,request_id)
);
CREATE INDEX physical_roll_reservations ON physical_roll_sessions(character_id,reserved_item,expires_at) WHERE status='CREATED';

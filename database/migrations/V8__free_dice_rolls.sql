CREATE TABLE free_rolls (
 id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 request_id uuid NOT NULL, request_digest text NOT NULL, result jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(user_id,request_id)
);
CREATE INDEX free_rolls_owner_history ON free_rolls(user_id,created_at DESC,id DESC);

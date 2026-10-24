ALTER TABLE player_character_runtime ADD COLUMN warp_pressure integer NOT NULL DEFAULT 0 CHECK(warp_pressure >= 0);
ALTER TABLE player_character_runtime ADD COLUMN pending_action jsonb;
CREATE TABLE character_action_requests (
 user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 request_id uuid NOT NULL,
 character_id uuid NOT NULL REFERENCES player_characters(id) ON DELETE CASCADE,
 request_digest text NOT NULL,
 result jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(user_id,request_id)
);
-- Trusted grants are provisioned by a host administrator after a GM decision.
-- No player-facing endpoint creates or edits approvals.
CREATE TABLE character_creation_approvals (
 user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 profile_id text NOT NULL REFERENCES ruleset_profiles(id),
 scope text NOT NULL CHECK(scope IN ('blank_null_bound','warlock_pyromancy')),
 approved_by text NOT NULL CHECK(length(approved_by)>0),
 evidence text NOT NULL CHECK(length(evidence)>0),
 created_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(user_id,profile_id,scope)
);

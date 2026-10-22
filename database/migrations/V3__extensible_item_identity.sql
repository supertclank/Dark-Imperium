-- Shared catalog identity lets equipment reference future armour/gear without
-- polymorphic IDs or dropping referential integrity. Weapon statistics stay typed.
CREATE TABLE items (
    id uuid PRIMARY KEY,
    kind text NOT NULL,
    UNIQUE(id, kind)
);
INSERT INTO items(id, kind) SELECT id, 'weapon' FROM weapons;
ALTER TABLE weapons ADD COLUMN item_kind text NOT NULL DEFAULT 'weapon' CHECK(item_kind = 'weapon');
ALTER TABLE weapons ADD CONSTRAINT weapons_item_fkey FOREIGN KEY(id, item_kind) REFERENCES items(id, kind);
ALTER TABLE character_equipment DROP CONSTRAINT character_equipment_weapon_id_fkey;
ALTER TABLE character_equipment RENAME COLUMN weapon_id TO item_id;
ALTER TABLE character_equipment ADD CONSTRAINT equipment_item_fkey FOREIGN KEY(item_id) REFERENCES items(id);

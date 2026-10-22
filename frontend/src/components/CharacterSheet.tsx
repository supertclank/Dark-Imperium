"use client";
import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, Character } from "@/lib/api";
import { useResource, ResourceState } from "./Resource";
export function CharacterSheet({ id }: { id: string }) {
  const {
    data: character,
    error,
    retry,
  } = useResource<Character>(`/characters/${id}`);
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState("");
  const router = useRouter();
  async function rename(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const name = new FormData(e.currentTarget).get("name");
    setBusy(true);
    setActionError("");
    try {
      await api(`/characters/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ name }),
      });
      setEditing(false);
      retry();
    } catch (e) {
      setActionError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function remove() {
    setBusy(true);
    setActionError("");
    try {
      await api(`/characters/${id}`, { method: "DELETE" });
      router.push("/characters");
    } catch (e) {
      setActionError((e as Error).message);
      setBusy(false);
    }
  }
  if (!character) return <ResourceState error={error} retry={retry} />;
  return (
    <>
      <Link href="/characters" className="back-link">
        ← Your characters
      </Link>
      <div className="sheet-heading">
        <div className="sheet-emblem" aria-hidden="true">
          ✦
        </div>
        <div>
          <p className="eyebrow">
            PERSONNEL RECORD / {id.slice(0, 8).toUpperCase()}
          </p>
          <h1>{character.name}</h1>
          <p>
            {character.species.name} <span className="separator">/</span>{" "}
            {character.characterClass.name} <span className="separator">/</span>{" "}
            Level {character.level}
          </p>
        </div>
        <button className="secondary" onClick={() => setEditing((v) => !v)}>
          Rename
        </button>
      </div>
      {editing && (
        <form className="panel inline-form" onSubmit={rename}>
          <label htmlFor="rename">Character name</label>
          <input
            id="rename"
            name="name"
            defaultValue={character.name}
            maxLength={80}
            required
          />
          <button disabled={busy}>Save name</button>
          <button
            type="button"
            className="text-button"
            onClick={() => setEditing(false)}
          >
            Cancel
          </button>
        </form>
      )}
      {actionError && (
        <p role="alert" className="error">
          {actionError}
        </p>
      )}
      <div className="sheet-layout">
        <div>
          <section className="panel">
            <div className="section-title">
              <h2>Attributes</h2>
              <span className="eyebrow">PLACEHOLDER VALUES</span>
            </div>
            <div className="attributes">
              {Object.entries(character.attributes).map(([key, value]) => (
                <div className="attribute" key={key}>
                  <span>{key}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
          </section>
          <section className="panel">
            <div className="section-title">
              <h2>Attacks & equipment</h2>
              <span className="eyebrow">
                LOADOUT / {character.equipment.length}
              </span>
            </div>
            {character.equipment.map((w) => (
              <article className="weapon-row" key={w.id}>
                <div>
                  <span className="eyebrow">{w.category} WEAPON</span>
                  <h3>{w.name}</h3>
                  <p className="muted">{w.description}</p>
                </div>
                <dl className="weapon-stats">
                  <div>
                    <dt>Damage</dt>
                    <dd>
                      {w.damageDice} <small>{w.damageType}</small>
                    </dd>
                  </div>
                  <div>
                    <dt>Range</dt>
                    <dd>
                      {w.normalRange} / {w.longRange} <small>m</small>
                    </dd>
                  </div>
                </dl>
                <div className="tags">
                  {w.properties.map((p) => (
                    <span key={p.key}>{p.label}</span>
                  ))}
                </div>
              </article>
            ))}
          </section>
        </div>
        <aside>
          <section className="panel vitality">
            <p className="eyebrow">VITAL SIGNS</p>
            <h2>Wounds</h2>
            <div className="wounds">
              {character.currentWounds}
              <span>/ {character.calculated.maxWounds}</span>
            </div>
            <meter
              min={0}
              max={character.calculated.maxWounds}
              value={character.currentWounds}
              aria-label="Current wounds"
            />
            <dl>
              <div>
                <dt>Movement</dt>
                <dd>{character.calculated.movement} m</dd>
              </div>
              <div>
                <dt>Level</dt>
                <dd>{character.level}</dd>
              </div>
            </dl>
          </section>
          <div className="field-note">
            <span className="eyebrow">DEVELOPMENT RULESET</span>
            <p>
              These statistics are placeholders, not final game rules. Weapon
              properties are descriptive in this edition.
            </p>
          </div>
        </aside>
      </div>
      <div className="danger-zone">
        {confirmDelete ? (
          <>
            <p>
              Delete <strong>{character.name}</strong>? This permanently removes
              this character.
            </p>
            <button className="danger" disabled={busy} onClick={remove}>
              {busy ? "Deleting…" : "Delete permanently"}
            </button>
            <button
              className="text-button"
              onClick={() => setConfirmDelete(false)}
            >
              Keep character
            </button>
          </>
        ) : (
          <button
            className="text-button"
            onClick={() => setConfirmDelete(true)}
          >
            Delete character
          </button>
        )}
      </div>
    </>
  );
}

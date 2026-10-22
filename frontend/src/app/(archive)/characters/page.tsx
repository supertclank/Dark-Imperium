"use client";
import Link from "next/link";
import { useResource, ResourceState } from "@/components/Resource";
import { Character } from "@/lib/api";
export default function Characters() {
  const { data, error, retry } = useResource<Character[]>("/characters");
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">01 / PERSONNEL</p>
          <h1>Your characters</h1>
          <p className="muted">
            Every record belongs to a story still being written.
          </p>
        </div>
        <Link href="/characters/new" className="button primary">
          + Create character
        </Link>
      </div>
      {!data ? (
        <ResourceState error={error} retry={retry} />
      ) : data.length === 0 ? (
        <section className="empty panel">
          <div className="empty-mark" aria-hidden="true">
            ✦
          </div>
          <p className="eyebrow">AWAITING YOUR FIRST RECORD</p>
          <h2>The ranks are open.</h2>
          <p>Create your first character and begin their service record.</p>
          <Link href="/characters/new" className="button primary">
            Create a character →
          </Link>
        </section>
      ) : (
        <>
          <p className="eyebrow record-count">
            {data.length} ACTIVE {data.length === 1 ? "RECORD" : "RECORDS"}
          </p>
          <div className="card-grid">
            {data.map((character, i) => (
              <Link
                href={`/characters/${character.id}`}
                className="character-card"
                key={character.id}
              >
                <div className="card-top">
                  <span className="eyebrow">
                    RECORD {String(i + 1).padStart(3, "0")}
                  </span>
                  <span className="level-tag">LVL {character.level}</span>
                </div>
                <div className="character-emblem" aria-hidden="true">
                  ✦
                </div>
                <h2>{character.name}</h2>
                <p>
                  {character.species.name} · {character.characterClass.name}
                </p>
                <div className="card-bottom">
                  <span>
                    {character.equipment.map((w) => w.name).join(", ")}
                  </span>
                  <span>Open record ↗</span>
                </div>
              </Link>
            ))}
          </div>
        </>
      )}
    </>
  );
}

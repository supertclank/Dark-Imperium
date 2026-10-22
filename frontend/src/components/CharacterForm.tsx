"use client";
import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { api, Character, Content, Weapon } from "@/lib/api";
import { useResource, ResourceState } from "./Resource";

export function CharacterForm() {
  const species = useResource<Content[]>("/species");
  const classes = useResource<Content[]>("/classes");
  const weapons = useResource<Weapon[]>("/weapons");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const [selection, setSelection] = useState({
    speciesId: "",
    classId: "",
    weaponId: "",
  });
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      const character = await api<Character>("/characters", {
        method: "POST",
        body: JSON.stringify({ name: form.get("name"), ...selection }),
      });
      router.push(`/characters/${character.id}`);
    } catch (e) {
      setError((e as Error).message);
      setBusy(false);
    }
  }
  const errorResource = [species, classes, weapons].find((r) => r.error);
  if (errorResource)
    return (
      <ResourceState error={errorResource.error} retry={errorResource.retry} />
    );
  if (!species.data || !classes.data || !weapons.data)
    return <p role="status">Loading character options…</p>;
  const groups = [
    { key: "speciesId" as const, label: "Species", items: species.data },
    { key: "classId" as const, label: "Class", items: classes.data },
    {
      key: "weaponId" as const,
      label: "Starting equipment",
      items: weapons.data,
    },
  ];
  return (
    <form onSubmit={submit} className="builder">
      <div className="builder-fields">
        <section className="panel">
          <span className="eyebrow">01 / IDENTITY</span>
          <h2>Give them a name.</h2>
          <label htmlFor="character-name">Character name</label>
          <input
            id="character-name"
            name="name"
            required
            maxLength={80}
            placeholder="Enter a name for the record"
            autoComplete="off"
          />
        </section>
        {groups.map((group, index) => (
          <fieldset className="panel" key={group.key}>
            <legend>
              {String(index + 2).padStart(2, "0")} / {group.label}
            </legend>
            <div className="choice-grid">
              {group.items.map((item) => (
                <label
                  className={`choice ${selection[group.key] === item.id ? "selected" : ""}`}
                  key={item.id}
                >
                  <input
                    type="radio"
                    name={group.key}
                    required
                    value={item.id}
                    checked={selection[group.key] === item.id}
                    onChange={() =>
                      setSelection((s) => ({ ...s, [group.key]: item.id }))
                    }
                  />
                  <span>
                    <strong>{item.name}</strong>
                    <span className="choice-description">
                      {item.description}
                    </span>
                    {"damageDice" in item && (
                      <span className="weapon-inline">
                        {String(item.damageDice)} {String(item.damageType)} ·{" "}
                        {String(item.normalRange)} m
                      </span>
                    )}
                  </span>
                </label>
              ))}
            </div>
          </fieldset>
        ))}
      </div>
      <aside className="builder-summary panel">
        <p className="eyebrow">SERVICE RECORD</p>
        <h2>Ready for the line.</h2>
        <dl>
          {groups.map((g) => (
            <div key={g.key}>
              <dt>{g.label}</dt>
              <dd>
                {g.items.find((i) => i.id === selection[g.key])?.name ||
                  "Not selected"}
              </dd>
            </div>
          ))}
          <div>
            <dt>Starting level</dt>
            <dd>1</dd>
          </div>
        </dl>
        <p className="small muted">
          Attributes and wounds use placeholder rules. You can reopen your saved
          sheet at any time.
        </p>
        {error && (
          <p role="alert" className="error">
            {error}
          </p>
        )}
        <button disabled={busy} className="primary">
          {busy ? "Saving record…" : "Save character →"}
        </button>
      </aside>
    </form>
  );
}

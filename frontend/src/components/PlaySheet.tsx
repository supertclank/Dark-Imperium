"use client";
import { useState, type ReactNode } from "react";
import type { SavedCharacter } from "@/lib/builder";
import { signed } from "@/lib/builder";
import type { RollOption } from "@/lib/rolls";
import { SheetInspector, type Inspection } from "./SheetInspector";
import { SheetNotes } from "./SheetNotes";
import { RollActionButton } from "./RollActionButton";
type Props = {
  character: SavedCharacter;
  options: RollOption[];
  disabled: boolean;
  onRoll: (o: RollOption) => void;
};
export function PlaySheet({ character, options, disabled, onRoll }: Props) {
  const c = character.calculated,
    [tab, setTab] = useState("Actions");
  const tabs = [
    "Actions",
    "Inventory",
    "Features & Traits",
    "Origin & Character",
    "Notes",
    "Extras",
  ];
  const [target, setTarget] = useState<{
      id: string;
      name: string;
      local?: Inspection;
    } | null>(null),
    [inventoryQuery, setInventoryQuery] = useState(""),
    [inventoryFilter, setInventoryFilter] = useState("All"),
    [featureFilter, setFeatureFilter] = useState("All");
  const inspect = (id: string, name: string) => (
    <button
      type="button"
      className="inspect-link"
      aria-label={`Inspect ${name}`}
      onClick={() => setTarget({ id, name })}
    >
      {name}
    </button>
  );
  const inventoryKind = (id: string) =>
    c.actions.some((a) => a.itemId === id)
      ? "Weapons"
      : id.startsWith("di.armour.")
        ? "Armour"
        : "Other";

  const find = (category: string, label: string) =>
    options.find(
      (o) =>
        o.category === category &&
        o.label.toLowerCase() === label.toLowerCase(),
    );
  function roll(option: RollOption | undefined, content: ReactNode) {
    return option ? (
      <RollActionButton
        option={option}
        disabled={disabled}
        onRoll={() => onRoll(option)}
      >
        {content}
        <span aria-hidden="true" className="roll-glyph">
          ◆
        </span>
      </RollActionButton>
    ) : (
      <span>{content}</span>
    );
  }
  const groups = c.features.reduce<Record<string, typeof c.features>>(
    (all, f) => {
      const key = f.id.includes(".species.")
        ? "Species"
        : f.id.includes(".origin.")
          ? "Origin"
          : f.id.includes(".subclass.")
            ? "Subclass"
            : f.id.includes(".talent.")
              ? "Talents"
              : f.id.includes(".class.")
                ? "Class"
                : "Other traits";
      (all[key] ??= []).push(f);
      return all;
    },
    {},
  );
  function weapon(action: (typeof c.actions)[number]) {
    const attack = options.find(
        (o) => o.itemId === action.itemId && o.category === "attack",
      ),
      damage = options.find(
        (o) => o.itemId === action.itemId && o.category === "damage",
      );
    return (
      <article className="play-weapon" key={action.id}>
        <div className="play-weapon-title">
          <h3>{inspect(action.itemId, action.name)}</h3>
          <span className="small muted">{action.properties.join(" · ")}</span>
        </div>
        <div className="play-weapon-stats">
          <div>
            <small>Range</small>
            <span>
              {action.range.kind === "reach"
                ? `${action.range.distance?.value} ft`
                : `${action.range.normal?.value}/${action.range.long?.value} ft`}
            </span>
          </div>
          <div>
            <small>{attack ? "Attack" : "Save DC"}</small>
            {attack ? (
              roll(attack, signed(attack.modifier))
            ) : (
              <span>{action.saveDc ?? "—"}</span>
            )}
          </div>
          <div>
            <small>
              {damage?.consumes
                ? `Use one · ${damage.quantity} remaining`
                : "Damage"}
            </small>
            {roll(
              damage,
              <>
                {action.damageExpression} <small>{action.damageType}</small>
              </>,
            )}
          </div>
        </div>
        <p className="weapon-binding">
          Attack ability:{" "}
          <strong>{action.attackAbilityId ?? action.ability ?? "None"}</strong>{" "}
          · Damage ability:{" "}
          <strong>
            {action.damageAbilityId ??
              (action.save ? "None" : action.ability) ??
              "None"}
          </strong>
        </p>
        {damage && !damage.available && (
          <p className="small">{damage.reason}</p>
        )}
        <button
          className="text-button small"
          onClick={() => setTarget({ id: action.itemId, name: action.name })}
        >
          Rules & details
        </button>
      </article>
    );
  }
  return (
    <div className="play-sheet">
      <header className="play-header">
        <div>
          <p className="eyebrow">PERSONNEL RECORD · LEVEL {character.level}</p>
          <h1>{character.name}</h1>
          <p>
            {character.species.name} · {character.origin.name} ·{" "}
            {character.characterClass.name}
            {c.subclass ? ` · ${c.subclass.name}` : ""}
          </p>
        </div>
        <div className="combat-strip">
          <div>
            <small>HP</small>
            <strong>
              {character.runtime.currentHp}
              <span> / {c.maximumWounds}</span>
            </strong>
          </div>
          <div>
            <small>AC</small>
            <strong>{c.defence}</strong>
          </div>
          <div>
            <small>Initiative</small>
            {roll(find("ability", "Initiative"), signed(c.initiative))}
          </div>
          <div>
            <small>Move</small>
            <strong>
              {c.movement}
              <span> ft</span>
            </strong>
          </div>
          <div>
            <small>Proficiency</small>
            <strong>{signed(c.proficiencyBonus)}</strong>
          </div>
        </div>
      </header>
      <section className="ability-strip" aria-label="Ability scores">
        {Object.entries(c.attributes).map(([key, score]) => (
          <div key={key}>
            <h2>{key.slice(0, 3).toUpperCase()}</h2>
            {roll(
              find("attribute", `${key} check`),
              signed(c.attributeModifiers[key]),
            )}
            <small>Score {score}</small>
          </div>
        ))}
      </section>
      <div className="play-columns">
        <aside className="play-basics">
          <section>
            <h2>Saving throws</h2>
            {Object.entries(c.saves).map(([key, save]) => (
              <div className="stat-line" key={key}>
                <span>
                  <span
                    className="proficiency-mark"
                    aria-label={
                      save.proficient ? "Proficient" : "Not proficient"
                    }
                  >
                    {save.proficient ? "●" : "○"}
                  </span>
                  {key.slice(0, 3).toUpperCase()}
                </span>
                {roll(find("save", `${key} save`), signed(save.modifier))}
              </div>
            ))}
          </section>
          <section>
            <h2>Senses</h2>
            <div className="stat-line">
              <span>Darkvision</span>
              <strong>{c.darkvisionFeet ?? 0} ft</strong>
            </div>
            {c.size && (
              <div className="stat-line">
                <span>Size</span>
                <span>{c.size}</span>
              </div>
            )}
          </section>
          <section>
            <h2>Training</h2>
            <ul className="training-list">
              {c.proficiencies.map((p) => (
                <li key={p.id}>{inspect(p.id, p.name)}</li>
              ))}
            </ul>
            {c.proceduralProficiencies?.map((p) => (
              <p className="small" key={p}>
                {p}
              </p>
            ))}
          </section>
        </aside>
        <section className="play-skills">
          <h2>Skills</h2>
          {Object.entries(c.skills).map(([key, skill]) => (
            <div className="stat-line" key={key}>
              <span>
                <span
                  className="proficiency-mark"
                  aria-label={
                    skill.proficient ? "Proficient" : "Not proficient"
                  }
                >
                  {skill.proficient ? "●" : "○"}
                </span>
                {inspect(key, skill.name)}
              </span>
              {roll(find("skill", skill.name), signed(skill.modifier))}
            </div>
          ))}
        </section>
        <section className="play-central">
          <div
            className="play-tabs"
            role="tablist"
            aria-label="Character play sections"
          >
            {tabs.map((name, i) => (
              <button
                key={name}
                role="tab"
                id={`play-tab-${i}`}
                aria-controls={`play-content-${i}`}
                aria-selected={tab === name}
                tabIndex={tab === name ? 0 : -1}
                onClick={() => setTab(name)}
                onKeyDown={(e) => {
                  if (
                    ["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)
                  ) {
                    e.preventDefault();
                    const next =
                      e.key === "Home"
                        ? 0
                        : e.key === "End"
                          ? tabs.length - 1
                          : (i +
                              (e.key === "ArrowRight" ? 1 : tabs.length - 1)) %
                            tabs.length;
                    setTab(tabs[next]);
                    document.getElementById(`play-tab-${next}`)?.focus();
                  }
                }}
              >
                {name}
              </button>
            ))}
          </div>
          <div
            role="tabpanel"
            id={`play-content-${tabs.indexOf(tab)}`}
            aria-labelledby={`play-tab-${tabs.indexOf(tab)}`}
            tabIndex={0}
          >
            {tab === "Actions" && (
              <>
                <p className="small muted play-note">
                  Roll from a modifier or damage formula. Hits and conditional
                  effects remain manual.
                </p>
                {c.actions.map(weapon)}
                {options
                  .filter(
                    (o) =>
                      !o.itemId &&
                      !["attribute", "skill", "save", "ability"].includes(
                        o.category,
                      ),
                  )
                  .map((o) => (
                    <div className="stat-line" key={o.id}>
                      <span>{o.label}</span>
                      {roll(
                        o,
                        o.groups
                          .map((g) => `${g.count}d${g.sides}`)
                          .join(" + "),
                      )}
                    </div>
                  ))}
                {Object.keys(character.runtime.resources).length > 0 && (
                  <section>
                    <h3>Limited use · manual tracking</h3>
                    {Object.entries(character.runtime.resources).map(
                      ([key, value]) => (
                        <div className="stat-line" key={key}>
                          <button
                            className="inspect-link"
                            onClick={() =>
                              setTarget({
                                id: key,
                                name: key.replaceAll("_", " "),
                                local: {
                                  id: key,
                                  name: key.replaceAll("_", " "),
                                  kind: "Resource",
                                  description:
                                    "Track this resource manually under the feature’s canonical usage rules.",
                                  fields: [
                                    {
                                      label: "Remaining",
                                      value: String(value.remaining),
                                    },
                                    {
                                      label: "Maximum",
                                      value: String(value.maximum),
                                    },
                                    {
                                      label: "Recovery",
                                      value: value.recovery.replaceAll(
                                        "_",
                                        " ",
                                      ),
                                    },
                                  ],
                                  status: "Manual tracking",
                                },
                              })
                            }
                          >
                            {key.replaceAll("_", " ")}
                          </button>
                          <span>
                            {value.remaining} / {value.maximum} ·{" "}
                            {value.recovery.replaceAll("_", " ")}
                          </span>
                        </div>
                      ),
                    )}
                  </section>
                )}
              </>
            )}
            {tab === "Inventory" && (
              <>
                <h2>Inventory</h2>
                <div className="sheet-filters">
                  <label>
                    Search inventory
                    <input
                      type="search"
                      value={inventoryQuery}
                      onChange={(e) => setInventoryQuery(e.target.value)}
                    />
                  </label>
                  <label>
                    Show items
                    <select
                      value={inventoryFilter}
                      onChange={(e) => setInventoryFilter(e.target.value)}
                    >
                      {[
                        "All",
                        "Equipped",
                        ...Array.from(
                          new Set(
                            character.inventory.map((i) =>
                              inventoryKind(i.definitionId),
                            ),
                          ),
                        ),
                      ].map((x) => (
                        <option key={x}>{x}</option>
                      ))}
                    </select>
                  </label>
                </div>
                {character.inventory
                  .filter(
                    (i) =>
                      i.name
                        .toLowerCase()
                        .includes(inventoryQuery.toLowerCase()) &&
                      (inventoryFilter === "All" ||
                        (inventoryFilter === "Equipped" && i.equipped) ||
                        inventoryKind(i.definitionId) === inventoryFilter),
                  )
                  .map((item) => (
                    <div
                      className="inventory-line stat-line"
                      key={item.definitionId}
                    >
                      {inspect(item.definitionId, item.name)}
                      <span>
                        ×{item.quantity}
                        {item.equipped ? " · Equipped" : ""}
                      </span>
                    </div>
                  ))}
              </>
            )}
            {tab === "Features & Traits" && (
              <>
                <label className="feature-filter">
                  Feature category
                  <select
                    value={featureFilter}
                    onChange={(e) => setFeatureFilter(e.target.value)}
                  >
                    {["All", ...Object.keys(groups)].map((x) => (
                      <option key={x}>{x}</option>
                    ))}
                  </select>
                </label>
                {Object.entries(groups)
                  .filter(
                    ([name]) =>
                      featureFilter === "All" || featureFilter === name,
                  )
                  .map(([name, features]) => (
                    <section key={name}>
                      <h2>{name}</h2>
                      {features.map((f) => (
                        <details className="feature-line" key={f.id}>
                          <summary>
                            <span>{f.name}</span>
                            <small>
                              {f.classification === "AUTOMATED"
                                ? "Calculated"
                                : f.classification === "BLOCKED"
                                  ? "Unavailable"
                                  : f.classification === "PARTIAL"
                                    ? "Conditional / manual"
                                    : "Manual"}
                            </small>
                          </summary>
                          {f.playerNote && <p>{f.playerNote}</p>}
                          <p>{f.text}</p>
                          {inspect(f.id, f.name)}
                        </details>
                      ))}
                    </section>
                  ))}
              </>
            )}
            {tab === "Origin & Character" && (
              <>
                <h2>Origin & Character</h2>
                <dl className="identity-details">
                  {[
                    [
                      "Species",
                      character.selections.speciesId,
                      character.species.name,
                    ],
                    [
                      "Origin",
                      character.selections.originId,
                      character.origin.name,
                    ],
                    [
                      "Class",
                      character.selections.classId,
                      character.characterClass.name,
                    ],
                    [
                      "Trait",
                      character.selections.traitId,
                      character.trait.name,
                    ],
                    ...(c.subclass
                      ? [["Subclass", c.subclass.id, c.subclass.name]]
                      : []),
                  ].map(([label, id, name]) => (
                    <div key={label}>
                      <dt>{label}</dt>
                      <dd>{inspect(id, name)}</dd>
                    </div>
                  ))}
                </dl>
                {c.contacts?.length ? (
                  <>
                    <h3>Contacts</h3>
                    {c.contacts.map((contact) => (
                      <p key={contact.id}>{contact.text}</p>
                    ))}
                  </>
                ) : null}
              </>
            )}
            <SheetNotes characterId={character.id} active={tab === "Notes"} />
            {tab === "Extras" && (
              <>
                <h2>Pinned ruleset</h2>
                <p className="small">{character.rulesetProfileId}</p>
                <p className="profile-digest">{character.rulesetDigest}</p>
                <p className="small">
                  Existing characters keep their historical ruleset. The fixed
                  Finesse Dexterity amendment applies to new v7 characters; no
                  silent profile migration occurs.
                </p>
                <h3>Manual adjudication</h3>
                <p>
                  Resolve targets, hit/miss, critical damage, conditional
                  effects and resource recovery at the table. No blocked psychic
                  content or level 5 rules are enabled.
                </p>
              </>
            )}
          </div>
        </section>
      </div>
      {target && (
        <SheetInspector
          characterId={character.id}
          target={target}
          options={options}
          disabled={disabled}
          onRoll={onRoll}
          onClose={() => setTarget(null)}
        />
      )}
    </div>
  );
}

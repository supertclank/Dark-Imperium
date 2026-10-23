"use client";
import { useState, type ReactNode } from "react";
import type { SavedCharacter } from "@/lib/builder";
import { signed } from "@/lib/builder";
import type { RollOption } from "@/lib/rolls";
import { RollActionButton } from "./RollActionButton";
type Props = {
  character: SavedCharacter;
  options: RollOption[];
  disabled: boolean;
  onRoll: (o: RollOption) => void;
  abilities: Record<string, string>;
  onAbility: (key: string, value: string) => void;
};
export function PlaySheet({
  character,
  options,
  disabled,
  onRoll,
  abilities,
  onAbility,
}: Props) {
  const c = character.calculated,
    [tab, setTab] = useState("Actions");
  const tabs = ["Actions", "Inventory", "Features & Traits"];
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
    const choices = attack?.abilities ?? damage?.abilities ?? [];
    const selectedAbility = abilities[action.itemId] ?? choices[0];
    const attackModifier =
      attack?.modifierChoices?.[selectedAbility] ?? attack?.modifier;
    const damageModifier = damage?.modifierChoices?.[selectedAbility];
    const damageExpression =
      damageModifier === undefined
        ? action.damageExpression
        : damage!.groups.map((g) => `${g.count}d${g.sides}`).join(" + ") +
          (damageModifier === 0 ? "" : ` ${signed(damageModifier)}`);
    return (
      <article className="play-weapon" key={action.id}>
        <div className="play-weapon-title">
          <h3>{action.name}</h3>
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
              roll(attack, signed(attackModifier!))
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
                {damageExpression} <small>{action.damageType}</small>
              </>,
            )}
          </div>
        </div>
        {choices.length > 0 && (
          <label className="finesse-choice">
            Ability
            <select
              aria-label={`${action.name} ability`}
              value={abilities[action.itemId] ?? choices[0]}
              disabled={disabled}
              onChange={(e) => onAbility(action.itemId, e.target.value)}
            >
              {choices.map((a) => (
                <option key={a}>{a}</option>
              ))}
            </select>
            <small>Server-calculated ability choice</small>
          </label>
        )}
        {damage && !damage.available && (
          <p className="small">{damage.reason}</p>
        )}
        <details>
          <summary>Rules & details</summary>
          {c.equipmentNotes?.[action.itemId] && (
            <p>{c.equipmentNotes[action.itemId]}</p>
          )}
          {action.save && (
            <p>
              DC {action.saveDc} {action.save.attribute} save. Damage outcomes
              use the pinned source policy.
            </p>
          )}
          {action.area && (
            <p>
              Radius {action.area.radius.value} {action.area.radius.unit}
            </p>
          )}
          <p className="small">
            Targets, hits, conditional effects and critical damage are resolved
            manually.
          </p>
        </details>
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
          <details>
            <summary>Profile & identity</summary>
            <p>
              {character.trait.name} · {character.rulesetProfileId}
            </p>
            <small>
              Saved character calculations; conditional rules require manual
              adjudication.
            </small>
          </details>
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
                <li key={p.id}>{p.name}</li>
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
                {skill.name}
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
                          <span>{key.replaceAll("_", " ")}</span>
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
                {character.inventory.map((item) => (
                  <details className="inventory-line" key={item.definitionId}>
                    <summary>
                      <span>{item.name}</span>
                      <span>
                        ×{item.quantity}
                        {item.equipped ? " · Equipped" : ""}
                      </span>
                    </summary>
                    {c.equipmentNotes?.[item.definitionId] && (
                      <p>{c.equipmentNotes[item.definitionId]}</p>
                    )}
                    {options
                      .filter((o) => o.itemId === item.definitionId)
                      .map((o) => (
                        <div key={o.id}>{roll(o, o.label)}</div>
                      ))}
                  </details>
                ))}
              </>
            )}
            {tab === "Features & Traits" && (
              <>
                {Object.entries(groups).map(([name, features]) => (
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
                        <small>
                          {f.sources
                            .map(
                              (s) =>
                                `${s.locator.heading} · PDF ${s.locator.pdfPage}`,
                            )
                            .join("; ")}
                        </small>
                      </details>
                    ))}
                  </section>
                ))}
              </>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

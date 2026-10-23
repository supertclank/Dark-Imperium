"use client";
import { useState } from "react";
import type { RollOption, RollResult } from "@/lib/rolls";

type Props = {
  count: number;
  actionIds: string[];
  options: RollOption[];
  disabled: boolean;
  onAttack: (option: RollOption, done: (result: RollResult) => void) => void;
  onDamage: (option: RollOption, parent: RollResult) => void;
};
/** Optional play aid only. Each roll still owns a separate server-authorised session. */
export function AttackSequence({
  count,
  actionIds,
  options,
  disabled,
  onAttack,
  onDamage,
}: Props) {
  const [results, setResults] = useState<RollResult[] | null>(null);
  const [weapon, setWeapon] = useState("");
  const legal = options.filter(
    (o) =>
      o.category === "attack" &&
      !!o.actionId &&
      actionIds.includes(o.actionId) &&
      !o.consumes,
  );
  const selected = legal.find((o) => o.itemId === weapon) ?? legal[0];
  if (count < 2) return null;
  return (
    <section className="attack-sequence" aria-label="Attack action sequence">
      {results === null ? (
        <button
          disabled={disabled || !legal.some((o) => o.available)}
          onClick={() => setResults([])}
        >
          Start Attack action
        </button>
      ) : (
        <>
          <h3>Attack action</h3>
          <p>
            {results.length < count
              ? `Attack ${results.length + 1} of ${count}`
              : `${count} attacks complete`}
          </p>
          <p className="small muted">
            One Attack action on your turn. Resolve hits, ammunition and
            conditional effects manually.
          </p>
          {results.length < count && (
            <>
              <label>
                Weapon for next attack
                <select
                  aria-label="Weapon for next attack"
                  value={selected?.itemId ?? ""}
                  disabled={disabled}
                  onChange={(e) => setWeapon(e.target.value)}
                >
                  {legal.map((o) => (
                    <option
                      key={o.id}
                      value={o.itemId!}
                      disabled={!o.available}
                    >
                      {o.label}
                    </option>
                  ))}
                </select>
              </label>
              <button
                disabled={disabled || !selected?.available}
                onClick={() => {
                  if (selected)
                    onAttack(selected, (result) =>
                      setResults((prior) =>
                        prior &&
                        !prior.some((x) => x.id === result.id) &&
                        prior.length < count
                          ? [...prior, result]
                          : prior,
                      ),
                    );
                }}
              >
                Roll attack {results.length + 1} of {count}
              </button>
            </>
          )}
          <ol>
            {results.map((result, i) => {
              const damage = options.find(
                (o) =>
                  o.actionId === result.actionId &&
                  o.category === "damage" &&
                  !o.consumes,
              );
              return (
                <li key={result.id}>
                  Attack {i + 1}: {result.label} · {result.total}
                  {damage && (
                    <button
                      disabled={disabled || !damage.available}
                      onClick={() => onDamage(damage, result)}
                    >
                      Roll damage for attack {i + 1} after confirming hit
                    </button>
                  )}
                </li>
              );
            })}
          </ol>
          <button
            className="secondary"
            disabled={disabled}
            onClick={() => setResults(null)}
          >
            {results.length < count ? "End sequence" : "Close sequence"}
          </button>
        </>
      )}
    </section>
  );
}

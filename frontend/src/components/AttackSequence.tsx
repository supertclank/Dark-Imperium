"use client";
import { useState } from "react";
import type { RollOption, RollResult } from "@/lib/rolls";

type AuthoritySlot={id:string;kind:"authority";saveDc:number};
type Props = {
  onAuthority?:()=>Promise<AuthoritySlot>;
  authorityAvailable?:boolean;
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
  onDamage, onAuthority, authorityAvailable,
}: Props) {
  const [results, setResults] = useState<(RollResult|AuthoritySlot)[] | null>(null);
  const [weapon, setWeapon] = useState("");
  const [authorityBusy,setAuthorityBusy]=useState(false),[authorityError,setAuthorityError]=useState("");
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
          disabled={authorityBusy || disabled || !legal.some((o) => o.available)}
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
                  disabled={authorityBusy || disabled}
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
                disabled={authorityBusy || disabled || !selected?.available}
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
          {results.length<count && onAuthority && !results.some(r=>"kind" in r && r.kind==="authority") && <button disabled={disabled||authorityBusy||!authorityAvailable} onClick={async()=>{setAuthorityBusy(true);setAuthorityError("");try{const slot=await onAuthority();setResults(prior=>prior?[...prior,slot]:prior);}catch(e){setAuthorityError((e as Error).message);}finally{setAuthorityBusy(false);}}}>Replace attack {results.length+1} with Authority (spends one use)</button>}
          {authorityError&&<p role="alert">{authorityError}</p>}
          <ol>
            {results.map((result, i) => {
              if("kind" in result)return <li key={result.id}>Attack slot {i+1}: Authority · Wisdom save DC {result.saveDc} · use spent · target outcome manual</li>;
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
                      disabled={authorityBusy || disabled || !damage.available}
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
            disabled={authorityBusy || disabled}
            onClick={() => setResults(null)}
          >
            {results.length < count ? "End sequence" : "Close sequence"}
          </button>
        </>
      )}
    </section>
  );
}

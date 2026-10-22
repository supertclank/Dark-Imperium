import { DicePresentationProps } from "@/lib/rolls";
import { signed } from "@/lib/builder";

/** Future visual presenters take this same immutable result; text remains the fallback. */
export function DiceResult({result:r}:DicePresentationProps) {
  return <article className="roll-result" aria-label={`${r.label} result`}>
    <h3>{r.label}</h3>
    <p className="small muted">{r.characterName} · <time dateTime={r.timestamp}>{new Date(r.timestamp).toLocaleString()}</time> · Private</p>
    {r.dice.groups.map((g,i)=><p key={i}>d{g.sides}: {g.dice.join(" + ")} · Kept: {g.kept.join(", ")}{g.discarded.length>0?` · Discarded: ${g.discarded.join(", ")}`:""}</p>)}
    <p>Modifier: {signed(r.dice.modifier)}{r.context.ability?` · ${r.context.ability}`:""}</p>
    <p className="roll-total">Total: <strong>{r.total}</strong>{r.damageType?` ${r.damageType.name}`:""}</p>
    {r.naturalResult!==null && <p>Natural result: {r.naturalResult}{r.criticalCandidate?" · Critical candidate":""}{r.naturalOne?" · Natural 1":""}</p>}
    {r.rollType==="attack" && <p>Attack total only. Determine the hit manually; critical damage is not applied automatically.</p>}
    {r.rollType==="damage" && !r.grenade && <p>Baseline damage; apply hit and critical rules manually.</p>}
    {r.parentResultId && <p className="small">Linked attack: {r.parentResultId}</p>}
    {r.grenade && <><p>DC {r.grenade.saveDc} {r.grenade.saveAttribute} save · Failed save: {r.grenade.outcomes.failure} · Successful save: {r.grenade.outcomes.success} (half, rounded down).</p><p>{r.grenade.application}</p></>}
    {r.consumption && <p>Consumed {r.consumption.quantity} Frag Grenade · Remaining at execution: {r.consumption.remaining}.</p>}
  </article>;
}

"use client";
import { useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import { SavedCharacter, signed } from "@/lib/builder";
import { RollHistory, RollOption, RollOptions, RollRequest, RollResult } from "@/lib/rolls";
import { DicePresentation, type PresentationEvent } from "./DicePresentation";
import { DiceResult } from "./DiceResult";

type Props={character:SavedCharacter;onRefresh:()=>Promise<void>};
export function RollPanel({character,onRefresh}:Props) {
  const [options,setOptions]=useState<RollOptions|null>(null);
  const [history,setHistory]=useState<RollHistory>({items:[],limit:25,hasMore:false});
  const [latest,setLatest]=useState<RollResult|null>(null);
  const [abilities,setAbilities]=useState<Record<string,string>>({});
  const [confirmation,setConfirmation]=useState<RollOption|null>(null);
  const [busy,setBusy]=useState(false),[error,setError]=useState("");
  const [lastRequest,setLastRequest]=useState<RollRequest|null>(null),[uncertain,setUncertain]=useState(false);
  const [presentation,setPresentation]=useState<PresentationEvent|null>(null);
  const seenResults=useRef(new Set<string>());
  function present(result:RollResult,replay=false){setPresentation(p=>({result,serial:(p?.serial??0)+1,replay}));}
  const inFlight=useRef(false);
  const base=`/characters/${character.id}/rolls`;
  useEffect(()=>{
    let active=true;
    Promise.all([api<RollOptions>(`${base}/options`),api<RollHistory>(base)]).then(([o,h])=>{if(active){setOptions(o);setHistory(h);}}).catch(e=>{if(active)setError(e.message);});
    return()=>{active=false;};
  },[base,character.runtime.stateVersion]);
  async function refresh(){await onRefresh();const [o,h]=await Promise.all([api<RollOptions>(`${base}/options`),api<RollHistory>(base)]);setOptions(o);setHistory(h);}
  async function submit(request:RollRequest){
    if(inFlight.current)return;
    inFlight.current=true;setBusy(true);setError("");setLastRequest(request);setConfirmation(null);
    try {
      const result=await api<RollResult>(base,{method:"POST",body:JSON.stringify(request)});
      present(result,seenResults.current.has(result.id));seenResults.current.add(result.id);
      setLatest(result);setUncertain(false);
      setHistory(h=>({...h,items:[result,...h.items.filter(r=>r.id!==result.id)].slice(0,25)}));
      try {await refresh();} catch {setError("Roll saved. Refresh the sheet to load current inventory and history.");setOptions(null);}
    } catch(e) {
      const failure=e as ApiError;
      setError(failure.message);
      const ambiguous=!(e instanceof ApiError) || failure.status===0 || failure.status>=500;
      setUncertain(ambiguous);
      if(!ambiguous){setLastRequest(null);try{await refresh();}catch{setOptions(null);}}
    } finally {inFlight.current=false;setBusy(false);}
  }
  function requestRoll(option:RollOption,parent?:RollResult,confirmed=false){
    if(!options || !option.available || busy || uncertain)return;
    if(option.consumes && !confirmed){setConfirmation(option);return;}
    const ability=option.abilities.length?(parent?.context.ability || abilities[option.itemId!] || option.abilities[0]):undefined;
    void submit({requestId:crypto.randomUUID(),rollId:option.id,profileId:options.profileId,profileDigest:options.profileDigest,
      expectedStateVersion:options.stateVersion,visibility:"PRIVATE",confirmConsumption:option.consumes,
      ...(ability?{ability}:{}),...(parent?{parentResultId:parent.id}:{})});
  }
  const grouped=options?.options.reduce<Record<string,RollOption[]>>((groups,o)=>{const key=o.itemId || o.category;(groups[key]??=[]).push(o);return groups;},{}) || {};
  const again=latest?options?.options.find(o=>o.id===latest.requestedRollId && !o.consumes):undefined;
  const linkedDamage=latest?.rollType==="attack"?options?.options.find(o=>o.actionId===latest.actionId && o.category==="damage"):undefined;
  return <section className="panel roll-panel" aria-labelledby="rolling-heading">
    <h2 id="rolling-heading">Roll dice</h2>
    <p>Private, server-resolved rolls. Checks and weapon rolls do not spend ammunition. Frag Grenade use consumes one grenade after confirmation.</p>
    <p className="small muted">Resolve targets, hits, critical damage and conditional features manually. No target HP is changed.</p>
    {!options && !error && <p role="status">Loading supported rolls…</p>}
    <DicePresentation event={presentation}/>
    <div className="roll-controls">{Object.entries(grouped).map(([key,items])=>{
      const weapon=!!items[0].itemId;
      const label=weapon?character.calculated.actions.find(a=>a.itemId===key)?.name || items[0].label:({attribute:"Ability checks",skill:"Skill checks",save:"Saving throws",ability:"Initiative"}[key] || key);
      const choices=items[0].abilities;
      return <details key={key} open={weapon || key==="ability"}><summary>{label}</summary>
        {choices.length>0 && <><label htmlFor={`roll-ability-${key}`}>{label} ability</label><select id={`roll-ability-${key}`} disabled={busy||uncertain} value={abilities[key]||choices[0]} onChange={e=>setAbilities({...abilities,[key]:e.target.value})}>{choices.map(a=><option key={a} value={a}>{a}</option>)}</select></>}
        <div className="roll-button-grid">{items.map(option=><div key={option.id}>
          <button type="button" disabled={!option.available || busy || uncertain} onClick={()=>requestRoll(option)} aria-label={option.consumes?"Use Frag Grenade and roll damage":`Roll ${option.label}`}>
            {option.consumes?"Use Frag Grenade / Roll damage":`Roll ${option.label}`}
          </button>
          <p className="small muted">Baseline: {option.groups.map(g=>`${g.count}d${g.sides}`).join(" + ")} {signed(option.modifier)}{option.consumes?` · Quantity: ${option.quantity}`:""}{choices.length?" · Selected ability is calculated on the server":""}</p>
          {!option.available && <p>{option.reason}</p>}
        </div>)}</div>
      </details>;
    })}</div>
    {confirmation && <div className="consumption-confirm" role="group" aria-label="Confirm grenade use"><p>Use Frag Grenade? This will consume 1 of {confirmation.quantity}.</p><button type="button" disabled={busy} onClick={()=>requestRoll(confirmation,undefined,true)}>Confirm use of one Frag Grenade</button><button type="button" disabled={busy} onClick={()=>setConfirmation(null)}>Cancel grenade use</button></div>}
    {busy && <p role="status">Resolving roll on the server…</p>}
    {error && <p role="alert">{error}</p>}
    {uncertain && <p>The outcome is uncertain. Retry this same request to recover the original result without duplicate consumption.</p>}
    {lastRequest && uncertain && <button type="button" className="secondary" disabled={busy} onClick={()=>void submit(lastRequest)}>Retry same request</button>}
    <button type="button" className="secondary" disabled={busy} onClick={()=>{setError("");void refresh().catch(e=>setError(e.message));}}>Refresh rolls and character</button>
    <div aria-live="polite" aria-atomic="true">{latest && <><h3>Latest result</h3><DiceResult result={latest} mode="TEXT_ONLY"/><div className="roll-result-actions"><button type="button" className="secondary" onClick={()=>present(latest,true)}>Replay animation</button>{again&&<button type="button" disabled={busy||uncertain||!again.available} onClick={()=>{if(!options)return;const request:RollRequest={requestId:crypto.randomUUID(),rollId:again.id,profileId:options.profileId,profileDigest:options.profileDigest,expectedStateVersion:options.stateVersion,visibility:"PRIVATE",confirmConsumption:false,...(latest.context.ability&&again.abilities.length?{ability:latest.context.ability}:{})};void submit(request);}}>Roll Again</button>}</div>{linkedDamage && <button type="button" disabled={busy||uncertain||!linkedDamage.available} onClick={()=>requestRoll(linkedDamage,latest)}>Roll linked damage after manually confirming hit</button>}</>}</div>
    <h3>Recent rolls</h3>
    {!history.items.length?<p>No rolls recorded yet.</p>:<ol className="roll-history">{history.items.map(result=><li key={result.id}><details><summary><time dateTime={result.timestamp}>{new Date(result.timestamp).toLocaleTimeString()}</time> · {result.label} · {result.total}{result.damageType?` ${result.damageType.name}`:""}</summary><DiceResult result={result} mode="TEXT_ONLY"/><button type="button" className="secondary" onClick={()=>present(result,true)}>Replay Dice</button></details></li>)}</ol>}
    {history.hasMore && <p>Showing the latest {history.limit} rolls. Older results remain stored.</p>}
  </section>;
}

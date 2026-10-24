"use client";
import type {Choice,Draft} from '@/lib/builder';
import {eligiblePower,type PsychicPolicy} from '@/lib/psychic';
export function PowerChoices({choice,draft,policy,disabled,onChange,approvals=[]}:{choice:Choice;draft:Draft;policy:PsychicPolicy;disabled:boolean;onChange:(ids:string[])=>void;approvals?:string[]}){
 const selected=draft.answers[choice.id]||[];
 const other=new Set(Object.entries(draft.answers).filter(([k])=>k!==choice.id&&k.startsWith('di.choice.psychic.')&&k.includes('_level_')).flatMap(([,v])=>v));
 const powers=policy.powers.filter(p=>choice.options.some(o=>'di.power.'+o.id===p.id)&&eligiblePower(p,draft.classId,draft.answers['di.choice.psyker.subclass']?.[0]||'',policy,approvals));
 return <fieldset className="panel"><legend>{choice.name}</legend><p aria-live="polite">{selected.length} of {choice.cardinality.max} selected</p><div className="archive-choice-grid">{powers.map(p=>{const id=p.id.split('.').at(-1)!;const checked=selected.includes(id);return <article className="panel" key={id}><label><input type="checkbox" checked={checked} disabled={disabled||other.has(id)||(!checked&&selected.length>=choice.cardinality.max)} onChange={e=>onChange(e.target.checked?[...selected,id]:selected.filter(x=>x!==id))}/>{p.name}</label><p>{p.tier} · {p.tags.join(', ')} · {p.actionType.replaceAll('_',' ')} · {p.range}</p><p>{p.attack?'Psychic attack':p.save?`${p.save} save`:'Manual effect'} · Warp +{p.warpPressureCost}</p><details><summary>Power details</summary><p>{p.description}</p><p>{p.manualNote}</p>{p.rulePending&&<p>{p.rulePending.id}: {p.rulePending.text}</p>}</details>{other.has(id)&&<p>Already known</p>}</article>})}</div></fieldset>;
}

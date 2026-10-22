"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { SavedCharacter } from "@/lib/builder";
import { useResource, ResourceState } from "./Resource";
import { CalculatedSummary } from "./CalculatedSummary";
export function CharacterSheet({id}:{id:string}) {
 const {data:character,error,retry}=useResource<SavedCharacter>(`/characters/${id}`);
 const [confirm,setConfirm]=useState(false),[busy,setBusy]=useState(false),[failure,setFailure]=useState("");
 const router=useRouter();
 async function remove(){setBusy(true);try{await api(`/characters/${id}`,{method:"DELETE"});router.push("/characters");}catch(e){setFailure((e as Error).message);setBusy(false);}}
 if(!character)return <ResourceState error={error} retry={retry}/>;
 return <><Link href="/characters" className="back-link">← Your characters</Link><header className="sheet-heading"><div><p className="eyebrow">PERSONNEL RECORD · LEVEL {character.level}</p><h1>{character.name}</h1><p>{character.species.name} · {character.origin.name} · {character.characterClass.name}</p><p>{character.trait.name}</p></div></header>
 <div className="field-note"><strong>Playable with manual rules</strong><p>This sheet uses the validated narrow ruleset. Manual features remain visible; no action spends ammunition or inventory here.</p><small>Ruleset: {character.rulesetProfileId}</small></div>
 <CalculatedSummary calculated={{...character.calculated,inventory:character.inventory}} currentHp={character.runtime.currentHp}/>
 <section className="panel"><h2>Limited-use resources</h2><dl>{Object.entries(character.runtime.resources).map(([key,r])=><div key={key}><dt>{key.replaceAll("_"," ")} · manual tracking</dt><dd>{r.remaining} / {r.maximum} · {r.recovery.replaceAll("_"," ")}</dd></div>)}</dl><p className="muted">Ammunition loading and combat state changes are not automated in this release.</p></section>
 <div className="danger-zone">{failure && <p role="alert">{failure}</p>}{confirm?<><p>Permanently delete <strong>{character.name}</strong> and its inventory?</p><button className="danger" disabled={busy} onClick={remove}>Delete permanently</button><button className="secondary" disabled={busy} onClick={()=>setConfirm(false)}>Keep character</button></>:<button className="text-button" onClick={()=>setConfirm(true)}>Delete character</button>}</div></>;
}

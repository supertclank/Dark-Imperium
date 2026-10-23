"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useResource, ResourceState } from "./Resource";
import { Profile, Draft, Choice, Issue, Validation, SavedCharacter, initialDraft, startingInventory, signed, pathProfile, changePath } from "@/lib/builder";
import { ChoiceCard, SubclassDetails } from "./ChoiceCard";
import { AbilityAllocation } from "./AbilityAllocation";
import { CalculatedSummary } from "./CalculatedSummary";

const steps = ["Identity", "Species", "Origin", "Ability Scores", "Class", "Universal Trait", "Proficiencies & Skills", "Equipment", "Review"];
export function CharacterForm() {
  const {data:baseProfile,error,retry}=useResource<Profile>("/character-builder/profile");
  const [draft,setDraft]=useState<Draft|null>(null),[step,setStep]=useState(0),[busy,setBusy]=useState(false),[failure,setFailure]=useState("");
  const [issues,setIssues]=useState<Issue[]>([]),[validation,setValidation]=useState<Validation|null>(null);
  const router=useRouter(),heading=useRef<HTMLHeadingElement>(null);
  useEffect(()=>{ if(baseProfile) { setDraft(initialDraft(baseProfile,crypto.randomUUID()));setStep(0);setValidation(null); } },[baseProfile]);
  useEffect(()=>{heading.current?.focus();},[step]);
  // Ability previews come from the backend; React never implements a game formula.
  useEffect(()=>{
    if(!draft || step!==3)return;
    let current=true;
    const timer=setTimeout(()=>{api<Validation>("/characters/validate",{method:"POST",body:JSON.stringify(draft)}).then(v=>{if(current)setValidation(v);}).catch(()=>{});},250);
    return ()=>{current=false;clearTimeout(timer);};
  },[draft,step]);
  if(!baseProfile || !draft)return <ResourceState error={error} retry={retry}/>;
  const profile=pathProfile(baseProfile,draft);
  const update=(next:Partial<Draft>)=>{setDraft(("originId" in next || "classId" in next || "speciesId" in next || "level" in next)?changePath(baseProfile,draft,next):{...draft,...next});setIssues([]);setFailure("");setValidation(null);};
  const answer=(choice:Choice,option:string,checked=true)=>{
    const old=draft.answers[choice.id] || [];
    const selected=choice.cardinality.max===1 ? (option?[option]:[]) : checked?[...old,option]:old.filter(x=>x!==option);
    update({answers:{...draft.answers,[choice.id]:selected}});
  };
  const choiceControl=(choice:Choice)=><fieldset className="panel" key={choice.id} aria-describedby={`${choice.id}-help`}>
    <legend>{choice.name}</legend><p id={`${choice.id}-help`} className="muted">Choose {choice.cardinality.min}{choice.cardinality.max!==choice.cardinality.min?`–${choice.cardinality.max}`:""}.</p>
    {choice.cardinality.max===1 ? <><label htmlFor={choice.id}>{choice.name}</label><select id={choice.id} value={draft.answers[choice.id]?.[0] || ""} onChange={e=>answer(choice,e.target.value)}><option value="">Choose an option</option>{choice.options.map(o=><option key={o.id} value={o.id}>{o.label}</option>)}</select></> : <div className="choice-grid">{choice.options.map(o=><label className="choice compact-choice" key={o.id}><input type="checkbox" checked={draft.answers[choice.id]?.includes(o.id)||false} disabled={busy || (!draft.answers[choice.id]?.includes(o.id) && (draft.answers[choice.id]?.length||0)>=choice.cardinality.max)} onChange={e=>answer(choice,o.id,e.target.checked)}/><span>{o.label}</span></label>)}</div>}
    {choice.purpose==="subclass" && <SubclassDetails detail={choice.options.find(o=>o.id===draft.answers[choice.id]?.[0])?.detail} level={draft.level}/>}
  </fieldset>;
  const selector=(group:"species"|"origins"|"classes"|"traits",field:"speciesId"|"originId"|"classId"|"traitId")=><div className="archive-choice-grid">{profile[group].map(item=><ChoiceCard key={item.id} item={item} name={field} selected={draft[field]===item.id} onSelect={()=>{if(!busy)update({[field]:item.id});}} levels={group==="classes"?baseProfile.pathConfigurations?.filter(p=>p.speciesId===draft.speciesId && p.originId===draft.originId && p.classId===item.id).map(p=>p.level):undefined}/>)}</div>;
  const relevant=(issue:Issue)=>{
    const fields=[["name"],["speciesId"],["originId"],["attributes",...profile.choices.filter(c=>c.purpose==="attribute").map(c=>`answers.${c.id}`)],["classId","level",...profile.choices.filter(c=>c.purpose==="subclass").map(c=>`answers.${c.id}`)],["traitId"],profile.choices.filter(c=>c.purpose!=="attribute").map(c=>`answers.${c.id}`),["inventory","packageChoices"], [""]][step];
    return issue.field.startsWith("profile") || fields.some(f=>issue.field.startsWith(f));
  };
  async function next() {
    if(!draft)return;setBusy(true);setFailure("");
    try {const result=await api<Validation>("/characters/validate",{method:"POST",body:JSON.stringify(draft)});setValidation(result);const selected=step===7?result.errors:result.errors.filter(relevant);setIssues(selected);if(!selected.length)setStep(i=>Math.min(i+1,8));}
    catch(e){setFailure((e as Error).message);}finally{setBusy(false);}
  }
  async function save() {
    if(!draft)return;setBusy(true);setFailure("");
    try {const saved=await api<SavedCharacter>("/characters",{method:"POST",body:JSON.stringify(draft)});router.push(`/characters/${saved.id}`);}
    catch(e){setFailure((e as Error).message);if(e && typeof e==="object" && "issues" in e)setIssues(e.issues as Issue[]);setBusy(false);}
  }
  return <div className="production-builder">
    <div className="field-note"><strong>Supported creation path</strong><p>{profile.availability.find(a=>a.status==="SUPPORTED")?.message}</p><details><summary>Catalogue availability</summary>{profile.availability.filter(a=>a.status!=="SUPPORTED").map(a=><p key={a.status}><strong>{a.status==="MANUAL"?"Manual play":"Not currently available"}</strong> — {a.message}</p>)}</details></div>
    <nav aria-label="Character creation progress"><ol className="builder-steps">{steps.map((title,index)=><li key={title} aria-current={step===index?"step":undefined}><span>{index+1}</span> {title}</li>)}</ol></nav>
    <h2 ref={heading} tabIndex={-1}>{step+1}. {steps[step]}</h2>
    <form onSubmit={e=>{e.preventDefault();if(step===8)void save();else void next();}}>
      <fieldset disabled={busy} className="builder-stage">
      {step===0 && <div className="panel"><label htmlFor="character-name">Character name</label><input id="character-name" maxLength={80} value={draft.name} onChange={e=>update({name:e.target.value})} autoComplete="off"/><p className="muted">A name is all you need to begin. Biography and portraits can wait.</p></div>}
      {step===1 && selector("species","speciesId")}
      {step===2 && selector("origins","originId")}
      {step===3 && <><AbilityAllocation profile={profile} draft={draft} preview={validation?.abilityPreview} onChange={attributes=>update({attributes})}/>{profile.choices.some(c=>c.purpose==="attribute") && <section className="species-bonus"><h3>Species ability bonuses</h3><p>These bonuses are separate from your Standard Array base scores.</p>{profile.choices.filter(c=>c.purpose==="attribute").map(choiceControl)}</section>}</>}
      {step===4 && <>{selector("classes","classId")}<section className="panel"><label htmlFor="character-level">Level</label><select id="character-level" value={draft.level} onChange={e=>update({level:Number(e.target.value)})}>{profile.levels.map(level=><option key={level} value={level}>{level}</option>)}</select><p>Hit Die d{profile.training.hitDie}</p>{profile.choices.filter(c=>c.purpose==="subclass").map(choiceControl)}<p>Saving throw proficiencies: {profile.training.savingThrows.join(", ")}</p></section></>}
      {step===5 && selector("traits","traitId")}
      {step===6 && profile.choices.filter(c=>c.purpose!=="attribute" && c.purpose!=="subclass").map(choiceControl)}
      {step===7 && <section className="panel">{profile.package.choices.map(choice=><div key={choice.id}><label htmlFor={`package-${choice.id}`}>{choice.id} equipment</label><select id={`package-${choice.id}`} value={draft.packageChoices[choice.id]||""} onChange={e=>{const choices={...draft.packageChoices,[choice.id]:e.target.value};update({packageChoices:choices,inventory:startingInventory(profile,choices)});}}><option value="">Choose equipment</option>{choice.options.map(o=><option key={o.id} value={o.id}>{profile.equipment.find(x=>x.id===o.id)?.name}</option>)}</select></div>)}<h3>Starting inventory</h3><ul>{draft.inventory.map(i=><li key={i.definitionId}>{profile.equipment.find(x=>x.id===i.definitionId)?.name} × {i.quantity}{i.equipped?" · equipped":""}</li>)}</ul><p className="muted">Only reviewed equipment is available. Other package alternatives are unavailable in this release.</p></section>}
      {step===8 && <><section className="panel"><h3>{draft.name}</h3><p>{profile.species.find(x=>x.id===draft.speciesId)?.name} · {profile.origins.find(x=>x.id===draft.originId)?.name} · {profile.classes.find(x=>x.id===draft.classId)?.name} · Level {draft.level}</p><p>{profile.traits.find(x=>x.id===draft.traitId)?.name}</p></section>{validation?.calculated ? <CalculatedSummary calculated={validation.calculated}/> : <p role="status">Validate the complete draft before saving.</p>}</>}
      </fieldset>
      {(issues.length>0 || failure) && <div className="error panel" role="alert">{failure && <p>{failure}</p>}<ul>{issues.map((issue,i)=><li key={`${issue.field}-${i}`}><strong>{issue.field}</strong>: {issue.message}</li>)}</ul></div>}
      <div className="builder-navigation">{step>0 && <button type="button" className="secondary" disabled={busy} onClick={()=>{setStep(i=>i-1);setIssues([]);}}>Back</button>}{step===8 ? <button className="primary" disabled={busy || !validation?.calculated}>{busy?"Saving character…":"Create character"}</button> : <button className="primary" disabled={busy}>{busy?"Validating…":"Continue"}</button>}</div>
    </form>
  </div>;
}

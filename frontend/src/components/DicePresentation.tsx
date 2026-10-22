"use client";
import { useEffect,useRef,useState } from 'react';
import type { RollResult } from '@/lib/rolls';
import { defaultPreferences,effectiveMode,presentRoll,preferenceKey,readPreferences,type DicePreferences } from '@/lib/dice-presentation';
import type { DiceTrayRenderer } from '@/lib/dice-renderer';
export type PresentationEvent={result:RollResult;serial:number;replay:boolean};
export function DicePresentation({event}:{event:PresentationEvent|null}) {
 const [preferences,setPreferences]=useState<DicePreferences>(defaultPreferences),[ready,setReady]=useState(false),[reduce,setReduce]=useState(false);
 const [closed,setClosed]=useState(false),[failure,setFailure]=useState(false),[settled,setSettled]=useState(false);
 const tray=useRef<HTMLElement>(null);
 const host=useRef<HTMLDivElement>(null),renderer=useRef<DiceTrayRenderer|null>(null),audio=useRef<AudioContext|null>(null),sound=useRef(false);
 const currentEvent=useRef(event),skipped=useRef(false);currentEvent.current=event;
 const mode=effectiveMode(preferences.mode,reduce),model=event?presentRoll(event.result):null;
 useEffect(()=>{try{setPreferences(readPreferences(localStorage.getItem(preferenceKey)));}catch{}setReady(true);
  const media=window.matchMedia?.('(prefers-reduced-motion: reduce)');if(!media)return;setReduce(media.matches);const update=()=>setReduce(media.matches);media.addEventListener('change',update);return()=>media.removeEventListener('change',update);
 },[]);
 useEffect(()=>{sound.current=preferences.sound;if(ready)try{localStorage.setItem(preferenceKey,JSON.stringify(preferences));}catch{}},[preferences,ready]);
 useEffect(()=>()=>{void audio.current?.close();},[]);
 useEffect(()=>{if(!preferences.sound)return;const unlock=()=>{try{audio.current??=new AudioContext();void audio.current.resume().catch(()=>{});}catch{}};document.addEventListener('pointerdown',unlock);document.addEventListener('keydown',unlock);return()=>{document.removeEventListener('pointerdown',unlock);document.removeEventListener('keydown',unlock);};},[preferences.sound]);
 useEffect(()=>{if(!event||!tray.current)return;const bounds=tray.current.getBoundingClientRect();if(bounds.top<0||bounds.bottom>window.innerHeight)tray.current.scrollIntoView?.({block:'nearest',behavior:'instant'});},[event,closed]);
 function clickSound(){if(!sound.current||!audio.current)return;try{const ctx=audio.current;if(ctx.state!=='running')return;const oscillator=ctx.createOscillator(),gain=ctx.createGain();oscillator.type='triangle';oscillator.frequency.setValueAtTime(145,ctx.currentTime);oscillator.frequency.exponentialRampToValueAtTime(55,ctx.currentTime+.09);gain.gain.setValueAtTime(.035,ctx.currentTime);gain.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.12);oscillator.connect(gain).connect(ctx.destination);oscillator.start();oscillator.stop(ctx.currentTime+.13);}catch{}}
 // Reuse the renderer across rolls. Load only when a completed result actually needs 3D.
 useEffect(()=>{
  if(!ready||!event||closed||mode!=='3D'||failure||!host.current)return;
  let active=true;
  import('@/lib/dice-renderer').then(({createDiceRenderer})=>{
   if(!active||!host.current)return;
   try {renderer.current=createDiceRenderer(host.current,()=>{if(active)setFailure(true);},()=>{if(active){setSettled(true);clickSound();}});
    renderer.current.show(presentRoll(currentEvent.current!.result),skipped.current);
   }catch{if(active)setFailure(true);}
  }).catch(()=>{if(active)setFailure(true);});
  return()=>{active=false;renderer.current?.dispose();renderer.current=null;};
 // A new event uses the existing renderer below, rather than rebuilding its GPU resources.
 // eslint-disable-next-line react-hooks/exhaustive-deps
 },[ready,!!event,closed,mode,failure]);
 useEffect(()=>{skipped.current=false;setClosed(false);setSettled(mode!=='3D');if(event&&renderer.current){try{renderer.current.show(presentRoll(currentEvent.current!.result),skipped.current);}catch{setFailure(true);}}},[event]);
 function setSound(enabled:boolean){setPreferences(p=>({...p,sound:enabled}));if(enabled)try{audio.current??=new AudioContext();void audio.current.resume().catch(()=>{});}catch{}}
 return <div className="dice-presentation">
  <details className="dice-preferences"><summary>Dice presentation settings</summary><div className="dice-settings-grid">
   <label>Dice presentation<select aria-label="Dice presentation" value={preferences.mode} onChange={e=>setPreferences(p=>({...p,mode:e.target.value as DicePreferences['mode']}))}><option value="3D">3D</option><option value="REDUCED_MOTION">Reduced Motion</option><option value="TEXT_ONLY">Text Only</option></select></label>
   <label>Dice sound<select aria-label="Dice sound" value={preferences.sound?'on':'off'} onChange={e=>setSound(e.target.value==='on')}><option value="off">Off</option><option value="on">On</option></select></label>
  </div><p className="small muted">Saved on this device. System reduced-motion settings take priority. Sound is optional and may require enabling it in this session.</p></details>
  {model&&!closed&&<section ref={tray} className={`dice-tray ${model.natural===20||model.natural===1?'dice-natural':''}`} aria-label="Dice presentation tray">
   <div className="dice-tray-heading"><div><span className="eyebrow">{event?.replay?'REPLAY ANIMATION · STORED RESULT':'AUTHORITATIVE RESULT'}</span><h3>{model.label}</h3></div><button type="button" className="secondary" onClick={()=>setClosed(true)} aria-label="Close dice tray">Close</button></div>
   {mode==='3D'&&!failure?<><div className="dice-canvas" ref={host}/>{!settled&&<button type="button" className="secondary" onClick={()=>{skipped.current=true;renderer.current?.skip();setSettled(true);}}>Skip animation</button>}</>:null}
   {failure&&mode==='3D'&&<p role="status">3D dice unavailable. Showing standard roll result.</p>}
   {mode==='REDUCED_MOTION'&&<p className="small muted">Reduced motion · static dice results</p>}
   <ol className="dice-values" aria-label="Authoritative individual dice">{model.dice.map(d=><li key={d.id} className={d.discarded?'discarded':''}><span>d{d.sides}</span><strong>{d.value}</strong><small>{d.discarded?'Discarded':'Kept'}</small></li>)}</ol>
   <p className="dice-equation">Modifier {model.modifier>=0?'+':''}{model.modifier} <span>→</span> <strong>Total {model.total}{model.damageType?` ${model.damageType}`:''}</strong></p>
   {model.natural!==null&&(model.natural===20||model.natural===1)&&<p>Natural {model.natural}{model.criticalCandidate?' · Critical candidate':''} · Gameplay effects remain manually adjudicated.</p>}
  </section>}
 </div>;
}

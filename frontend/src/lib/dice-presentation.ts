import type { RollResult } from './rolls';
export type PresentationMode='3D'|'REDUCED_MOTION'|'TEXT_ONLY';
export type PresentedDie={id:string;sides:number;value:number;discarded:boolean};
export type DicePresentation={id:string;label:string;category:string;dice:PresentedDie[];modifier:number;total:number;natural:number|null;criticalCandidate:boolean;naturalOne:boolean;damageType:string|null};
/** Copies stored outcomes only. No RNG, calculation, API, or character mechanics. */
export function presentRoll(result:RollResult):DicePresentation {
 return {id:result.id,label:result.label,category:result.rollType,
  dice:result.dice.groups.flatMap((g,group)=>g.dice.map((value,index)=>({id:`${result.id}:${group}:${index}`,sides:g.sides,value,discarded:g.discardedIndices.includes(index)}))),
  modifier:result.dice.modifier,total:result.total,natural:result.naturalResult,criticalCandidate:result.criticalCandidate,naturalOne:result.naturalOne,damageType:result.damageType?.name??null};
}
export const preferenceKey='dark-imperium.dice-presentation.v1';
export type DicePreferences={mode:PresentationMode;sound:boolean};
export const defaultPreferences:DicePreferences={mode:'3D',sound:false};
export function readPreferences(value:string|null):DicePreferences {
 try {const p=JSON.parse(value||'null');return {mode:['3D','REDUCED_MOTION','TEXT_ONLY'].includes(p?.mode)?p.mode:'3D',sound:p?.sound===true};}catch{return defaultPreferences;}
}
export function effectiveMode(mode:PresentationMode,reduce:boolean):PresentationMode {return mode==='3D'&&reduce?'REDUCED_MOTION':mode;}

export type RollOption = {
  id: string; label: string; category: string; actionId: string | null; itemId: string | null;
  available: boolean; reason: string | null; consumes: boolean; quantity: number | null;
  abilities: string[]; groups: { count:number; sides:number }[]; modifier:number;
};
export type RollOptions = { profileId:string; profileDigest:string; stateVersion:number; options:RollOption[] };
export type RollRequest = { requestId:string; rollId:string; profileId:string; profileDigest:string; expectedStateVersion:number; ability?:string; parentResultId?:string; visibility:"PRIVATE"; confirmConsumption:boolean };
export type RollResult = {
  request?:RollRequest; id:string; requestId:string; characterId:string; characterName:string; label:string; rollType:string;
  actionId:string|null; requestedRollId:string; rulesetProfileId:string; rulesetDigest:string;
  timestamp:string; total:number; naturalResult:number|null; criticalCandidate:boolean; naturalOne:boolean;
  dice:{ groups:{ sides:number; dice:number[]; kept:number[]; discarded:number[]; keptIndices:number[]; discardedIndices:number[]; keep:string }[]; modifier:number; total:number };
  damageType:{id:string;name:string}|null; parentResultId:string|null;
  context:{ ability:string|null; targetResolution:string; criticalDamage:string };
  stateVersionBefore:number; stateVersionAfter:number;
  consumption:{itemId:string;quantity:number;remaining:number}|null;
  grenade:{saveAttribute:string;saveDc:number;outcomes:{failure:number;success:number};application:string}|null;
};
export type RollHistory={items:RollResult[];limit:number;hasMore:boolean};
// Presentation consumes a completed server result; it can never determine a result.
export type DicePresentationMode="TEXT_ONLY"|"REDUCED_MOTION"|"3D";
export type DicePresentationProps={result:RollResult;mode?:DicePresentationMode};

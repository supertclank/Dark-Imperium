export type PsychicPower = {id:string;name:string;tier:string;tags:string[];actionType:string;range:string;attack:boolean;save:string|null;description:string;warpPressureCost:number;extraWarpPressure:number;automationStatus:string;manualNote:string;empoweredOptions:string[];sources:{locator:{pdfPage:number;heading:string}}[];roll?:{count:number;sides:number;kind:string;damageType:string|null};rulePending?:{id:string;text:string}};
export type PsychicPolicy = {powers:PsychicPower[];disciplineTags:Record<string,string>;empoweredOptions:{id:string;name:string;description:string}[]};
export type PsychicCalculation = {ability:string;abilityModifier:number;attackModifier:number;saveDc:number;powers:PsychicPower[];empoweredOptions:PsychicPolicy['empoweredOptions']};
/** Presentation filtering only. The backend independently enforces the same source restrictions. */
export function eligiblePower(power:PsychicPower,classId:string,discipline:string,policy:PsychicPolicy,approvals:string[]=[]){
 if(classId==='di.class.psyker')return !power.tags.includes('Warlock') && (power.tags.includes('Universal') || power.tags.includes(policy.disciplineTags[discipline]));
 if(classId==='di.class.aeldari_warlock')return !power.tags.includes('Malefic') && (power.tags.some(t=>['Universal','Divination','Telekinesis','Warlock'].includes(t)) || (approvals.includes('warlock_pyromancy')&&power.tags.includes('Pyromancy')));
 return false;
}

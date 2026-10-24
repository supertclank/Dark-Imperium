import type {PsychicPolicy,PsychicCalculation} from "./psychic";
export type FeatureView = { id?:string; name:string; text:string; manual?:boolean; classification?:"AUTOMATED"|"PARTIAL"|"MANUAL"|"BLOCKED"; playerNote?:string };
export type SubclassDetail = { id:string; name:string; levels:{level:number;features:FeatureView[]}[] };
export type ChoicePresentation = { summary:string; stats:{label:string;value:string}[]; groups:{label:string;items:{name:string;state?:string}[]}[]; features:FeatureView[]; levels:{level:number;features:FeatureView[]}[] };
export type OptionRecord = { id: string; name: string; description: string; presentation?:ChoicePresentation };
export type Choice = { id: string; name: string; purpose: string; cardinality: { min: number; max: number }; options: { id: string; label: string; detail?:SubclassDetail }[] };
export type InventorySelection = { definitionId: string; quantity: number; equipped: boolean };
export type Draft = { profileId: string; profileDigest: string; requestId: string; name: string; speciesId: string; originId: string; classId: string; traitId: string; level: number; attributes: Record<string, number>; answers: Record<string, string[]>; packageChoices: Record<string, string>; inventory: InventorySelection[] };
export type PathConfiguration = { speciesId:string; originId:string; classId:string; level:number; choices:string[]; features:string[] };
export type Profile = { approvalScopes?:string[]; psychic?:PsychicPolicy|null; pathConfigurations?:PathConfiguration[]; packages?:Record<string,Profile["package"]>; classTraining?:Record<string,Profile["training"]>; featureCatalogue?:OptionRecord[]; id: string; digest: string; name: string; attributes: string[]; standardArray: number[]; levels: number[]; species: OptionRecord[]; origins: OptionRecord[]; classes: OptionRecord[]; traits: OptionRecord[]; choices: Choice[]; levelFeatures: OptionRecord[]; equipment: OptionRecord[]; armour: string[]; training: { hitDie: number; savingThrows: string[] }; package: { fixed: { item: { id: string }; quantity: number }[]; choices: { id: string; options: { id: string }[]; quantity: number }[] }; availability: { status: string; message: string }[] };
export type Issue = { code: string; field: string; message: string };
export type Calculation = {
  psychic?:PsychicCalculation; classActions?:{authority?:{saveDc:number}};
  attackAction?:{replacementActions?:{id:string;maximumPerAttackAction:number;consumesResource:string}[];attacksPerAttackAction:number;featureIds:string[];actionIds:string[];scope:string;turnTracking:boolean};
  advancementSelection?:{talentId?:string;label:string;benefit?:string;subchoiceLabel?:string;subchoiceText?:string;note?:string;classification?:string}|null;
  abilityAdjustments?:{attribute:string;amount:number;minimum:number;before:number;after:number;floorApplied:boolean}[];
  speciesMechanics?:{kind:string;contexts?:string[];text?:string;name?:string;count?:number;sides?:number;ability?:string}[]; size?:string; darkvisionFeet?:number;
  subclass?:OptionRecord|null; contacts?:{id:string;text:string}[]; proceduralProficiencies?:string[]; equipmentNotes?:Record<string,string>;
  attributes: Record<string, number>; attributeModifiers: Record<string, number>; proficiencyBonus: number; maximumWounds: number; defence: number; movement: number; initiative: number;
  saves: Record<string, { modifier: number; proficient: boolean }>;
  skills: Record<string, { name: string; modifier: number; proficient: boolean; attribute: string }>;
  proficiencies: OptionRecord[];
  features: { id: string; name: string; text: string; manual: boolean; classification?:"AUTOMATED"|"PARTIAL"|"MANUAL"|"BLOCKED"; playerNote?:string; sources: { locator: { heading: string; pdfPage: number } }[] }[];
  inventory: (InventorySelection & { name: string })[];
  actions: { id: string; itemId: string; name: string; attackBonus: number | null; ability: string | null; attackAbilityId?:string|null; damageAbilityId?:string|null; damageExpression: string; damageType: string; range: { kind: string; normal?: { value: number; unit: string }; long?: { value: number; unit: string }; distance?: { value: number; unit: string } }; properties: string[]; saveDc: number | null; save?: { attribute: string; outcomes: Record<string, { damageMultiplier: { numerator:number; denominator:number }; rounding:string }> } | null; area?: { radius: { value: number; unit: string } } | null; manual: boolean }[];
  rollDefinitions: { id: string; category: string; label: string }[]; rollAuthority: string; readiness: string;
};
export type Validation = { status: string; errors: Issue[]; calculated?: Calculation | null; abilityPreview?: { scores: Record<string,number>; modifiers: Record<string,number>; breakdown?:Record<string,{base:number;speciesAdjustment:number;adjustments:{amount:number;minimum:number;before:number;after:number;floorApplied:boolean}[]}> } | null };
export type CharacterSummary = { id: string; name: string; species: { name: string }; origin: { name: string }; characterClass: { name: string }; level: number; updatedAt: string; rulesetProfileId: string };
export type SavedCharacter = CharacterSummary & { rulesetDigest: string; selections: Draft; trait: { name: string }; calculated: Calculation; approvalScopes?:string[]; runtime: { currentWarpPressure?:number;pendingAction?:{id:string;name:string;stage:string;peril?:string;perilDescription?:string;powerId?:string;empoweredOption?:string;empoweredInstruction?:string;saveDc?:number;targetNumber?:number;rerolled?:boolean;effectDice?:{total:number;groups:{dice:number[]}[]}}|null; currentHp: number; stateVersion: number; resources: Record<string, { remaining: number; maximum: number; recovery: string }> }; inventory: (InventorySelection & { id: string; name: string; ammunition: unknown })[] };
export function startingInventory(profile: Profile, choices: Record<string,string>): InventorySelection[] {
  return [...profile.package.fixed.map(row => ({ definitionId: row.item.id, quantity: row.quantity })), ...profile.package.choices.filter(row => choices[row.id]).map(row => ({ definitionId: choices[row.id], quantity: row.quantity }))].map(row => ({ ...row, equipped: profile.armour.includes(row.definitionId) }));
}
export function initialDraft(profile: Profile, requestId: string): Draft {
  const first=profile.pathConfigurations?.[0];
  if(first) profile=pathProfile(profile,first);
  const packageChoices = Object.fromEntries(profile.package.choices.filter(c => c.options.length === 1).map(c => [c.id,c.options[0].id]));
  return { profileId:profile.id, profileDigest:profile.digest, requestId, name:"", speciesId:profile.species[0]?.id || "", originId:profile.origins[0]?.id || "", classId:profile.classes[0]?.id || "", traitId:profile.traits[0]?.id || "", level:profile.levels[0], attributes:{}, answers:Object.fromEntries(profile.choices.filter(c=>c.options.length===1 && c.cardinality.max===1).map(c=>[c.id,[c.options[0].id]])), packageChoices, inventory:startingInventory(profile,packageChoices) };
}
export const signed = (value:number) => value >= 0 ? `+${value}` : String(value);

/** Presentation filters only; the server validates every complete path and choice. */
export function pathProfile(base:Profile,draft:Pick<Draft,"speciesId"|"originId"|"classId"|"level">):Profile {
  if(!base.pathConfigurations)return base;
  const family=base.pathConfigurations.filter(p=>p.speciesId===draft.speciesId && p.originId===draft.originId && p.classId===draft.classId);
  const current=family.find(p=>p.level===draft.level);
  return {...base,origins:base.origins.filter(o=>base.pathConfigurations!.some(p=>p.speciesId===draft.speciesId && p.originId===o.id)),classes:base.classes.filter(c=>base.pathConfigurations!.some(p=>p.speciesId===draft.speciesId && p.originId===draft.originId && p.classId===c.id)),levels:family.map(p=>p.level).filter(level=>base.levels.includes(level)),choices:base.choices.filter(c=>current?.choices.includes(c.id)),package:base.packages?.[draft.classId]||base.package,training:base.classTraining?.[draft.classId]||base.training,levelFeatures:(base.featureCatalogue||[]).filter(f=>current?.features.includes(f.id))};
}
export function changePath(base:Profile,draft:Draft,next:Partial<Draft>):Draft {
  let result={...draft,...next};
  if(!base.pathConfigurations)return result;
  const eligible=base.pathConfigurations.filter(p=>p.speciesId===result.speciesId);
  if(!eligible.some(p=>p.originId===result.originId))result={...result,originId:eligible[0]?.originId||""};
  if(!eligible.some(p=>p.originId===result.originId && p.classId===result.classId))result={...result,classId:eligible.find(p=>p.originId===result.originId)?.classId||""};
  let profile=pathProfile(base,result);
  if(!profile.levels.includes(result.level)) {result={...result,level:profile.levels[0]||1};profile=pathProfile(base,result);}
  const answers=Object.fromEntries(profile.choices.map(c=>[c.id,result.answers[c.id] || (c.options.length===1 && c.cardinality.max===1?[c.options[0].id]:[])]));
  const packageChoices=Object.fromEntries(profile.package.choices.map(c=>[c.id,c.options.some(o=>o.id===result.packageChoices[c.id])?result.packageChoices[c.id]:c.options.length===1?c.options[0].id:""]));
  return {...result,answers,packageChoices,inventory:startingInventory(profile,packageChoices)};
}

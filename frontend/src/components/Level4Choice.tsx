import {useState} from "react";
import {ChoiceCard} from "./ChoiceCard";
export type ImprovementOption={id:string;label:string;branch:string;abilities?:string[];talentId?:string;requirement?:string;benefit?:string;classification?:string;note?:string;subchoiceId?:string;subchoiceLabel?:string;subchoiceText?:string};
export type ImprovementPolicy={choiceId:string;branches:string[];options:ImprovementOption[]};
export function Level4Choice({policy,value,owned,onChange,disabled=false}:{policy:ImprovementPolicy;value:string;owned:string[];onChange:(value:string)=>void;disabled?:boolean}){
 const [branch,setBranch]=useState(""),[talent,setTalent]=useState("");
 const [first,setFirst]=useState(""),[second,setSecond]=useState("");
 const options=policy.options.filter(o=>!o.talentId||!owned.includes(o.talentId));
 const talents=options.filter((o,i,a)=>o.talentId&&a.findIndex(x=>x.talentId===o.talentId)===i);
 const abilities=Array.from(new Set(options.flatMap(o=>o.abilities||[])));
 function changeBranch(next:string){setBranch(next);setTalent("");setFirst("");setSecond("");onChange("");}
 function split(a:string,b:string){setFirst(a);setSecond(b);onChange(options.find(o=>o.branch==="ASI_SPLIT"&&o.abilities?.includes(a)&&o.abilities?.includes(b)&&a!==b)?.id||"");}
 const subchoices=options.filter(o=>o.talentId===talent);
 return <fieldset disabled={disabled} className="builder-stage"><legend>Choose your Level 4 advancement</legend><div className="level4-branches">{policy.branches.map(b=><label key={b}><input type="radio" name="level4-branch" checked={branch===b} onChange={()=>changeBranch(b)}/>{b==="TALENT"?"Talent":b==="ASI_PLUS_TWO"?"Ability Score Improvement: +2 to one ability":"Ability Score Improvement: +1 to two different abilities"}</label>)}</div>
 {branch==="ASI_PLUS_TWO"&&<><label htmlFor="asi-two">Ability to increase by 2</label><select id="asi-two" value={value} onChange={e=>onChange(e.target.value)}><option value="">Choose an ability</option>{options.filter(o=>o.branch===branch).map(o=><option key={o.id} value={o.id}>{o.label}</option>)}</select></>}
 {branch==="ASI_SPLIT"&&<div className="ability-inputs">{[["First ability",first],["Second ability",second]].map(([label,v],i)=><label key={label}>{label}<select value={v} onChange={e=>i===0?split(e.target.value,second):split(first,e.target.value)}><option value="">Choose an ability</option>{abilities.filter(a=>a===(i===0?first:second)||a!==(i===0?second:first)).map(a=><option key={a} value={a}>{a}</option>)}</select></label>)}</div>}
 {branch==="TALENT"&&<><div className="archive-choice-grid">{talents.map(o=><ChoiceCard key={o.talentId} name="level4-talent" selected={talent===o.talentId} onSelect={()=>{if(!disabled){setTalent(o.talentId!);onChange(o.subchoiceId?"":o.id);}}} item={{id:o.talentId!,name:o.benefit?.split("\n")[0].replace(/^Talent: /,"")||o.label,description:o.benefit||"",presentation:{summary:o.benefit||"",stats:[{label:"Requirement",value:o.requirement||"General Talent"},{label:"Effects",value:o.classification==="PARTIAL"?"Some effects require manual adjudication":"Manual tracking required"}],groups:[],features:[{name:"Playing this Talent",text:o.note||""}],levels:[]}}}/>)}</div>{subchoices.some(o=>o.subchoiceId)&&<><label htmlFor="talent-subchoice">Talent choice</label><select id="talent-subchoice" value={value} onChange={e=>onChange(e.target.value)}><option value="">Choose one option</option>{subchoices.map(o=><option key={o.id} value={o.id}>{o.subchoiceLabel}</option>)}</select><p>{subchoices.find(o=>o.id===value)?.subchoiceText}</p></>}</>}
 </fieldset>;
}

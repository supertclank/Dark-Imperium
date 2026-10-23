import { FeatureView, OptionRecord, SubclassDetail } from "@/lib/builder";
export function ChoiceFeatureList({features}:{features:FeatureView[]}) {
 return <div className="choice-features">{features.map((f,i)=><section key={f.id||`${f.name}-${i}`}><h4>{f.name}</h4>{(f.classification || f.manual) && <span className="choice-badge">{f.classification?{AUTOMATED:"Calculated",PARTIAL:"Partly calculated",MANUAL:"Manual tracking",BLOCKED:"Unavailable"}[f.classification]:"Manual tracking"}</span>}<p>{f.text}</p>{f.playerNote && <p className="muted">{f.playerNote}</p>}</section>)}</div>;
}
export function SubclassDetails({detail,level}:{detail?:SubclassDetail;level:number}) {
 if(!detail)return null;
 return <section className="subclass-detail" aria-label={`${detail.name} details`} aria-live="polite"><h3>{detail.name}</h3>{detail.levels.filter(l=>l.level<=level).map(l=><div key={l.level}><p className="eyebrow">Level {l.level} feature</p><ChoiceFeatureList features={l.features}/></div>)}</section>;
}
export function ChoiceCard({item,name,selected,onSelect,levels}:{item:OptionRecord;name:string;selected:boolean;onSelect:()=>void;levels?:number[]}) {
 const p=item.presentation;
 return <article className={`archive-choice ${selected?"is-selected":""}`} onClick={e=>{if(!(e.target as HTMLElement).closest("input, label, details, button, a, select"))onSelect();}}>
  <label className="archive-choice-select"><input type="radio" name={name} checked={selected} onChange={onSelect} aria-label={item.name}/><span className="archive-choice-title"><strong>{item.name}</strong><span className="selection-state">{selected?"Selected":"Select"}</span></span></label>
  <p className="choice-intro">{p?.summary || (!p || (!p.stats.length && !p.groups.length && !p.features.length && !p.levels.length)?item.description:"")}</p>
  {!!p?.stats.length && <dl className="choice-stats">{p.stats.map((s,i)=><div key={`${s.label}-${i}`}><dt>{s.label}</dt><dd>{s.value}</dd></div>)}</dl>}
  {p && (!!p.groups.length || !!p.features.length || !!p.levels.length) && <details className="choice-details"><summary>Details for {item.name}</summary>
   {p.groups.map((g,index)=><section className="choice-group" key={`${g.label}-${index}`}><h4>{g.label}</h4><ul className="choice-badges">{g.items.map((x,i)=><li key={`${x.name}-${i}`}><span className="choice-badge">{x.name}{x.state && <> <span className="badge-state">{x.state}{["RARE","LIMITED"].includes(x.state)?" · GM approval required":""}</span></>}</span></li>)}</ul></section>)}
   {!!p.features.length && <><h3>Features</h3><ChoiceFeatureList features={p.features}/></>}
   {p.levels.filter(l=>!levels || levels.includes(l.level)).map(l=><section key={l.level}><h3>Level {l.level}</h3><ChoiceFeatureList features={l.features}/></section>)}
  </details>}
 </article>;
}

import { Profile, Draft, Validation, signed } from "@/lib/builder";
export function availableScores(pool:number[],attributes:Record<string,number>,key:string) {
 return pool.filter(value=>attributes[key]===value || !Object.entries(attributes).some(([other,used])=>other!==key && used===value));
}
export function AbilityAllocation({profile,draft,preview,onChange}:{profile:Profile;draft:Draft;preview:Validation["abilityPreview"];onChange:(attributes:Record<string,number>)=>void}) {
 function assign(key:string,value:string) {
  const next={...draft.attributes};
  if(value==="")delete next[key];
  else {const n=Number(value);if(!availableScores(profile.standardArray,draft.attributes,key).includes(n))return;next[key]=n;}
  onChange(next);
 }
 return <section className="panel ability-allocation" aria-label="Standard Array allocation"><h3>Standard Array</h3><p>Assign each score once. Clear a base score to return it to the pool; other abilities stay as you assigned them.</p><p className="score-pool" aria-live="polite">Available: {profile.standardArray.filter(n=>!Object.values(draft.attributes).includes(n)).join(" · ") || "All scores assigned"}</p>
 <div className="ability-table"><div className="ability-table-heading" aria-hidden="true"><span>Ability</span><span>Base</span><span>Species</span><span>Final</span><span>Modifier</span></div>
 {profile.attributes.map(key=>{const row=preview?.breakdown?.[key];return <div className="ability-row" key={key}><label htmlFor={`base-${key}`}>{key}</label><div><span className="mobile-column" aria-hidden="true">Base</span><select id={`base-${key}`} value={draft.attributes[key]??""} onChange={e=>assign(key,e.target.value)}><option value="" aria-label="Unassigned">—</option>{availableScores(profile.standardArray,draft.attributes,key).map(n=><option key={n} value={n}>{n}</option>)}</select></div><div aria-label={`${key} species adjustment`}><span className="mobile-column" aria-hidden="true">Species</span>{row?signed(row.speciesAdjustment):"—"}</div><div aria-label={`${key} final score`}><span className="mobile-column" aria-hidden="true">Final</span><strong>{preview?.scores[key]??"—"}</strong></div><div aria-label={`${key} modifier`}><span className="mobile-column" aria-hidden="true">Modifier</span>{preview?signed(preview.modifiers[key]):"—"}</div>{row?.adjustments.map((a,i)=><p className="ability-explanation" key={i}>Additional adjustment {signed(a.amount)}; minimum {a.minimum}. {a.before} → {a.after}{a.floorApplied?" (floor applied)":""}. Included in final score.</p>)}</div>;})}</div>
 {!preview && <p className="muted" role="status">Assign all six base scores and choose any species bonuses to see server-calculated final scores.</p>}
 </section>;
}

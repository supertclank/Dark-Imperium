import React from 'react';
import {it,expect} from 'vitest';
import {render,screen} from '@testing-library/react';
import {initialDraft,pathProfile,changePath,Profile,Calculation} from '../src/lib/builder';
import profileData from './fixtures/tier2-profile.json';
import saved from './fixtures/character.json';
import {CalculatedSummary} from '../src/components/CalculatedSummary';
const profile=profileData as Profile;
it('restricts levels to the selected class',()=>{
 const d=initialDraft(profile,'request');expect(pathProfile(profile,d).levels).toEqual([1,2,3]);
 const scum=changePath(profile,{...d,level:3},{classId:'di.class.hive_scum'});
 expect(scum.level).toBe(1);expect(pathProfile(profile,scum).levels).toEqual([1]);
 expect(scum.inventory.some(x=>x.definitionId==='di.weapon.knife')).toBe(true);
 expect(scum.inventory.some(x=>x.definitionId==='di.weapon.lasgun')).toBe(false);
});
it('requires doctrine only at level three and clears it when returning to level two',()=>{
 const d=changePath(profile,initialDraft(profile,'request'),{level:3});
 expect(pathProfile(profile,d).choices.some(c=>c.purpose==='subclass')).toBe(true);
 const lower=changePath(profile,{...d,answers:{...d.answers,'di.choice.veteran.subclass':['marksman']}},{level:2});
 expect(lower.answers).not.toHaveProperty('di.choice.veteran.subclass');
});
it('changes Origin skill choices without retaining stale grants',()=>{
 const d=initialDraft(profile,'request');const next=changePath(profile,d,{originId:'di.background.voidborn'});
 expect(next.answers).not.toHaveProperty('di.choice.hiveborn.skills');expect(pathProfile(profile,next).choices.some(c=>c.id==='di.choice.voidborn.skills')).toBe(true);
});
it('shows unavailable features contacts and procedural training plainly',()=>{
 const c={...saved.calculated,contacts:[{id:'black_market_contact',text:'A trusted black-market contact'}],proceduralProficiencies:['Airlocks'],features:[{...saved.calculated.features[0],name:'Suppressing Fire',classification:'BLOCKED',playerNote:'Unavailable until Suppression is resolved.'}]} as Calculation;
 render(<CalculatedSummary calculated={c}/>);
 expect(screen.getByText('Suppressing Fire · Unavailable')).toBeInTheDocument();expect(screen.getByText('A trusted black-market contact')).toBeInTheDocument();expect(screen.getByText('Airlocks')).toBeInTheDocument();
});
it('does not show an empty contacts section for older projections',()=>{
 render(<CalculatedSummary calculated={saved.calculated as Calculation}/>);expect(screen.queryByRole('heading',{name:'Contacts'})).not.toBeInTheDocument();
});

it('creation levels do not expose advancement-only configurations',()=>{
 const creation={...profile,levels:[1]};const d=initialDraft(creation,'request');
 expect(pathProfile(creation,d).levels).toEqual([1]);
 expect(changePath(creation,d,{level:3}).level).toBe(1);
});
it('sheet shows granted subclass features without leaking future progression prose',()=>{
 const c={...saved.calculated,subclass:{id:'di.subclass.example.ranger',name:'Ranger',description:'Future level-seven benefit'},features:[{...saved.calculated.features[0],id:'di.feature.subclass.example.ranger.level_3',name:'Ranger 3',text:'Current source-backed feature',classification:'MANUAL'}]} as Calculation;
 render(<CalculatedSummary calculated={c}/>);
 expect(screen.queryByText('Future level-seven benefit')).not.toBeInTheDocument();
 expect(screen.getAllByText('Current source-backed feature').length).toBeGreaterThan(0);
});

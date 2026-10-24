import {render,screen,fireEvent,waitFor} from '@testing-library/react';
import {it,expect,vi} from 'vitest';
import {PowerChoices} from '../src/components/PowerChoices';
import {PowersPanel,ClassActions} from '../src/components/PowersPanel';
import {eligiblePower,type PsychicPolicy} from '../src/lib/psychic';
import type {Draft,SavedCharacter,Choice} from '../src/lib/builder';
import data from './fixtures/psychic-policy.json';
import old from './fixtures/roll-character.json';
import {api} from '../src/lib/api';
vi.mock('../src/lib/api',()=>({api:vi.fn()}));
const policy=data as PsychicPolicy;
const draft={...old.selections,classId:'di.class.psyker',answers:{'di.choice.psyker.subclass':['biomancer']}} as Draft;
const choice:Choice={id:'di.choice.psychic.minor_level_1',name:'Minor powers',purpose:'feature',cardinality:{min:2,max:2},options:policy.powers.filter(p=>p.tier==='minor').map(p=>({id:p.id.split('.').at(-1)!,label:p.name}))};
const character={...old,rulesetProfileId:'di-phb-1.0-tier1-v10',level:5,selections:draft,calculated:{...old.calculated,psychic:{ability:'wisdom',abilityModifier:4,attackModifier:7,saveDc:15,powers:policy.powers.filter(p=>p.id==='di.power.warp_spark'),empoweredOptions:policy.empoweredOptions}},runtime:{...old.runtime,currentWarpPressure:3,resources:{empowered_manifestation:{remaining:1,maximum:1,recovery:'short_rest'}}}} as SavedCharacter;
it('shows legal powers with exact count and excludes other-discipline and Warlock-locked powers',()=>{
 render(<PowerChoices choice={choice} draft={draft} policy={policy} disabled={false} onChange={()=>{}}/>);
 expect(screen.getByText('0 of 2 selected')).toBeTruthy();expect(screen.getByLabelText('Flesh Knit')).toBeTruthy();expect(screen.queryByLabelText('Warp Bite')).toBeNull();expect(screen.queryByLabelText('Conceal')).toBeNull();
});
it('forbids duplicate picks across advancement choices',()=>{
 const d={...draft,answers:{...draft.answers,'di.choice.psychic.minor_level_1':['warp_spark','kinetic_push']}};
 render(<PowerChoices choice={{...choice,id:'di.choice.psychic.minor_level_3',cardinality:{min:1,max:1}}} draft={d} policy={policy} disabled={false} onChange={()=>{}}/>);
 expect(screen.getByLabelText('Warp Spark')).toBeDisabled();expect(screen.getAllByText('Already known')).toHaveLength(2);
});
it('requires explicit Warlock Pyromancy permission and never allows Malefic',()=>{
 const pyro=policy.powers.find(p=>p.id==='di.power.ashen_brand')!;const malefic=policy.powers.find(p=>p.id==='di.power.warp_bite')!;
 expect(eligiblePower(pyro,'di.class.aeldari_warlock','',policy)).toBe(false);expect(eligiblePower(pyro,'di.class.aeldari_warlock','',policy,['warlock_pyromancy'])).toBe(true);expect(eligiblePower(malefic,'di.class.aeldari_warlock','',policy,['warlock_pyromancy'])).toBe(false);
});
it('renders backend psychic statistics and submits identities without forged costs or modifiers',async()=>{
 vi.mocked(api).mockResolvedValue(character);const refresh=vi.fn().mockResolvedValue(undefined);
 render(<PowersPanel character={character} disabled={false} onRefresh={refresh}/>);
 expect(screen.getByText('wisdom +4')).toBeTruthy();expect(screen.getByText('+7')).toBeTruthy();
 fireEvent.click(screen.getByRole('button',{name:'Manifest Warp Spark'}));await waitFor(()=>expect(refresh).toHaveBeenCalled());const payload=JSON.parse(vi.mocked(api).mock.calls.at(-1)![1]!.body as string);expect(payload.powerId).toBe('di.power.warp_spark');expect(payload).not.toHaveProperty('warpPressureCost');expect(payload).not.toHaveProperty('attackModifier');
});
it('resumes a saved pending stage without implicitly rolling',()=>{
 const onRoll=vi.fn();render(<ClassActions character={{...character,runtime:{...character.runtime,pendingAction:{id:'cast',name:'Warp Spark',stage:'perils_check'}}}} options={[]} disabled={false} onRoll={onRoll} onRefresh={async()=>{}}/>);
 expect(screen.getByText(/Progress is saved/)).toBeTruthy();expect(onRoll).not.toHaveBeenCalled();expect(screen.queryByText('Complete short rest')).toBeNull();
});

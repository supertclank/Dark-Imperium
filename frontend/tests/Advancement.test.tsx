import React from "react";
import {it,expect,vi,beforeEach} from "vitest";
import {render,screen,fireEvent,waitFor} from "@testing-library/react";
import {AdvancementPanel} from "../src/components/AdvancementPanel";
import {SavedCharacter} from "../src/lib/builder";
import saved from "./fixtures/character.json";
const state=vi.hoisted(()=>({api:vi.fn()}));
vi.mock("../src/lib/api",async importOriginal=>({...await importOriginal<object>(),api:state.api}));
const ready={available:true,nextLevel:2,stateVersion:1,requiredChoices:[],blockers:[]};
const preview={fromLevel:1,toLevel:2,maximumHpBefore:11,maximumHpAfter:18,currentHp:4,proficiencyBonus:2,newFeatures:[{id:"f",name:"Suppressing Fire",classification:"BLOCKED",playerNote:"Unavailable pending PHB-RULE-022"}],profileId:"v2",profileDigest:"digest"};
beforeEach(()=>{vi.clearAllMocks();state.api.mockResolvedValue(ready);});
it("does not offer advancement for an uncertified path",async()=>{state.api.mockResolvedValue({...ready,available:false});render(<AdvancementPanel character={saved as unknown as SavedCharacter} onChanged={vi.fn()}/>);await waitFor(()=>expect(state.api).toHaveBeenCalled());expect(screen.queryByRole("button")).toBeNull();});
it("reviews server HP and preserves request UUID after uncertain confirmation",async()=>{
 const changed=vi.fn();state.api.mockResolvedValueOnce(ready).mockResolvedValueOnce(preview).mockRejectedValueOnce(new Error("Connection lost")).mockResolvedValueOnce({character:saved});
 render(<AdvancementPanel character={saved as unknown as SavedCharacter} onChanged={changed}/>);
 fireEvent.click(await screen.findByRole("button",{name:"Level up to 2"}));fireEvent.click(screen.getByRole("button",{name:"Review advancement"}));
 expect(await screen.findByText(/Current HP remains 4/)).toBeInTheDocument();expect(changed).not.toHaveBeenCalled();
 fireEvent.click(screen.getByRole("button",{name:"Confirm advancement"}));expect(await screen.findByRole("alert")).toHaveTextContent("Connection lost");
 fireEvent.click(screen.getByRole("button",{name:"Confirm advancement"}));await waitFor(()=>expect(changed).toHaveBeenCalledWith(saved));
 expect(state.api.mock.calls[2][1].body).toBe(state.api.mock.calls[3][1].body);
});

it("requires explicit profile-upgrade consent before sending a preview",async()=>{
 state.api.mockResolvedValueOnce({...ready,nextLevel:4,requiresProfileUpgrade:true}).mockResolvedValueOnce({...preview,toLevel:4});
 render(<AdvancementPanel character={saved as unknown as SavedCharacter} onChanged={vi.fn()}/>);
 fireEvent.click(await screen.findByRole("button",{name:"Level up to 4"}));expect(screen.getByRole("button",{name:"Review advancement"})).toBeDisabled();
 fireEvent.click(screen.getByRole("checkbox",{name:/I confirm the validated rules profile upgrade/}));fireEvent.click(screen.getByRole("button",{name:"Review advancement"}));
 await screen.findByRole("button",{name:"Confirm advancement"});expect(JSON.parse(state.api.mock.calls[1][1].body).confirmProfileUpgrade).toBe(true);
});
it("shows explicit upgrade consent at level two without calling it level four",async()=>{
 state.api.mockResolvedValueOnce({...ready,requiresProfileUpgrade:true}).mockResolvedValueOnce(preview);
 render(<AdvancementPanel character={saved as unknown as SavedCharacter} onChanged={vi.fn()}/>);
 fireEvent.click(await screen.findByRole("button",{name:"Level up to 2"}));
 expect(screen.getByText(/This advancement uses a newer validated/)).toBeInTheDocument();
 expect(screen.getByRole("button",{name:"Review advancement"})).toBeDisabled();
 fireEvent.click(screen.getByRole("checkbox",{name:/I confirm the validated/}));fireEvent.click(screen.getByRole("button",{name:"Review advancement"}));
 await screen.findByRole("button",{name:"Confirm advancement"});
 expect(JSON.parse(state.api.mock.calls[1][1].body)).toMatchObject({destinationLevel:2,confirmProfileUpgrade:true});
});

import React from "react";
import { beforeEach, expect, it, vi } from "vitest";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { RollPanel } from "../src/components/RollPanel";
import { DiceResult } from "../src/components/DiceResult";
import { ApiError } from "../src/lib/api";
import { SavedCharacter } from "../src/lib/builder";
import { RollResult } from "../src/lib/rolls";
import character from "./fixtures/roll-character.json";
import options from "./fixtures/roll-options.json";
import attack from "./fixtures/roll-result.json";
import grenade from "./fixtures/grenade-result.json";
const state=vi.hoisted(()=>({api:vi.fn(),refresh:vi.fn()}));
vi.mock("../src/lib/api",async(importOriginal)=>({...await importOriginal<typeof import("../src/lib/api")>(),api:state.api}));
const posts=()=>state.api.mock.calls.filter(c=>c[1]?.method==="POST");
const display=()=>render(<RollPanel character={character as SavedCharacter} onRefresh={state.refresh}/>);
beforeEach(()=>{
 vi.clearAllMocks();localStorage.setItem("dark-imperium.dice-presentation.v1",JSON.stringify({mode:"TEXT_ONLY",sound:false}));state.refresh.mockResolvedValue(undefined);
 state.api.mockImplementation((path:string,init?:RequestInit)=>Promise.resolve(init?.method==="POST"?attack:path.endsWith("/options")?options:{items:[],limit:25,hasMore:false}));
});
it("loads labelled roll controls without implicitly rolling",async()=>{display();expect(await screen.findByRole("button",{name:"Roll Lasgun attack"})).toHaveAttribute("type","button");fireEvent.click(screen.getByText("Ability checks",{exact:true}));expect(screen.getByRole("button",{name:"Roll strength check"})).toBeEnabled();expect(posts()).toHaveLength(0);});
it("waits for authoritative response and disables duplicate clicks",async()=>{
 let finish!:(value:unknown)=>void;
 state.api.mockImplementation((path:string,init?:RequestInit)=>init?.method==="POST"?new Promise(resolve=>{finish=resolve;}):Promise.resolve(path.endsWith("/options")?options:{items:[],limit:25,hasMore:false}));
 display();const button=await screen.findByRole("button",{name:"Roll Lasgun attack"});fireEvent.click(button);expect(button).toBeDisabled();expect(screen.getByRole("status")).toHaveTextContent("Resolving roll");expect(screen.queryByText("Latest result")).not.toBeInTheDocument();
 await act(async()=>finish(attack));expect(await screen.findByText("Latest result")).toBeInTheDocument();expect(screen.getByRole("article",{name:"Lasgun attack result"})).toHaveTextContent(`Total: ${attack.total}`);
});
it("sends only a roll identity and permitted context with current state",async()=>{display();fireEvent.click(await screen.findByRole("button",{name:"Roll Lasgun attack"}));await waitFor(()=>expect(posts()).toHaveLength(1));const body=JSON.parse(posts()[0][1].body);expect(body.rollId).toBe(options.options.find(o=>o.label==="Lasgun attack")!.id);expect(body.expectedStateVersion).toBe(0);for(const key of ["dice","modifier","total","userId","definition"])expect(body).not.toHaveProperty(key);});
it("sends the permitted Finesse ability choice",async()=>{display();const select=await screen.findByLabelText("Combat Blade ability");fireEvent.change(select,{target:{value:"dexterity"}});fireEvent.click(screen.getByRole("button",{name:"Roll Combat Blade attack"}));await waitFor(()=>expect(JSON.parse(posts()[0][1].body).ability).toBe("dexterity"));});
it("requires grenade confirmation and refreshes quantity after committed result",async()=>{
 let used=false;
 state.api.mockImplementation((path:string,init?:RequestInit)=>{
  if(init?.method==="POST"){used=true;return Promise.resolve(grenade);}
  return Promise.resolve(path.endsWith("/options")?{...options,stateVersion:used?1:0,options:options.options.map(o=>o.consumes?{...o,quantity:used?1:2}:o)}:{items:used?[grenade]:[],limit:25,hasMore:false});
 });
 display();fireEvent.click(await screen.findByRole("button",{name:"Use Frag Grenade and roll damage"}));expect(posts()).toHaveLength(0);expect(screen.getByText("Use Frag Grenade? This will consume 1 of 2.")).toBeInTheDocument();fireEvent.click(screen.getByRole("button",{name:"Confirm use of one Frag Grenade"}));await waitFor(()=>expect(state.refresh).toHaveBeenCalled());expect(await screen.findByText(/Quantity: 1/)).toBeInTheDocument();expect(JSON.parse(posts()[0][1].body).confirmConsumption).toBe(true);
});
it("cancel leaves grenade inventory untouched",async()=>{display();fireEvent.click(await screen.findByRole("button",{name:"Use Frag Grenade and roll damage"}));fireEvent.click(screen.getByRole("button",{name:"Cancel grenade use"}));expect(posts()).toHaveLength(0);expect(screen.queryByRole("group",{name:"Confirm grenade use"})).not.toBeInTheDocument();});
it("disables exhausted actions with a readable reason",async()=>{state.api.mockResolvedValue({...options,items:[],options:options.options.map(o=>o.consumes?{...o,available:false,quantity:0,reason:"You have no Frag Grenades remaining."}:o)});display();expect(await screen.findByRole("button",{name:"Use Frag Grenade and roll damage"})).toBeDisabled();expect(screen.getByText("You have no Frag Grenades remaining.")).toBeInTheDocument();});
it("uncertain failures retry the exact request and cannot start another roll",async()=>{
 let count=0;state.api.mockImplementation((path:string,init?:RequestInit)=>init?.method==="POST"?(++count===1?Promise.reject(new ApiError(0,"Connection lost")):Promise.resolve(attack)):Promise.resolve(path.endsWith("/options")?options:{items:[],limit:25,hasMore:false}));
 display();fireEvent.click(await screen.findByRole("button",{name:"Roll Lasgun attack"}));expect(await screen.findByRole("alert")).toHaveTextContent("Connection lost");expect(screen.getByRole("button",{name:"Roll Combat Blade attack"})).toBeDisabled();fireEvent.click(screen.getByRole("button",{name:"Retry same request"}));await waitFor(()=>expect(posts()).toHaveLength(2));expect(posts()[0][1].body).toBe(posts()[1][1].body);
});
it("state conflicts show server feedback and refresh instead of fabricating results",async()=>{state.api.mockImplementation((path:string,init?:RequestInit)=>init?.method==="POST"?Promise.reject(new ApiError(409,"Character state changed. Refresh before rolling.")):Promise.resolve(path.endsWith("/options")?options:{items:[],limit:25,hasMore:false}));display();fireEvent.click(await screen.findByRole("button",{name:"Roll Lasgun attack"}));expect(await screen.findByRole("alert")).toHaveTextContent("Character state changed");await waitFor(()=>expect(state.refresh).toHaveBeenCalled());expect(screen.queryByText("Latest result")).not.toBeInTheDocument();});
it("history uses stored totals and survives a fresh mount without rolling",async()=>{state.api.mockImplementation((path:string)=>Promise.resolve(path.endsWith("/options")?options:{items:[attack],limit:25,hasMore:true}));display();expect(await screen.findByText(new RegExp(`Lasgun attack · ${attack.total}`))).toBeInTheDocument();expect(screen.getByText(/Older results remain stored/)).toBeInTheDocument();expect(posts()).toHaveLength(0);});
it("links damage to its attack while leaving hit adjudication explicit",async()=>{display();fireEvent.click(await screen.findByRole("button",{name:"Roll Lasgun attack"}));fireEvent.click(await screen.findByRole("button",{name:"Roll linked damage after manually confirming hit"}));await waitFor(()=>expect(posts()).toHaveLength(2));expect(JSON.parse(posts()[1][1].body).parentResultId).toBe(attack.id);});
it("native button handles keyboard-generated activation and supplies live result text",async()=>{display();const button=await screen.findByRole("button",{name:"Roll Initiative"});button.focus();expect(button).toHaveFocus();fireEvent.click(button,{detail:0});await waitFor(()=>expect(posts()).toHaveLength(1));expect(await screen.findByText("Latest result")).toBeInTheDocument();});
it("text presenter exposes individual kept discarded dice and grenade outcomes",()=>{render(<DiceResult result={{...grenade,dice:{...grenade.dice,groups:[{sides:6,dice:[4,3,5],kept:[4,5],discarded:[3],keptIndices:[0,2],discardedIndices:[1],keep:"HIGHEST"}]}} as RollResult} mode="3D"/>);expect(screen.getByText(/Discarded: 3/)).toBeInTheDocument();expect(screen.getByText(/Target-by-target application/)).toBeInTheDocument();expect(screen.getByText(/Successful save:/)).toBeInTheDocument();});
it("replays persisted grenade presentation after a fresh mount without any backend mutation",async()=>{
 const request={requestId:grenade.requestId,rollId:options.options.find(o=>o.consumes)!.id,profileId:options.profileId,profileDigest:options.profileDigest,expectedStateVersion:0,confirmConsumption:true};
 const recorded={...grenade,request};
 state.api.mockImplementation((path:string,init?:RequestInit)=>Promise.resolve(init?.method==="POST"?recorded:path.endsWith("/options")?{...options,stateVersion:1}:{items:[recorded],limit:25,hasMore:false}));
 display();fireEvent.click(await screen.findByRole("button",{name:"Replay Dice"}));
 expect(posts()).toHaveLength(0);expect(await screen.findByText("REPLAY ANIMATION · STORED RESULT")).toBeInTheDocument();
});

it("Roll Again submits a fresh UUID and replay animation does not submit",async()=>{display();fireEvent.click(await screen.findByRole("button",{name:"Roll Lasgun attack"}));fireEvent.click(await screen.findByRole("button",{name:"Replay animation"}));expect(posts()).toHaveLength(1);fireEvent.click(screen.getByRole("button",{name:"Roll Again"}));await waitFor(()=>expect(posts()).toHaveLength(2));expect(JSON.parse(posts()[0][1].body).requestId).not.toBe(JSON.parse(posts()[1][1].body).requestId);});
it("grenade success offers replay but never casual Roll Again",async()=>{state.api.mockImplementation((path:string,init?:RequestInit)=>Promise.resolve(init?.method==="POST"?grenade:path.endsWith("/options")?options:{items:[],limit:25,hasMore:false}));display();fireEvent.click(await screen.findByRole("button",{name:"Use Frag Grenade and roll damage"}));fireEvent.click(screen.getByRole("button",{name:"Confirm use of one Frag Grenade"}));fireEvent.click(await screen.findByRole("button",{name:"Replay animation"}));expect(posts()).toHaveLength(1);expect(screen.queryByRole("button",{name:"Roll Again"})).not.toBeInTheDocument();});
it("uses the actual consumable name for Frag Bomb confirmation",async()=>{
 state.api.mockImplementation((path:string)=>Promise.resolve(path.endsWith("/options")?{...options,options:options.options.filter(o=>o.consumes).map(o=>({...o,label:"Frag Bomb damage",itemId:"di.weapon.frag_bomb",quantity:1}))}:{items:[],limit:25,hasMore:false}));
 display();fireEvent.click(await screen.findByRole("button",{name:"Use Frag Bomb and roll damage"}));
 expect(screen.getByText("Use Frag Bomb? This will consume 1 of 1.")).toBeInTheDocument();expect(screen.getByRole("button",{name:"Confirm use of one Frag Bomb"})).toBeInTheDocument();expect(posts()).toHaveLength(0);
});
it("displays exact fractional damage without claiming integer rounding",()=>{
 render(<DiceResult result={{...grenade,grenade:{...grenade.grenade!,outcomes:{failure:5,success:"5/2"}}} as RollResult} mode="TEXT_ONLY"/>);
 expect(screen.getByText(/Successful save: 5\/2/)).toBeInTheDocument();expect(screen.queryByText(/rounded down/)).not.toBeInTheDocument();
});

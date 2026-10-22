import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, within } from "@testing-library/react";
import { CharacterForm } from "../src/components/CharacterForm";
import profile from "./fixtures/profile.json";
import saved from "./fixtures/character.json";
const { push, api } = vi.hoisted(() => ({ push: vi.fn(), api: vi.fn() }));
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("../src/lib/api", () => ({ api }));
vi.mock("../src/components/Resource", () => ({useResource: () => ({data:profile,error:"",retry:vi.fn()}),ResourceState: () => null}));
const valid={status:"VALID",errors:[],calculated:saved.calculated};
async function next(title:string){fireEvent.click(screen.getByRole("button",{name:"Continue"}));await screen.findByRole("heading",{name:title});}
async function ability(){fireEvent.change(screen.getByLabelText("Character name"),{target:{value:"Cassian"}});await next("2. Species");await next("3. Origin");await next("4. Ability Scores");}
async function review(){
 await ability();
 for(const choice of profile.choices.filter(c=>c.purpose==="attribute")) fireEvent.change(document.getElementById(choice.id)!,{target:{value:saved.selections.answers[choice.id as keyof typeof saved.selections.answers][0]}});
 await next("5. Class");await next("6. Universal Trait");await next("7. Proficiencies & Skills");
 for(const choice of profile.choices.filter(c=>c.purpose!=="attribute")){
  const answers=saved.selections.answers[choice.id as keyof typeof saved.selections.answers];
  if(choice.cardinality.max===1)fireEvent.change(document.getElementById(choice.id)!,{target:{value:answers[0]}});
  else {const group=screen.getByRole("group",{name:choice.name});for(const id of answers){const label=choice.options.find(o=>o.id===id)!.label;fireEvent.click(within(group).getByRole("checkbox",{name:label}));}}
 }
 await next("8. Equipment");await next("9. Review");
}
describe("production character builder",()=>{
 beforeEach(()=>{vi.clearAllMocks();api.mockImplementation((path:string)=>Promise.resolve(path==="/characters"?saved:valid));});
 it("loads supported profile and keeps unsupported content out of selectors",async()=>{render(<CharacterForm/>);await ability();expect(screen.queryByRole("radio",{name:/Ratling/})).not.toBeInTheDocument();expect(screen.getByText("Supported creation path")).toBeInTheDocument();expect(screen.getByLabelText("strength")).toHaveValue("15");});
 it("shows required-field errors without advancing",async()=>{api.mockResolvedValue({status:"INVALID",errors:[{field:"name",code:"INVALID_NAME",message:"Enter a name."}]});render(<CharacterForm/>);fireEvent.click(screen.getByRole("button",{name:"Continue"}));expect(await screen.findByRole("alert")).toHaveTextContent("Enter a name.");expect(screen.getByRole("heading",{name:"1. Identity"})).toBeInTheDocument();});
 it("submits score assignments for server validation and displays allocation errors",async()=>{render(<CharacterForm/>);await ability();fireEvent.change(screen.getByLabelText("strength"),{target:{value:"14"}});api.mockResolvedValue({status:"INVALID",errors:[{field:"attributes",code:"INVALID_ABILITY_ALLOCATION",message:"Assign each score once."}]});fireEvent.click(screen.getByRole("button",{name:"Continue"}));expect(await screen.findByRole("alert")).toHaveTextContent("Assign each score once.");expect(JSON.parse(api.mock.calls.at(-1)![1].body).attributes.strength).toBe(14);});
 it("preserves identity when navigating backwards",async()=>{render(<CharacterForm/>);await ability();for(let i=0;i<3;i++)fireEvent.click(screen.getByRole("button",{name:"Back"}));expect(screen.getByLabelText("Character name")).toHaveValue("Cassian");});
 it("reviews server calculations and saves canonical selections then redirects",async()=>{render(<CharacterForm/>);await review();expect(screen.getByRole("heading",{name:"Core statistics"})).toBeInTheDocument();expect(screen.getByText("3d6")).toBeInTheDocument();expect(screen.getByText(/rounding floor/)).toBeInTheDocument();fireEvent.click(screen.getByRole("button",{name:"Create character"}));await waitFor(()=>expect(push).toHaveBeenCalledWith(`/characters/${saved.id}`));const call=api.mock.calls.find(c=>c[0]==="/characters")!;const draft=JSON.parse(call[1].body);expect(draft.answers).toEqual(saved.selections.answers);expect(draft.inventory.find((i:{definitionId:string})=>i.definitionId==="di.weapon.frag_grenade").quantity).toBe(2);expect(draft).not.toHaveProperty("ownerId");expect(draft).not.toHaveProperty("calculated");});
 it("keeps the reviewed draft and displays structured save errors",async()=>{render(<CharacterForm/>);await review();api.mockRejectedValue(Object.assign(new Error("Draft rejected"),{issues:[{field:"profileDigest",code:"STALE_PROFILE",message:"Reload the builder."}]}));fireEvent.click(screen.getByRole("button",{name:"Create character"}));expect(await screen.findByRole("alert")).toHaveTextContent("Reload the builder.");expect(screen.getByRole("heading",{name:"Cassian"})).toBeInTheDocument();expect(push).not.toHaveBeenCalled();});
});

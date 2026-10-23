import React from "react";
import { it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Characters from "../src/app/(archive)/characters/page";
import { CharacterSheet } from "../src/components/CharacterSheet";
import saved from "./fixtures/character.json";
const state=vi.hoisted(()=>({data:null as unknown,push:vi.fn(),api:vi.fn()}));
vi.mock("../src/components/AdvancementPanel",()=>({AdvancementPanel:()=>null}));
vi.mock("../src/components/RollPanel",()=>({RollPanel:()=>null}));
vi.mock("next/navigation",()=>({useRouter:()=>({push:state.push})}));
vi.mock("../src/lib/api",()=>({api:state.api}));
vi.mock("../src/components/Resource",()=>({useResource:()=>({data:state.data,error:"",retry:vi.fn()}),ResourceState:()=>null}));
beforeEach(()=>{vi.clearAllMocks();state.data=null;state.api.mockResolvedValue(undefined);});
it("lists an empty-state creation link",()=>{state.data=[];render(<Characters/>);expect(screen.getByRole("link",{name:/Create a character/})).toHaveAttribute("href","/characters/new");});
it("lists owned character summary and a reopen link",()=>{state.data=[saved];render(<Characters/>);expect(screen.getByRole("link",{name:new RegExp(saved.name)})).toHaveAttribute("href",`/characters/${saved.id}`);expect(screen.getByText(/Schola Progenium/)).toBeInTheDocument();});
it("displays persisted statistics without implicitly executing actions",()=>{state.data=saved;render(<CharacterSheet id={saved.id}/>);expect(screen.getByText("11 / 11")).toBeInTheDocument();expect(screen.getByText("Frag Grenade × 2")).toBeInTheDocument();expect(screen.getByText(/Tactical Aim · Manual/)).toBeInTheDocument();expect(screen.queryByRole("button",{name:/roll/i})).not.toBeInTheDocument();expect(state.api).not.toHaveBeenCalled();});
it("requires confirmation before deleting and navigates to list",async()=>{state.data=saved;render(<CharacterSheet id={saved.id}/>);fireEvent.click(screen.getByRole("button",{name:"Delete character"}));expect(state.api).not.toHaveBeenCalled();fireEvent.click(screen.getByRole("button",{name:"Delete permanently"}));await waitFor(()=>expect(state.push).toHaveBeenCalledWith("/characters"));expect(state.api).toHaveBeenCalledWith(`/characters/${saved.id}`,{method:"DELETE"});});

it("keeps panel identities distinct when consumed inventory version equals level",()=>{
 const errors=vi.spyOn(console,"error").mockImplementation(()=>{});
 try { state.data={...saved,runtime:{...saved.runtime,stateVersion:saved.level}};render(<CharacterSheet id={saved.id}/>);expect(errors.mock.calls.flat().join(" ")).not.toMatch(/same key|unique.*key/i);expect(screen.getByText("11 / 11")).toBeInTheDocument();expect(state.api).not.toHaveBeenCalled(); }
 finally { errors.mockRestore(); }
});

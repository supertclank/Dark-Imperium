import React from "react";
import { it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { SheetNotes } from "../src/components/SheetNotes";
import { SheetInspector } from "../src/components/SheetInspector";
import { api } from "../src/lib/api";
vi.mock("../src/lib/api", () => ({ api: vi.fn() }));
beforeEach(() => vi.resetAllMocks());
it("keeps unsaved notes across tabs and saves against the loaded revision", async () => {
  vi.mocked(api)
    .mockResolvedValueOnce({ text: "Old note", version: 2 })
    .mockResolvedValueOnce({ text: "Updated note", version: 3 });
  const view = render(<SheetNotes characterId="owned" active />);
  await waitFor(() =>
    expect(screen.getByLabelText("Session notes")).toHaveValue("Old note"),
  );
  fireEvent.change(screen.getByLabelText("Session notes"), {
    target: { value: "Updated note" },
  });
  view.rerender(<SheetNotes characterId="owned" active={false} />);
  view.rerender(<SheetNotes characterId="owned" active />);
  expect(screen.getByLabelText("Session notes")).toHaveValue("Updated note");
  fireEvent.click(screen.getByRole("button", { name: "Save notes" }));
  await screen.findByText("Notes saved.");
  expect(api).toHaveBeenLastCalledWith("/characters/owned/notes", {
    method: "PUT",
    body: JSON.stringify({ text: "Updated note", expectedVersion: 2 }),
  });
});
it("preserves the draft on a revision conflict", async () => {
  vi.mocked(api)
    .mockResolvedValueOnce({ text: "", version: 0 })
    .mockRejectedValueOnce(new Error("Notes changed elsewhere."));
  render(<SheetNotes characterId="owned" active />);
  await waitFor(() =>
    expect(screen.getByLabelText("Session notes")).toBeEnabled(),
  );
  fireEvent.change(screen.getByLabelText("Session notes"), {
    target: { value: "Keep this draft" },
  });
  fireEvent.click(screen.getByRole("button", { name: "Save notes" }));
  await screen.findByRole("alert");
  expect(screen.getByLabelText("Session notes")).toHaveValue("Keep this draft");
});
it("loads pinned details and closes with Escape without presenting an ability selector", async () => {
  vi.mocked(api).mockResolvedValue({
    id: "di.weapon.knife",
    name: "Knife",
    kind: "weapon",
    description: "Canonical knife rules",
    fields: [{ label: "Attack ability", value: "Dexterity" }],
    status: "Baseline rolls available",
  });
  const close = vi.fn();
  render(
    <SheetInspector
      characterId="owned"
      target={{ id: "di.weapon.knife", name: "Knife" }}
      options={[]}
      disabled={false}
      onRoll={vi.fn()}
      onClose={close}
    />,
  );
  await screen.findByText("Canonical knife rules");
  expect(api).toHaveBeenCalledWith("/characters/owned/details/di.weapon.knife");
  expect(screen.getByText("Dexterity")).toBeVisible();
  expect(screen.queryByRole("combobox")).toBeNull();
  fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
  expect(close).toHaveBeenCalledOnce();
});
it('mobile inspector locks background scrolling and restores opening focus',async()=>{
 vi.stubGlobal('matchMedia',()=>({matches:true,addEventListener:vi.fn(),removeEventListener:vi.fn()}));
 const opener=document.createElement('button');document.body.append(opener);opener.focus();
 const view=render(<SheetInspector characterId="owned" target={{id:'local',name:'Resource',local:{id:'local',name:'Resource',kind:'resource',description:'Manual tracking',fields:[],status:'Manual'}}} options={[]} disabled={false} onRoll={vi.fn()} onClose={vi.fn()}/>);
 expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal','true');
 expect(document.body.style.overflow).toBe('hidden');
 view.unmount();expect(document.body.style.overflow).toBe('');expect(document.activeElement).toBe(opener);opener.remove();vi.unstubAllGlobals();
});

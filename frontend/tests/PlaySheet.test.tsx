import React from "react";
import { it, expect, vi } from "vitest";
import { render, screen, fireEvent, within } from "@testing-library/react";
import { PlaySheet } from "../src/components/PlaySheet";
import type { SavedCharacter } from "../src/lib/builder";
import type { RollOption } from "../src/lib/rolls";
import character from "./fixtures/roll-character.json";
import options from "./fixtures/roll-options.json";
const setup = () => {
  const onRoll = vi.fn();
  render(
    <PlaySheet
      character={character as SavedCharacter}
      options={options.options as RollOption[]}
      disabled={false}
      onRoll={onRoll}
      abilities={{}}
      onAbility={() => {}}
    />,
  );
  return onRoll;
};
it("exposes compact server-calculated header and six ability controls without rolling on mount", () => {
  const onRoll = setup();
  expect(
    screen.getByRole("heading", { name: character.name }),
  ).toBeInTheDocument();
  expect(screen.getByText("HP")).toBeInTheDocument();
  expect(
    within(screen.getByRole("region", { name: "Ability scores" })).getAllByRole(
      "button",
    ),
  ).toHaveLength(6);
  expect(onRoll).not.toHaveBeenCalled();
});
it("directly dispatches checks saves skills initiative attack and damage from the sheet", () => {
  const onRoll = setup();
  for (const label of [
    "strength check",
    "strength save",
    "Acrobatics",
    "Initiative",
    "Lasgun attack",
    "Lasgun damage",
  ]) {
    fireEvent.click(screen.getByRole("button", { name: `Roll ${label}` }));
    expect(onRoll.mock.lastCall?.[0].label).toBe(label);
  }
  expect(onRoll).toHaveBeenCalledTimes(6);
});
it("keeps inventory and traits behind accessible keyboard tabs with manual flags", () => {
  setup();
  const actions = screen.getByRole("tab", { name: "Actions" });
  expect(actions).toHaveAttribute("aria-selected", "true");
  fireEvent.keyDown(actions, { key: "ArrowRight" });
  expect(screen.getByRole("tab", { name: "Inventory" })).toHaveFocus();
  expect(
    screen.getByRole("heading", { name: "Inventory" }),
  ).toBeInTheDocument();
  expect(screen.getByText("Frag Grenade")).toBeInTheDocument();
  fireEvent.keyDown(screen.getByRole("tab", { name: "Inventory" }), {
    key: "End",
  });
  expect(
    screen.getByRole("tab", { name: "Features & Traits" }),
  ).toHaveAttribute("aria-selected", "true");
  expect(screen.getAllByText("Manual").length).toBeGreaterThan(0);
});
it("shows proficient and non-proficient markers beside server modifiers", () => {
  setup();
  expect(screen.getAllByLabelText("Proficient").length).toBeGreaterThan(0);
  expect(screen.getAllByLabelText("Not proficient").length).toBeGreaterThan(0);
});

it("displays server-supplied Finesse alternatives without recalculating modifiers", () => {
  const choices = options.options.map((o) => ({
    ...o,
    modifierChoices: { strength: 2, dexterity: 7 },
  }));
  render(
    <PlaySheet
      character={character as SavedCharacter}
      options={choices as RollOption[]}
      disabled={false}
      onRoll={() => {}}
      abilities={{ "di.weapon.combat_blade": "dexterity" }}
      onAbility={() => {}}
    />,
  );
  expect(
    screen.getByRole("button", { name: "Roll Combat Blade attack" }),
  ).toHaveTextContent("+7");
  expect(
    screen.getByRole("button", { name: "Roll Combat Blade damage" }),
  ).toHaveTextContent("1d6 +7");
});

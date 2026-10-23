import { render, screen, fireEvent, act } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import { AttackSequence } from "../src/components/AttackSequence";
import type { RollOption, RollResult } from "../src/lib/rolls";
const weapon = (name: string, modifier: number): RollOption => ({
  id: name,
  actionId: name,
  itemId: name,
  label: name + " attack",
  category: "attack",
  available: true,
  reason: null,
  consumes: false,
  quantity: 1,
  abilities: [],
  groups: [{ count: 1, sides: 20 }],
  modifier,
});
const knife = weapon("Knife", 6),
  club = weapon("Club", 5),
  ranged = weapon("Laspistol", 6);
const damage = {
  ...knife,
  id: "knife-damage",
  label: "Knife damage",
  category: "damage",
};
const grenade = { ...weapon("Grenade", 0), consumes: true };
const result = (id: string, actionId = "Knife") =>
  ({
    id,
    requestId: id,
    actionId,
    label: actionId + " attack",
    total: 17,
  }) as RollResult;
it("advances only after a saved independent result and permits a different second weapon", () => {
  const callbacks: ((r: RollResult) => void)[] = [];
  const attack = vi.fn((_o, done) => callbacks.push(done));
  const onDamage = vi.fn();
  render(
    <AttackSequence
      count={2}
      actionIds={["Knife", "Club", "Laspistol", "Grenade"]}
      options={[knife, club, ranged, damage, grenade]}
      disabled={false}
      onAttack={attack}
      onDamage={onDamage}
    />,
  );
  fireEvent.click(screen.getByText("Start Attack action"));
  expect(screen.queryByRole("option", { name: "Grenade attack" })).toBeNull();
  fireEvent.click(screen.getByText("Roll attack 1 of 2"));
  expect(screen.getByText("Attack 1 of 2")).toBeTruthy(); // failed or unfinished roll cannot advance
  act(() => callbacks[0](result("first")));
  expect(screen.getByText("Attack 2 of 2")).toBeTruthy();
});
it("retains separate damage parents and ignores duplicate completion", async () => {
  const { act } = await import("@testing-library/react");
  let done: (r: RollResult) => void = () => {};
  const onAttack = vi.fn((_o, callback) => {
    done = callback;
  });
  const onDamage = vi.fn();
  render(
    <AttackSequence
      count={2}
      actionIds={["Knife", "Club"]}
      options={[knife, club, damage]}
      disabled={false}
      onAttack={onAttack}
      onDamage={onDamage}
    />,
  );
  fireEvent.click(screen.getByText("Start Attack action"));
  fireEvent.click(screen.getByText("Roll attack 1 of 2"));
  act(() => {
    done(result("first"));
    done(result("first"));
  });
  expect(screen.getByText("Attack 2 of 2")).toBeTruthy();
  fireEvent.change(screen.getByRole("combobox"), { target: { value: "Club" } });
  fireEvent.click(screen.getByText("Roll attack 2 of 2"));
  expect(onAttack.mock.calls[1][0]).toEqual(club);
  act(() => done(result("second", "Club")));
  expect(screen.getByText("2 attacks complete")).toBeTruthy();
  expect(screen.queryByText("Roll attack 3 of 2")).toBeNull();
  fireEvent.click(
    screen.getByText("Roll damage for attack 1 after confirming hit"),
  );
  expect(onDamage).toHaveBeenCalledWith(damage, result("first"));
});
it("does not offer Extra Attack below capacity two or when the coordinator is busy", () => {
  const p = {
    count: 1,
    actionIds: ["Knife"],
    options: [knife],
    disabled: false,
    onAttack: vi.fn(),
    onDamage: vi.fn(),
  };
  const view = render(<AttackSequence {...p} />);
  expect(screen.queryByText("Start Attack action")).toBeNull();
  view.rerender(<AttackSequence {...p} count={2} disabled />);
  expect(screen.getByText("Start Attack action")).toBeDisabled();
});

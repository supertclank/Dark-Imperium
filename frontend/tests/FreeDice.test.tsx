import React from "react";
import { it, expect, vi, beforeEach } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import { FreeDice } from "../src/components/FreeDice";
import { physicalSession } from "./physical-fixture";
import fixture from "./fixtures/roll-result.json";
const mock = vi.hoisted(() => ({
  api: vi.fn(),
  settle: () => {},
  show: vi.fn(),
}));
vi.mock("../src/lib/api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../src/lib/api")>()),
  api: mock.api,
}));
vi.mock("../src/components/Session", () => ({
  useSession: () => ({ user: { id: "tester" } }),
}));
vi.mock("../src/lib/dice-renderer", () => ({
  startPhysicalRoll: (
    _s: unknown,
    _h: unknown,
    _a: unknown,
    done: (v: number[][]) => void,
  ) => {
    mock.show();
    mock.settle = () => done([[13]]);
    return Promise.resolve({ skip: mock.settle, dispose: () => {} });
  },
}));
const result = {
  ...fixture,
  id: "free-1",
  rollType: "FREE_ROLL",
  label: "2d20",
  characterName: "Free dice",
  dice: { ...fixture.dice, modifier: 0 },
  naturalResult: null,
  physical: {
    source: "PHYSICS",
    presentationSeed: physicalSession.presentationSeed,
    physicsVersion: physicalSession.physicsVersion,
    geometryVersion: physicalSession.geometryVersion,
    rawPhysicalValues: [[13]],
  },
};
beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
  mock.api.mockImplementation((_path: string, init?: RequestInit) =>
    Promise.resolve(
      init?.method === "POST"
        ? _path.endsWith("/finalize")
          ? result
          : physicalSession
        : { items: [], limit: 25, hasMore: false },
    ),
  );
});
it("builds pool with add remove and clear and sends no modifier", async () => {
  render(<FreeDice />);
  fireEvent.click(screen.getByRole("button", { name: "Dice" }));
  fireEvent.click(screen.getByRole("button", { name: "d20" }));
  fireEvent.click(screen.getByRole("button", { name: "Add d20" }));
  fireEvent.click(screen.getByRole("button", { name: "d100" }));
  expect(screen.getByLabelText("Dice pool")).toHaveTextContent("2d20 + 1d100");
  fireEvent.click(screen.getByRole("button", { name: "Remove d100" }));
  fireEvent.click(screen.getByRole("button", { name: "Roll pool" }));
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  const post = mock.api.mock.calls.find((c) => c[1]?.method === "POST")!;
  expect(JSON.parse(post[1].body).pool).toEqual([{ sides: 20, count: 2 }]);
  expect(JSON.parse(post[1].body)).not.toHaveProperty("modifier");
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.queryByText("Free roll history")).not.toBeInTheDocument();
  await act(async () => mock.settle());
  expect(screen.getByText("Free roll history")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Clear Dice" }));
  expect(screen.getByLabelText("Dice pool")).toHaveTextContent("Choose dice");
});
it("replay masks history without POST and Roll Again uses a new UUID", async () => {
  render(<FreeDice />);
  fireEvent.click(screen.getByRole("button", { name: "Dice" }));
  fireEvent.click(screen.getByRole("button", { name: "d20" }));
  fireEvent.click(screen.getByRole("button", { name: "Roll pool" }));
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  await act(async () => mock.settle());
  fireEvent.click(screen.getByRole("button", { name: "Replay Dice" }));
  await waitFor(() => expect(mock.show).toHaveBeenCalledTimes(2));
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(
    mock.api.mock.calls.filter((c) => c[1]?.method === "POST"),
  ).toHaveLength(2);
  await act(async () => mock.settle());
  fireEvent.click(screen.getByRole("button", { name: "Roll Again" }));
  await waitFor(() => expect(mock.show).toHaveBeenCalledTimes(3));
  const posts = mock.api.mock.calls.filter(
    (c) => c[0] === "/roll-sessions/free",
  );
  expect(JSON.parse(posts[0][1].body).requestId).not.toBe(
    JSON.parse(posts[1][1].body).requestId,
  );
});

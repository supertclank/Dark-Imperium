import React from "react";
import { beforeEach, it, expect, vi } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import { RollPanel } from "../src/components/RollPanel";
import type { SavedCharacter } from "../src/lib/builder";
import { physicalSession } from "./physical-fixture";
import character from "./fixtures/roll-character.json";
import options from "./fixtures/roll-options.json";
import attack from "./fixtures/roll-result.json";
const mock = vi.hoisted(() => ({
  api: vi.fn(),
  show: vi.fn(),
  settle: () => {},
  settling: () => {},
}));
vi.mock("../src/lib/api", async (original) => ({
  ...(await original<typeof import("../src/lib/api")>()),
  api: mock.api,
}));
vi.mock("../src/lib/dice-renderer", () => ({
  startPhysicalRoll: (
    _s: unknown,
    _h: unknown,
    _a: unknown,
    done: (v: number[][]) => void,
    _f: unknown,
    cocked: () => void,
  ) => {
    mock.show();
    mock.settle = () => done([[13]]);
    mock.settling = cocked;
    return Promise.resolve({ skip: mock.settle, dispose: () => {} });
  },
}));
beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
});
it("does not persist or reveal a character result until physical faces are accepted", async () => {
  let saved = false;
  mock.api.mockImplementation((path: string, init?: RequestInit) => {
    if (init?.method === "POST") {
      if (path.endsWith("/finalize")) {
        saved = true;
        return Promise.resolve({
          ...attack,
          physical: {
            source: "PHYSICS",
            presentationSeed: physicalSession.presentationSeed,
            physicsVersion: physicalSession.physicsVersion,
            geometryVersion: physicalSession.geometryVersion,
            rawPhysicalValues: [[13]],
          },
        });
      }
      return Promise.resolve(physicalSession);
    }
    return Promise.resolve(
      path.endsWith("/options")
        ? options
        : { items: saved ? [attack] : [], limit: 25, hasMore: false },
    );
  });
  render(
    <RollPanel
      character={character as SavedCharacter}
      onRefresh={async () => {}}
    />,
  );
  fireEvent.click(
    await screen.findByRole("button", { name: "Roll Lasgun attack" }),
  );
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  expect(saved).toBe(false);
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.queryByText("Latest result")).not.toBeInTheDocument();
  expect(
    screen.getByText("History hidden until dice settle."),
  ).toBeInTheDocument();
  act(() => mock.settling());
  expect(screen.queryByText(/Lasgun attack ·/)).not.toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: /linked damage/ }),
  ).not.toBeInTheDocument();
  await act(async () => mock.settle());
  expect(saved).toBe(true);
  expect(screen.getByText("Latest result")).toBeInTheDocument();
  expect(
    screen.getByRole("button", { name: /linked damage/ }),
  ).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Replay animation" }));
  await waitFor(() => expect(mock.show).toHaveBeenCalledTimes(2));
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.queryByText("Latest result")).not.toBeInTheDocument();
  expect(
    mock.api.mock.calls.filter((c) => c[1]?.method === "POST"),
  ).toHaveLength(2);
});

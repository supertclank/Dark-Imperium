import { beforeEach, expect, it, vi } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import React from "react";
import {
  presentRoll,
  readPreferences,
  effectiveMode,
  preferenceKey,
} from "../src/lib/dice-presentation";
import {
  dieGeometry,
  dieFaceMap,
  settledOrientation,
} from "../src/lib/dice-geometry";
import { DicePresentation } from "../src/components/DicePresentation";
import type { RollResult } from "../src/lib/rolls";
import grenade from "./fixtures/grenade-result.json";
import attack from "./fixtures/roll-result.json";
const mock = vi.hoisted(() => ({
  show: vi.fn(),
  skip: vi.fn(),
  dispose: vi.fn(),
  create: vi.fn(),
  failure: () => {},
  settle: () => {},
  settling: () => {},
}));
vi.mock("../src/lib/dice-renderer", () => ({
  createDiceRenderer: (...args: unknown[]) => mock.create(...args),
}));
beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
  mock.create.mockImplementation((_host, failed, settle, settling) => {
    mock.failure = failed;
    mock.settle = settle;
    mock.settling = settling;
    mock.skip.mockImplementation(settle);
    return mock;
  });
  Object.defineProperty(window, "matchMedia", {
    configurable: true,
    value: vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    })),
  });
});
const event = (result = grenade, serial = 1) => ({
  result: result as RollResult,
  serial,
  replay: false,
});
it("copies every die and metadata without recomputing authoritative totals", () => {
  const result = { ...grenade, total: 999 };
  const p = presentRoll(result as RollResult);
  expect(p.total).toBe(999);
  expect(p.dice.map((d) => d.value)).toEqual(grenade.dice.groups[0].dice);
  expect(p.dice).toHaveLength(3);
  expect(new Set(p.dice.map((d) => d.id)).size).toBe(3);
  expect(p.damageType).toBe(grenade.damageType.name);
});
it("preserves discarded identity with equal values and authoritative critical metadata", () => {
  const r = {
    ...attack,
    naturalResult: 20,
    criticalCandidate: false,
    dice: {
      ...attack.dice,
      groups: [
        {
          sides: 20,
          dice: [20, 20],
          kept: [20],
          discarded: [20],
          keptIndices: [1],
          discardedIndices: [0],
          keep: "HIGHEST",
        },
      ],
    },
  };
  const p = presentRoll(r as RollResult);
  expect(p.dice.map((d) => d.discarded)).toEqual([true, false]);
  expect(p.natural).toBe(20);
  expect(p.criticalCandidate).toBe(false);
});
it("retains d100 values without needing a mechanics conversion", () => {
  const r = structuredClone(grenade);
  r.dice.groups[0].sides = 100;
  r.dice.groups[0].dice = [100];
  expect(presentRoll(r as RollResult).dice[0].value).toBe(100);
});
it.each([4, 6, 8, 10, 12, 20])(
  "d%i has numbered faces and every target settles physically upward",
  (sides) => {
    const g = dieGeometry(sides),
      faces = dieFaceMap(g);
    expect(faces).toHaveLength(sides);
    for (let value = 1; value <= sides; value++) {
      const normal = faces[value - 1].normal
        .clone()
        .applyQuaternion(settledOrientation(g, value));
      expect(normal.y).toBeCloseTo(1, 7);
    }
    g.dispose();
  },
);
it("validates corrupt preferences and respects system motion priority", () => {
  expect(readPreferences("{")).toEqual({ mode: "3D", sound: false });
  expect(readPreferences('{"mode":"bad","sound":"yes"}').sound).toBe(false);
  expect(effectiveMode("3D", true)).toBe("REDUCED_MOTION");
  expect(effectiveMode("TEXT_ONLY", true)).toBe("TEXT_ONLY");
});

it("holds all text until the all-dice callback, including settling", async () => {
  const reveal = vi.fn();
  render(<DicePresentation event={event()} onReveal={reveal} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  act(() => mock.settling());
  expect(screen.getByText("Settling…")).toBeInTheDocument();
  expect(reveal).not.toHaveBeenCalled();
  expect(screen.queryByText(/Successful save:/)).not.toBeInTheDocument();
  act(() => mock.settle());
  expect(screen.getByRole("article")).toHaveTextContent(
    `Total: ${grenade.total}`,
  );
  expect(reveal).toHaveBeenCalledTimes(1);
});
it("text-only reveals immediately without initializing physics", async () => {
  localStorage.setItem(preferenceKey, JSON.stringify({ mode: "TEXT_ONLY" }));
  const reveal = vi.fn();
  render(<DicePresentation event={event()} onReveal={reveal} />);
  expect(await screen.findByRole("article")).toHaveTextContent(
    `Total: ${grenade.total}`,
  );
  expect(reveal).toHaveBeenCalledTimes(1);
  expect(mock.create).not.toHaveBeenCalled();
});
it("reduced motion places static dice before revealing", async () => {
  localStorage.setItem(
    preferenceKey,
    JSON.stringify({ mode: "REDUCED_MOTION" }),
  );
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  expect(mock.show.mock.calls[0][1]).toBe(true);
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  act(() => mock.settle());
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(await screen.findByRole("article")).toBeInTheDocument();
});
it("skip requests final placement and only its completion reveals", async () => {
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  mock.skip.mockImplementation(() => {});
  fireEvent.click(screen.getByRole("button", { name: "Skip animation" }));
  expect(mock.skip).toHaveBeenCalled();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  act(() => mock.settle());
  expect(screen.getByRole("article")).toBeInTheDocument();
});
it("replay remasks the stored result and does not mutate values", async () => {
  const view = render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  act(() => mock.settle());
  expect(screen.getByRole("article")).toBeInTheDocument();
  view.rerender(
    <DicePresentation event={{ ...event(grenade, 2), replay: true }} />,
  );
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  await waitFor(() => expect(mock.show).toHaveBeenCalledTimes(2));
  expect(mock.show.mock.calls[1][0]).toEqual(mock.show.mock.calls[0][0]);
  act(() => mock.settle());
  expect(screen.getByRole("article")).toHaveTextContent(
    `Total: ${grenade.total}`,
  );
});
it("failed initialization reveals the stored result without rerolling", async () => {
  mock.create.mockRejectedValue(Error("No GPU"));
  render(<DicePresentation event={event()} />);
  expect(await screen.findByText(/3D unavailable/)).toBeInTheDocument();
  expect(screen.getByRole("article")).toHaveTextContent(
    `Total: ${grenade.total}`,
  );
});
it("context loss disposes physics and reveals once", async () => {
  const reveal = vi.fn();
  render(<DicePresentation event={event()} onReveal={reveal} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  act(() => mock.failure());
  expect(await screen.findByRole("article")).toBeInTheDocument();
  expect(mock.dispose).toHaveBeenCalled();
  expect(reveal).toHaveBeenCalledTimes(1);
});
it("unmount discards stale completion callbacks", async () => {
  const reveal = vi.fn();
  const view = render(<DicePresentation event={event()} onReveal={reveal} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  view.unmount();
  act(() => mock.settle());
  expect(reveal).not.toHaveBeenCalled();
  expect(mock.dispose).toHaveBeenCalled();
});

it("changing display preference after reveal does not replay or expose a new animation", async () => {
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.show).toHaveBeenCalled());
  act(() => mock.settle());
  fireEvent.change(
    screen.getByRole("combobox", { name: "Dice presentation" }),
    { target: { value: "REDUCED_MOTION" } },
  );
  expect(mock.show).toHaveBeenCalledTimes(1);
  expect(screen.queryByText("Rolling…")).not.toBeInTheDocument();
});

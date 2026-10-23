import React from "react";
import { beforeEach, it, expect, vi } from "vitest";
import {
  render,
  screen,
  waitFor,
  act,
  fireEvent,
} from "@testing-library/react";
import { DicePresentation } from "../src/components/DicePresentation";
import { physicalSession } from "./physical-fixture";
import fixture from "./fixtures/roll-result.json";
import { preferenceKey } from "../src/lib/dice-presentation";
const mock = vi.hoisted(() => ({
  api: vi.fn(),
  start: vi.fn(),
  complete: (_v: number[][]) => {},
  fail: () => {},
  cocked: () => {},
  skip: vi.fn(),
  dispose: vi.fn(),
}));
vi.mock("../src/lib/api", () => ({ api: mock.api }));
vi.mock("../src/lib/dice-renderer", () => ({
  startPhysicalRoll: (...args: unknown[]) => mock.start(...args),
}));
const event = () => ({ session: physicalSession, serial: 1, replay: false });
beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
  mock.api.mockResolvedValue(fixture);
  mock.start.mockImplementation((_s, _h, _animate, complete, fail, cocked) => {
    mock.complete = complete;
    mock.fail = fail;
    mock.cocked = cocked;
    return Promise.resolve(mock);
  });
});
it("holds result until physical faces and server acceptance, submits exact observed values", async () => {
  let accept!: (v: unknown) => void;
  mock.api.mockImplementation(() => new Promise((r) => (accept = r)));
  const reveal = vi.fn();
  render(<DicePresentation event={event()} onReveal={reveal} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(mock.api).not.toHaveBeenCalled();
  act(() => mock.complete([[13]]));
  expect(JSON.parse(mock.api.mock.calls[0][1].body).values).toEqual([[13]]);
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.getByText("Saving physical result…")).toBeInTheDocument();
  await act(async () => accept(fixture));
  expect(screen.getByRole("article")).toHaveTextContent(
    `Total: ${fixture.total}`,
  );
  expect(reveal).toHaveBeenCalledTimes(1);
});
it("cocked reroll keeps result hidden and does not submit partial faces", async () => {
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  act(() => mock.cocked());
  expect(screen.getByText("Cocked die – rerolling")).toBeInTheDocument();
  expect(mock.api).not.toHaveBeenCalled();
});
it.each(["TEXT_ONLY", "REDUCED_MOTION"])(
  "%s runs the same physical session before final submission",
  async (mode) => {
    localStorage.setItem(preferenceKey, JSON.stringify({ mode }));
    render(<DicePresentation event={event()} />);
    await waitFor(() => expect(mock.start).toHaveBeenCalled());
    expect(mock.start.mock.calls[0][0]).toEqual(physicalSession);
    expect(mock.start.mock.calls[0][2]).toBe(false);
    if (mode === "TEXT_ONLY") expect(mock.start.mock.calls[0][1]).toBeNull();
    expect(mock.api).not.toHaveBeenCalled();
    act(() => mock.complete([[9]]));
    expect(await screen.findByRole("article")).toBeInTheDocument();
  },
);
it("skip accelerates existing simulation without selecting a face", async () => {
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  fireEvent.click(screen.getByRole("button", { name: "Skip animation" }));
  expect(mock.skip).toHaveBeenCalled();
  expect(mock.api).not.toHaveBeenCalled();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
});
it("engine failure requests exactly one server fallback without client values", async () => {
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  act(() => mock.fail());
  await screen.findByRole("article");
  expect(mock.api).toHaveBeenCalledTimes(1);
  expect(JSON.parse(mock.api.mock.calls[0][1].body)).toMatchObject({
    values: null,
    fallback: true,
  });
});
it("lost finalisation response retries identical physical values without a second simulation", async () => {
  mock.api
    .mockRejectedValueOnce(Error("Connection lost"))
    .mockResolvedValueOnce(fixture);
  render(<DicePresentation event={event()} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  act(() => mock.complete([[11]]));
  fireEvent.click(
    await screen.findByRole("button", { name: "Retry submission" }),
  );
  await screen.findByRole("article");
  expect(mock.api.mock.calls[0][1].body).toBe(mock.api.mock.calls[1][1].body);
  expect(mock.start).toHaveBeenCalledTimes(1);
});
it("legacy replay shows canonical stored result with no session or submission", async () => {
  render(
    <DicePresentation event={{ result: fixture, serial: 1, replay: true }} />,
  );
  expect(await screen.findByRole("article")).toHaveTextContent(
    `Total: ${fixture.total}`,
  );
  expect(mock.api).not.toHaveBeenCalled();
  expect(mock.start).not.toHaveBeenCalled();
});
it("physical replay reruns seed without modifying canonical values or making requests", async () => {
  const result = {
    ...fixture,
    physical: {
      source: "PHYSICS" as const,
      presentationSeed: physicalSession.presentationSeed,
      physicsVersion: physicalSession.physicsVersion,
      geometryVersion: physicalSession.geometryVersion,
      rawPhysicalValues: [[13]],
    },
  };
  render(<DicePresentation event={{ result, serial: 1, replay: true }} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  act(() => mock.complete([[fixture.dice.groups[0].dice[0] % 20 + 1]]));
  expect(screen.getByRole("article")).toHaveTextContent(
    `Total: ${fixture.total}`,
  );
  expect(mock.dispose).toHaveBeenCalled();
  expect(screen.getByText(/Replay trajectory differs/)).toBeInTheDocument();
  expect(mock.api).not.toHaveBeenCalled();
});
it("cancel releases session and ignores late physical completion", async () => {
  const cancel = vi.fn();
  render(<DicePresentation event={event()} onCancel={cancel} />);
  await waitFor(() => expect(mock.start).toHaveBeenCalled());
  fireEvent.click(screen.getByRole("button", { name: "Cancel roll" }));
  await waitFor(() => expect(cancel).toHaveBeenCalled());
  expect(mock.api.mock.calls[0][0]).toContain("/cancel");
  expect(mock.dispose).toHaveBeenCalled();
  act(() => mock.complete([[13]]));
  expect(mock.api).toHaveBeenCalledTimes(1);
});

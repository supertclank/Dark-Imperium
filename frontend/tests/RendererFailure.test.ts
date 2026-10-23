import { it, expect, vi, afterEach, beforeEach } from "vitest";
import { physicalSession } from "./physical-fixture";
const mock = vi.hoisted(() => ({
  step: vi.fn(),
  values: vi.fn(),
  dispose: vi.fn(),
  failWebgl: false,
  canvas: null as HTMLCanvasElement | null,
  render: vi.fn(),
}));
vi.mock("../src/lib/physical-simulation", () => ({
  createSimulation: vi.fn(async () => ({
    dice: [],
    width: 6,
    depth: 4.5,
    step: mock.step,
    values: mock.values,
    dispose: mock.dispose,
  })),
}));
vi.mock("three", async (original) => ({
  ...(await original<typeof import("three")>()),
  WebGLRenderer: class {
    domElement: HTMLCanvasElement;
    constructor() {
      if (mock.failWebgl) throw Error("WebGL unavailable");
      this.domElement = document.createElement("canvas");
      mock.canvas = this.domElement;
    }
    setPixelRatio() {}
    setSize() {}
    render() {
      mock.render();
    }
    dispose() {}
    forceContextLoss() {}
  },
}));
import { startPhysicalRoll } from "../src/lib/dice-renderer";
beforeEach(() => {
  vi.useFakeTimers();
  vi.clearAllMocks();
  mock.failWebgl = false;
  mock.canvas = null;
  mock.step.mockReturnValue(true);
  mock.values.mockReturnValue([[13]]);
  vi.stubGlobal(
    "ResizeObserver",
    class {
      observe() {}
      disconnect() {}
    },
  );
  vi.stubGlobal(
    "requestAnimationFrame",
    vi.fn(() => 1),
  );
  vi.stubGlobal("cancelAnimationFrame", vi.fn());
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});
it("WebGL initialization failure completes the same physical world once", async () => {
  mock.failWebgl = true;
  const done = vi.fn(),
    fail = vi.fn();
  const handle = await startPhysicalRoll(
    physicalSession,
    document.createElement("div"),
    true,
    done,
    fail,
    vi.fn(),
  );
  await vi.runAllTimersAsync();
  expect(done).toHaveBeenCalledExactlyOnceWith([[13]]);
  expect(fail).not.toHaveBeenCalled();
  handle.dispose();
  expect(mock.dispose).toHaveBeenCalledOnce();
});
it("context loss keeps the authorised world and finishes without new values or duplicate callback", async () => {
  const done = vi.fn(),
    fail = vi.fn();
  const handle = await startPhysicalRoll(
    physicalSession,
    document.createElement("div"),
    true,
    done,
    fail,
    vi.fn(),
  );
  mock.canvas!.dispatchEvent(
    new Event("webglcontextlost", { cancelable: true }),
  );
  await vi.runAllTimersAsync();
  expect(done).toHaveBeenCalledExactlyOnceWith([[13]]);
  expect(fail).not.toHaveBeenCalled();
  handle.dispose();
});
it("headless text mode never constructs a WebGL renderer", async () => {
  mock.failWebgl = true;
  const done = vi.fn();
  const handle = await startPhysicalRoll(
    physicalSession,
    null,
    false,
    done,
    vi.fn(),
    vi.fn(),
  );
  await vi.runAllTimersAsync();
  expect(done).toHaveBeenCalledExactlyOnceWith([[13]]);
  expect(mock.canvas).toBeNull();
  handle.dispose();
});

import { it, expect } from "vitest";
import { simulationClock } from "../src/lib/simulation-clock";
import { createSimulation } from "../src/lib/physical-simulation";
import { physicalSession } from "./physical-fixture";
import { physicsTuning } from "../src/lib/dice-physics";
it("bounds catch-up after stalls and rejects invalid wall time", () => {
  const steps = simulationClock(1 / 60, 0.1);
  expect(steps(30)).toBe(6);
  expect(steps(0)).toBe(0);
  expect(steps(-1)).toBe(0);
  expect(steps(NaN)).toBe(0);
  expect(steps(Infinity)).toBe(0);
});
it.each([30, 60, 120, 144])(
  "uses exactly 60 fixed steps per second at %i Hz",
  (hz) => {
    const steps = simulationClock(1 / 60, 0.1);
    let count = 0;
    for (let i = 0; i < hz * 10; i++) count += steps(1 / hz);
    expect(count).toBe(600);
  },
);
it("produces identical settled faces at 30 60 120 144 Hz and with long frame stalls", async () => {
  const input = {
    ...physicalSession,
    groups: [
      { count: 1, sides: 20, keep: "ALL", keepCount: 1 },
      { count: 4, sides: 6, keep: "ALL", keepCount: 4 },
    ],
  };
  const results = [];
  for (const hz of [30, 60, 120, 144, 0]) {
    const sim = await createSimulation(input),
      steps = simulationClock(physicsTuning.timestep, physicsTuning.maxCatchup);
    let done = false;
    for (let f = 0; f < 10000 && !done; f++) {
      const count = steps(hz ? 1 / hz : f % 30 === 0 ? 1.5 : 1 / 30);
      expect(count).toBeLessThanOrEqual(6);
      for (let n = 0; n < count && !done; n++) {
        done = sim.step();
        for (const d of sim.dice) {
          const p = d.body.translation();
          expect(Math.abs(p.x)).toBeLessThan(sim.width + 1);
          expect(Math.abs(p.z)).toBeLessThan(sim.depth + 1);
          expect(p.y).toBeGreaterThan(-1);
        }
      }
    }
    expect(done).toBe(true);
    results.push(sim.values());
    sim.dispose();
  }
  for (const result of results) expect(result).toEqual(results[0]);
}, 30000);

import { it, expect } from "vitest";
import { Quaternion, Vector3 } from "three";
import { dieGeometry, dieFaceMap } from "../src/lib/dice-geometry";
import { createSimulation, readTopFace } from "../src/lib/physical-simulation";
import { physicalSession } from "./physical-fixture";
it.each([4, 6, 8, 10, 12, 20])(
  "detects every numbered d%i face without changing its rotation",
  (sides) => {
    const g = dieGeometry(sides);
    for (const face of dieFaceMap(g)) {
      const q = new Quaternion().setFromUnitVectors(
          face.normal,
          new Vector3(0, 1, 0),
        ),
        before = q.clone();
      expect(readTopFace(g, q)).toBe(face.value);
      expect(q.equals(before)).toBe(true);
    }
    g.dispose();
  },
);
it.each([
  ["edge", new Vector3(1, 1, 0)],
  ["corner", new Vector3(1, 1, 1)],
  ["wall lean", new Vector3(0.6, 1, 0)],
  ["die lean", new Vector3(0.5, 1, 0.3)],
] as const)("rejects a cocked cube on %s", (_name, normal) => {
  const g = dieGeometry(6);
  const q = new Quaternion().setFromUnitVectors(
    normal.clone().normalize(),
    new Vector3(0, 1, 0),
  );
  expect(readTopFace(g, q)).toBeNull();
  g.dispose();
});
it("seeded physical outcomes are identical with animated or accelerated step batches and never rotate after acceptance", async () => {
  const input = {
    ...physicalSession,
    groups: [
      { count: 1, sides: 20, keep: "ALL", keepCount: 1 },
      { count: 1, sides: 12, keep: "ALL", keepCount: 1 },
      { count: 1, sides: 8, keep: "ALL", keepCount: 1 },
      { count: 2, sides: 6, keep: "ALL", keepCount: 2 },
    ],
  };
  const a = await createSimulation(input),
    b = await createSimulation(input);
  let done = false;
  for (let i = 0; i < 2400 && !done; i++) done = a.step();
  expect(done).toBe(true);
  const rotations = a.dice.map((d) => ({ ...d.body.rotation() }));
  for (let i = 0; i < 100; i++) a.step();
  expect(a.dice.map((d) => ({ ...d.body.rotation() }))).toEqual(rotations);
  done = false;
  for (let batch = 0; batch < 20 && !done; batch++)
    for (let i = 0; i < 120 && !done; i++) done = b.step();
  expect(done).toBe(true);
  expect(a.values()).toEqual(b.values());
  expect(a.dice.map((d) => readTopFace(d.geometry, d.body.rotation()))).toEqual(
    a.dice.map((d) => d.value),
  );
  a.dispose();
  b.dispose();
});
it("rerolls only an ambiguous die using its next authorised sub-seed", async () => {
  const rerolled: string[] = [];
  const sim = await createSimulation(
    {
      ...physicalSession,
      groups: [{ count: 2, sides: 6, keep: "ALL", keepCount: 2 }],
    },
    (d) => rerolled.push(d.id),
  );
  const [valid, cocked] = sim.dice;
  valid.value = 1;
  valid.body.setBodyType(1, true);
  const frozen = { ...valid.body.rotation() };
  cocked.steps = 599;
  sim.step();
  expect(rerolled).toEqual([cocked.id]);
  expect(cocked.attempt).toBe(1);
  expect(valid.attempt).toBe(0);
  expect(valid.body.rotation()).toEqual(frozen);
  sim.dispose();
});
it("bounds cocked retries instead of choosing an ambiguous face", async () => {
  const sim = await createSimulation({ ...physicalSession, maxRerolls: 0 });
  sim.dice[0].steps = 599;
  expect(() => sim.step()).toThrow(/retry limit/);
  expect(sim.dice[0].value).toBeNull();
  sim.dispose();
});
it("physical percentile pair combines actual top faces including double zero", async () => {
  const sim = await createSimulation({
    ...physicalSession,
    groups: [{ count: 1, sides: 100, keep: "ALL", keepCount: 1 }],
  });
  let done = false;
  for (let i = 0; i < 2400 && !done; i++) done = sim.step();
  expect(done).toBe(true);
  const tens = sim.dice.find((d) => d.percentile === "tens")!,
    units = sim.dice.find((d) => d.percentile === "units")!;
  expect(sim.values()[0][0]).toBe(
    (tens.value! % 10) * 10 + (units.value! % 10) || 100,
  );
  tens.value = 10;
  units.value = 10;
  expect(sim.values()).toEqual([[100]]);
  sim.dispose();
});

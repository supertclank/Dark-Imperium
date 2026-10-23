import { beforeAll, it, expect } from "vitest";
import RAPIER from "@dimforge/rapier3d-compat";
import {
  makeBoundaries,
  createBody,
  physicsTuning,
  nearSettled,
} from "../src/lib/dice-physics";
import {Vector3} from "three";
import { dieGeometry, dieFaceMap, settledOrientation } from "../src/lib/dice-geometry";
import { physicalDice, presentRoll } from "../src/lib/dice-presentation";
import type { RollResult } from "../src/lib/rolls";
import fixture from "./fixtures/grenade-result.json";
beforeAll(async () => {
  await RAPIER.init();
});
it.each([4, 6, 8, 10, 12, 20])(
  "d%i collides with floor walls and corners and loses energy",
  (sides) => {
    const world = new RAPIER.World({ x: 0, y: physicsTuning.gravity, z: 0 });
    world.timestep = physicsTuning.timestep;
    makeBoundaries(world, 5, 5);
    const g = dieGeometry(sides);
    const b = createBody(
      world,
      new Float32Array(g.getAttribute("position").array),
      { x: 0, y: 3, z: 0 },
    );
    b.setLinvel({ x: 15, y: -3, z: 15 }, true);
    b.setAngvel({ x: 8, y: 4, z: 3 }, true);
    for (let i = 0; i < 600; i++) {
      world.step();
      const p = b.translation();
      expect(p.y).toBeGreaterThan(-0.1);
      expect(Math.abs(p.x)).toBeLessThan(5.1);
      expect(Math.abs(p.z)).toBeLessThan(5.1);
    }
    expect(nearSettled(b)).toBe(true);
    world.free();
    g.dispose();
  },
);
it("dice exchange momentum instead of passing through", () => {
  const world = new RAPIER.World({ x: 0, y: 0, z: 0 });
  const g = dieGeometry(6),
    vertices = new Float32Array(g.getAttribute("position").array);
  const a = createBody(world, vertices, { x: -2, y: 1, z: 0 }),
    b = createBody(world, vertices, { x: 0, y: 1, z: 0 });
  a.setLinvel({ x: 5, y: 0, z: 0 }, true);
  for (let i = 0; i < 40; i++) world.step();
  expect(b.translation().x).toBeGreaterThan(0.5);
  expect(a.translation().x).toBeLessThan(b.translation().x);
  world.free();
  g.dispose();
});
it.each([
  [74, 7, 4],
  [100, 10, 10],
  [10, 1, 10],
  [1, 10, 1],
])(
  "percentile %i preserves source identity across both physical dice",
  (value, tens, units) => {
    const result = structuredClone(fixture) as RollResult;
    result.dice.groups[0].sides = 100;
    result.dice.groups[0].dice = [value];
    const dice = physicalDice(presentRoll(result));
    expect(dice.map((d) => d.value)).toEqual([tens, units]);
    expect(dice.map((d) => d.authoritativeValue)).toEqual([value, value]);
    expect(new Set(dice.map((d) => d.id)).size).toBe(2);
  },
);

it.each([4,6,8,10,12,20])('every authoritative d%i orientation has a planar supporting face',sides=>{const g=dieGeometry(sides),p=g.getAttribute('position');for(const face of dieFaceMap(g)){const q=settledOrientation(g,face.value),points=Array.from({length:p.count},(_,i)=>new Vector3().fromBufferAttribute(p,i).applyQuaternion(q));const low=Math.min(...points.map(v=>v.y));const contact:Vector3[]=[];for(const v of points.filter(v=>Math.abs(v.y-low)<1e-5))if(!contact.some(c=>c.distanceToSquared(v)<1e-8))contact.push(v);expect(contact.length).toBeGreaterThanOrEqual(3);}g.dispose();});

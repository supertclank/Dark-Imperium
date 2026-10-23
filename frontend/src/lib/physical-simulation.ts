import RAPIER from "@dimforge/rapier3d-compat";
import { Quaternion, Vector3, type BufferGeometry } from "three";
import { dieGeometry, dieFaceMap } from "./dice-geometry";
import {
  createBody,
  makeBoundaries,
  nearSettled,
  physicsTuning,
} from "./dice-physics";
import type { RollSession } from "./rolls";
export const PHYSICS_VERSION = "rapier-0.21.0-di-1",
  GEOMETRY_VERSION = "di-physical-2";
let initialization: Promise<void> | undefined;
export type PhysicalDie = {
  id: string;
  groupIndex: number;
  dieIndex: number;
  sides: number;
  percentile?: "tens" | "units";
  geometry: BufferGeometry;
  body: RAPIER.RigidBody;
  value: number | null;
  attempt: number;
  steps: number;
  stable: number;
};
/** Seeded presentation randomness only; no outcome is selected in advance. */
export function seededRandom(seed: string) {
  let a = 0x9e3779b9;
  for (const c of seed) a = Math.imul(a ^ c.charCodeAt(0), 0x85ebca6b);
  return () => {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export function readTopFace(
  geometry: BufferGeometry,
  rotation: { x: number; y: number; z: number; w: number },
): number | null {
  const q = new Quaternion(rotation.x, rotation.y, rotation.z, rotation.w),
    ranked = dieFaceMap(geometry)
      .map((f) => ({
        value: f.value,
        dot: f.normal
          .clone()
          .applyQuaternion(q)
          .dot(new Vector3(0, 1, 0)),
      }))
      .sort((a, b) => b.dot - a.dot);
  return ranked[0].dot >= 0.985 && ranked[0].dot - ranked[1].dot > 0.04
    ? ranked[0].value
    : null;
}
export async function createSimulation(
  session: RollSession,
  onCocked: (die: PhysicalDie) => void = () => {},
) {
  await (initialization ??= RAPIER.init());
  const world = new RAPIER.World({ x: 0, y: physicsTuning.gravity, z: 0 });
  world.timestep = physicsTuning.timestep;
  const specs = session.groups.flatMap((g, groupIndex) =>
    Array.from({ length: g.count }, (_, dieIndex) =>
      g.sides === 100
        ? [
            { groupIndex, dieIndex, sides: 10, percentile: "tens" as const },
            { groupIndex, dieIndex, sides: 10, percentile: "units" as const },
          ]
        : [{ groupIndex, dieIndex, sides: g.sides }],
    ).flat(),
  );
  const columns = Math.ceil(Math.sqrt(specs.length)),
    rows = Math.ceil(specs.length / columns),
    width = Math.max(6, columns * 1.4 + 1),
    depth = Math.max(4.5, rows * 1.4 + 1);
  makeBoundaries(world, width, depth);
  const dice: PhysicalDie[] = specs.map((spec, index) => {
    const geometry = dieGeometry(spec.sides);
    return {
      ...spec,
      id: `${spec.groupIndex}:${spec.dieIndex}:${"percentile" in spec ? spec.percentile : "single"}`,
      geometry,
      body: createBody(
        world,
        new Float32Array(geometry.getAttribute("position").array),
        { x: 0, y: 3, z: 0 },
      ),
      value: null,
      attempt: 0,
      steps: 0,
      stable: 0,
    };
  });
  function launch(d: PhysicalDie, index: number) {
    const rng = seededRandom(
      `${session.presentationSeed}:${d.id}:${d.attempt}`,
    );
    d.body.setBodyType(RAPIER.RigidBodyType.Dynamic, true);
    d.body.setTranslation(
      {
        x: ((index % columns) - (columns - 1) / 2) * 2.6 + (rng() - 0.5) * 0.2,
        y: 3 + rng() * 2,
        z:
          (Math.floor(index / columns) - (rows - 1) / 2) * 2.6 +
          (rng() - 0.5) * 0.2,
      },
      true,
    );
    const u = rng(),
      v = rng() * Math.PI * 2,
      w = rng() * Math.PI * 2;
    d.body.setRotation(
      {
        x: Math.sqrt(1 - u) * Math.sin(v),
        y: Math.sqrt(1 - u) * Math.cos(v),
        z: Math.sqrt(u) * Math.sin(w),
        w: Math.sqrt(u) * Math.cos(w),
      },
      true,
    );
    d.body.setLinvel(
      { x: (rng() - 0.5) * 7, y: -1 - rng() * 2, z: (rng() - 0.5) * 7 },
      true,
    );
    d.body.setAngvel(
      { x: (rng() - 0.5) * 20, y: (rng() - 0.5) * 20, z: (rng() - 0.5) * 20 },
      true,
    );
    d.steps = 0;
    d.stable = 0;
  }
  dice.forEach(launch);
  let disposed = false;
  function step() {
    if (disposed) throw Error("Simulation disposed");
    world.step();
    dice.forEach((d, index) => {
      if (d.value !== null) return;
      d.steps++;
      const p = d.body.translation();
      let contact = false;
      for (let i = 0; i < d.body.numColliders(); i++)
        world.contactPairsWith(d.body.collider(i), () => {
          contact = true;
        });
      if (nearSettled(d.body) && contact) d.stable++;
      else d.stable = 0;
      if (d.stable >= physicsTuning.stableSteps) {
        const face = readTopFace(d.geometry, d.body.rotation());
        if (face !== null) {
          d.value = face;
          d.body.setLinvel({ x: 0, y: 0, z: 0 }, true);
          d.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
          d.body.setBodyType(RAPIER.RigidBodyType.Fixed, true);
          return;
        }
      }
      if (
        d.stable >= physicsTuning.stableSteps ||
        d.steps >= physicsTuning.maxStepsPerAttempt ||
        Math.abs(p.x) > width ||
        Math.abs(p.z) > depth ||
        p.y < -0.2
      ) {
        if (d.attempt >= session.maxRerolls)
          throw Error("Cocked-die retry limit reached");
        d.attempt++;
        onCocked(d);
        launch(d, index);
      }
    });
    return dice.every((d) => d.value !== null);
  }
  function values() {
    if (dice.some((d) => d.value === null)) throw Error("Dice not settled");
    return session.groups.map((g, groupIndex) =>
      Array.from({ length: g.count }, (_, dieIndex) => {
        const members = dice.filter(
          (d) => d.groupIndex === groupIndex && d.dieIndex === dieIndex,
        );
        if (g.sides !== 100) return members[0].value!;
        const tens = members.find((d) => d.percentile === "tens")!.value! % 10,
          units = members.find((d) => d.percentile === "units")!.value! % 10;
        return tens * 10 + units || 100;
      }),
    );
  }
  return {
    world,
    dice,
    width,
    depth,
    step,
    values,
    dispose() {
      if (disposed) return;
      disposed = true;
      world.free();
      dice.forEach((d) => d.geometry.dispose());
    },
  };
}
export type PhysicalSimulation = Awaited<ReturnType<typeof createSimulation>>;

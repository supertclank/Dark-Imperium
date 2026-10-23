import {
  physicsTuning as tuning,
  makeBoundaries,
  createBody,
  nearSettled,
} from "./dice-physics";
import RAPIER from "@dimforge/rapier3d-compat";
import * as T from "three";
import { physicalDice } from "./dice-presentation";
import type { DicePresentation } from "./dice-presentation";
import { dieGeometry, dieFaceMap, settledOrientation } from "./dice-geometry";
export const brassTheme = {
  body: 0x343b30,
  edge: 0xb79c60,
  ink: "#e9ddbd",
  face: "#30382c",
};
export type DiceTrayRenderer = {
  show: (model: DicePresentation, instant: boolean) => void;
  skip: () => void;
  dispose: () => void;
};
/** Lazy browser-only renderer. Its only input is an already completed presentation model. */
export async function createDiceRenderer(
  host: HTMLElement,
  onFailure: () => void,
  onSettle: () => void,
  onSettling: () => void = () => {},
): Promise<DiceTrayRenderer> {
  await RAPIER.init();

  let walls: RAPIER.Collider[] = [];

  const renderer = new T.WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: "low-power",
  });
  const world = new RAPIER.World({ x: 0, y: tuning.gravity, z: 0 });
  world.timestep = tuning.timestep;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  host.appendChild(renderer.domElement);
  renderer.domElement.setAttribute("aria-hidden", "true");
  const scene = new T.Scene(),
    camera = new T.OrthographicCamera(-5, 5, 3, -3, 0.1, 100);
  camera.position.set(0, 20, 8);
  camera.lookAt(0, 0, 0);
  scene.add(new T.HemisphereLight(0xffefd0, 0x18221c, 2.5));
  const key = new T.DirectionalLight(0xffdba0, 3);
  key.position.set(-3, 5, 8);
  scene.add(key);
  const group = new T.Group();
  scene.add(group);
  const geometries = new Map<number, T.BufferGeometry>(),
    textures = new Map<string, T.CanvasTexture>();
  const owned: T.Material[] = [];
  let frame = 0,
    started = 0,
    disposed = false,
    settled = true,
    last = 0,
    accumulator = 0,
    converging = 0,
    quietSince = 0;
  let dice: {
    group: T.Group;
    end: T.Quaternion;
    x: number;
    y: number;
    index: number;
    spread: number;
    body: RAPIER.RigidBody;
    start?: T.Quaternion;
    from?: T.Vector3;
  }[] = [];
  function geometry(sides: number) {
    let g = geometries.get(sides);
    if (!g) {
      g = dieGeometry(sides);
      geometries.set(sides, g);
    }
    return g;
  }
  function texture(value: number | string) {
    const id = String(value);
    let t = textures.get(id);
    if (t) return t;
    const c = document.createElement("canvas");
    c.width = c.height = 128;
    const ctx = c.getContext("2d");
    if (!ctx) throw Error("Canvas unavailable");
    ctx.clearRect(0, 0, 128, 128);
    ctx.fillStyle = brassTheme.ink;
    ctx.font = "bold 88px Georgia";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(id, 64, 65);
    if (value === 6 || value === 9) {
      ctx.fillRect(46, 110, 36, 3);
    }
    t = new T.CanvasTexture(c);
    t.colorSpace = T.SRGBColorSpace;
    textures.set(id, t);
    return t;
  }
  function draw() {
    if (disposed) return;
    try {
      renderer.render(scene, camera);
    } catch {
      onFailure();
    }
  }
  function height(d: (typeof dice)[number], q: T.Quaternion) {
    const p = geometry(d.group.userData.sides as number).getAttribute(
      "position",
    );
    let low = 0;
    for (let i = 0; i < p.count; i++)
      low = Math.min(
        low,
        new T.Vector3().fromBufferAttribute(p, i).applyQuaternion(q).y,
      );
    return -low + 0.015;
  }
  function size() {
    if (disposed) return;
    const width = Math.max(host.clientWidth, 240),
      pixelHeight = Math.max(host.clientHeight, 240);
    renderer.setSize(width, pixelHeight);
    const columns = Math.min(dice.length, width < 500 ? 3 : 5) || 1;
    const rows = Math.ceil(dice.length / columns) || 1;
    const halfHeight = Math.max(
      5,
      rows * 1.5,
      (columns * 1.5) / (width / pixelHeight),
    );
    camera.left = (-halfHeight * width) / pixelHeight;
    camera.right = -camera.left;
    camera.top = halfHeight;
    camera.bottom = -halfHeight;
    camera.updateProjectionMatrix();
    for (const wall of walls) world.removeCollider(wall, true);
    walls = [];
    const x = Math.max(2, camera.right - 1),
      z = halfHeight - 0.6;
    walls = makeBoundaries(world, x, z);
    dice.forEach((d, i) => {
      d.x = ((i % columns) - (columns - 1) / 2) * 2.4;
      d.y = T.MathUtils.clamp(((rows - 1) / 2 - Math.floor(i / columns)) * 2.4 + d.spread,-z+1.2,z-1.2);
      if (settled) {
        d.group.position.set(d.x, height(d, d.end), d.y);
        d.body.setTranslation(d.group.position, true);
      } else {
        const p = d.body.translation();
        d.body.setTranslation(
          {
            x: T.MathUtils.clamp(p.x, -x + 1.2, x - 1.2),
            y: p.y,
            z: T.MathUtils.clamp(p.z, -z + 1.2, z - 1.2),
          },
          true,
        );
      }
    });
    draw();
  }
  const observer = new ResizeObserver(size);
  observer.observe(host);
  function finish() {
    cancelAnimationFrame(frame);
    settled = true;
    for (const d of dice) {
      d.group.position.set(d.x, height(d, d.end), d.y);
      d.group.quaternion.copy(d.end);
      d.body.setBodyType(RAPIER.RigidBodyType.Fixed, true);
      d.body.setTranslation(d.group.position, true);
      d.body.setRotation(d.end, true);
    }
    draw();
    onSettle();
  }
  function tick(now: number) {
    if (disposed) return;
    accumulator += Math.min((now - last) / 1000, 0.1);
    last = now;
    while (accumulator >= 1 / 60) {
      world.step();
      accumulator -= 1 / 60;
    }
    const quiet = dice.every(
      (d) =>
        nearSettled(d.body) &&
        Math.abs(d.body.translation().y - height(d, d.group.quaternion)) < 0.08,
    );
    if (!quiet) quietSince = 0;
    else if (!quietSince) quietSince = now;
    if (
      !converging &&
      ((now - started > 1400 && quietSince > 0 && now - quietSince > 180) ||
        now - started > tuning.maxDuration)
    ) {
      converging = now;
      onSettling();
      // Preserve the physical spread when its circumspheres leave faces unobscured.
      const positions = dice.map((d) => d.body.translation());
      if (
        positions.every((p, i) =>
          positions.every(
            (q, j) => i === j || Math.hypot(p.x - q.x, p.z - q.z) > 2.4,
          ),
        )
      ) {
        dice.forEach((d, i) => {
          d.x = positions[i].x;
          d.y = positions[i].z;
        });
      }
      for (const d of dice) {
        d.start = d.group.quaternion.clone();
        d.from = d.group.position.clone();
        d.body.setBodyType(RAPIER.RigidBodyType.KinematicPositionBased, true);
      }
    }
    for (const d of dice) {
      if (converging) {
        const t = Math.min((now - converging) / tuning.convergenceDuration, 1),
          e = t * t * (3 - 2 * t);
        d.group.quaternion.slerpQuaternions(d.start!, d.end, e);
        d.group.position.lerpVectors(
          d.from!,
          new T.Vector3(d.x, height(d, d.group.quaternion), d.y),
          e,
        );
        d.group.position.y = Math.max(
          d.group.position.y,
          height(d, d.group.quaternion),
        );
        d.body.setNextKinematicTranslation(d.group.position);
        d.body.setNextKinematicRotation(d.group.quaternion);
      } else {
        d.group.position.copy(d.body.translation());
        d.group.quaternion.copy(d.body.rotation());
      }
    }
    draw();
    if (converging && now - converging >= tuning.convergenceDuration) finish();
    else frame = requestAnimationFrame(tick);
  }
  function clear() {
    cancelAnimationFrame(frame);
    group.traverse((o) => {
      if (
        o instanceof T.Mesh &&
        !Array.from(geometries.values()).includes(o.geometry)
      )
        o.geometry.dispose();
    });
    group.clear();
    for (const m of owned) m.dispose();
    owned.length = 0;
    for (const d of dice) world.removeRigidBody(d.body);
    dice = [];
  }
  const lost = (event: Event) => {
    event.preventDefault();
    cancelAnimationFrame(frame);
    onFailure();
  };
  renderer.domElement.addEventListener("webglcontextlost", lost);
  return {
    show(model, instant) {
      clear();
      settled = instant;
      converging = 0;
      accumulator = 0;
      // Large pools remain fully textual; never crowd or silently omit a die from a rendered pool.
      if (
        physicalDice(model).length > 20 ||
        physicalDice(model).some(
          (d) => ![4, 6, 8, 10, 12, 20].includes(d.sides),
        )
      )
        throw Error("Use textual pool presentation");
      physicalDice(model).forEach((die, index) => {
        const g = geometry(die.sides),
          body = new T.Group(),
          material = new T.MeshStandardMaterial({
            color: brassTheme.body,
            roughness: 0.65,
            metalness: 0.35,
            transparent: die.discarded,
            opacity: die.discarded ? 0.45 : 1,
          });
        owned.push(material);
        body.add(new T.Mesh(g, material));
        dieFaceMap(g).forEach((face, i) => {
          const mat = new T.MeshBasicMaterial({
            map: texture(
              die.percentile === "tens"
                ? String(((i + 1) % 10) * 10).padStart(2, "0")
                : die.percentile === "units"
                  ? (i + 1) % 10
                  : i + 1,
            ),
            transparent: true,
            opacity: die.discarded ? 0.45 : 1,
            depthWrite: false,
            polygonOffset: true,
            polygonOffsetFactor: -1,
          });
          owned.push(mat);
          const labelGeometry = new T.PlaneGeometry(
            die.sides === 20 ? 0.4 : die.sides === 4 ? 0.55 : 0.53,
            die.sides === 20 ? 0.4 : die.sides === 4 ? 0.55 : 0.53,
          );
          const label = new T.Mesh(labelGeometry, mat);
          label.position.copy(face.center).addScaledVector(face.normal, 0.008);
          label.quaternion.copy(face.numeralOrientation);
          body.add(label);
        });
        body.userData.sides = die.sides;
        const rigid = createBody(
          world,
          new Float32Array(g.getAttribute("position").array),
          { x: 0, y: 3, z: 0 },
        );
        rigid.setLinvel(
          { x: (Math.random() - 0.5) * 8, y: -2, z: (Math.random() - 0.5) * 8 },
          true,
        );
        rigid.setAngvel(
          {
            x: Math.random() * 10,
            y: Math.random() * 10,
            z: Math.random() * 10,
          },
          true,
        );
        group.add(body);
        dice.push({
          group: body,
          end: settledOrientation(g, die.value).premultiply(new T.Quaternion().setFromAxisAngle(new T.Vector3(0,1,0),(Math.random()-.5)*.3)),
          x: 0,
          y: 0,
          index,
          body: rigid,
          spread: (Math.random()-.5)*1.3,
        });
      });
      size();
      for (const d of dice) {
        d.body.setTranslation({ x: d.x, y: 3 + Math.random(), z: d.y }, true);
      }
      if (instant) finish();
      else {
        started = last = performance.now();
        frame = requestAnimationFrame(tick);
      }
    },
    skip: finish,
    dispose() {
      if (disposed) return;
      disposed = true;
      cancelAnimationFrame(frame);
      observer.disconnect();
      renderer.domElement.removeEventListener("webglcontextlost", lost);
      clear();
      for (const g of geometries.values()) g.dispose();
      for (const t of textures.values()) t.dispose();
      world.free();
      renderer.dispose();
      renderer.forceContextLoss();
      renderer.domElement.remove();
    },
  };
}

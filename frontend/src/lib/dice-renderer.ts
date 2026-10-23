import * as T from "three";
import { simulationClock } from "./simulation-clock";
import {
  createSimulation,
  type PhysicalSimulation,
} from "./physical-simulation";
import { dieFaceMap } from "./dice-geometry";
import { physicsTuning } from "./dice-physics";
import type { RollSession } from "./rolls";
export type PhysicalRenderer = { skip: () => void; dispose: () => void };
export async function startPhysicalRoll(
  session: RollSession,
  host: HTMLElement | null,
  animate: boolean,
  onComplete: (values: number[][]) => void,
  onFailure: (error: unknown) => void,
  onCocked: () => void,
): Promise<PhysicalRenderer> {
  const sim = await createSimulation(session, onCocked);
  let renderer: T.WebGLRenderer | undefined,
    observer: ResizeObserver | undefined,
    frame = 0,
    timer: ReturnType<typeof setTimeout> | undefined,
    disposed = false,
    finished = false,
    fast = !animate;
  const scene = new T.Scene(),
    camera = new T.OrthographicCamera(-8, 8, 6, -6, 0.1, 100);
  camera.position.set(0, 25, 9);
  camera.lookAt(0, 0, 0);
  const meshes: T.Group[] = [],
    materials: T.Material[] = [],
    labelGeometries: T.BufferGeometry[] = [],
    textures = new Map<string, T.CanvasTexture>();
  function texture(label: string) {
    let t = textures.get(label);
    if (t) return t;
    const c = document.createElement("canvas");
    c.width = c.height = 128;
    const ctx = c.getContext("2d");
    if (!ctx) throw Error("Canvas unavailable");
    ctx.fillStyle = "#eee1bb";
    ctx.font = label.length > 1 ? "bold 66px Georgia" : "bold 86px Georgia";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, 64, 64);
    if (label === "6" || label === "9") ctx.fillRect(47, 109, 34, 3);
    t = new T.CanvasTexture(c);
    t.colorSpace = T.SRGBColorSpace;
    textures.set(label, t);
    return t;
  }
  if (host && sim.dice.length <= 20)
    try {
      renderer = new T.WebGLRenderer({
        alpha: true,
        antialias: true,
        powerPreference: "low-power",
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
      host.appendChild(renderer.domElement);
      renderer.domElement.addEventListener("webglcontextlost", contextLost);
      renderer.domElement.setAttribute("aria-hidden", "true");
      scene.add(new T.HemisphereLight(0xffefd0, 0x18221c, 2.2));
      const light = new T.DirectionalLight(0xffdeb1, 2.5);
      light.position.set(-3, 8, 5);
      scene.add(light);
      for (const die of sim.dice) {
        const group = new T.Group(),
          material = new T.MeshStandardMaterial({
            color: 0x28352c,
            roughness: 0.7,
            metalness: 0.2,
          });
        materials.push(material);
        group.add(new T.Mesh(die.geometry, material));
        for (const face of dieFaceMap(die.geometry)) {
          const label =
            die.percentile === "tens"
              ? String((face.value % 10) * 10).padStart(2, "0")
              : die.percentile === "units"
                ? String(face.value % 10)
                : String(face.value);
          const mat = new T.MeshBasicMaterial({
            map: texture(label),
            transparent: true,
            depthWrite: false,
            polygonOffset: true,
            polygonOffsetFactor: -1,
          });
          materials.push(mat);
          const size =
            die.sides === 4 && face.vertices.length === 3
              ? 0.25
              : die.sides === 20
                ? 0.4
                : 0.5;
          const g = new T.PlaneGeometry(size, size);
          labelGeometries.push(g);
          const mesh = new T.Mesh(g, mat);
          mesh.position.copy(face.center).addScaledVector(face.normal, 0.007);
          mesh.quaternion.copy(face.numeralOrientation);
          group.add(mesh);
        }
        scene.add(group);
        meshes.push(group);
      }
      const resize = () => {
        if (disposed || !renderer || !host) return;
        const w = Math.max(host.clientWidth, 200),
          h = Math.max(host.clientHeight, 200),
          half = Math.max(sim.depth + 1, (sim.width + 1) / (w / h));
        renderer.setSize(w, h);
        camera.left = (-half * w) / h;
        camera.right = -camera.left;
        camera.top = half;
        camera.bottom = -half;
        camera.updateProjectionMatrix();
        draw();
      };
      observer = new ResizeObserver(resize);
      observer.observe(host);
      resize();
    } catch {
      renderer?.dispose();
      renderer?.domElement.remove();
      renderer = undefined;
      fast = true;
    }
  else fast = true;
  function contextLost(event: Event) {
    event.preventDefault();
    // Keep the already-authorised world and faces; losing presentation must never reroll.
    renderer?.domElement.remove();
    fast = true;
    cancelAnimationFrame(frame);
    clearTimeout(timer);
    if (!disposed && !finished)
      timer = setTimeout(() => tick(performance.now()), 0);
  }
  function draw() {
    if (!renderer || disposed) return;
    sim.dice.forEach((d, i) => {
      meshes[i]?.position.copy(d.body.translation());
      meshes[i]?.quaternion.copy(d.body.rotation());
    });
    try {
      renderer.render(scene, camera);
    } catch {
      fast = true;
    }
  }
  let previous = performance.now();
  const stepsForFrame = simulationClock(
    physicsTuning.timestep,
    physicsTuning.maxCatchup,
  );
  function tick(now: number) {
    if (disposed || finished) return;
    try {
      let count = 0;
      if (fast) count = 120;
      else {
        count = stepsForFrame((now - previous) / 1000);
      }
      previous = now;
      for (let i = 0; i < count; i++)
        if (sim.step()) {
          finished = true;
          break;
        }
      if (animate || finished) draw();
      if (finished) {
        const raw = sim.values();
        if (!animate && renderer)
          timer = setTimeout(() => {
            if (!disposed) onComplete(raw);
          }, 150);
        else onComplete(raw);
      } else if (fast) timer = setTimeout(() => tick(performance.now()), 0);
      else frame = requestAnimationFrame(tick);
    } catch (e) {
      finished = true;
      onFailure(e);
    }
  }
  if (fast) timer = setTimeout(() => tick(performance.now()), 0);
  else frame = requestAnimationFrame(tick);
  return {
    skip() {
      if (disposed || finished) return;
      fast = true;
      cancelAnimationFrame(frame);
      clearTimeout(timer);
      timer = setTimeout(() => tick(performance.now()), 0);
    },
    dispose() {
      if (disposed) return;
      disposed = true;
      cancelAnimationFrame(frame);
      clearTimeout(timer);
      observer?.disconnect();
      materials.forEach((m) => m.dispose());
      labelGeometries.forEach((g) => g.dispose());
      textures.forEach((t) => t.dispose());
      renderer?.domElement.removeEventListener("webglcontextlost", contextLost);
      renderer?.dispose();
      renderer?.forceContextLoss();
      renderer?.domElement.remove();
      sim.dispose();
    },
  };
}

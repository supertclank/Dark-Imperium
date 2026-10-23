import * as T from "three";
import { ConvexGeometry } from "three/examples/jsm/geometries/ConvexGeometry.js";
/** Shared physical/render geometry. Accepted settled face normals resolve raw values. */
export function dieGeometry(sides: number): T.BufferGeometry {
  switch (sides) {
    case 4: {
      // Truncated tips provide a real resting cap opposite each numbered face.
      const tetra = new T.TetrahedronGeometry(1),
        p = tetra.getAttribute("position"),
        vertices: T.Vector3[] = [];
      for (let i = 0; i < p.count; i++) {
        const v = new T.Vector3().fromBufferAttribute(p, i);
        if (!vertices.some((a) => a.distanceToSquared(v) < 1e-8))
          vertices.push(v);
      }
      tetra.dispose();
      return new ConvexGeometry(
        vertices.flatMap((v, i) =>
          vertices
            .filter((_, j) => i !== j)
            .map((w) => v.clone().lerp(w, 0.26)),
        ),
      );
    }
    case 6:
      return new T.BoxGeometry(1.35, 1.35, 1.35).toNonIndexed();
    case 8:
      return new T.OctahedronGeometry(1);
    case 12:
      return new T.DodecahedronGeometry(1);
    case 20:
      return new T.IcosahedronGeometry(1);
    case 10: {
      // Polar dual of a pentagonal antiprism: ten planar kite faces.
      const top = Array.from(
        { length: 5 },
        (_, i) =>
          new T.Vector3(
            Math.cos((i * 2 * Math.PI) / 5),
            0.5,
            Math.sin((i * 2 * Math.PI) / 5),
          ),
      );
      const bottom = Array.from(
        { length: 5 },
        (_, i) =>
          new T.Vector3(
            Math.cos(((i + 0.5) * 2 * Math.PI) / 5),
            -0.5,
            Math.sin(((i + 0.5) * 2 * Math.PI) / 5),
          ),
      );
      const dual = [new T.Vector3(0, 2, 0), new T.Vector3(0, -2, 0)];
      function polar(a: T.Vector3, b: T.Vector3, c: T.Vector3) {
        const n = b.clone().sub(a).cross(c.clone().sub(a)).normalize();
        if (n.dot(a) < 0) n.negate();
        dual.push(n.divideScalar(n.dot(a)));
      }
      for (let i = 0; i < 5; i++) {
        polar(top[i], top[(i + 1) % 5], bottom[i]);
        polar(bottom[i], bottom[(i + 1) % 5], top[(i + 1) % 5]);
      }
      const scale = 1 / Math.max(...dual.map((v) => v.length()));
      return new ConvexGeometry(dual.map((v) => v.multiplyScalar(scale)));
    }
    default:
      throw new Error("Unsupported presentation die");
  }
}
export function dieFaces(geometry: T.BufferGeometry) {
  const p = geometry.getAttribute("position");
  const faces: {
    normal: T.Vector3;
    center: T.Vector3;
    vertices: T.Vector3[];
  }[] = [];
  for (let i = 0; i < p.count; i += 3) {
    const a = new T.Vector3().fromBufferAttribute(p, i),
      b = new T.Vector3().fromBufferAttribute(p, i + 1),
      c = new T.Vector3().fromBufferAttribute(p, i + 2);
    const normal = b.clone().sub(a).cross(c.clone().sub(a)).normalize();
    let face = faces.find((f) => f.normal.dot(normal) > 0.99999);
    if (!face) {
      face = { normal, center: new T.Vector3(), vertices: [] };
      faces.push(face);
    }
    for (const v of [a, b, c])
      if (!face.vertices.some((x) => x.distanceToSquared(v) < 0.000001))
        face.vertices.push(v);
  }
  for (const face of faces) {
    for (const v of face.vertices) face.center.add(v);
    face.center.divideScalar(face.vertices.length);
  }
  return faces;
}
export function faceOrientation(normal: T.Vector3) {
  return new T.Quaternion().setFromUnitVectors(new T.Vector3(0, 0, 1), normal);
}
export function dieFaceMap(geometry: T.BufferGeometry) {
  const faces = dieFaces(geometry),
    major = faces.filter((f) => f.vertices.length === 6);
  if (faces.length === 8 && major.length === 4) {
    return faces.map((face, index) => {
      const primary =
        face.vertices.length === 6
          ? major.indexOf(face)
          : major.reduce(
              (best, f, i) =>
                f.normal.dot(face.normal) < major[best].normal.dot(face.normal)
                  ? i
                  : best,
              0,
            );
      return {
        ...face,
        index,
        value: primary + 1,
        numeralOrientation: faceOrientation(face.normal),
      };
    });
  }
  return faces.map((face, index) => ({
    ...face,
    index,
    value: index + 1,
    numeralOrientation: faceOrientation(face.normal),
  }));
}

import RAPIER from "@dimforge/rapier3d-compat";
export const physicsTuning = {
  friction: 0.7,
  restitution: 0.32,
  linearDamping: 0.8,
  angularDamping: 0.9,
  gravity: -25,
  timestep: 1 / 60,
  maxCatchup: 0.1,
  maxDuration: 3200,
  convergenceDuration: 700,
};
export function makeBoundaries(world: RAPIER.World, x: number, z: number) {
  return [
    [x + 1, 0.5, z + 1, 0, -0.5, 0],
    [0.5, 8, z + 1, -x - 0.5, 7, 0],
    [0.5, 8, z + 1, x + 0.5, 7, 0],
    [x + 1, 8, 0.5, 0, 7, -z - 0.5],
    [x + 1, 8, 0.5, 0, 7, z + 0.5],
  ].map(([hx, hy, hz, px, py, pz]) =>
    world.createCollider(
      RAPIER.ColliderDesc.cuboid(hx, hy, hz)
        .setTranslation(px, py, pz)
        .setFriction(physicsTuning.friction)
        .setRestitution(physicsTuning.restitution),
    ),
  );
}
export function createBody(
  world: RAPIER.World,
  vertices: Float32Array,
  position: { x: number; y: number; z: number },
) {
  const body = world.createRigidBody(
    RAPIER.RigidBodyDesc.dynamic()
      .setTranslation(position.x, position.y, position.z)
      .setLinearDamping(physicsTuning.linearDamping)
      .setAngularDamping(physicsTuning.angularDamping)
      .setCcdEnabled(true),
  );
  const hull = RAPIER.ColliderDesc.convexHull(vertices);
  if (!hull) throw Error("Invalid die hull");
  world.createCollider(
    hull
      .setFriction(physicsTuning.friction)
      .setRestitution(physicsTuning.restitution),
    body,
  );
  return body;
}
export function nearSettled(body: RAPIER.RigidBody) {
  const v = body.linvel(),
    w = body.angvel();
  return Math.hypot(v.x, v.y, v.z) < 0.15 && Math.hypot(w.x, w.y, w.z) < 0.2;
}

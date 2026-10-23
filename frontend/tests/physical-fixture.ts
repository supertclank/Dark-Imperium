import type { RollSession } from "../src/lib/rolls";
export const physicalSession: RollSession = {
  rollSessionId: "11111111-1111-4111-8111-111111111111",
  label: "Physical roll",
  groups: [{ count: 1, sides: 20, keep: "ALL", keepCount: 1 }],
  modifier: 0,
  presentationSeed: "aa23bb45cc67dd89".repeat(4),
  expiresAt: "2099-01-01T00:00:00Z",
  status: "CREATED",
  physicsVersion: "rapier-0.21.0-di-1",
  geometryVersion: "di-physical-2",
  maxRerolls: 3,
};

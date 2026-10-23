import { it, expect } from "vitest";
import { createSimulation } from "../src/lib/physical-simulation";
import { physicalSession } from "./physical-fixture";
import { writeFileSync, mkdirSync } from "node:fs";
// Broad deterministic smoke sample, not a fairness or gambling certification.
it("all physical dice have diverse seeds and no catastrophic face bias", async () => {
  const report = [];
  for (const sides of [4, 6, 8, 10, 12, 20, 100]) {
    const counts = Array(sides).fill(0);
    let failures = 0,
      rerolls = 0;
    const samples = 400;
    for (let n = 0; n < samples; n++) {
      const sim = await createSimulation(
        {
          ...physicalSession,
          presentationSeed: `distribution-smoke-v1-${sides}-${n}`,
          groups: [{ count: 1, sides, keep: "ALL", keepCount: 1 }],
        },
        () => rerolls++,
      );
      try {
        let done = false;
        for (let i = 0; i < 2400 && !done; i++) done = sim.step();
        if (!done) failures++;
        else counts[sim.values()[0][0] - 1]++;
      } catch {
        failures++;
      } finally {
        sim.dispose();
      }
    }
    const accepted = samples - failures,
      expected = accepted / sides;
    const chiSquare = counts.reduce(
      (sum, n) => sum + (n - expected) ** 2 / expected,
      0,
    );
    report.push({ sides, samples, failures, rerolls, counts, chiSquare });
    expect(failures).toBeLessThan(samples * 0.1);
    expect(Math.max(...counts)).toBeLessThan(expected * 3 + 10);
    expect(counts.filter((n) => n > 0).length).toBeGreaterThanOrEqual(
      Math.floor(sides * 0.9),
    );
    expect(chiSquare).toBeLessThan(sides * 4 + 30);
  }
  mkdirSync("../docs/verification/production", { recursive: true });
  writeFileSync(
    "../docs/verification/production/distribution-smoke.json",
    JSON.stringify(
      {
        qualification:
          "Catastrophic-bias smoke check only; no fairness certification",
        report,
      },
      null,
      2,
    ),
  );
}, 180000);

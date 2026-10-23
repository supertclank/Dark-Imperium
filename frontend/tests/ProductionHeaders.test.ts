import { afterEach, expect, it, vi } from "vitest";
import config from "../next.config";

afterEach(() => vi.unstubAllEnvs());

it("allows production physics WASM while keeping JavaScript eval disabled", async () => {
  vi.stubEnv("NODE_ENV", "production");
  const routes = await config.headers!();
  const policy = routes.find((r) => r.source === "/:path*")!.headers.find(
    (h) => h.key === "Content-Security-Policy",
  )!.value;
  const directives = Object.fromEntries(
    policy.split(";").map((directive) => {
      const [name, ...values] = directive.trim().split(/\s+/);
      return [name, values];
    }),
  );
  expect(directives["script-src"]).toContain("'wasm-unsafe-eval'");
  expect(directives["script-src"]).not.toContain("'unsafe-eval'");
  expect(directives["connect-src"]).toEqual(["'self'"]);
  expect(directives["frame-ancestors"]).toEqual(["'none'"]);
});

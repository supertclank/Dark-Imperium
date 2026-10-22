import { afterEach, describe, it, expect, vi } from "vitest";
import { api, ApiError } from "../src/lib/api";
afterEach(() => vi.unstubAllGlobals());
describe("API client", () => {
  it("preserves structured error messages", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ error: { message: "Character not found." } }),
            { status: 404 },
          ),
        ),
    );
    await expect(api("/characters/missing")).rejects.toMatchObject({
      status: 404,
      message: "Character not found.",
    });
  });
  it("supports an empty logout response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(null, { status: 204 })),
    );
    await expect(
      api("/auth/logout", { method: "POST" }),
    ).resolves.toBeUndefined();
  });
  it("turns network failures into actionable errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("fetch failed")),
    );
    await expect(api("/characters")).rejects.toBeInstanceOf(ApiError);
  });
});

it("preserves field-level creation validation errors", async () => {
  const issues=[{code:"STALE_PROFILE",field:"profileDigest",message:"Reload the builder."}];
  vi.stubGlobal("fetch",vi.fn().mockResolvedValue(new Response(JSON.stringify({status:"INVALID",errors:issues}),{status:422})));
  await expect(api("/characters",{method:"POST",body:"{}"})).rejects.toMatchObject({status:422,issues});
});

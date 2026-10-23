import { it, expect, vi, afterEach } from "vitest";
import { NextRequest } from "next/server";
import { GET, PUT } from "../src/app/api/[...path]/route";
afterEach(() => vi.unstubAllGlobals());
it("proxies canonical detail IDs but rejects traversal", async () => {
  const fetcher = vi
    .fn()
    .mockResolvedValue(new Response("{}", { status: 200 }));
  vi.stubGlobal("fetch", fetcher);
  expect(
    (
      await GET(
        new NextRequest(
          "http://localhost/api/characters/id/details/di.weapon.knife",
        ),
        {
          params: Promise.resolve({
            path: ["characters", "id", "details", "di.weapon.knife"],
          }),
        },
      )
    ).status,
  ).toBe(200);
  expect(
    (
      await GET(new NextRequest("http://localhost/api/test"), {
        params: Promise.resolve({
          path: ["characters", "..", "details", "di.weapon.knife"],
        }),
      })
    ).status,
  ).toBe(400);
  expect(fetcher).toHaveBeenCalledTimes(1);
});
it("exports PUT and accepts full Unicode notes within the notes-only byte limit", async () => {
  const fetcher = vi
    .fn()
    .mockResolvedValue(new Response("{}", { status: 200 }));
  vi.stubGlobal("fetch", fetcher);
  const request = new NextRequest("http://localhost/api/characters/id/notes", {
    method: "PUT",
    body: JSON.stringify({ text: "界".repeat(20000), expectedVersion: 0 }),
  });
  expect(
    (
      await PUT(request, {
        params: Promise.resolve({ path: ["characters", "id", "notes"] }),
      })
    ).status,
  ).toBe(200);
  expect(fetcher).toHaveBeenCalledOnce();
});
it.each([
  "..",
  "di.weapon..knife",
  "di.weapon.%2e%2e",
  "di.weapon/knife",
  "di.weapon\\knife",
  "di.weapon.knife?x=1",
])("rejects malformed canonical detail ID %s", async (id) => {
  const fetcher = vi.fn();
  vi.stubGlobal("fetch", fetcher);
  const result = await GET(new NextRequest("http://localhost/api/test"), {
    params: Promise.resolve({ path: ["characters", "id", "details", id] }),
  });
  expect(result.status).toBe(400);
  expect(fetcher).not.toHaveBeenCalled();
});
it("larger body allowance is not applied to another endpoint", async () => {
  const fetcher = vi.fn();
  vi.stubGlobal("fetch", fetcher);
  const result = await PUT(
    new NextRequest("http://localhost/api/characters/id/rolls", {
      method: "PUT",
      body: "x".repeat(17000),
    }),
    { params: Promise.resolve({ path: ["characters", "id", "rolls"] }) },
  );
  expect(result.status).toBe(413);
  expect(fetcher).not.toHaveBeenCalled();
});

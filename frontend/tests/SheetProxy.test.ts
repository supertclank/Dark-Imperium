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

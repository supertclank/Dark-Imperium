import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
const error = (status: number, code: string, message: string) =>
  Response.json({ error: { code, message } }, { status });

async function proxy(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> },
) {
  const { path } = await context.params;
  const detailPath =
    path.length === 4 && path[0] === "characters" && path[2] === "details";
  if (
    path.some(
      (segment, index) =>
        !(
          detailPath && index === 3 ? /^di(?:\.[a-z0-9_-]+)+$/ : /^[a-zA-Z0-9-]+$/
        ).test(segment),
    )
  )
    return error(400, "INVALID_PATH", "Invalid API path.");
  const headers = new Headers();
  for (const key of ["cookie", "content-type", "origin"]) {
    const value = request.headers.get(key);
    if (value) headers.set(key, value);
  }
  let body: Uint8Array | undefined;
  if (request.body && !["GET", "HEAD"].includes(request.method)) {
    const reader = request.body.getReader();
    const chunks: Uint8Array[] = [];
    let size = 0;
    while (true) {
      const chunk = await reader.read();
      if (chunk.done) break;
      size += chunk.value.length;
      if (
        size >
        (path.length === 3 && path[0] === "characters" && path[2] === "notes"
          ? 131_072
          : 16_384)
      ) {
        await reader.cancel();
        return error(413, "REQUEST_TOO_LARGE", "Request body is too large.");
      }
      chunks.push(chunk.value);
    }
    body = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) {
      body.set(chunk, offset);
      offset += chunk.length;
    }
  }
  try {
    const response = await fetch(
      `${process.env.BACKEND_URL || "http://localhost:8080"}/api/${path.join("/")}`,
      {
        method: request.method,
        headers,
        body: body as BodyInit | undefined,
        cache: "no-store",
        redirect: "manual",
        signal: AbortSignal.timeout(15_000),
      },
    );
    const output = new Headers({ "Cache-Control": "no-store" });
    for (const key of ["content-type", "location"]) {
      const v = response.headers.get(key);
      if (v) output.set(key, v);
    }
    for (const cookie of response.headers.getSetCookie())
      output.append("set-cookie", cookie);
    return new Response(response.body, {
      status: response.status,
      headers: output,
    });
  } catch {
    return error(
      503,
      "SERVICE_UNAVAILABLE",
      "The archive is temporarily unavailable. Please try again.",
    );
  }
}
export {
  proxy as GET,
  proxy as POST,
  proxy as PATCH,
  proxy as PUT,
  proxy as DELETE,
};

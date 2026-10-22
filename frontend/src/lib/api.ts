export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public issues: { code: string; field: string; message: string }[] = [],
  ) {
    super(message);
  }
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api${path}`, {
      ...init,
      credentials: "same-origin",
      cache: "no-store",
      headers: { "Content-Type": "application/json", ...init.headers },
    });
  } catch {
    throw new ApiError(0, "Connection lost. Check your network and try again.");
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new ApiError(
      response.status,
      payload?.error?.message || (payload?.errors?.length ? "Please review the highlighted choices." : "The request could not be completed."),
      payload?.errors || [],
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}
export type Content = { id: string; name: string; description: string };
export type Weapon = Content & {
  category: string;
  damageDice: string;
  damageType: string;
  normalRange: number;
  longRange: number;
  properties: { key: string; label: string }[];
};
export type User = { id: string; email: string };

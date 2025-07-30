export const API =
  (process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://127.0.0.1:8000')
    .replace(/\/+$/, '');                     // trim trailing slash(es)

export async function api<T>(
  path: string,
  token?: string,
  init: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init.headers,
    },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`HTTP ${res.status} – ${text}`);
  }
  return res.json() as Promise<T>;
}

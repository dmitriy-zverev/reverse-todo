import type {
  CreateEntryResponse,
  Entry,
  TagCategory,
  TodaySummary,
  User,
  WeeklyReport,
} from "./types";

const API = import.meta.env.VITE_API_URL ?? "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  register: (email: string, password: string) =>
    request<User>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  login: (email: string, password: string) =>
    request<User>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => request<User>("/auth/me"),
  logout: () => request<void>("/auth/logout", { method: "POST" }),
  createEntry: (raw_text: string, mood?: number) =>
    request<CreateEntryResponse>("/entries", {
      method: "POST",
      body: JSON.stringify({ raw_text, mood }),
    }),
  listEntries: (from?: string, to?: string) => {
    const params = new URLSearchParams();
    if (from) params.set("date_from", from);
    if (to) params.set("date_to", to);
    const q = params.toString();
    return request<Entry[]>(`/entries${q ? `?${q}` : ""}`);
  },
  updateEntry: (
    id: string,
    patch: { mood?: number | null; category?: TagCategory; tag_ids?: string[] },
  ) =>
    request<Entry>(`/entries/${id}`, {
      method: "PATCH",
      body: JSON.stringify(patch),
    }),
  deleteEntry: (id: string) => request<void>(`/entries/${id}`, { method: "DELETE" }),
  weeklyReport: (week?: string) =>
    request<WeeklyReport>(`/reports/weekly${week ? `?week=${week}` : ""}`),
  todaySummary: () => request<TodaySummary>("/reports/today"),
};

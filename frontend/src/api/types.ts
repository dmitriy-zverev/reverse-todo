export type TagCategory =
  | "work"
  | "learning"
  | "health"
  | "home"
  | "relationships"
  | "creative"
  | "finance"
  | "invisible_work";

export interface Tag {
  id: string;
  name: string;
  category: TagCategory;
}

export interface Entry {
  id: string;
  raw_text: string;
  entry_date: string;
  source: string;
  mood: number | null;
  energy: number | null;
  project_id: string | null;
  tags: Tag[];
  skills: { id: string; name: string }[];
  created_at: string;
}

export interface CreateEntryResponse {
  entry: Entry;
  suggestion: {
    tag_names: string[];
    category: TagCategory | null;
    project_name: string | null;
    skill_names: string[];
    confidence: number;
  };
}

export interface WeeklyReport {
  week_start: string;
  week_end: string;
  total_entries: number;
  daily_counts: number[];
  category_counts: { category: TagCategory; count: number }[];
  top_project: { project_id: string; project_name: string; count: number } | null;
  streaks: { label: string; days: number }[];
  invisible_work_count: number;
  narrative: string;
}

export interface TodaySummary {
  entry_date: string;
  entry_count: number;
  entries: Entry[];
}

export interface User {
  id: string;
  email: string;
  timezone: string;
}

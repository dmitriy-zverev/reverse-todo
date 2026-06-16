import type { WeekStats } from "../lib/week-stats";
import { categoryLabel } from "../lib/category-labels";
import { pluralDays, pluralEntries } from "../lib/archive-stats";
import { PageFactsInline } from "./page-facts-inline";

interface WeekFactsInlineProps {
  stats?: WeekStats;
}

export function WeekFactsInline({ stats }: WeekFactsInlineProps) {
  const parts: string[] = [];

  if (stats && stats.totalEntries > 0) {
    parts.push(pluralEntries(stats.totalEntries));
    if (stats.topCategory) {
      parts.push(categoryLabel(stats.topCategory));
    }
    if (stats.activeDays > 0) {
      parts.push(pluralDays(stats.activeDays));
    }
  }

  return <PageFactsInline parts={parts} label="Сводка недели" />;
}

import type { Entry } from "../api/types";
import type { ArchiveStats } from "../lib/archive-stats";
import { pluralDays, pluralEntries } from "../lib/archive-stats";
import { categoryLabel } from "../lib/category-labels";
import { dominantCategory } from "../lib/today-stats";
import { PageFactsInline } from "./page-facts-inline";

interface ArchiveFactsInlineProps {
  stats?: ArchiveStats;
  filteredEntries?: Entry[];
}

export function ArchiveFactsInline({ stats, filteredEntries }: ArchiveFactsInlineProps) {
  const parts: string[] = [];

  if (stats && stats.totalEntries > 0) {
    parts.push(pluralEntries(stats.totalEntries));
    if (stats.topCategory) {
      parts.push(categoryLabel(stats.topCategory));
    }
    if (stats.dayCount > 0) {
      parts.push(pluralDays(stats.dayCount));
    }
  } else if (filteredEntries && filteredEntries.length > 0) {
    parts.push(pluralEntries(filteredEntries.length));
    const topCategory = dominantCategory(filteredEntries);
    if (topCategory) {
      parts.push(categoryLabel(topCategory));
    }
  }

  return <PageFactsInline parts={parts} label="Сводка истории" />;
}

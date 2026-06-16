import type { TagCategory } from "../api/types";
import { categoryLabel } from "../lib/category-labels";
import { PageFactsInline } from "./page-facts-inline";

interface TodayFactsStripProps {
  entryCount: number;
  dominantCategory?: TagCategory;
  daysJournaled: number;
  layout?: "inline" | "cards";
}

export function TodayFactsStrip({
  entryCount,
  dominantCategory,
  daysJournaled,
  layout = "inline",
}: TodayFactsStripProps) {
  const parts: string[] = [];

  if (entryCount > 0) {
    parts.push(entryCount === 1 ? "1 запись" : `${entryCount} записей`);
  }
  if (dominantCategory) {
    parts.push(categoryLabel(dominantCategory));
  }
  if (daysJournaled > 0) {
    parts.push(
      daysJournaled === 1
        ? "1 день за неделю"
        : `${daysJournaled} ${daysJournaled < 5 ? "дня" : "дней"} за неделю`,
    );
  }

  if (layout === "inline") {
    return <PageFactsInline parts={parts} label="Сводка дня" />;
  }

  const tiles: { label: string; value: string }[] = [];
  if (entryCount > 0) {
    tiles.push({
      label: "сегодня",
      value: entryCount === 1 ? "1 запись" : `${entryCount} записей`,
    });
  }
  if (dominantCategory) {
    tiles.push({
      label: "больше",
      value: categoryLabel(dominantCategory),
    });
  }
  if (daysJournaled > 0) {
    tiles.push({
      label: "неделя",
      value:
        daysJournaled === 1
          ? "1 день"
          : `${daysJournaled} ${daysJournaled < 5 ? "дня" : "дней"}`,
    });
  }

  return (
    <div
      className="grid gap-[var(--space-card-gap)] sm:grid-cols-3"
      aria-label="Сводка дня"
      role="list"
    >
      {tiles.map((tile) => (
        <div
          key={tile.label}
          className="rounded-[var(--radius-ui)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-center"
          role="listitem"
        >
          <p className="page-eyebrow">{tile.label}</p>
          <p className="text-ink mt-1.5 font-display text-base leading-tight">
            {tile.value}
          </p>
        </div>
      ))}
    </div>
  );
}

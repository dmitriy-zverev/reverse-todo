import type { WeekStats } from "../lib/week-stats";
import { formatCount } from "../lib/week-stats";
import { categoryLabel } from "../lib/category-labels";
import { pluralDays, pluralEntries } from "../lib/archive-stats";
import { WashiCard } from "./washi-card";

interface WeekStatsStripProps {
  stats: WeekStats;
}

export function WeekStatsStrip({ stats }: WeekStatsStripProps) {
  if (stats.totalEntries === 0) {
    return null;
  }

  const tiles: { label: string; value: string; wide?: boolean }[] = [
    { label: "всего", value: pluralEntries(stats.totalEntries) },
    { label: "дней", value: pluralDays(stats.activeDays) },
    {
      label: "в среднем",
      value: `${formatCount(stats.averagePerActiveDay)} записей`,
    },
    {
      label: "пик",
      value: `${stats.peakDayLabel} · ${stats.peakCount}`,
    },
  ];

  if (stats.topCategory) {
    tiles.push({
      label: "чаще",
      value: categoryLabel(stats.topCategory),
      wide: true,
    });
  }

  return (
    <WashiCard
      className="week-panel"
      padded={false}
      aria-label="Сводка недели"
      role="list"
    >
      <p className="page-eyebrow week-panel__head">сводка</p>
      <div className="week-stats-grid">
        {tiles.map((tile) => (
          <div
            key={tile.label}
            className={tile.wide ? "week-stats-cell week-stats-cell--wide" : "week-stats-cell"}
            role="listitem"
          >
            <p className="page-eyebrow">{tile.label}</p>
            <p className="week-stats-value">{tile.value}</p>
          </div>
        ))}
      </div>
    </WashiCard>
  );
}

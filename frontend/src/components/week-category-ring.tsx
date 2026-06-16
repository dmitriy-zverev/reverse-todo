import type { TagCategory } from "../api/types";
import { categoryColor } from "../lib/category-colors";
import { categoryLabel } from "../lib/category-labels";
import { WashiCard } from "./washi-card";

interface WeekCategoryRingProps {
  items: { category: TagCategory; count: number }[];
}

export function WeekCategoryRing({ items }: WeekCategoryRingProps) {
  const total = items.reduce((sum, item) => sum + item.count, 0);
  if (total === 0) {
    return null;
  }

  let cursor = 0;
  const segments = items.map((item) => {
    const start = (cursor / total) * 100;
    cursor += item.count;
    const end = (cursor / total) * 100;
    return `${categoryColor(item.category)} ${start}% ${end}%`;
  });

  return (
    <WashiCard className="week-panel h-full" padded={false}>
      <p className="page-eyebrow week-panel__head">круг категорий</p>
      <div className="week-panel__body flex items-center gap-5">
        <div
          className="haiku-ring shrink-0"
          style={{ background: `conic-gradient(${segments.join(", ")})` }}
          role="img"
          aria-label="Распределение по категориям"
        />
        <ul className="week-ring-legend">
          {items.map((item) => (
            <li key={item.category} className="week-ring-legend__item">
              <span className="week-ring-legend__name">
                <span
                  className="week-ring-legend__dot"
                  style={{ background: categoryColor(item.category) }}
                  aria-hidden
                />
                <span className="truncate">{categoryLabel(item.category)}</span>
              </span>
              <span className="week-ring-legend__pct">
                {Math.round((item.count / total) * 100)}%
              </span>
            </li>
          ))}
        </ul>
      </div>
    </WashiCard>
  );
}

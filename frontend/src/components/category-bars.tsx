import type { CSSProperties } from "react";
import type { TagCategory } from "../api/types";
import { categoryColor } from "../lib/category-colors";
import { categoryLabel } from "../lib/category-labels";
import { WashiCard } from "./washi-card";

interface CategoryBarsProps {
  items: { category: TagCategory; count: number }[];
}

export function CategoryBars({ items }: CategoryBarsProps) {
  const max = Math.max(...items.map((i) => i.count), 1);

  return (
    <WashiCard className="week-panel" padded={false}>
      <p className="page-eyebrow week-panel__head">категории</p>
      <div>
        {items.map((item, index) => (
          <div
            key={item.category}
            className="week-panel__body animate-ma-rise border-t border-[var(--color-border)]"
            style={{ "--ma-stagger": index } as CSSProperties}
          >
            <div className="week-category-row">
              <span className="week-category-row__label">
                {categoryLabel(item.category)}
              </span>
              <span className="week-category-row__count">{item.count}</span>
            </div>
            <div className="week-ink-track">
              <div
                className="week-ink-bar"
                style={{
                  width: `${(item.count / max) * 100}%`,
                  background: categoryColor(item.category),
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </WashiCard>
  );
}

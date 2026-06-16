import type { CSSProperties } from "react";
import { Link } from "react-router-dom";
import { todayIsoDate } from "../lib/format-time";
import { WashiCard } from "./washi-card";

interface DotWeekStripProps {
  counts: number[];
  labels?: string[];
  dayDates?: string[];
  compact?: boolean;
  slim?: boolean;
}

export function DotWeekStrip({
  counts,
  labels,
  dayDates,
  compact = false,
  slim = false,
}: DotWeekStripProps) {
  const max = Math.max(...counts, 1);
  const today = todayIsoDate();
  const railHeight = slim ? 44 : compact ? 56 : 72;

  return (
    <WashiCard
      className={slim ? "week-rail-card week-rail-card--slim" : "week-rail-card"}
    >
      {!slim && <p className="page-eyebrow mb-3">неделя</p>}
      <div
        className="week-rail"
        style={{ "--week-rail-height": `${railHeight}px` } as CSSProperties}
        role="img"
        aria-label="Активность по дням недели"
      >
        <div className="week-rail__grid">
          {counts.map((count, index) => {
            const date = dayDates?.[index];
            const isToday = date === today;
            const isWeekend = index >= 5;
            const barHeight =
              count === 0 ? 0 : Math.max(10, Math.round((count / max) * (railHeight - 8)));
            const label = labels?.[index];

            const column = (
              <div
                className={[
                  "week-rail__day",
                  count > 0 ? "week-rail__day--active" : "",
                  isToday ? "week-rail__day--today" : "",
                  isWeekend ? "week-rail__day--weekend" : "",
                ].join(" ")}
              >
                <span className="week-rail__count" aria-hidden>
                  {count > 0 ? count : ""}
                </span>
                <div className="week-rail__bar-track">
                  {count > 0 ? (
                    <span
                      data-haiku-bar=""
                      className="week-rail__bar"
                      style={{ height: `${barHeight}px` }}
                      title={`${count} записей`}
                    />
                  ) : (
                    <span className="week-rail__void" aria-hidden />
                  )}
                </div>
                {label && <span className="week-rail__label">{label}</span>}
              </div>
            );

            if (date && count > 0) {
              return (
                <Link
                  key={index}
                  to={`/archive?date=${date}`}
                  className="week-rail__link"
                  aria-label={`${label ?? `День ${index + 1}`}, ${count} записей`}
                >
                  {column}
                </Link>
              );
            }

            return (
              <div key={index} className="week-rail__link">
                {column}
              </div>
            );
          })}
        </div>
        <div className="week-rail__baseline" aria-hidden />
      </div>
    </WashiCard>
  );
}

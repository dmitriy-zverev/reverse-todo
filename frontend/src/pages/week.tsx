import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { CategoryBars } from "../components/category-bars";
import { DotWeekStrip } from "../components/dot-week-strip";
import { HaikuVerse } from "../components/haiku-verse";
import { SplitPageLayout } from "../components/split-page-layout";
import { WashiCard } from "../components/washi-card";
import { WeekCategoryRing } from "../components/week-category-ring";
import { WeekDayBalance } from "../components/week-day-balance";
import { WeekFactsInline } from "../components/week-facts-inline";
import { WeekStatsStrip } from "../components/week-stats-strip";
import { api } from "../api/client";
import { addDays } from "../lib/format-time";
import { computeWeekStats } from "../lib/week-stats";

const DAY_LABELS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

export function WeekPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["weekly"],
    queryFn: () => api.weeklyReport(),
  });

  const dotCounts = data?.daily_counts ?? Array(7).fill(0);
  const dayDates = data
    ? Array.from({ length: 7 }, (_, i) => addDays(data.week_start, i))
    : undefined;

  const stats = useMemo(
    () => (data ? computeWeekStats(data, DAY_LABELS) : undefined),
    [data],
  );

  const sortedCategories = useMemo(
    () =>
      data
        ? [...data.category_counts].sort((a, b) => b.count - a.count)
        : [],
    [data],
  );

  const hasAsideNotes =
    (data?.streaks.length ?? 0) > 0 || (data?.invisible_work_count ?? 0) > 0;

  return (
    <SplitPageLayout
      title="Неделя"
      contentTitle="Активность"
      titleFooter={<WeekFactsInline stats={stats} />}
      aside={
        <>
          {isLoading ? (
            <WashiCard className="week-panel week-haiku-card" padded={false}>
              <p className="page-eyebrow week-panel__head">хайку недели</p>
              <p className="week-panel__body !pt-0 text-sm text-[var(--color-ink-muted)]">
                Собираю факты…
              </p>
            </WashiCard>
          ) : (
            data && (
              <>
                <HaikuVerse text={data.narrative} />
                {stats && <WeekStatsStrip stats={stats} />}
                {hasAsideNotes && (
                  <WashiCard className="week-panel" padded={false}>
                  <p className="page-eyebrow week-panel__head">ещё</p>
                  <div className="week-panel__body week-aside-notes border-t border-[var(--color-border)]">
                    {data.streaks.map((streak) => (
                      <div key={streak.label} className="week-aside-note">
                        <span className="week-aside-note__label">{streak.label}</span>
                        <span className="week-aside-note__value">{streak.days} дня</span>
                      </div>
                    ))}
                    {data.invisible_work_count > 0 && (
                      <div className="week-aside-note">
                        <span className="week-aside-note__label">невидимое</span>
                        <span className="week-aside-note__value">
                          {data.invisible_work_count} записей
                        </span>
                      </div>
                    )}
                  </div>
                </WashiCard>
              )}
            </>
            )
          )}
          {!isLoading && data?.total_entries === 0 && (
            <WashiCard className="week-panel week-haiku-card" padded={false}>
              <p className="page-eyebrow week-panel__head">неделя</p>
              <div className="week-panel__body !pt-0">
                <p className="haiku-verse m-0">
                  Неделя без записей.
                  <br />
                  Вернись вечером.
                  <br />
                  Факты важнее планов.
                </p>
              </div>
            </WashiCard>
          )}
        </>
      }
    >
      {data && stats && (
        <div className="week-feed">
          <DotWeekStrip counts={dotCounts} labels={DAY_LABELS} dayDates={dayDates} />
          {sortedCategories.length > 0 && (
            <div className="week-feed__duo">
              <CategoryBars items={sortedCategories} />
              <WeekCategoryRing items={sortedCategories} />
            </div>
          )}
          <WeekDayBalance
            weekdayEntries={stats.weekdayEntries}
            weekendEntries={stats.weekendEntries}
          />
        </div>
      )}
    </SplitPageLayout>
  );
}

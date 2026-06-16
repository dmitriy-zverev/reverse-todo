import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect } from "react";
import { WashiCard } from "../components/washi-card";
import { DotWeekStrip } from "../components/dot-week-strip";
import { EntryComposer } from "../components/entry-composer";
import { EvidenceLine } from "../components/evidence-line";
import { SplitPageLayout } from "../components/split-page-layout";
import { TodayFactsStrip } from "../components/today-facts-strip";
import { api } from "../api/client";
import type { TodaySummary } from "../api/types";
import { categoryLabel } from "../lib/category-labels";
import { addDays } from "../lib/format-time";
import { dominantCategory } from "../lib/today-stats";

const DAY_LABELS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

export function TodayPage() {
  const qc = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["today"],
    queryFn: () => api.todaySummary(),
  });
  const { data: weekly } = useQuery({
    queryKey: ["weekly"],
    queryFn: () => api.weeklyReport(),
  });

  const create = useMutation({
    mutationFn: ({ text, mood }: { text: string; mood?: number }) =>
      api.createEntry(text, mood),
    onSuccess: (response) => {
      qc.setQueryData<TodaySummary>(["today"], (current) => {
        if (!current) return current;
        const without = current.entries.filter((item) => item.id !== response.entry.id);
        return {
          ...current,
          entry_count: without.length + 1,
          entries: [response.entry, ...without],
        };
      });
      void qc.invalidateQueries({ queryKey: ["today"] });
      void qc.invalidateQueries({ queryKey: ["weekly"] });
      void qc.invalidateQueries({ queryKey: ["archive"] });
    },
  });

  useEffect(() => {
    if (!create.data) return;
    const timer = window.setTimeout(() => {
      create.reset();
    }, 5000);
    return () => window.clearTimeout(timer);
  }, [create.data, create.reset]);

  const topCategory = data ? dominantCategory(data.entries) : undefined;
  const daysJournaled = weekly?.daily_counts.filter((count) => count > 0).length ?? 0;
  const dotCounts = weekly?.daily_counts ?? Array(7).fill(0);
  const dayDates = weekly
    ? Array.from({ length: 7 }, (_, i) => addDays(weekly.week_start, i))
    : undefined;

  return (
    <SplitPageLayout
      title="Что сделано сегодня?"
      contentTitle="Записи"
      titleFooter={
        <TodayFactsStrip
          entryCount={data?.entry_count ?? 0}
          dominantCategory={topCategory}
          daysJournaled={daysJournaled}
        />
      }
      aside={
        <>
          <EntryComposer
            onSubmit={async (text, mood) => {
              await create.mutateAsync({ text, mood });
            }}
          />
          {create.data && (
            <WashiCard className="text-sm text-[var(--color-ink-muted)]">
              Похоже на {categoryLabel(create.data.suggestion.category ?? undefined)}
              {create.data.suggestion.project_name
                ? ` · ${create.data.suggestion.project_name}`
                : ""}
            </WashiCard>
          )}
        </>
      }
    >
      {weekly && (
        <DotWeekStrip
          compact
          slim
          counts={dotCounts}
          labels={DAY_LABELS}
          dayDates={dayDates}
        />
      )}
      {isLoading && <p className="text-sm text-[var(--color-ink-muted)]">Загружаю…</p>}
      {!isLoading && data?.entry_count === 0 && (
        <WashiCard className="text-sm text-[var(--color-ink-muted)]">
          День ещё пуст. Одна строка — уже прогресс.
        </WashiCard>
      )}
      {data?.entries.map((entry) => (
        <EvidenceLine key={entry.id} entry={entry} />
      ))}
    </SplitPageLayout>
  );
}

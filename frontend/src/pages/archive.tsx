import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { ArchiveFactsInline } from "../components/archive-facts-inline";
import { ArchiveStatsStrip } from "../components/archive-stats-strip";
import { DailyQuote } from "../components/daily-quote";
import { EvidenceLine } from "../components/evidence-line";
import { SplitPageLayout } from "../components/split-page-layout";
import { WashiCard } from "../components/washi-card";
import { api } from "../api/client";
import { computeArchiveStats, pluralEntries } from "../lib/archive-stats";
import { formatEntryDateHeader } from "../lib/format-time";
import { groupEntriesByDate } from "../lib/today-stats";

export function ArchivePage() {
  const [params, setParams] = useSearchParams();
  const filterDate = params.get("date") ?? undefined;

  const { data, isLoading } = useQuery({
    queryKey: ["archive", filterDate],
    queryFn: () =>
      filterDate ? api.listEntries(filterDate, filterDate) : api.listEntries(),
  });

  const groups = data ? groupEntriesByDate(data) : [];
  const stats = useMemo(
    () => (data && !filterDate ? computeArchiveStats(data) : undefined),
    [data, filterDate],
  );

  return (
    <SplitPageLayout
      className="split-page--archive"
      title="История"
      contentTitle="Записи"
      titleFooter={
        <ArchiveFactsInline stats={stats} filteredEntries={filterDate ? data : undefined} />
      }
      headerAside={
        filterDate ? (
          <button
            type="button"
            className="archive-filter-clear"
            onClick={() => setParams({})}
          >
            все дни
          </button>
        ) : undefined
      }
      aside={
        <>
          <DailyQuote />
          {stats && <ArchiveStatsStrip stats={stats} />}
          {filterDate && data && data.length > 0 && (
            <WashiCard className="week-panel" padded={false}>
              <p className="page-eyebrow week-panel__head">этот день</p>
              <div className="week-panel__body week-aside-notes border-t border-[var(--color-border)]">
                <div className="week-aside-note">
                  <span className="week-aside-note__label">дата</span>
                  <span className="week-aside-note__value capitalize">
                    {formatEntryDateHeader(filterDate)}
                  </span>
                </div>
                <div className="week-aside-note">
                  <span className="week-aside-note__label">записей</span>
                  <span className="week-aside-note__value">{pluralEntries(data.length)}</span>
                </div>
              </div>
            </WashiCard>
          )}
          {!isLoading && groups.length === 0 && (
            <WashiCard className="week-panel week-haiku-card">
              <p className="haiku-verse">Пока нет записей.</p>
            </WashiCard>
          )}
        </>
      }
    >
      {isLoading && <p className="text-sm text-[var(--color-ink-muted)]">Загружаю…</p>}
      <div className="archive-feed">
        {groups.map(([date, entries]) => (
          <section key={date} className="archive-day-group">
            {!filterDate && (
              <header className="archive-date-header">
                <h2 className="archive-date-header__label">
                  {formatEntryDateHeader(date)}
                </h2>
                <div className="archive-date-header__brush" aria-hidden />
              </header>
            )}
            {entries.map((entry, index) => (
              <EvidenceLine key={entry.id} entry={entry} index={index} />
            ))}
          </section>
        ))}
      </div>
    </SplitPageLayout>
  );
}

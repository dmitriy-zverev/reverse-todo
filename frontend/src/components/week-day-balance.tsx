import { WashiCard } from "./washi-card";

interface WeekDayBalanceProps {
  weekdayEntries: number;
  weekendEntries: number;
}

export function WeekDayBalance({ weekdayEntries, weekendEntries }: WeekDayBalanceProps) {
  const total = weekdayEntries + weekendEntries;
  if (total === 0) {
    return null;
  }

  const weekdayPct = (weekdayEntries / total) * 100;
  const weekendPct = (weekendEntries / total) * 100;

  return (
    <WashiCard className="week-panel" padded={false}>
      <p className="page-eyebrow week-panel__head">будни и выходные</p>
      <div className="week-panel__body space-y-4 border-t border-[var(--color-border)]">
        <BalanceRow label="будни" count={weekdayEntries} percent={weekdayPct} tone="ink" />
        <BalanceRow
          label="выходные"
          count={weekendEntries}
          percent={weekendPct}
          tone="accent"
        />
      </div>
    </WashiCard>
  );
}

interface BalanceRowProps {
  label: string;
  count: number;
  percent: number;
  tone: "ink" | "accent";
}

function BalanceRow({ label, count, percent, tone }: BalanceRowProps) {
  return (
    <div>
      <div className="week-category-row">
        <span className="week-category-row__label">{label}</span>
        <span className="week-category-row__count">{count}</span>
      </div>
      <div className="week-ink-track">
        <div
          className={tone === "accent" ? "week-ink-bar week-ink-bar--accent" : "week-ink-bar"}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}

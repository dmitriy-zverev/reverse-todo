import { DAILY_QUOTES } from "../data/daily-quotes";
import { quoteIndexForDate } from "../lib/daily-quote";
import { WashiCard } from "./washi-card";

interface DailyQuoteProps {
  date?: Date;
}

export function DailyQuote({ date = new Date() }: DailyQuoteProps) {
  const index = quoteIndexForDate(date, DAILY_QUOTES.length);
  const text = DAILY_QUOTES[index];

  return (
    <WashiCard
      className="week-panel week-haiku-card"
      padded={false}
      aria-label="Цитата дня"
    >
      <p className="page-eyebrow week-panel__head">цитата дня</p>
      <div className="week-panel__body !pt-0">
        <blockquote className="haiku-verse m-0 not-italic">{text}</blockquote>
      </div>
    </WashiCard>
  );
}

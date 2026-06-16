import type { CSSProperties } from "react";
import type { Entry } from "../api/types";
import { useEntryMutations } from "../hooks/use-entry-mutations";
import { categoryColor } from "../lib/category-colors";
import { formatEntryTime } from "../lib/format-time";
import { EntryControls } from "./entry-controls";
import { WashiCard } from "./washi-card";

interface EvidenceLineProps {
  entry: Entry;
}

export function EvidenceLine({ entry }: EvidenceLineProps) {
  const mutations = useEntryMutations();
  const category = entry.tags[0]?.category;
  const accentColor = category ? categoryColor(category) : "var(--color-ink)";

  return (
    <WashiCard
      as="article"
      padded={false}
      clip={false}
      accent={undefined}
      className="evidence-card"
      style={{ "--evidence-accent": accentColor } as CSSProperties}
    >
      <div className="evidence-card__body">
        <header className="evidence-card__head">
          <time dateTime={entry.created_at} className="evidence-card__time">
            {formatEntryTime(entry.created_at)}
          </time>
        </header>

        <div className="evidence-card__brush" aria-hidden />

        <p className="evidence-card__text">{entry.raw_text}</p>
      </div>

      <footer className="evidence-card__foot">
        <EntryControls entry={entry} mutations={mutations} />
      </footer>
    </WashiCard>
  );
}

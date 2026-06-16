import { WashiCard } from "./washi-card";

interface HaikuVerseProps {
  text: string;
}

export function HaikuVerse({ text }: HaikuVerseProps) {
  return (
    <WashiCard
      className="week-panel week-haiku-card"
      padded={false}
      aria-label="Хайку недели"
    >
      <p className="page-eyebrow week-panel__head">хайку недели</p>
      <div className="week-panel__body !pt-0">
        <p className="haiku-verse m-0">{text}</p>
      </div>
    </WashiCard>
  );
}

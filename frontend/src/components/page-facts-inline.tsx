interface PageFactsInlineProps {
  parts: string[];
  label: string;
}

export function PageFactsInline({ parts, label }: PageFactsInlineProps) {
  if (parts.length === 0) {
    return (
      <p className="page-stats-inline" aria-hidden="true">
        {"\u00A0"}
      </p>
    );
  }

  return (
    <p className="page-stats-inline" aria-label={label}>
      {parts.join(" · ")}
    </p>
  );
}

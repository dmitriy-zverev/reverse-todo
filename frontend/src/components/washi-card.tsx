import type { CSSProperties, ElementType, ReactNode } from "react";

interface WashiCardProps {
  children: ReactNode;
  className?: string;
  accent?: string;
  as?: ElementType;
  style?: CSSProperties;
  role?: string;
  padded?: boolean;
  clip?: boolean;
}

export function WashiCard({
  children,
  className = "",
  accent,
  as: Tag = "div",
  style,
  role,
  padded = true,
  clip = true,
}: WashiCardProps) {
  return (
    <Tag
      className={[
        "relative rounded-[var(--radius-ui)] border border-[var(--color-border)] bg-[var(--color-surface)]",
        clip ? "overflow-hidden" : "overflow-visible",
        padded ? "px-[var(--space-card-x)] py-[var(--space-card-y)]" : "",
        className,
      ].join(" ")}
      style={style}
      role={role}
    >
      {accent && (
        <span
          className="pointer-events-none absolute bottom-3 left-0 top-3 w-px"
          style={{ background: accent }}
          aria-hidden
        />
      )}
      {children}
    </Tag>
  );
}

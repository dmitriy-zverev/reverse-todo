import type { ReactNode } from "react";

interface SplitPageLayoutProps {
  title: string;
  titleFooter?: ReactNode;
  aside: ReactNode;
  children: ReactNode;
  contentTitle?: string;
  contentMeta?: ReactNode;
  headerAside?: ReactNode;
  className?: string;
}

export function SplitPageLayout({
  title,
  titleFooter,
  aside,
  children,
  contentTitle,
  contentMeta,
  headerAside,
  className,
}: SplitPageLayoutProps) {
  const mobileSectionLabel = contentTitle ? (
    <div className="flex w-full items-end justify-between gap-3">
      <p className="page-eyebrow">{contentTitle}</p>
      {contentMeta}
    </div>
  ) : (
    contentMeta
  );

  return (
    <main className="split-page-layout">
      <div
        className={["split-page", titleFooter && "split-page--with-subtitle", className]
          .filter(Boolean)
          .join(" ")}
      >
        <div className="split-page__title-row">
          <div className="split-page__title-main min-w-0">
            <h1 className="font-display text-ink text-3xl leading-none lg:text-[2rem]">
              {title}
            </h1>
            {titleFooter && <div className="split-page__title-sub">{titleFooter}</div>}
          </div>

          <div className="split-page__title-end">
            {headerAside}
            <div className="split-page__title-label hidden items-end justify-end gap-3 lg:flex">
              {contentTitle ? (
                <p className="page-eyebrow">{contentTitle}</p>
              ) : (
                <span className="split-page__title-label-spacer" aria-hidden />
              )}
              {contentMeta}
            </div>
          </div>
        </div>

        <aside className="split-page__aside">{aside}</aside>

        <section className="split-page__feed" aria-label={contentTitle}>
          {mobileSectionLabel && <div className="lg:hidden">{mobileSectionLabel}</div>}
          {children}
        </section>
      </div>
    </main>
  );
}

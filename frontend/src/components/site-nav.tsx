import { useLayoutEffect, useRef, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

const links = [
  { to: "/", label: "Сегодня" },
  { to: "/week", label: "Неделя" },
  { to: "/archive", label: "История" },
];

function isLinkActive(pathname: string, to: string) {
  if (to === "/") {
    return pathname === "/";
  }
  return pathname.startsWith(to);
}

function navLinkClass(isActive: boolean) {
  return [
    "site-nav__link",
    isActive ? "site-nav__link--active" : "",
    "rounded-[var(--radius-ui)] px-3 py-2 text-center text-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--color-surface)]",
    isActive
      ? "font-medium text-[var(--color-accent)]"
      : "text-[var(--color-ink-muted)] hover:bg-[var(--color-card-muted)]/80 hover:text-[var(--color-ink)]",
  ].join(" ");
}

interface SiteNavProps {
  layout: "row" | "grid";
}

export function SiteNav({ layout }: SiteNavProps) {
  const location = useLocation();
  const containerRef = useRef<HTMLDivElement>(null);
  const [indicator, setIndicator] = useState({ left: 0, width: 0 });

  useLayoutEffect(() => {
    const container = containerRef.current;
    if (!container) {
      return;
    }
    const activeLink = container.querySelector<HTMLElement>('[data-nav-active="true"]');
    if (!activeLink) {
      return;
    }
    setIndicator({
      left: activeLink.offsetLeft,
      width: activeLink.offsetWidth,
    });
  }, [location.pathname, layout]);

  const navClass = layout === "grid" ? "site-nav site-nav--grid" : "site-nav site-nav--row";

  return (
    <div ref={containerRef} className={navClass}>
      <span
        className="site-nav__indicator"
        style={{
          width: indicator.width,
          transform: `translateX(${indicator.left}px)`,
        }}
        aria-hidden
      />
      {links.map((link) => {
        const active = isLinkActive(location.pathname, link.to);
        return (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={navLinkClass(active)}
            data-nav-active={active ? "true" : undefined}
          >
            {link.label}
          </NavLink>
        );
      })}
    </div>
  );
}

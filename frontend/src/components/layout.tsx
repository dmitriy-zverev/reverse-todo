import { NavLink, Outlet } from "react-router-dom";
import { WashiCard } from "./washi-card";

const links = [
  { to: "/", label: "Сегодня" },
  { to: "/week", label: "Неделя" },
  { to: "/archive", label: "История" },
];

function navLinkClass(isActive: boolean) {
  return [
    "rounded-[var(--radius-ui)] px-3 py-2 text-center text-sm transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--color-surface)]",
    isActive
      ? "bg-[var(--color-accent-soft)] font-medium text-[var(--color-accent)]"
      : "text-[var(--color-ink-muted)] hover:bg-[var(--color-card-muted)]/80 hover:text-[var(--color-ink)]",
  ].join(" ");
}

export function Layout() {
  return (
    <div className="layout-frame">
      <div className="grain pointer-events-none fixed inset-0" aria-hidden />
      <div className="layout-shell">
        <header className="layout-header">
          <nav className="layout-header__nav" aria-label="Основная навигация">
            <WashiCard className="layout-header__tabs !px-1 !py-1">
              <div className="flex gap-1">
                {links.map((link) => (
                  <NavLink
                    key={link.to}
                    to={link.to}
                    className={({ isActive }) => navLinkClass(isActive)}
                    end={link.to === "/"}
                  >
                    {link.label}
                  </NavLink>
                ))}
              </div>
            </WashiCard>
          </nav>
        </header>
        <div className="layout-outlet">
          <Outlet />
        </div>
      </div>
      <nav className="layout-bottom-nav lg:hidden" aria-label="Основная навигация">
        <WashiCard className="layout-bottom-nav__card !px-1 !py-1">
          <div className="grid grid-cols-3 gap-1">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => navLinkClass(isActive)}
                end={link.to === "/"}
              >
                {link.label}
              </NavLink>
            ))}
          </div>
        </WashiCard>
      </nav>
    </div>
  );
}

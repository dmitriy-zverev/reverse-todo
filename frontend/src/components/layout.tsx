import { Outlet } from "react-router-dom";
import { SiteNav } from "./site-nav";
import { WashiCard } from "./washi-card";

export function Layout() {
  return (
    <div className="layout-frame">
      <div className="grain pointer-events-none fixed inset-0" aria-hidden />
      <div className="layout-shell">
        <header className="layout-header">
          <nav className="layout-header__nav" aria-label="Основная навигация">
            <WashiCard className="layout-header__tabs !px-1 !py-1">
              <SiteNav layout="row" />
            </WashiCard>
          </nav>
        </header>
        <div className="layout-outlet">
          <Outlet />
        </div>
      </div>
      <nav className="layout-bottom-nav lg:hidden" aria-label="Основная навигация">
        <WashiCard className="layout-bottom-nav__card !px-1 !py-1">
          <SiteNav layout="grid" />
        </WashiCard>
      </nav>
    </div>
  );
}

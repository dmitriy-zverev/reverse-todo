import { Link } from "react-router-dom";

export function SiteBrand() {
  return (
    <Link to="/" className="site-brand" aria-label="Заметки — на главную">
      <span className="site-brand__name">Заметки</span>
    </Link>
  );
}

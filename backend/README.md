# Reverse To-Do Backend

FastAPI backend for the Reverse To-Do anti-task tracker.

Local dev uses **SQLite** (`sqlite+aiosqlite:///./reverse_todo.db`).

```bash
cp .env.example .env
uv sync --all-extras
uv run alembic revision --autogenerate -m "initial"
uv run alembic upgrade head
uv run fastapi dev
```

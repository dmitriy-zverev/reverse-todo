# Reverse To-Do

Anti-task tracker: record what you **did**, not what you plan. Web-first MVP with FastAPI + React.

## Stack

- **Backend:** FastAPI, SQLAlchemy async, SQLite (local dev), Clean Architecture, TDD
- **Frontend:** React, Vite, Tailwind v4, TanStack Query, Evening Ledger UI

## Quick start

```bash
make setup
make migrate-new MSG="initial"
make migrate
make dev            # API :8000 + UI :5173
```

Or step by step:

```bash
cd backend && cp .env.example .env
make install
make migrate-new MSG="initial"
make migrate
make dev-api   # terminal 1
make dev-web   # terminal 2
```

Open http://localhost:5173 — API proxied to :8000.

SQLite file: `backend/reverse_todo.db` (gitignored).

`make help` — all commands.

### Tests

```bash
make test
```

## Architecture

```
api → application → domain ← infrastructure
```

- Domain: entities, repository Protocols, ClassificationProvider port
- Application: use cases (CreateEntry, GetWeeklyReport, auth)
- Infrastructure: SQLAlchemy repos, RuleBasedClassifier, JWT cookies
- Telegram adapter reuses CreateEntryUseCase (phase 2)

## MVP screens

- **Today** — composer + Evidence Lines
- **Week** — narrative + dot-week + category bars
- **Archive** — dated ledger feed

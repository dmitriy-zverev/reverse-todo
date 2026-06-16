.DEFAULT_GOAL := help

BACKEND_DIR := backend
FRONTEND_DIR := frontend
UV := uv --directory $(BACKEND_DIR)
NPM := npm --prefix $(FRONTEND_DIR)

.PHONY: help install setup env migrate migrate-new dev dev-api dev-web test test-api test-web lint build clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install backend (uv) and frontend (npm) dependencies
	$(UV) sync --all-extras
	$(NPM) ci

setup: env install ## First-time setup: .env + deps

env: ## Copy backend/.env.example → backend/.env if missing
	@test -f $(BACKEND_DIR)/.env || cp $(BACKEND_DIR)/.env.example $(BACKEND_DIR)/.env

migrate: ## Apply Alembic migrations (upgrade head)
	$(UV) run alembic upgrade head

migrate-new: ## Create migration — usage: make migrate-new MSG="add users"
	@test -n "$(MSG)" || (echo 'Usage: make migrate-new MSG="description"' && exit 1)
	$(UV) run alembic revision --autogenerate -m "$(MSG)"

dev-api: ## Run FastAPI dev server (:8000)
	$(UV) run fastapi dev

dev-web: ## Run Vite dev server (:5173)
	$(NPM) run dev

dev: ## Run API + frontend dev servers (API ready before Vite)
	@trap 'kill 0' INT TERM EXIT; \
	$(MAKE) dev-api & \
	echo "Waiting for API on :8000..."; \
	for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do \
		curl -sf http://127.0.0.1:8000/health >/dev/null 2>&1 && break; \
		sleep 0.5; \
	done; \
	curl -sf http://127.0.0.1:8000/health >/dev/null || (echo "API failed to start on :8000" && exit 1); \
	$(MAKE) dev-web

test: test-api test-web ## Run all tests

test-api: ## Backend pytest with coverage
	$(UV) run pytest --cov=src/reverse_todo --cov-report=term-missing

test-web: ## Frontend vitest with coverage
	$(NPM) test -- --run --coverage

lint: ## Ruff check (backend)
	$(UV) run ruff check src tests

build: ## Build frontend for production
	$(NPM) run build

clean: ## Remove caches, build artifacts, local venv, SQLite DB
	rm -rf $(BACKEND_DIR)/.venv $(BACKEND_DIR)/.pytest_cache $(BACKEND_DIR)/.ruff_cache $(BACKEND_DIR)/htmlcov $(BACKEND_DIR)/.coverage
	rm -f $(BACKEND_DIR)/reverse_todo.db $(BACKEND_DIR)/reverse_todo.db-*
	rm -rf $(FRONTEND_DIR)/node_modules $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/coverage

# Repository Guidelines

## Project Structure & Module Organization

LootPrice is a monorepo for a game key price aggregator. The active backend lives in `backend/`: `main.py` exposes the FastAPI app, while `app/api`, `app/core`, `app/models`, `app/schemas`, and `app/crawlers` hold routes, infrastructure, SQLModel tables, Pydantic DTOs, and store integrations. Tests live in `backend/tests/` and should mirror the module under test with files named `test_<module>.py`. Project decisions and contracts are documented in `docs/`; AI-specific workflows live in `ai/`. The React frontend is currently only a `frontend/.gitkeep` placeholder.

## Build, Test, and Development Commands

- `make install`: creates `.venv`, installs `backend/requirements.txt`, and installs Lefthook when available.
- `make dev`: starts Docker Compose services and runs `uvicorn main:app --reload` from `backend/`.
- `make test`: runs Pytest from `backend/`.
- `make lint`: runs `ruff check .` from `backend/`.
- `make format`: runs `ruff format .` from `backend/`.

Copy `backend/.env.example` to `backend/.env` before local development. Keep secrets in `.env`, never in source.

## Coding Style & Naming Conventions

Backend code targets Python 3.11+ and FastAPI. Use `async`/`await` for routes and I/O, type hints for all function parameters and returns, and standard `logging` instead of `print()` in production code. Ruff is the formatter and linter: 88-character lines, double quotes, spaces for indentation, and import sorting enabled. Use `NUMERIC(10,2)`/decimal-safe types for money; never use `float` for prices. Database schema changes require Alembic migrations.

## Testing Guidelines

Use Pytest for unit and integration tests. Add focused tests for every new feature, crawler parser, API route, or bug fix. Test files belong in `backend/tests/` and should be named `test_<feature>.py`. Run `make test` before opening a PR, and pair risky changes with regression tests.

## Commit & Pull Request Guidelines

Git history and Lefthook enforce Conventional Commits, for example `feat(crawler): add nuuvem scraper`, `fix(auth): refresh token expiry`, or `docs(schema): update prices table`. Branches should use prefixes such as `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, or `test/`.

Pull requests should use `.github/PULL_REQUEST_TEMPLATE.md`, describe the change and validation performed, link the related Jira/GitHub item when applicable, and include screenshots for UI work. Do not merge without green CI and review.

## Agent-Specific Instructions

Before project work, read `docs/project_state.md`, `docs/architecture.md`, and the relevant skill: `ai/backend-developer/SKILL.md` for backend or `ai/frontend-developer/SKILL.md` for frontend. Keep changes scoped, avoid direct pushes to `master`, and update `docs/project_state.md` when files, cards, or technical decisions change.

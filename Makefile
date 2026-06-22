.PHONY: install dev db-up migrate test lint format help

# Variáveis
PYTHON = python3
PIP = $(PYTHON) -m pip
VENV = .venv
ACTIVATE = . $(VENV)/bin/activate
DOCKER_COMPOSE = docker compose

help:
	@echo "Comandos disponíveis:"
	@echo "  make install  - Instala dependências, cria venv e configura Lefthook"
	@echo "  make dev      - Sobe o banco (Docker) e inicia o servidor FastAPI"
	@echo "  make db-up    - Sobe apenas o banco PostgreSQL via Docker Compose"
	@echo "  make migrate  - Executa migrations Alembic"
	@echo "  make test     - Executa os testes unitários com Pytest"
	@echo "  make lint     - Executa o linter Ruff"
	@echo "  make format   - Executa o formatador Ruff"

install:
	virtualenv $(VENV)
	$(ACTIVATE) && $(PIP) install -r backend/requirements.txt
	@if command -v lefthook > /dev/null; then \
		lefthook install; \
	else \
		echo "Lefthook não encontrado. Por favor, instale-o globalmente primeiro."; \
	fi

dev:
	$(DOCKER_COMPOSE) up -d
	$(ACTIVATE) && cd backend && uvicorn main:app --reload

db-up:
	$(DOCKER_COMPOSE) up -d db

migrate:
	$(ACTIVATE) && cd backend && alembic upgrade head

test:
	$(ACTIVATE) && cd backend && pytest

lint:
	$(ACTIVATE) && cd backend && ruff check .

format:
	$(ACTIVATE) && cd backend && ruff format .

.PHONY: install dev test lint format help

# Variáveis
PYTHON = python3
PIP = $(PYTHON) -m pip
VENV = .venv
ACTIVATE = . $(VENV)/bin/activate

help:
	@echo "Comandos disponíveis:"
	@echo "  make install  - Instala dependências, cria venv e configura Lefthook"
	@echo "  make dev      - Sobe o banco (Docker) e inicia o servidor FastAPI"
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
	docker-compose up -d
	$(ACTIVATE) && cd backend && uvicorn main:app --reload

test:
	$(ACTIVATE) && cd backend && pytest

lint:
	$(ACTIVATE) && cd backend && ruff check .

format:
	$(ACTIVATE) && cd backend && ruff format .

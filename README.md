# LootPrice

> Agregador e comparador de preços de chaves de jogos digitais.

[![CI](https://github.com/RodrigoVieira06/lootprice/actions/workflows/ci.yml/badge.svg)](https://github.com/RodrigoVieira06/lootprice/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

O LootPrice realiza scraping e consome APIs de múltiplas lojas, normaliza os dados e exibe em uma interface única onde cada jogo está mais barato.

---

## Arquitetura

```
[ Nuuvem Scraper ]  [ Steam API ]
         │                │
         └────────┬────────┘
                  ▼
       [ Normalization Engine ]
                  │
                  ▼
          [ PostgreSQL 15+ ]
                  │
                  ▼
           [ FastAPI REST ]
                  │
                  ▼
          [ React SPA (MVP) ]
```

Documentação completa: [`docs/architecture.md`](docs/architecture.md)

---

## Pré-requisitos

- Ubuntu (máquina nativa ou WSL2 no Windows)
- Python 3.11+
- Docker & Docker Compose
- Node.js 20+
- Lefthook instalado globalmente

> **Acesso remoto:** O ambiente de desenvolvimento recomendado é uma máquina Ubuntu acessada via SSH. Use **[Tailscale](https://tailscale.com)** para acesso SSH seguro de qualquer lugar e **[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)** para expor a aplicação durante testes sem precisar de VPS.

---

## Primeiros Passos

```bash
# 1. Clone o repositório
git clone https://github.com/RodrigoVieira06/lootprice.git
cd lootprice

# 2. Copie as variáveis de ambiente
cp backend/.env.example backend/.env
# Edite backend/.env com suas credenciais

# 3. Instale dependências e configure git hooks
make install

# 4. Inicie o servidor de desenvolvimento
make dev
```

API disponível em `http://localhost:8000`
Documentação Swagger em `http://localhost:8000/docs`

---

## Comandos Disponíveis

| Comando | Descrição |
|---|---|
| `make install` | Instala dependências e configura Lefthook |
| `make dev` | Sobe o banco e inicia o servidor FastAPI |
| `make lint` | Executa Ruff check |
| `make format` | Formata o código com Ruff |
| `make test` | Executa todos os testes com Pytest |

Comandos de banco/migrations/crawlers (`make db-up`, `make migrate`, `make crawl`) estão planejados para os próximos cards e só devem ser usados após entrarem no `Makefile`.

---

## Estrutura do Repositório

```
lootprice/
├── ai/
│   ├── README.md             # Índice das ferramentas de IA
│   ├── backend-developer/    # Skill: backend sênior LootPrice
│   ├── frontend-developer/   # Skill: frontend sênior LootPrice
│   └── reviewer/SKILL.md     # Skill: revisor de código
├── docs/
│   ├── architecture.md       # Visão arquitetural completa
│   ├── database_schema.md    # Schema do banco de dados
│   ├── project_state.md      # Estado vivo do projeto (cards, decisões, última sessão)
├── backend/
│   ├── app/
│   │   ├── api/v1/           # Endpoints REST
│   │   ├── core/             # Config, DB, segurança, dependências
│   │   ├── models/           # Tabelas SQLModel
│   │   ├── schemas/          # DTOs Pydantic
│   └── crawlers/            # Scrapers por loja
├── frontend/.gitkeep         # Placeholder; SPA ainda não implementada
├── .github/
│   ├── workflows/ci.yml      # CI: lint + testes
│   └── PULL_REQUEST_TEMPLATE.md
├── docker-compose.yml
├── Makefile
└── lefthook.yml
```

---

## Stack

**Backend:** Python 3.11, FastAPI, SQLModel, Alembic, PostgreSQL 15, HTTPX, BeautifulSoup4, Pydantic v2, python-jose, passlib, slowapi, Ruff, Pytest

**Frontend (MVP):** React mais recente, TypeScript/TSX, Vite, SCSS, Axios, Zod, React Hook Form, Zustand, Biome, Jest, pnpm

**Infra:** Docker + Docker Compose, Nginx, Tailscale (acesso SSH), Cloudflare Tunnel (exposição pública)

---

## Qualidade de Código

- **Linting/Formatting:** Ruff (substitui Black + isort + Flake8)
- **Testes:** Pytest com httpx para testes de integração da API
- **Git Hooks:** Lefthook — bloqueia commits com lint failing ou mensagem fora do padrão
- **CI:** GitHub Actions roda lint + testes em todo push e PR

**Padrão de commits:** [Conventional Commits](https://www.conventionalcommits.org/)

```
feat(crawler): adicionar suporte ao scraper da Nuuvem
fix(auth): corrigir expiração do refresh token
docs(schema): atualizar modelagem da tabela prices
```

---

## Desenvolvimento com IA

Este projeto usa MCP (Model Context Protocol) extensivamente:

- **GitHub MCP** — criar issues, abrir PRs, comentar, verificar CI
- **Jira MCP** — gerenciar cards e sprints via chat
- **DevTools MCP** — inspecionar frontend em tempo real

As ferramentas de IA do projeto estão organizadas em [`ai/`](ai/README.md):
- **[`ai/backend-developer/SKILL.md`](ai/backend-developer/SKILL.md)** — skill para backend, banco, crawlers, autenticação e CI backend
- **[`ai/frontend-developer/SKILL.md`](ai/frontend-developer/SKILL.md)** — skill para React, TSX, SCSS, Biome, Jest, pnpm, UX e integração frontend
- **[`ai/reviewer/SKILL.md`](ai/reviewer/SKILL.md)** — skill de review: analisa PRs via MCP GitHub e posta review estruturado

O estado atual do projeto (cards, decisões, última sessão) está em [`docs/project_state.md`](docs/project_state.md).

---

## Roadmap

| Fase | Status | Escopo |
|---|---|---|
| Fase 1 — MVP | 🔄 Em andamento | Backend, crawlers Steam + Nuuvem, auth (local + OAuth), revogação de tokens, API REST, rate limiting, Nginx |
| Fase 1.5 — Frontend | ⏳ Planejado | React SPA: busca, detalhe de jogo, login/registro |
| Fase 2 — Expansão | ⏳ Planejado | Admin panel, mais lojas (GOG, GMG), wishlist, alertas |
| Fase 3 — Escala | ⏳ Planejado | Histórico de preços, alertas, G2A/Eneba, consoles |

---

## Licença

MIT — veja [LICENSE](LICENSE) para detalhes.

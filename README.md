# LootPrice

> Agregador e comparador de preços de chaves de jogos digitais.

[![CI](https://github.com/RodrigoVieira06/lootprice/actions/workflows/ci.yml/badge.svg)](https://github.com/RodrigoVieira06/lootprice/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

O LootPrice realiza scraping, consome APIs ou importa feeds de múltiplas lojas, normaliza os dados e exibe em uma interface única onde cada jogo está mais barato. A monetização por afiliados é feita via redirect interno com métricas, não por links externos expostos diretamente no frontend.

---

## Arquitetura

```
[ Nuuvem Feed/Scraper ]  [ Steam API ]  [ Lojas Futuras ]
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
                  ├── [ Affiliate Redirect + Click Metrics ]
                  │
                  ▼
          [ React SPA (MVP) ]
```

Documentação completa para IA: [`AGENTS.md`](AGENTS.md)
Estratégia de lojas, afiliados e riscos: [`docs/affiliate_store_strategy.md`](docs/affiliate_store_strategy.md)

---

## Afiliados e Fontes de Dados

O projeto não assume "crawler por padrão". Cada loja deve declarar:

- fonte permitida: `api`, `feed`, `scraper`, `manual` ou `disabled`;
- permissão para exibir preço;
- permissão para deep link afiliado;
- suporte a `subid`/`click_id` para tracking;
- status de compliance e nível de risco.

Todo botão de compra deve usar um endpoint interno de saída, como `/api/v1/out/{price_id}`, para registrar clique e só então redirecionar para a loja. Marketplaces de keys como G2A, Eneba e Kinguin ficam fora do MVP inicial até existirem campos, UX e regras claras para risco, região e vendedor.

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

---

## Estrutura do Repositório

```
lootprice/
├── ai/
│   ├── README.md             # Índice das ferramentas de IA
│   ├── backend-developer/    # Skill: backend sênior LootPrice
│   ├── frontend-developer/   # Skill: frontend sênior LootPrice
│   ├── reviewer/             # Skill: revisor de código
│   └── scrum-master/         # Skill: scrum master
├── docs/
│   ├── database_schema.md    # Schema do banco de dados
│   └── issues_mvp.md         # Issues detalhadas para o MVP
├── backend/
│   ├── app/
│   │   ├── api/v1/           # Endpoints REST
│   │   ├── core/             # Config, DB, segurança, dependências
│   │   ├── models/           # Tabelas SQLModel
│   │   ├── schemas/          # DTOs Pydantic
│   │   └── crawlers/         # Scrapers por loja
│   └── tests/
├── frontend/.gitkeep         # Placeholder; SPA ainda não implementada
├── .github/
│   ├── workflows/ci.yml      # CI: lint + testes
│   └── PULL_REQUEST_TEMPLATE.md
├── AGENTS.md                 # Contexto unificado para IA
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

## Gestão do Projeto

O LootPrice usa **GitHub Issues** como sistema de gestão de tarefas:

- Issues são criadas com prefixo de coluna no título: `[Backlog]`, `[Developing]`, `[Code Review]`, `[Done]`, etc.
- Labels de tipo (`type:feat`, `type:fix`, `type:chore`) e prioridade (`priority:high`, `priority:medium`, `priority:low`)
- Milestones para fases do projeto
- Issues detalhadas em [`docs/issues_mvp.md`](docs/issues_mvp.md)

---

## Desenvolvimento com IA

Este projeto usa MCP (Model Context Protocol) extensivamente:

- **GitHub MCP** — criar issues, abrir PRs, comentar, verificar CI
- **DevTools MCP** — inspecionar frontend em tempo real

As ferramentas de IA do projeto estão organizadas em [`ai/`](ai/README.md):
- **[`ai/backend-developer/SKILL.md`](ai/backend-developer/SKILL.md)** — skill para backend, banco, crawlers, autenticação e CI
- **[`ai/frontend-developer/SKILL.md`](ai/frontend-developer/SKILL.md)** — skill para React, TSX, SCSS, Biome, Jest, pnpm, UX e integração frontend
- **[`ai/reviewer/SKILL.md`](ai/reviewer/SKILL.md)** — skill de review: analisa PRs via MCP GitHub e posta review estruturado
- **[`ai/scrum-master/SKILL.md`](ai/scrum-master/SKILL.md)** — skill de scrum master: gerencia issues do GitHub como cards do projeto

O contexto unificado para IA está em [`AGENTS.md`](AGENTS.md).

---

## Roadmap

| Fase | Status | Escopo |
|---|---|---|
| Fase 1 — MVP | 🔄 Em andamento | Backend, crawlers Steam + Nuuvem, auth (local + OAuth), revogação de tokens, API REST, rate limiting, Nginx |
| Fase 1 — Afiliados | ⏳ Planejado | Store compliance, outbound redirect, métricas de clique e validação de programas de afiliado |
| Fase 1.5 — Frontend | ⏳ Planejado | React SPA: busca, detalhe de jogo, login/registro usando `outbound_url` interno |
| Fase 2 — Expansão | ⏳ Planejado | Admin panel, mais lojas (GOG, GMG), wishlist, alertas |
| Fase 3 — Escala | ⏳ Planejado | Histórico de preços, alertas, G2A/Eneba/Kinguin, consoles |

---

## Licença

MIT — veja [LICENSE](LICENSE) para detalhes.

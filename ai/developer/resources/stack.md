# LootPrice — Referência: Stack Tecnológica

> Referência técnica para uso das skills. Sem instruções — só dados.

---

## Backend & Crawler

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| FastAPI | latest | Framework web assíncrono |
| SQLModel | latest | ORM (sobre SQLAlchemy) |
| Alembic | latest | Migrations de banco — obrigatório desde o dia 1 |
| Pydantic | v2 | Validação de dados e DTOs |
| HTTPX | latest | HTTP client assíncrono (crawlers e testes) |
| BeautifulSoup4 | latest | Parsing de HTML (Nuuvem scraper) |
| python-jose | latest | JWT encoding/decoding |
| passlib + bcrypt | latest | Hashing de senhas |
| slowapi | latest | Rate limiting para FastAPI |
| Ruff | latest | Linter + formatter (substitui Black/isort/Flake8) |
| Pytest + pytest-asyncio | latest | Testes unitários e de integração |

> ⚠️ `python-jose`: monitorar manutenção — migrar para `PyJWT` + `authlib` se inativo 6+ meses (DT-02)

---

## Banco de Dados & Infra

| Tecnologia | Finalidade |
|---|---|
| PostgreSQL 15+ | Banco principal |
| Docker Compose | PostgreSQL local (bound em `127.0.0.1:5432`) |
| Nginx | Proxy reverso — repassa `CF-Connecting-IP` para FastAPI |
| Tailscale | SSH seguro sem IP fixo |
| Cloudflare Tunnel | HTTPS público (bloqueado — requer domínio. Ver DT-04 em `docs/project_state.md`) |

---

## Frontend

| Tecnologia | Finalidade |
|---|---|
| React 18 | Framework UI |
| TypeScript | Tipagem estrita |
| Vite | Build tool |
| TailwindCSS | Estilo |
| Axios | HTTP client |
| Zod | Validação de schemas |
| React Hook Form | Formulários |
| Zustand | State management |

---

## Métricas & Observabilidade

| Tecnologia | Finalidade |
|---|---|
| PostHog | Tudo-em-um: Product Analytics, Session Replay, Feature Flags e error tracking básico |

---

## Tooling & DevOps

| Ferramenta | Finalidade |
|---|---|
| Makefile | Atalhos: `make dev`, `make test`, `make crawl`, `make migrate` |
| Lefthook | Git hooks: lint + commit message no pre-commit |
| `.github/workflows/ci.yml` | CI: lint (Ruff) + testes (Pytest) em cada PR/push |
| MCP GitHub | Criar branches, PRs, comentar, verificar CI |
| MCP Jira | Criar e mover cards do backlog |
| MCP DevTools | Inspecionar browser, console, screenshots |

---

## Variáveis de Ambiente (`backend/.env`)

```env
# Banco
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/lootprice

# JWT
SECRET_KEY=             # gerar com: openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth — Google
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# OAuth — Discord
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=

# Frontend (prefixo VITE_ expõe para o cliente)
VITE_API_URL=http://localhost:8000/api/v1

# PostHog
VITE_POSTHOG_KEY=
VITE_POSTHOG_HOST=https://us.i.posthog.com
```

---

## Comandos Frequentes

```bash
make install                            # Instala deps + configura virtualenv
make dev                                # Sobe banco + inicia FastAPI
make db-seed                            # Popula tabela stores
make migrate                            # Aplica migrations pendentes
make migrate-create msg="description"   # Cria nova migration
make migrate-rollback                   # Reverte última migration
make lint                               # Ruff check
make format                             # Ruff format
make test                               # Pytest
make crawl                              # Executa todos os crawlers
```

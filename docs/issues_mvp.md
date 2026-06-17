# LootPrice — Issues do MVP

> **Última atualização:** 2026-06-16
> **Audiência:** Desenvolvedores, Scrum Master IA, LLMs de apoio
> **Gestão:** GitHub Issues no repositório `RodrigoVieira06/lootprice`

Este documento define **todas as issues** necessárias para entregar o MVP do LootPrice (Fase 1 + Fase 1.5). Cada issue será criada como GitHub Issue com os campos descritos.

---

## Convenções

- **Tipo:** `epic` (agrupador), `task` (entregável), `subtask` (parte de uma task)
- **Estimativa:** `S` (< 2h), `M` (2-4h), `L` (4-8h), `XL` (> 8h)
- **Prefixo do título:** `[Backlog]` (inicial). Atualizar conforme fluxo de colunas
- **Labels de tipo:** `type:feat`, `type:fix`, `type:chore`, `type:docs`, `type:refactor`, `type:test`
- **Labels de prioridade:** `priority:high`, `priority:medium`, `priority:low`
- **Labels especiais:** `epic`, `blocked`
- **Milestones:** `Fase 1 - MVP Backend`, `Fase 1.5 - Frontend`

---

## Épicos

| ID | Épico | Milestone | Descrição |
|---|---|---|---|
| E1 | Setup & Infra | Fase 1 | Monorepo, Docker, Makefile, Lefthook, CI |
| E2 | Database & Models | Fase 1 | PostgreSQL, Alembic, models SQLModel, seeds |
| E3 | Autenticação | Fase 1 | JWT local, OAuth Google/Discord, RBAC, revogação |
| E4 | Crawlers | Fase 1 | Steam API, Nuuvem scraper, normalização, runner |
| E5 | API REST | Fase 1 | Endpoints públicos + admin |
| E6 | Segurança & Rate Limiting | Fase 1 | slowapi, headers, proteção |
| E7 | Frontend MVP | Fase 1.5 | React SPA, páginas, auth UI |
| E8 | Infra de Deploy | Fase 1 | Nginx, Cloudflare Tunnel |

---

## E1 — Setup & Infra

### ISSUE-01: Setup inicial do repositório monorepo

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] chore(infra): setup inicial do repositório monorepo` |
| **Labels** | `type:chore`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | Nenhuma |
| **Estimativa** | L |

**Descrição:**
Configurar a estrutura base do monorepo com todas as pastas, arquivos de configuração e tooling.

**Critérios de Aceitação:**
- [ ] Estrutura de pastas criada conforme `AGENTS.md` §3
- [ ] `Makefile` com targets: `install`, `dev`, `test`, `lint`, `format`
- [ ] `lefthook.yml` com pre-commit (ruff check + format) e commit-msg (Conventional Commits)
- [ ] `docker-compose.yml` com PostgreSQL 15 em `127.0.0.1:5432`
- [ ] `backend/.env.example` com todas as variáveis documentadas
- [ ] `backend/requirements.txt` com dependências base
- [ ] `backend/ruff.toml` configurado (88 chars, double quotes, import sorting)
- [ ] `backend/main.py` com app FastAPI mínima (`/health` retornando 200)
- [ ] `.gitignore` configurado
- [ ] `make install` funciona sem erros
- [ ] `make dev` sobe banco + servidor
- [ ] `make test` roda com 0 erros (pode ter 0 testes)

---

### ISSUE-02: Pipeline CI com GitHub Actions

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] chore(ci): pipeline CI com GitHub Actions` |
| **Labels** | `type:chore`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-01 |
| **Estimativa** | M |

**Descrição:**
Criar workflow CI que roda lint e testes em cada push e PR para `master`.

**Critérios de Aceitação:**
- [ ] `.github/workflows/ci.yml` criado
- [ ] Job `backend` roda: checkout → setup Python 3.11 → install deps → ruff check → ruff format --check → pytest
- [ ] Service `postgres:15` como banco de testes isolado
- [ ] Job `frontend` comentado (reativar quando frontend existir)
- [ ] CI passa em push e PR para `master`
- [ ] Branch protection configurada no GitHub: require PR + status checks

---

## E2 — Database & Models

### ISSUE-03: PostgreSQL + Alembic setup

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(database): PostgreSQL + Alembic setup` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-01 |
| **Estimativa** | M |

**Descrição:**
Configurar conexão async com PostgreSQL e inicializar Alembic para controle de migrations.

**Critérios de Aceitação:**
- [ ] `backend/app/core/database.py` com engine async e `get_session()`
- [ ] `backend/app/core/config.py` com `Settings` via pydantic-settings
- [ ] Alembic inicializado em `backend/migrations/`
- [ ] `alembic.ini` e `migrations/env.py` configurados para async
- [ ] Migration inicial com extensões `pgcrypto` e `citext`
- [ ] `make db-up` e `make migrate` no Makefile (ou documentar comandos)
- [ ] Teste de conexão com banco passando

---

### ISSUE-04: Models de lojas e jogos

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(database): models stores, games, store_products, prices` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-03 |
| **Estimativa** | L |

**Descrição:**
Criar models SQLModel para `stores`, `games`, `store_products` e `prices` conforme `docs/database_schema.md`.

**Critérios de Aceitação:**
- [ ] `backend/app/models/store.py` — model `Store`
- [ ] `backend/app/models/game.py` — model `Game`
- [ ] `backend/app/models/store_product.py` — model `StoreProduct`
- [ ] `backend/app/models/price.py` — model `Price`
- [ ] Todos os campos monetários usam `Decimal` + `NUMERIC(10,2)`
- [ ] Migration Alembic gerada e aplicada
- [ ] Constraints e índices conforme schema
- [ ] Seed de stores (Steam + Nuuvem) via migration ou script
- [ ] Testes unitários para validação dos models

---

### ISSUE-05: Model users com OAuth e RBAC

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(database): model users, oauth_accounts, revoked_tokens` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-03 |
| **Estimativa** | L |

**Descrição:**
Criar models de autenticação: `users`, `oauth_accounts` e `revoked_tokens`.

**Critérios de Aceitação:**
- [ ] `backend/app/models/user.py` — model `User` com `email` CITEXT, `role`, `hashed_password` nullable
- [ ] `backend/app/models/oauth_account.py` — model `OAuthAccount`
- [ ] `backend/app/models/revoked_token.py` — model `RevokedToken` com `token_jti`
- [ ] Migration Alembic gerada e aplicada
- [ ] `hashed_password` nunca incluso em schemas de response
- [ ] CHECK constraints para `role` e `provider`
- [ ] Testes unitários

---

### ISSUE-06: Model crawler_runs

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(database): model crawler_runs` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04 |
| **Estimativa** | S |

**Descrição:**
Model de observabilidade para execuções de crawler.

**Critérios de Aceitação:**
- [ ] `backend/app/models/crawler_run.py` — model `CrawlerRun`
- [ ] Migration Alembic
- [ ] CHECK constraint para `status`
- [ ] Índice em `(store_id, started_at DESC)`

---

## E3 — Autenticação

### ISSUE-07: Autenticação JWT local (login + registro)

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(auth): autenticação JWT local — login e registro` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-05 |
| **Estimativa** | L |

**Descrição:**
Implementar registro de usuário e login local com JWT (access + refresh tokens).

**Critérios de Aceitação:**
- [ ] `backend/app/core/security.py` — `create_access_token()`, `create_refresh_token()`, `decode_token()`, `hash_password()`, `verify_password()`
- [ ] `backend/app/api/v1/auth.py` — rotas `POST /auth/register` e `POST /auth/login`
- [ ] `backend/app/schemas/auth.py` — `LoginRequest`, `RegisterRequest`, `TokenResponse`
- [ ] Access token expira em 30min, refresh em 7 dias
- [ ] Refresh token inclui campo `jti` (UUID)
- [ ] Validação de email e senha via Pydantic
- [ ] Testes de integração para registro e login
- [ ] `hashed_password` nunca retornado

---

### ISSUE-08: Refresh e logout com revogação de tokens

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(auth): refresh token e logout com revogação` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-07 |
| **Estimativa** | M |

**Descrição:**
Implementar renovação de tokens e logout com blacklist de `jti`.

**Critérios de Aceitação:**
- [ ] `POST /auth/refresh` — renova access token usando refresh token válido
- [ ] `POST /auth/logout` — insere `jti` na tabela `revoked_tokens`
- [ ] `decode_token()` verifica blacklist antes de aceitar token
- [ ] `GET /auth/me` — retorna dados do usuário autenticado
- [ ] Teste: logout invalida o refresh token
- [ ] Teste: refresh com token revogado retorna 401

---

### ISSUE-09: OAuth Google

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(auth): OAuth Google login` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-07, ISSUE-05 |
| **Estimativa** | L |

**Descrição:**
Login social via Google OAuth2 com upsert de user e oauth_account.

**Critérios de Aceitação:**
- [ ] `GET /auth/google` — redirect para Google OAuth
- [ ] Callback processa code → user_info → upsert user + oauth_account
- [ ] Retorna JWT (mesmo formato do login local)
- [ ] Variáveis `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` em `.env`
- [ ] Testes com mock do provider

---

### ISSUE-10: OAuth Discord

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(auth): OAuth Discord login` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-09 |
| **Estimativa** | M |

**Descrição:**
Login social via Discord OAuth2, mesma estrutura do Google.

**Critérios de Aceitação:**
- [ ] `GET /auth/discord` — redirect + callback
- [ ] Upsert user + oauth_account
- [ ] JWT retornado
- [ ] Variáveis `DISCORD_CLIENT_ID` e `DISCORD_CLIENT_SECRET`
- [ ] Testes com mock

---

### ISSUE-11: RBAC — roles user e admin

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(auth): RBAC com roles user e admin` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-07 |
| **Estimativa** | M |

**Descrição:**
Dependencies de autorização para proteger rotas admin.

**Critérios de Aceitação:**
- [ ] `backend/app/core/dependencies.py` — `get_current_user()` e `require_admin()`
- [ ] Rotas admin protegidas com `Depends(require_admin)`
- [ ] Usuário sem role `admin` recebe 403 em rotas admin
- [ ] Testes: user normal → 403; admin → 200

---

## E4 — Crawlers

### ISSUE-12: Normalização de nomes e geração de slugs

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(crawler): normalização de nomes e geração de slugs` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04 |
| **Estimativa** | M |

**Descrição:**
Lógica de normalização que gera `canonical_name` e `slug` a partir do título bruto do jogo.

**Critérios de Aceitação:**
- [ ] Utilitário em `backend/app/crawlers/normalizer.py` (ou `core/`)
- [ ] Remove sufixos de plataforma ("- PC", "(Steam)", "™", "®")
- [ ] Lowercase, strip, replace múltiplos espaços
- [ ] Gera slug URL-friendly
- [ ] Testes com edge cases: "Cyberpunk 2077™", "Cyberpunk 2077 - PC", etc.

---

### ISSUE-13: Crawler Steam API

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(crawler): implementar crawler Steam via API pública` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04, ISSUE-12 |
| **Estimativa** | L |

**Descrição:**
Crawler que consulta a API pública da Steam e retorna dados no formato `RawGameData`.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/steam.py` herda de `BaseCrawler`
- [ ] `store_slug = "steam"`
- [ ] Usa HTTPX async
- [ ] Retorna `RawGameData` validado via Pydantic
- [ ] `try/except` com logging em todo I/O
- [ ] Testes com mock da API Steam

---

### ISSUE-14: Crawler Nuuvem (scraper)

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(crawler): implementar scraper Nuuvem` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04, ISSUE-12 |
| **Estimativa** | XL |

**Descrição:**
Scraper que coleta dados da Nuuvem via HTTPX + BeautifulSoup4.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/nuuvem.py` herda de `BaseCrawler`
- [ ] `store_slug = "nuuvem"`
- [ ] HTTPX async + BeautifulSoup4 para parsing
- [ ] Retorna `RawGameData` validado
- [ ] `try/except` + logging
- [ ] Respeita rate limiting (delay entre requests)
- [ ] Testes com HTML mockado

---

### ISSUE-15: Crawler runner (orquestrador)

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(crawler): implementar runner orquestrador de crawlers` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-13, ISSUE-14, ISSUE-06 |
| **Estimativa** | L |

**Descrição:**
Orquestrador que roda todos os crawlers, faz upsert no banco e registra `crawler_runs`.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/runner.py`
- [ ] Registra crawlers ativos
- [ ] Para cada crawler: executa `fetch()`, normaliza, upsert em `games`, `store_products`, `prices`
- [ ] Registra `crawler_runs` com status, contadores e erros
- [ ] Falha em um crawler não para os demais
- [ ] `make crawl` no Makefile
- [ ] Testes de integração

---

## E5 — API REST

### ISSUE-16: Endpoints públicos — busca, listagem e detalhe

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(api): endpoints públicos — busca, listagem e detalhe de jogos` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04 |
| **Estimativa** | L |

**Descrição:**
Implementar os endpoints públicos: busca, listagem paginada e detalhe de jogo com preços.

**Critérios de Aceitação:**
- [ ] `GET /api/v1/search?q={query}` — busca por `canonical_name` ILIKE
- [ ] `GET /api/v1/games` — listagem paginada
- [ ] `GET /api/v1/games/{slug}` — detalhe com preços ordenados por `price_brl`
- [ ] `GET /api/v1/prices?game_id={id}` — preços de um jogo
- [ ] Schemas de response: `GameRead`, `GameWithPrices`, `PriceRead`
- [ ] `backend/app/api/v1/router.py` agrega rotas
- [ ] Testes de integração para cada endpoint

---

### ISSUE-17: Endpoints admin

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(api): endpoints de administração` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-11, ISSUE-15, ISSUE-16 |
| **Estimativa** | M |

**Descrição:**
Endpoints protegidos por RBAC para administração.

**Critérios de Aceitação:**
- [ ] `POST /api/v1/admin/crawl` — força execução dos crawlers (role admin)
- [ ] `GET /api/v1/admin/stores` — lista lojas
- [ ] `PATCH /api/v1/admin/stores/{id}` — ativa/desativa loja
- [ ] `PATCH /api/v1/admin/games/{id}` — edita `canonical_name`
- [ ] Todas as rotas protegidas com `require_admin`
- [ ] Testes com user normal (403) e admin (200)

---

## E6 — Segurança & Rate Limiting

### ISSUE-18: Rate limiting com slowapi

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(security): rate limiting com slowapi` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-16 |
| **Estimativa** | M |

**Descrição:**
Configurar throttling em rotas públicas com `get_real_ip()` para compatibilidade com Cloudflare.

**Critérios de Aceitação:**
- [ ] `backend/app/core/rate_limit.py` — limiter + `get_real_ip()` lendo `CF-Connecting-IP` via Nginx
- [ ] Rotas de busca e listagem limitadas (ex: 30/min)
- [ ] Rota de login limitada (ex: 5/min)
- [ ] Middleware configurado no `main.py`
- [ ] Testes verificam header `X-RateLimit-Remaining`

---

## E7 — Frontend MVP

### ISSUE-19: Setup React SPA

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(frontend): setup React SPA com Vite + TSX + SCSS` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-16 (backend API disponível) |
| **Estimativa** | L |

**Descrição:**
Criar a base do frontend React com toda a toolchain configurada.

**Critérios de Aceitação:**
- [ ] Vite + React + TypeScript (TSX)
- [ ] SCSS configurado
- [ ] Zustand para state management
- [ ] Axios configurado com base URL da API
- [ ] Biome para lint/format
- [ ] Jest configurado
- [ ] pnpm como gerenciador
- [ ] Scripts: `dev`, `build`, `lint`, `format`, `test`
- [ ] `.env.example` com `VITE_API_URL`
- [ ] Estrutura: `src/components/`, `pages/`, `hooks/`, `services/`, `store/`, `types/`
- [ ] Job frontend reativado no CI

---

### ISSUE-20: Página de busca e listagem de jogos

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(frontend): página de busca e listagem de jogos` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-19, ISSUE-16 |
| **Estimativa** | L |

**Descrição:**
Página principal com barra de busca e grid de jogos com menor preço.

**Critérios de Aceitação:**
- [ ] Barra de busca com debounce
- [ ] Grid/lista de jogos com capa, título e menor preço
- [ ] Paginação ou scroll infinito
- [ ] Loading state e empty state
- [ ] Responsivo
- [ ] Service Axios para `/search` e `/games`
- [ ] Tipos TypeScript alinhados com schemas do backend

---

### ISSUE-21: Página de detalhe do jogo com comparação de preços

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(frontend): página de detalhe do jogo com comparação de preços` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-20 |
| **Estimativa** | L |

**Descrição:**
Página de detalhe mostrando todos os preços de todas as lojas, ordenados.

**Critérios de Aceitação:**
- [ ] Capa do jogo, título, canonical_name
- [ ] Lista de preços por loja: nome da loja, preço atual, preço original, % desconto
- [ ] Link direto para compra (affiliate_url)
- [ ] "Atualizado há X minutos" baseado em `scraped_at`
- [ ] Responsivo
- [ ] Service Axios para `/games/{slug}`

---

### ISSUE-22: Páginas de login e registro

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] feat(frontend): páginas de login e registro` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-19, ISSUE-07 |
| **Estimativa** | L |

**Descrição:**
Formulários de login (local + social) e registro.

**Critérios de Aceitação:**
- [ ] Formulário de login com email/senha (React Hook Form + Zod)
- [ ] Formulário de registro
- [ ] Botões de login social (Google, Discord)
- [ ] Gerenciamento de tokens (Zustand store)
- [ ] Redirect após login
- [ ] Validação client-side com Zod
- [ ] Tratamento de erros da API
- [ ] Testes de componente com Jest

---

## E8 — Infra de Deploy

### ISSUE-23: Nginx com suporte a CF-Connecting-IP

| Campo | Valor |
|---|---|
| **Tipo** | task |
| **Título** | `[Backlog] chore(infra): Nginx + CF-Connecting-IP` |
| **Labels** | `type:chore`, `priority:low`, `blocked` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-18 |
| **Estimativa** | M |

**Descrição:**
Configurar Nginx como proxy reverso com reescrita de header para IP real do Cloudflare.

> **⚠️ Bloqueado:** Requer domínio registrado para Cloudflare Tunnel.

**Critérios de Aceitação:**
- [ ] `nginx/nginx.conf` e `nginx/sites/lootprice.conf`
- [ ] `proxy_pass` para FastAPI
- [ ] Header `X-Forwarded-For` reescrito a partir de `CF-Connecting-IP`
- [ ] Docker Compose inclui service Nginx
- [ ] `get_real_ip()` do slowapi funciona com o header

---

## Grafo de Dependências

```
ISSUE-01 (setup)
  ├── ISSUE-02 (CI)
  ├── ISSUE-03 (PostgreSQL + Alembic)
  │     ├── ISSUE-04 (models lojas/jogos)
  │     │     ├── ISSUE-06 (crawler_runs)
  │     │     ├── ISSUE-12 (normalização)
  │     │     │     ├── ISSUE-13 (Steam crawler)
  │     │     │     └── ISSUE-14 (Nuuvem crawler)
  │     │     │           └── ISSUE-15 (runner) ← depende de 13, 14, 06
  │     │     └── ISSUE-16 (API pública)
  │     │           ├── ISSUE-17 (API admin) ← depende de 11, 15, 16
  │     │           ├── ISSUE-18 (rate limiting)
  │     │           │     └── ISSUE-23 (Nginx) ← bloqueado
  │     │           └── ISSUE-19 (frontend setup) ← Fase 1.5
  │     │                 ├── ISSUE-20 (busca)
  │     │                 │     └── ISSUE-21 (detalhe)
  │     │                 └── ISSUE-22 (login/registro)
  │     └── ISSUE-05 (models users)
  │           ├── ISSUE-07 (JWT local)
  │           │     ├── ISSUE-08 (refresh/logout)
  │           │     ├── ISSUE-09 (OAuth Google)
  │           │     │     └── ISSUE-10 (OAuth Discord)
  │           │     └── ISSUE-11 (RBAC)
  │           └── ISSUE-09 (OAuth Google) ← depende de 05 e 07
```

---

## Ordem de Execução Sugerida

Sequência recomendada respeitando dependências e prioridades:

1. **ISSUE-01** — Setup monorepo
2. **ISSUE-02** — CI
3. **ISSUE-03** — PostgreSQL + Alembic
4. **ISSUE-04** — Models lojas/jogos (paralelo com 05)
5. **ISSUE-05** — Models users
6. **ISSUE-06** — Model crawler_runs
7. **ISSUE-07** — JWT local
8. **ISSUE-08** — Refresh/logout
9. **ISSUE-11** — RBAC
10. **ISSUE-12** — Normalização
11. **ISSUE-13** — Steam crawler
12. **ISSUE-14** — Nuuvem crawler
13. **ISSUE-15** — Runner
14. **ISSUE-16** — API pública
15. **ISSUE-17** — API admin
16. **ISSUE-18** — Rate limiting
17. **ISSUE-09** — OAuth Google
18. **ISSUE-10** — OAuth Discord
19. **ISSUE-19** — Frontend setup (Fase 1.5)
20. **ISSUE-20** — Busca
21. **ISSUE-21** — Detalhe
22. **ISSUE-22** — Login/registro
23. **ISSUE-23** — Nginx (quando domínio disponível)

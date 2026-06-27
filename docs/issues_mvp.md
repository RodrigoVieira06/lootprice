# LootPrice — Issues do MVP

> **Última atualização:** 2026-06-26
> **Audiência:** Desenvolvedores, Scrum Master IA, LLMs de apoio
> **Gestão:** GitHub Issues no repositório `RodrigoVieira06/lootprice`

Este documento define **todas as issues** necessárias para entregar o MVP do LootPrice (Fase 1 + Fase 1.5). Cada issue está criada como GitHub Issue com os campos descritos.

---

## Convenções

- **Tipo:** `epic` (agrupador), `task` (entregável), `subtask` (parte de uma task)
- **Estimativa:** `S` (< 2h), `M` (2-4h), `L` (4-8h), `XL` (> 8h)
- **Prefixo do título:** `[Status] #N` — Status atualizado conforme fluxo de colunas
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
| E9 | Afiliados & Store Compliance | Fase 1 | Estratégia de lojas, permissões de ingestão, tracking de cliques e redirect afiliado |

---

## E1 — Setup & Infra

### ISSUE-01: Setup inicial do repositório monorepo

| Campo | Valor |
|---|---|
| **Ordem** | #1 |
| **GitHub** | [#24](https://github.com/RodrigoVieira06/lootprice/issues/24) |
| **Status** | `[Done]` |
| **Tipo** | task |
| **Título** | `#1 chore(infra): setup inicial do repositório monorepo` |
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
| **Ordem** | #2 |
| **GitHub** | [#25](https://github.com/RodrigoVieira06/lootprice/issues/25) |
| **Status** | `[Code Review]` |
| **Tipo** | task |
| **Título** | `#2 chore(ci): pipeline CI com GitHub Actions` |
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
| **Ordem** | #3 |
| **GitHub** | [#26](https://github.com/RodrigoVieira06/lootprice/issues/26) |
| **Status** | `[Prioritized]` |
| **Tipo** | task |
| **Título** | `#3 feat(database): PostgreSQL + Alembic setup` |
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
| **Ordem** | #4 |
| **GitHub** | [#27](https://github.com/RodrigoVieira06/lootprice/issues/27) |
| **Status** | `[Prioritized]` |
| **Tipo** | task |
| **Título** | `#4 feat(database): models stores, games, store_products, prices` |
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
- [ ] `Store` inclui política de ingestão: `ingestion_source`, permissões de preço/afiliado/scraping, `compliance_status`, `risk_level`, `terms_url`, `compliance_notes`
- [ ] Todos os campos monetários usam `Decimal` + `NUMERIC(10,2)`
- [ ] Migration Alembic gerada e aplicada
- [ ] Constraints e índices conforme schema
- [ ] Seed de stores (Steam + Nuuvem) via migration ou script com status inicial `needs_review`
- [ ] Testes unitários para validação dos models

---

### ISSUE-05: Model users com OAuth e RBAC

| Campo | Valor |
|---|---|
| **Ordem** | #5 |
| **GitHub** | [#28](https://github.com/RodrigoVieira06/lootprice/issues/28) |
| **Status** | `[Prioritized]` |
| **Tipo** | task |
| **Título** | `#5 feat(database): model users, oauth_accounts, revoked_tokens` |
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
| **Ordem** | #6 |
| **GitHub** | [#29](https://github.com/RodrigoVieira06/lootprice/issues/29) |
| **Status** | `[Prioritized]` |
| **Tipo** | task |
| **Título** | `#6 feat(database): model crawler_runs` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04, ISSUE-24 |
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
| **Ordem** | #7 |
| **GitHub** | [#30](https://github.com/RodrigoVieira06/lootprice/issues/30) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#7 feat(auth): autenticação JWT local — login e registro` |
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
| **Ordem** | #8 |
| **GitHub** | [#31](https://github.com/RodrigoVieira06/lootprice/issues/31) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#8 feat(auth): refresh token e logout com revogação` |
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

### ISSUE-09: RBAC — roles user e admin

| Campo | Valor |
|---|---|
| **Ordem** | #9 |
| **GitHub** | [#34](https://github.com/RodrigoVieira06/lootprice/issues/34) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#9 feat(auth): RBAC com roles user e admin` |
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

### ISSUE-10: Normalização de nomes e geração de slugs

| Campo | Valor |
|---|---|
| **Ordem** | #10 |
| **GitHub** | [#35](https://github.com/RodrigoVieira06/lootprice/issues/35) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#10 feat(crawler): normalização de nomes e geração de slugs` |
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

### ISSUE-11: Crawler Steam API

| Campo | Valor |
|---|---|
| **Ordem** | #11 |
| **GitHub** | [#36](https://github.com/RodrigoVieira06/lootprice/issues/36) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#11 feat(crawler): implementar crawler Steam via API pública` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04, ISSUE-10 |
| **Estimativa** | L |

**Descrição:**
Crawler que consulta a API pública da Steam e retorna dados no formato `RawGameData`.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/steam.py` herda de `BaseCrawler`
- [ ] `store_slug = "steam"`
- [ ] Usa HTTPX async e fonte/API permitida documentada em `docs/affiliate_store_strategy.md`
- [ ] Steam não é tratada como fonte principal de monetização afiliada sem validação formal
- [ ] Retorna `RawGameData` validado via Pydantic
- [ ] Retorna `store_url` limpa; não depende de link afiliado hardcoded
- [ ] `try/except` com logging em todo I/O
- [ ] Testes com mock da API Steam

---

### ISSUE-12: Crawler Nuuvem (scraper)

| Campo | Valor |
|---|---|
| **Ordem** | #12 |
| **GitHub** | [#37](https://github.com/RodrigoVieira06/lootprice/issues/37) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#12 feat(crawler): implementar scraper Nuuvem` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04, ISSUE-10 |
| **Estimativa** | XL |

**Descrição:**
Scraper que coleta dados da Nuuvem via HTTPX + BeautifulSoup4.

> **Atenção:** antes de implementar scraping real, validar termos/programa de afiliados. Se houver feed/API oficial, preferir feed/API ao scraper.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/nuuvem.py` herda de `BaseCrawler`
- [ ] `store_slug = "nuuvem"`
- [ ] Decisão de fonte registrada: `feed`, `api`, `scraper`, `manual` ou `disabled`
- [ ] Se `scraper`, `stores.allows_scraping = true` e `compliance_status = approved`
- [ ] HTTPX async + BeautifulSoup4 para parsing apenas se scraping for permitido
- [ ] Retorna `RawGameData` validado
- [ ] Retorna `store_url` limpa; geração de afiliado fica no redirect interno
- [ ] `try/except` + logging
- [ ] Respeita rate limiting (delay entre requests)
- [ ] Testes com HTML mockado

---

### ISSUE-13: Crawler runner (orquestrador)

| Campo | Valor |
|---|---|
| **Ordem** | #13 |
| **GitHub** | [#38](https://github.com/RodrigoVieira06/lootprice/issues/38) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#13 feat(crawler): implementar runner orquestrador de crawlers` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-11, ISSUE-12, ISSUE-06 |
| **Estimativa** | L |

**Descrição:**
Orquestrador que roda todos os crawlers, faz upsert no banco e registra `crawler_runs`.

**Critérios de Aceitação:**
- [ ] `backend/app/crawlers/runner.py`
- [ ] Registra crawlers ativos
- [ ] Ignora lojas `disabled`, sem `compliance_status = approved` ou sem permissão para a fonte configurada
- [ ] Para cada crawler: executa `fetch()`, normaliza, upsert em `games`, `store_products`, `prices`
- [ ] Registra `crawler_runs` com status, contadores e erros
- [ ] Falha em um crawler não para os demais
- [ ] `make crawl` no Makefile
- [ ] Testes de integração

---

## E5 — API REST

### ISSUE-14: Endpoints públicos — busca, listagem e detalhe

| Campo | Valor |
|---|---|
| **Ordem** | #14 |
| **GitHub** | [#39](https://github.com/RodrigoVieira06/lootprice/issues/39) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#14 feat(api): endpoints públicos — busca, listagem e detalhe de jogos` |
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
- [ ] Responses filtram lojas sem `compliance_status = approved`, `allows_price_display = true` ou `is_active = true`
- [ ] Responses de preço retornam `outbound_url` interno; não expõem `affiliate_url` externa como link primário
- [ ] Schemas de response: `GameRead`, `GameWithPrices`, `PriceRead`
- [ ] `backend/app/api/v1/router.py` agrega rotas
- [ ] Testes de integração para cada endpoint

---

### ISSUE-15: Endpoints admin

| Campo | Valor |
|---|---|
| **Ordem** | #15 |
| **GitHub** | [#40](https://github.com/RodrigoVieira06/lootprice/issues/40) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#15 feat(api): endpoints de administração` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-09, ISSUE-13, ISSUE-14 |
| **Estimativa** | M |

**Descrição:**
Endpoints protegidos por RBAC para administração.

**Critérios de Aceitação:**
- [ ] `POST /api/v1/admin/crawl` — força execução dos crawlers (role admin)
- [ ] `GET /api/v1/admin/stores` — lista lojas
- [ ] `PATCH /api/v1/admin/stores/{id}` — ativa/desativa loja
- [ ] Admin consegue visualizar e editar campos de compliance/ingestão de loja quando autorizados
- [ ] `PATCH /api/v1/admin/games/{id}` — edita `canonical_name`
- [ ] Todas as rotas protegidas com `require_admin`
- [ ] Testes com user normal (403) e admin (200)

---

## E6 — Segurança & Rate Limiting

### ISSUE-16: Rate limiting com slowapi

| Campo | Valor |
|---|---|
| **Ordem** | #16 |
| **GitHub** | [#41](https://github.com/RodrigoVieira06/lootprice/issues/41) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#16 feat(security): rate limiting com slowapi` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-14 |
| **Estimativa** | M |

**Descrição:**
Configurar throttling em rotas públicas com `get_real_ip()` para compatibilidade com Cloudflare.

**Critérios de Aceitação:**
- [ ] `backend/app/core/rate_limit.py` — limiter + `get_real_ip()` lendo `CF-Connecting-IP` via Nginx
- [ ] Rotas de busca e listagem limitadas (ex: 30/min)
- [ ] Rota de login limitada (ex: 5/min)
- [ ] Rota pública de outbound redirect limitada com política própria para evitar abuso de tracking
- [ ] Middleware configurado no `main.py`
- [ ] Testes verificam header `X-RateLimit-Remaining`

---

## E3 (continuação) — OAuth

### ISSUE-17: OAuth Google

| Campo | Valor |
|---|---|
| **Ordem** | #17 |
| **GitHub** | [#32](https://github.com/RodrigoVieira06/lootprice/issues/32) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#17 feat(auth): OAuth Google login` |
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

### ISSUE-18: OAuth Discord

| Campo | Valor |
|---|---|
| **Ordem** | #18 |
| **GitHub** | [#33](https://github.com/RodrigoVieira06/lootprice/issues/33) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#18 feat(auth): OAuth Discord login` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-17 |
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

## E7 — Frontend MVP

### ISSUE-19: Setup React SPA

| Campo | Valor |
|---|---|
| **Ordem** | #19 |
| **GitHub** | [#42](https://github.com/RodrigoVieira06/lootprice/issues/42) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#19 feat(frontend): setup React SPA com Vite + TSX + SCSS` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-14 (backend API disponível) |
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
| **Ordem** | #20 |
| **GitHub** | [#43](https://github.com/RodrigoVieira06/lootprice/issues/43) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#20 feat(frontend): página de busca e listagem de jogos` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-19, ISSUE-14 |
| **Estimativa** | L |

**Descrição:**
Página principal com barra de busca e grid de jogos com menor preço.

**Critérios de Aceitação:**
- [ ] Barra de busca com debounce
- [ ] Grid/lista de jogos com capa, título e menor preço
- [ ] Paginação ou scroll infinito
- [ ] Loading state e empty state
- [ ] Lista não exibe lojas/produtos sem permissão de preço retornados pela API
- [ ] Tipos já contemplam `outbound_url` e metadados de marketplace quando disponíveis
- [ ] Responsivo
- [ ] Service Axios para `/search` e `/games`
- [ ] Tipos TypeScript alinhados com schemas do backend

---

### ISSUE-21: Página de detalhe do jogo com comparação de preços

| Campo | Valor |
|---|---|
| **Ordem** | #21 |
| **GitHub** | [#44](https://github.com/RodrigoVieira06/lootprice/issues/44) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#21 feat(frontend): página de detalhe do jogo com comparação de preços` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1.5 - Frontend |
| **Dependências** | ISSUE-20 |
| **Estimativa** | L |

**Descrição:**
Página de detalhe mostrando todos os preços de todas as lojas, ordenados.

**Critérios de Aceitação:**
- [ ] Capa do jogo, título, canonical_name
- [ ] Lista de preços por loja: nome da loja, preço atual, preço original, % desconto
- [ ] Botão de compra usa `outbound_url` interno, nunca `affiliate_url` externa direta
- [ ] Sinaliza marketplace/risco/região quando a API fornecer esses metadados
- [ ] Estado visual para oferta bloqueada, indisponível ou sem permissão de redirect
- [ ] "Atualizado há X minutos" baseado em `scraped_at`
- [ ] Responsivo
- [ ] Service Axios para `/games/{slug}`

---

### ISSUE-22: Páginas de login e registro

| Campo | Valor |
|---|---|
| **Ordem** | #22 |
| **GitHub** | [#45](https://github.com/RodrigoVieira06/lootprice/issues/45) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#22 feat(frontend): páginas de login e registro` |
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
| **Ordem** | #23 |
| **GitHub** | [#46](https://github.com/RodrigoVieira06/lootprice/issues/46) |
| **Status** | `[Backlog]` ⚠️ bloqueado |
| **Tipo** | task |
| **Título** | `#23 chore(infra): Nginx + CF-Connecting-IP` |
| **Labels** | `type:chore`, `priority:low`, `blocked` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-16 |
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

## E9 — Afiliados & Store Compliance

### ISSUE-24: Estratégia de afiliados e matriz de lojas

| Campo | Valor |
|---|---|
| **Ordem** | #24 |
| **GitHub** | [#50](https://github.com/RodrigoVieira06/lootprice/issues/50) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#24 docs(affiliate): documentar estratégia de lojas, afiliados e riscos` |
| **Labels** | `type:docs`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | Nenhuma |
| **Estimativa** | M |

**Descrição:**
Manter documentação formal para decisão de lojas, fontes de ingestão, riscos de marketplaces, programas de afiliado e regras de tracking.

**Critérios de Aceitação:**
- [ ] `docs/affiliate_store_strategy.md` documenta princípios obrigatórios
- [ ] Matriz inicial cobre Steam, Epic, Xbox, Nintendo, PlayStation, Nuuvem, GMG, Fanatical, Humble, GOG, Eneba, G2A, Kinguin e itch.io
- [ ] Documento diferencia `api`, `feed`, `scraper`, `manual` e `disabled`
- [ ] Documento define que crawler não gera tracking comercial
- [ ] Documento define que frontend usa redirect interno
- [ ] Fontes oficiais/links de validação ficam listados no documento
- [ ] `AGENTS.md`, `README.md` e skills apontam para a estratégia

---

### ISSUE-25: Store policy e tracking de cliques no schema

| Campo | Valor |
|---|---|
| **Ordem** | #25 |
| **GitHub** | [#51](https://github.com/RodrigoVieira06/lootprice/issues/51) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#25 feat(database): adicionar store policy e affiliate_clicks` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-04 |
| **Estimativa** | L |

**Descrição:**
Adicionar campos de compliance/ingestão em `stores` e criar `affiliate_clicks` para registrar cliques antes do redirect.

**Critérios de Aceitação:**
- [ ] `stores` inclui `ingestion_source`, permissões de preço/deeplink/subid/scraping, `affiliate_network`, `affiliate_link_template`, `compliance_status`, `risk_level`, `terms_url`, `compliance_notes`
- [ ] `affiliate_clicks` criado conforme `docs/database_schema.md`
- [ ] `ip_hash` usa hash irreversível com salt de ambiente; IP bruto não é persistido
- [ ] Migration Alembic criada e testada
- [ ] Seeds de Steam/Nuuvem atualizados com `needs_review`
- [ ] Testes unitários cobrem defaults, constraints e índices

---

### ISSUE-26: Endpoint de outbound redirect afiliado

| Campo | Valor |
|---|---|
| **Ordem** | #26 |
| **GitHub** | [#52](https://github.com/RodrigoVieira06/lootprice/issues/52) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#26 feat(affiliate): endpoint de redirect e tracking de cliques` |
| **Labels** | `type:feat`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-14, ISSUE-16, ISSUE-25 |
| **Estimativa** | L |

**Descrição:**
Implementar `/api/v1/out/{price_id}` para registrar clique, montar link afiliado por loja e redirecionar com segurança.

**Critérios de Aceitação:**
- [ ] `GET /api/v1/out/{price_id}` valida loja, produto, preço e permissões
- [ ] Gera `click_id` único e registra `affiliate_clicks`
- [ ] Aplica `subid`/`click_id` apenas quando `allows_tracking_subid = true`
- [ ] Usa `affiliate_link_template` sem hardcoded de credenciais
- [ ] Responde 302 para destino válido
- [ ] Responde erro controlado para loja bloqueada, preço indisponível ou compliance pendente
- [ ] Rota tem rate limit
- [ ] Testes cobrem sucesso, bloqueios e loja sem tracking

---

### ISSUE-27: Admin de compliance e fontes de loja

| Campo | Valor |
|---|---|
| **Ordem** | #27 |
| **GitHub** | [#53](https://github.com/RodrigoVieira06/lootprice/issues/53) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#27 feat(admin): gerenciar compliance e fonte de lojas` |
| **Labels** | `type:feat`, `priority:medium` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-09, ISSUE-15, ISSUE-25 |
| **Estimativa** | M |

**Descrição:**
Permitir que admin veja e atualize o estado de compliance, fonte de ingestão e flags de afiliado das lojas.

**Critérios de Aceitação:**
- [ ] `GET /admin/stores` retorna campos de compliance e risco
- [ ] `PATCH /admin/stores/{id}` permite alterar `ingestion_source`, permissões, status, risco e notas
- [ ] Campos sensíveis de template afiliado não são expostos sem necessidade
- [ ] Validação impede `scraper` aprovado sem `allows_scraping = true`
- [ ] Testes cobrem admin, user normal e validações

---

### ISSUE-28: Pesquisa formal de programas de afiliado por loja

| Campo | Valor |
|---|---|
| **Ordem** | #28 |
| **GitHub** | [#54](https://github.com/RodrigoVieira06/lootprice/issues/54) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#28 docs(affiliate): validar termos e programas por loja` |
| **Labels** | `type:docs`, `priority:high` |
| **Milestone** | Fase 1 - MVP Backend |
| **Dependências** | ISSUE-24 |
| **Estimativa** | L |

**Descrição:**
Pesquisar e registrar termos oficiais, programa de afiliado, disponibilidade de feed/API e restrições para as lojas candidatas.

**Critérios de Aceitação:**
- [ ] Nuuvem validada quanto a afiliado, scraping, feed/API e deep link
- [ ] Steam validada quanto a API de preço/catálogo e uso comercial
- [ ] Green Man Gaming e Fanatical validadas como candidatas de lojas autorizadas
- [ ] GOG e Humble validadas para segunda onda
- [ ] Eneba, G2A e Kinguin avaliadas com riscos de marketplace
- [ ] Resultado de cada loja registrado em `docs/affiliate_store_strategy.md`
- [ ] Lojas sem validação permanecem `needs_review` ou `disabled`

---

### ISSUE-29: Conversões de afiliado via postback/API/CSV

| Campo | Valor |
|---|---|
| **Ordem** | #29 |
| **GitHub** | [#55](https://github.com/RodrigoVieira06/lootprice/issues/55) |
| **Status** | `[Backlog]` |
| **Tipo** | task |
| **Título** | `#29 feat(affiliate): importar conversões e comissões` |
| **Labels** | `type:feat`, `priority:low` |
| **Milestone** | Fase 2 - Expansão |
| **Dependências** | ISSUE-26, ISSUE-28 |
| **Estimativa** | XL |

**Descrição:**
Implementar reconciliação de conversões e comissões quando as redes/lojas oferecerem postback, API ou relatório CSV.

**Critérios de Aceitação:**
- [ ] Schema `affiliate_conversions` definido em migration futura
- [ ] Importador por rede/parceiro isolado por módulo
- [ ] Conversões vinculam `click_id` quando disponível
- [ ] Relatórios agregam cliques, conversões, comissão e taxa de aprovação
- [ ] Nenhuma credencial de rede fica hardcoded

---

## Grafo de Dependências

```
ISSUE-01 (#1) — setup
  ├── ISSUE-02 (#2) — CI
  ├── ISSUE-03 (#3) — PostgreSQL + Alembic
  │     ├── ISSUE-04 (#4) — models lojas/jogos
  │     │     ├── ISSUE-06 (#6) — crawler_runs
  │     │     ├── ISSUE-10 (#10) — normalização
  │     │     │     ├── ISSUE-11 (#11) — Steam crawler
  │     │     │     └── ISSUE-12 (#12) — Nuuvem crawler
  │     │     │           └── ISSUE-13 (#13) — runner ← depende de 11, 12, 06
  │     │     └── ISSUE-14 (#14) — API pública
  │     │           ├── ISSUE-15 (#15) — API admin ← depende de 09, 13, 14
  │     │           ├── ISSUE-16 (#16) — rate limiting
  │     │           │     └── ISSUE-23 (#23) — Nginx ← bloqueado
  │     │           ├── ISSUE-25 (#25) — store policy + affiliate_clicks
  │     │           │     └── ISSUE-26 (#26) — outbound redirect
  │     │           │           └── ISSUE-29 (#29) — conversões ← Fase 2
  │     │           ├── ISSUE-27 (#27) — admin compliance
  │     │           └── ISSUE-19 (#19) — frontend setup ← Fase 1.5
  │     │                 ├── ISSUE-20 (#20) — busca
  │     │                 │     └── ISSUE-21 (#21) — detalhe
  │     │                 └── ISSUE-22 (#22) — login/registro
  │     └── ISSUE-05 (#5) — models users
  │           ├── ISSUE-07 (#7) — JWT local
  │           │     ├── ISSUE-08 (#8) — refresh/logout
  │           │     ├── ISSUE-09 (#9) — RBAC
  │           │     └── ISSUE-17 (#17) — OAuth Google
  │           │           └── ISSUE-18 (#18) — OAuth Discord
  │           └── ISSUE-17 (#17) — OAuth Google ← depende de 05 e 07
ISSUE-24 (#24) — estratégia afiliados
  ├── ISSUE-25 (#25) — store policy + affiliate_clicks
  └── ISSUE-28 (#28) — pesquisa formal por loja
```

---

## Ordem de Execução

Sequência respeitando dependências e prioridades:

| Ordem | ISSUE | GitHub | Status |
|---|---|---|---|
| #1 | Setup monorepo | [#24](https://github.com/RodrigoVieira06/lootprice/issues/24) | ✅ **Done** |
| #2 | CI | [#25](https://github.com/RodrigoVieira06/lootprice/issues/25) | 🔄 **Code Review** |
| #3 | PostgreSQL + Alembic | [#26](https://github.com/RodrigoVieira06/lootprice/issues/26) | ⏳ **Prioritized** |
| #4 | Models lojas/jogos | [#27](https://github.com/RodrigoVieira06/lootprice/issues/27) | 📋 Backlog |
| #5 | Models users | [#28](https://github.com/RodrigoVieira06/lootprice/issues/28) | 📋 Backlog |
| #6 | Model crawler_runs | [#29](https://github.com/RodrigoVieira06/lootprice/issues/29) | 📋 Backlog |
| #7 | JWT local | [#30](https://github.com/RodrigoVieira06/lootprice/issues/30) | 📋 Backlog |
| #8 | Refresh/logout | [#31](https://github.com/RodrigoVieira06/lootprice/issues/31) | 📋 Backlog |
| #9 | RBAC | [#34](https://github.com/RodrigoVieira06/lootprice/issues/34) | 📋 Backlog |
| #10 | Normalização | [#35](https://github.com/RodrigoVieira06/lootprice/issues/35) | 📋 Backlog |
| #11 | Steam crawler | [#36](https://github.com/RodrigoVieira06/lootprice/issues/36) | 📋 Backlog |
| #12 | Nuuvem crawler | [#37](https://github.com/RodrigoVieira06/lootprice/issues/37) | 📋 Backlog |
| #13 | Runner | [#38](https://github.com/RodrigoVieira06/lootprice/issues/38) | 📋 Backlog |
| #14 | API pública | [#39](https://github.com/RodrigoVieira06/lootprice/issues/39) | 📋 Backlog |
| #15 | API admin | [#40](https://github.com/RodrigoVieira06/lootprice/issues/40) | 📋 Backlog |
| #16 | Rate limiting | [#41](https://github.com/RodrigoVieira06/lootprice/issues/41) | 📋 Backlog |
| #17 | OAuth Google | [#32](https://github.com/RodrigoVieira06/lootprice/issues/32) | 📋 Backlog |
| #18 | OAuth Discord | [#33](https://github.com/RodrigoVieira06/lootprice/issues/33) | 📋 Backlog |
| #19 | Frontend setup (Fase 1.5) | [#42](https://github.com/RodrigoVieira06/lootprice/issues/42) | 📋 Backlog |
| #20 | Busca | [#43](https://github.com/RodrigoVieira06/lootprice/issues/43) | 📋 Backlog |
| #21 | Detalhe | [#44](https://github.com/RodrigoVieira06/lootprice/issues/44) | 📋 Backlog |
| #22 | Login/registro | [#45](https://github.com/RodrigoVieira06/lootprice/issues/45) | 📋 Backlog |
| #23 | Nginx ⚠️ bloqueado | [#46](https://github.com/RodrigoVieira06/lootprice/issues/46) | 📋 Backlog |
| #24 | Estratégia afiliados | [#50](https://github.com/RodrigoVieira06/lootprice/issues/50) | ⏳ Prioritized |
| #25 | Store policy + affiliate_clicks | [#51](https://github.com/RodrigoVieira06/lootprice/issues/51) | ⏳ Prioritized |
| #26 | Outbound redirect | A criar | 📋 Backlog |
| #27 | Admin compliance | A criar | 📋 Backlog |
| #28 | Pesquisa formal por loja | [#54](https://github.com/RodrigoVieira06/lootprice/issues/54) | ⏳ Prioritized |
| #29 | Conversões afiliado | A criar | 📋 Backlog / Fase 2 |

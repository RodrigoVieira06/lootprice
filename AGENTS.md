# LootPrice — Contexto Unificado para IA

> **Versão:** 0.3.2-MVP
> **Status:** Desenvolvimento Ativo
> **Última atualização:** 2026-06-27
> **Audiência:** LLMs de apoio (Antigravity IDE, Claude Code, Gemini CLI, Cursor, Copilot)
> **Documentação humana:** `README.md`

> **Instrução para LLMs:** Este é o arquivo de contexto primário do projeto LootPrice.
> Leia-o inteiro antes de agir. Seja **direto ao ponto** em todas as respostas — evite explicações desnecessárias e foque em ação.
> Em caso de conflito entre este documento e o código real do repositório, **o código real prevalece** — sinalize a inconsistência antes de agir.

---

## Índice

1. [Visão Geral do Produto](#1-visão-geral-do-produto)
2. [Stack Tecnológica](#2-stack-tecnológica)
3. [Estrutura do Repositório](#3-estrutura-do-repositório)
4. [Modelagem de Dados](#4-modelagem-de-dados)
5. [API REST — Contratos](#5-api-rest--contratos)
6. [Autenticação e Autorização](#6-autenticação-e-autorização)
7. [Crawler Engine](#7-crawler-engine)
8. [Build, Test e Development Commands](#8-build-test-e-development-commands)
9. [Coding Style & Naming Conventions](#9-coding-style--naming-conventions)
10. [Testing Guidelines](#10-testing-guidelines)
11. [Commit, Branch & PR Guidelines](#11-commit-branch--pr-guidelines)
12. [Workflow de Desenvolvimento com IA](#12-workflow-de-desenvolvimento-com-ia)
13. [Git Workflow Obrigatório](#13-git-workflow-obrigatório)
14. [CI/CD e Qualidade de Código](#14-cicd-e-qualidade-de-código)
15. [Estado do Projeto](#15-estado-do-projeto)
16. [Roadmap Faseado](#16-roadmap-faseado)
17. [Riscos e Débitos Técnicos](#17-riscos-e-débitos-técnicos)
18. [Glossário](#18-glossário)
19. [Regras para Agentes](#19-regras-para-agentes)

---

## 1. Visão Geral do Produto

**LootPrice** é um agregador e comparador de preços de chaves de jogos digitais. O sistema coleta dados por API, feed, scraper permitido ou cadastro manual, normaliza os dados e expõe uma interface onde o usuário final encontra onde o jogo está mais barato.

A monetização por afiliados é feita por redirect interno com métricas de clique. Programa de afiliados não substitui crawler/feed/API; ele resolve atribuição comercial do clique.

### Proposta de Valor

```
Usuário busca jogo → LootPrice consulta N lojas permitidas → Resultado: lista ordenada do menor ao maior preço → Clique medido via redirect afiliado
```

### Personas

| Persona | Necessidade |
|---|---|
| Gamer casual | Encontrar o menor preço rapidamente |
| Gamer frequente | Acompanhar variação de preço ao longo do tempo (Fase 3) |
| Admin do sistema | Gerenciar lojas cadastradas, forçar re-scraping, monitorar saúde dos crawlers |

### Escopo do MVP

**Em Escopo:**

| Área | Entregável |
|---|---|
| Alvo | Jogos de PC apenas |
| Lojas Fase 1 | Nuuvem (scraper) e Steam (API pública) |
| Atualização | Manual via CLI ou agendamento local (Makefile) |
| Auth | JWT + Login Social (Google, Discord) + Login Local |
| Perfis | RBAC com roles `user` e `admin` |
| Backend | API REST: busca, listagem, comparação de preços, gestão de usuários |
| Frontend | SPA: busca de jogos, comparação de preços, autenticação |
| Afiliados | Store compliance, outbound redirect, métricas de clique |
| Tooling | Conventional Commits, Lefthook, Ruff, Pytest, Alembic |

**Fora de Escopo (Fases Futuras):** Wishlist, alertas de preço, histórico de preços, conversões de afiliado, apps Android/iOS, G2A/Eneba/Kinguin, consoles, customização avançada.

---

## 2. Stack Tecnológica

### Backend & Crawler

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Linguagem | Python 3.11+ | Maturidade no ecossistema de scraping |
| Framework Web | FastAPI | Performance, tipagem nativa, OpenAPI automático |
| ORM | SQLModel + Alembic | SQLModel para modelos, Alembic para migrations |
| Validação | Pydantic v2 | Incluso no SQLModel |
| Scraping | HTTPX (async) + BeautifulSoup4 | Requests assíncronas + parsing HTML |
| Linter/Formatter | Ruff | Substitui Black + isort + Flake8 |
| Testes | Pytest + pytest-asyncio + httpx | Unitários e integração |
| Autenticação | python-jose + passlib | JWT com bcrypt |
| Rate Limiting | slowapi | Throttling para FastAPI |
| Ambiente | Ubuntu nativo via SSH | Máquina própria (i7 10ª, 8GB RAM) |

> **⚠️ `python-jose`:** Monitorar atividade. Se inativa por 6+ meses, migrar para `PyJWT` + `authlib`.

### Banco de Dados & Infraestrutura

| Camada | Tecnologia |
|---|---|
| Banco de Dados | PostgreSQL 15+ |
| Container | Docker + Docker Compose |
| Migrations | Alembic |
| Proxy Reverso | Nginx |
| Acesso SSH | Tailscale |
| Exposição pública | Cloudflare Tunnel |

> **Gotcha — Cloudflare + slowapi:** `slowapi` precisa de `get_real_ip()` lendo `X-Forwarded-For` (reescrito pelo Nginx a partir de `CF-Connecting-IP`).

### Frontend

| Camada | Tecnologia |
|---|---|
| Framework | React mais recente (TypeScript/TSX) |
| Build | Vite.js |
| Estilo | SCSS |
| HTTP Client | Axios |
| Validação | React Hook Form + Zod |
| State Management | Zustand |
| Lint/Format | Biome |
| Testes | Jest |
| Pacotes | pnpm |
| Mobile futuro | SPA mobile-ready; React Native + Expo preferencial se mobile nativo virar prioridade; Tauri/Capacitor a avaliar |

### Tooling & DevOps

| Ferramenta | Finalidade |
|---|---|
| Makefile | Atalhos: `make install`, `make dev`, `make test`, `make lint`, `make format` |
| Lefthook | Git hooks: lint + commit message no pre-commit |
| GitHub Actions | CI: lint, testes, build a cada push/PR |
| GitHub Issues | Gestão de backlog e tarefas — use `gh` para escrita e MCP GitHub para leitura estruturada |

---

## 3. Estrutura do Repositório

> Esta é a estrutura-alvo do MVP. Para o estado real, verifique a árvore do repositório.

```
lootprice/                          # Raiz do Monorepo
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml                  # Lint + Testes em cada Push/PR
│   └── PULL_REQUEST_TEMPLATE.md    # Template para PRs
│
├── ai/
│   ├── README.md                   # Índice das ferramentas de IA
│   ├── lootprice-backend-developer/
│   │   └── SKILL.md                # Skill: backend sênior LootPrice
│   ├── lootprice-frontend-developer/
│   │   └── SKILL.md                # Skill: frontend sênior LootPrice
│   ├── lootprice-reviewer/
│   │   ├── SKILL.md                # Skill: revisor de código LootPrice
│   │   └── resources/
│   │       ├── checklist.md        # Checklist de conformidade
│   │       └── review_format.md    # Formato do review
│   └── scrum-master/
│       └── SKILL.md                # Skill: scrum master LootPrice
│
├── docs/
│   ├── database_schema.md          # Modelagem detalhada do banco
│   ├── affiliate_store_strategy.md # Estratégia de lojas, afiliados e riscos
│   ├── frontend_mobile_strategy.md # Regras para SPA mobile-ready e fase Android/iOS
│   └── issues_mvp.md              # Issues detalhadas para o MVP
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── games.py        # GET /games, GET /games/{slug}
│   │   │   │   ├── search.py       # GET /search?q=
│   │   │   │   ├── auth.py         # POST /auth/login, /register, /refresh, /logout
│   │   │   │   └── admin.py        # POST /admin/crawl, PATCH /admin/games, /stores
│   │   │   └── router.py           # Agregador de rotas
│   │   │
│   │   ├── core/
│   │   │   ├── config.py           # Settings via pydantic-settings (.env)
│   │   │   ├── database.py         # Engine e sessão do SQLModel
│   │   │   ├── security.py         # JWT encode/decode, hash de senha
│   │   │   ├── rate_limit.py       # slowapi limiter + get_real_ip()
│   │   │   └── dependencies.py     # get_current_user, require_admin
│   │   │
│   │   ├── models/                 # Tabelas do banco (SQLModel Table=True)
│   │   │   ├── game.py
│   │   │   ├── price.py
│   │   │   ├── store.py
│   │   │   ├── user.py
│   │   │   └── revoked_token.py
│   │   │
│   │   ├── schemas/                # DTOs Pydantic (sem Table=True)
│   │   │   ├── game.py
│   │   │   ├── price.py
│   │   │   └── auth.py
│   │   │
│   │   └── crawlers/
│   │       ├── base.py             # Classe abstrata BaseCrawler
│   │       ├── nuuvem.py
│   │       ├── steam.py
│   │       └── runner.py           # Orquestra todos os crawlers
│   │
│   ├── migrations/                 # Alembic migrations
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── tests/
│   │   ├── test_api/
│   │   ├── test_crawlers/
│   │   ├── test_core/
│   │   └── conftest.py
│   │
│   ├── .env.example
│   ├── main.py
│   ├── requirements.txt
│   └── ruff.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── platform/               # Adapters: outbound, storage, auth redirect, browser APIs
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   ├── .env.example
│   ├── vite.config.ts
│   └── package.json
│
├── nginx/
│   ├── nginx.conf
│   └── sites/
│       └── lootprice.conf
│
├── docker-compose.yml
├── Makefile
├── lefthook.yml
├── AGENTS.md                       # Este arquivo (contexto IA)
├── .gitignore
└── README.md                       # Documentação para humanos
```

---

## 4. Modelagem de Dados

> Documento completo: `docs/database_schema.md`

### Diagrama Entidade-Relacionamento (Simplificado)

```
users ──(1:N)── oauth_accounts
stores ──(1:N)── store_products ──(1:1)── prices
games  ──(1:N)── store_products
stores ──(1:N)── crawler_runs
prices ──(1:N)── affiliate_clicks
```

### Decisões de Design

- `canonical_name` editável pelo admin para corrigir falsos negativos
- `store_products` separa jogo canônico do produto específico de cada loja
- `stores` registra fonte permitida: `api`, `feed`, `scraper`, `manual` ou `disabled`
- `prices` guarda apenas o **preço atual** no MVP. Histórico na Fase 3
- `affiliate_clicks` registra cliques antes do redirect externo
- Frontend usa `outbound_url` interno; não expõe URL afiliada externa como link primário
- `price_brl` em `NUMERIC(10,2)`, nunca `FLOAT`
- `scraped_at` permite exibir "Atualizado há X minutos"
- `revoked_tokens` usa campo `jti` para blacklist eficiente sem Redis

---

## 5. API REST — Contratos

> Todos os endpoints prefixados com `/api/v1/`. Docs em `/docs` (Swagger) e `/redoc`.

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/search?q={query}` | Não | Busca jogos por nome |
| GET | `/games` | Não | Lista jogos com paginação |
| GET | `/games/{slug}` | Não | Detalhe com todos os preços |
| GET | `/prices?game_id={id}` | Não | Preços de um jogo específico |
| GET | `/out/{price_id}` | Não | Registra clique afiliado e redireciona para a loja |
| POST | `/auth/register` | Não | Cadastro local |
| POST | `/auth/login` | Não | Login local — retorna JWT |
| POST | `/auth/refresh` | JWT | Renova access token |
| POST | `/auth/logout` | JWT | Revoga refresh token |
| GET | `/auth/me` | JWT | Dados do usuário autenticado |
| GET | `/auth/google` | Não | Inicia OAuth Google |
| GET | `/auth/discord` | Não | Inicia OAuth Discord |
| POST | `/admin/crawl` | JWT (admin) | Força execução dos crawlers |
| GET | `/admin/stores` | JWT (admin) | Lista lojas |
| PATCH | `/admin/stores/{id}` | JWT (admin) | Ativa/desativa loja e gerencia compliance/fonte |
| PATCH | `/admin/games/{id}` | JWT (admin) | Edita canonical_name |

**Regra de afiliado:** endpoints públicos devem filtrar lojas sem `compliance_status = approved`, sem `allows_price_display` ou inativas. O frontend usa `outbound_url`; `affiliate_url` externa não deve ser o link primário.

### Exemplo — `GET /games/{slug}`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Cyberpunk 2077™",
  "canonical_name": "cyberpunk 2077",
  "slug": "cyberpunk-2077",
  "cover_url": "https://...",
  "prices": [
    {
      "store": "Nuuvem",
      "price_brl": 49.90,
      "original_price_brl": 199.90,
      "discount_percent": 75,
      "outbound_url": "/api/v1/out/550e8400-e29b-41d4-a716-446655440001",
      "is_marketplace": false,
      "is_available": true,
      "scraped_at": "2026-05-31T14:00:00Z"
    }
  ]
}
```

---

## 6. Autenticação e Autorização

### Fluxo JWT (Login Local)

```
POST /auth/login {email, password}
  → Verifica hash (passlib/bcrypt)
  → Gera access_token (30min) + refresh_token (7 dias, com jti)
  → Retorna {access_token, refresh_token, token_type: "bearer"}
```

### Logout / Revogação

```
POST /auth/logout {Authorization: Bearer <refresh_token>}
  → Decodifica → extrai jti
  → INSERT INTO revoked_tokens (token_jti, expires_at)
  → 200 {message: "Logged out successfully"}
```

### OAuth (Google / Discord)

```
GET /auth/google → Redirect provider → Callback → Upsert user + oauth_accounts → JWT
```

### RBAC

| Role | Permissões |
|---|---|
| `user` | Buscar jogos, visualizar preços, gerenciar perfil |
| `admin` | Tudo do `user` + crawl, gerenciar lojas, editar games |

### Variáveis de Ambiente Obrigatórias

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/lootprice
SECRET_KEY=<openssl rand -hex 32>
IP_HASH_SALT=<openssl rand -hex 32>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 7. Crawler Engine

### Classe Base

```python
class RawGameData(BaseModel):
    title: str
    external_id: str | None = None
    store_url: str                   # URL limpa/canônica do produto
    price_brl: Decimal              # Nunca float
    original_price_brl: Decimal | None = None
    affiliate_url: str | None = None # Legado/opcional; preferir redirect interno
    is_available: bool = True
    store_slug: str

class BaseCrawler(ABC):
    store_slug: str
    @abstractmethod
    async def fetch(self) -> AsyncGenerator[RawGameData, None]: ...
```

### Adicionando um Novo Crawler

1. Ler `docs/affiliate_store_strategy.md`
2. Validar e registrar fonte da loja: `api`, `feed`, `scraper`, `manual` ou `disabled`
3. Criar `backend/app/crawlers/{loja}.py` apenas se `scraper` for permitido
4. Herdar de `BaseCrawler`, definir `store_slug`
5. Implementar `fetch()` com HTTPX async + `RawGameData`
6. Registrar no `runner.py`
7. Escrever teste em `tests/test_crawlers/test_{loja}.py`

**Regra:** se termos não permitirem scraping, use feed/API/importador ou deixe a loja como `disabled`. Crawler não gera tracking comercial; tracking acontece no endpoint `/api/v1/out/{price_id}`.

### Critérios de Saúde

- Exceção em `fetch()` → runner loga e continua
- 0 resultados em 2 execuções → log `WARNING`
- `scraped_at` atualizado apenas em coleta bem-sucedida

---

## 8. Build, Test e Development Commands

```bash
make install   # Cria .venv, instala requirements.txt, instala Lefthook
make dev       # Docker Compose up + uvicorn --reload
make db-up     # Sobe apenas o PostgreSQL via Docker Compose
make migrate   # Executa migrations Alembic
make test      # Pytest do backend
make lint      # ruff check .
make format    # ruff format .
```

Copie `backend/.env.example` para `backend/.env` antes de rodar. Secrets ficam em `.env`, nunca no código.

---

## 9. Coding Style & Naming Conventions

- Python 3.11+ com FastAPI.
- `async`/`await` em rotas e I/O.
- Type hints em todos os parâmetros e retornos.
- `logging` padrão — nunca `print()` em produção.
- Ruff: 88 caracteres, aspas duplas, espaços, import sorting.
- `NUMERIC(10,2)` / `Decimal` para dinheiro — nunca `float`.
- Mudanças de schema exigem migration Alembic.

---

## 10. Testing Guidelines

- Pytest para unitários e integração.
- Testes em `backend/tests/test_<feature>.py`.
- `make test` antes de abrir PR.
- Testes obrigatórios para nova funcionalidade, crawler, rota ou bug fix.

---

## 11. Commit, Branch & PR Guidelines

### Conventional Commits (obrigatório)

```
feat(crawler): adiciona suporte ao scraper da Nuuvem
fix(auth): corrige expiração do refresh token
docs(schema): atualiza modelagem da tabela prices
chore(deps): atualiza FastAPI para 0.115
```

### Branches (obrigatório)

**Nunca faça push direto na `master`.** Sempre crie uma branch nova:

```
feat/<descricao>      fix/<descricao>
chore/<descricao>     docs/<descricao>
refactor/<descricao>  test/<descricao>
```

### Pull Requests

- Use `.github/PULL_REQUEST_TEMPLATE.md`
- Vincule a issue com `Closes #XX` no body
- Nunca merge sem CI verde e review
- **Nunca interaja com PR fechado ou mergeado**

### Branch Protection Rules (GitHub — `master`)

- ✅ Require pull request before merging
- ✅ Require status checks: `CI — Lint & Tests / Backend (Python)`
- ✅ Dismiss stale reviews on new commits
- ✅ Block direct pushes

---

## 12. Workflow de Desenvolvimento com IA

### Visão Geral da Toolchain

```
┌──────────────────────────────────────────────────────────────┐
│                    DESENVOLVIMENTO LOCAL                      │
│                                                              │
│  Editor (Antigravity IDE / Cursor / VS Code)                 │
│   └── Claude MCP: autocompletar, refatorar, documentar       │
│                                                              │
│  Terminal                                                    │
│   └── make dev | make test | make lint | make format         │
└──────────────────────────────────────────────────────────────┘
              │  git push / open PR
              ▼
┌──────────────────────────────────────────────────────────────┐
│                       GITHUB                                 │
│                                                              │
│  MCP GitHub                                                  │
│   ├── Criar e gerenciar Issues (cards do projeto)            │
│   ├── Revisar PRs: analisa diff + comenta no PR              │
│   ├── Consultar histórico de commits                         │
│   └── Criar branches a partir de tarefas                     │
│                                                              │
│  GitHub Actions (CI)                                         │
│   ├── Lint (Ruff)                                            │
│   ├── Testes (Pytest)                                        │
│   └── Build/test (Frontend — futuro)                         │
│                                                              │
│  gh CLI                                                      │
│   ├── Escrita em issues/PRs quando MCP GitHub retornar 403   │
│   ├── Criar PRs e comentar reviews                           │
│   └── Consultar checks com gh pr checks                       │
└──────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│                 DESENVOLVIMENTO FRONTEND                     │
│                                                              │
│  MCP DevTools (Browser)                                     │
│   ├── Inspecionar elementos e estilos em tempo real          │
│   ├── Ler erros do console                                   │
│   └── Validar responsive layout via screenshot               │
└──────────────────────────────────────────────────────────────┘
```

### Gestão de Tarefas — GitHub Issues

Issues do GitHub são os "cards" do projeto. O status de cada issue é sinalizado por um **prefixo no título**:

| Prefixo | Significado |
|---|---|
| `[Backlog]` | Issue criada, aguardando priorização |
| `[Prioritized]` | Priorizada para o ciclo atual |
| `[Developing]` | Em desenvolvimento ativo |
| `[Code Review]` | PR aberto, aguardando review |
| `[QA]` | Em teste/validação |
| `[Deploying]` | Em processo de deploy |
| `[Done]` | Concluída e mergeada |

**Exemplo de título de issue:**
```
[Developing] feat(crawler): implementar scraper Nuuvem
```

Para mover uma issue de coluna, atualize o prefixo do título via `gh issue edit`.

### Regras de Uso de IA no Projeto

1. Todo código gerado por IA passa pelo CI — nenhuma exceção
2. Commits seguem Conventional Commits
3. LLMs usam este arquivo como contexto primário — mantenha-o atualizado
4. Revisões de PR por IA são complementares ao entendimento humano
5. Para operações de escrita no GitHub, use `gh` por padrão; MCP GitHub pode ser usado para leitura estruturada

---

## 13. Git Workflow Obrigatório

> **⚠️ Regra para IAs e desenvolvedores:** Todo código deve seguir estritamente o fluxo abaixo. Nenhum push é permitido diretamente na branch `master`.

```
1. Criar issue no GitHub (ou receber issue existente)
2. Atualizar título da issue para [Developing] via `gh issue edit`
3. Criar branch local: git checkout -b <prefixo>/<descricao>
4. Desenvolver e realizar commits convencionais incrementais
5. Realizar o push para a branch remota
6. Abrir Pull Request contra master (com "Closes #XX" no body)
7. Atualizar título da issue para [Code Review] via `gh issue edit`
8. Executar/Aguardar review (AI review + CI status checks)
9. Se aprovado, mergear o PR
10. Atualizar título da issue para [Done]
```

**Antes de interagir com qualquer PR:** verificar `state` e `merged` via `gh pr view <N> --json state,merged`. **Nunca** faça push, commit ou comente em PR com state `closed` ou `merged`.

---

## 14. CI/CD e Qualidade de Código

### Pipeline CI (`ci.yml`)

```yaml
on: [pull_request, push]
branches: [master]

jobs:
  backend:
    services:
      postgres: 15
    steps:
      - Checkout
      - Setup Python 3.11
      - pip install -r requirements.txt
      - ruff check .
      - ruff format --check .
      - pytest tests/ -v

  # frontend:
  #   Desabilitado; reativar quando frontend/package.json existir.
```

### AI Review via Skill

Review manual invocando `ai/reviewer/SKILL.md` com MCP GitHub:

```
PR aberto → IA invoca skill → Lê contexto + diff → Posta review no PR via `gh pr comment`
```

### Git Hooks (Lefthook)

```yaml
pre-commit:
  parallel: true
  commands:
    ruff-check:
      root: "backend/"
      glob: "*.py"
      run: ruff check {staged_files}
    ruff-format:
      root: "backend/"
      glob: "*.py"
      run: ruff format {staged_files}

commit-msg:
  commands:
    conventional-commit:
      run: shell regex para Conventional Commits
```

---

## 15. Estado do Projeto

### Metadados

| Campo | Valor |
|---|---|
| **Versão** | 0.3.2 |
| **Última atualização** | 2026-06-27 |
| **Fase atual** | Desenvolvimento — Arquitetura de afiliados, store compliance e models core |

### Estrutura de Arquivos Atual

```
lootprice/
├── .github/
│   ├── workflows/ci.yml              ✅
│   └── PULL_REQUEST_TEMPLATE.md      ✅
├── ai/
│   ├── README.md                     ✅
│   ├── lootprice-backend-developer/SKILL.md   ✅
│   ├── lootprice-frontend-developer/SKILL.md  ✅
│   ├── lootprice-reviewer/SKILL.md            ✅
│   └── lootprice-scrum-master/SKILL.md        ✅
├── docs/
│   ├── affiliate_store_strategy.md   ✅
│   ├── database_schema.md            ✅
│   ├── frontend_mobile_strategy.md   ✅
│   └── issues_mvp.md                 ✅
├── backend/
│   ├── app/
│   │   ├── core/config.py          ✅
│   │   ├── core/database.py        ✅
│   │   ├── models/store.py         ✅
│   │   ├── models/game.py          ✅
│   │   ├── models/store_product.py ✅
│   │   ├── models/price.py         ✅
│   │   ├── models/affiliate_click.py ✅
│   │   ├── models/user.py          ✅
│   │   ├── models/oauth_account.py ✅
│   │   ├── models/revoked_token.py ✅
│   │   ├── core/privacy.py         ✅
│   │   ├── schemas/user.py         ✅
│   │   ├── crawlers/normalizer.py ✅
│   │   └── api/, schemas/, crawlers/  ✅
│   ├── migrations/                 ✅
│   │   ├── env.py                  ✅
│   │   ├── versions/202606210001_create_postgresql_extensions.py ✅
│   │   ├── versions/202606220001_create_core_catalog_tables.py ✅
│   │   └── versions/202606270001_create_auth_tables.py ✅
│   │   └── versions/202606270002_add_store_policy_affiliate_clicks.py ✅
│   ├── tests/ (conftest.py, test_main.py, test_database.py, test_models.py, test_privacy.py, test_crawler_normalizer.py) ✅
│   ├── alembic.ini                 ✅
│   ├── .env.example                  ✅
│   ├── main.py                       ✅
│   ├── requirements.txt              ✅
│   └── ruff.toml                     ✅
├── frontend/.gitkeep                  ⏳ Placeholder
├── AGENTS.md                         ✅ Este arquivo
├── docker-compose.yml                ✅
├── Makefile                          ✅
├── lefthook.yml                      ✅
└── README.md                         ✅
```

### Decisões Tomadas

| Data | Decisão | Motivo |
|---|---|---|
| 2026-05 | Monorepo | 1 dev + LLM-assisted; contexto unificado |
| 2026-05 | Alembic obrigatório desde o dia 1 | Evitar debt de schema sem rastreamento |
| 2026-05 | `prices` como snapshot (sem histórico) | Simplicidade MVP |
| 2026-05 | `canonical_name` editável pelo admin | Normalização automática falha em edge cases |
| 2026-05 | `NUMERIC(10,2)` para preços | Precisão exata para dinheiro |
| 2026-05 | `slowapi` desde o MVP | API pública sem throttle é risco |
| 2026-06 | `revoked_tokens` no schema | Refresh tokens sem revogação são risco real |
| 2026-06 | Ubuntu físico como dev | Hardware superior a VPS nessa faixa |
| 2026-06 | Tailscale + Cloudflare Tunnel | SSH seguro sem IP fixo |
| 2026-06 | Manter `python-jose` no MVP | Trocar adiciona risco sem benefício imediato |
| 2026-06 | PostgreSQL bound em `127.0.0.1` | Segurança: não escuta em todos os IPs |
| 2026-06 | AI Review via Skill (não Actions) | Skill local tem contexto superior e usa `gh` para postar |
| 2026-06 | Stack frontend: SCSS + Biome + Jest + pnpm | Padronizar antes da criação frontend |
| 2026-06 | Schema separa `games`, `store_products`, `prices` | Evitar acoplamento jogo/loja |
| 2026-06 | Migração de Jira para GitHub Issues | Centralizar gestão no mesmo ecossistema |
| 2026-06 | Contexto IA unificado em `AGENTS.md` | Eliminar fragmentação entre 3 arquivos |
| 2026-06 | Alembic configurado em modo async | Compatível com `postgresql+asyncpg` e FastAPI async |
| 2026-06 | Makefile usa `docker compose` | Ambiente local usa Docker Compose v2 |
| 2026-06 | Models core de catálogo criados antes das rotas | `stores`, `games`, `store_products` e `prices` sustentam busca e comparação |
| 2026-06 | Skills usam `gh` para escrita no GitHub | Evitar bloqueios `403 Resource not accessible by integration` do MCP e reduzir retrabalho |
| 2026-06 | Programa de afiliados não substitui fonte de dados | Afiliado monetiza clique; API/feed/scraper/manual alimenta catálogo e preço |
| 2026-06 | Toda loja exige política de ingestão e compliance | Evitar crawler proibido por termos e reduzir risco de bloqueio/legal |
| 2026-06 | Cliques de compra passam por redirect interno | Permite métricas, `click_id/subid`, bloqueio de lojas inválidas e privacidade controlada |
| 2026-06 | Marketplaces de keys ficam fora do MVP inicial | G2A/Eneba/Kinguin exigem UX de risco, região, vendedor e reputação |
| 2026-06 | Frontend Fase 1.5 será web-first e mobile-ready | Preparar Android/iOS futuro sem adicionar stack mobile antes da fase mobile |
| 2026-06 | Mobile futuro comparará React Native + Expo, Tauri v2 e Capacitor | React Native + Expo é preferencial se mobile nativo virar prioridade; Tauri/Capacitor preservam mais reuso da SPA |
| 2026-06 | Models de autenticação criados em migration própria | `users`, `oauth_accounts` e `revoked_tokens` desbloqueiam JWT local, OAuth, RBAC e logout real |
| 2026-06 | Store policy e `affiliate_clicks` criados em migration própria | Flags de compliance/ingestão e métricas de clique sustentam redirect afiliado do MVP |

### Débitos Técnicos

| ID | Problema | Status |
|---|---|---|
| DT-01 | Limpeza periódica de `revoked_tokens` expirados | Aberto — Fase 2 |
| DT-02 | `python-jose` com manutenção irregular | Monitorar |
| DT-03 | Sem validação de IPs Cloudflare no `X-Forwarded-For` | Aberto |
| DT-04 | Nginx + CF-Connecting-IP bloqueado sem domínio | Bloqueado |
| DT-05 | Termos/afiliado das lojas ainda pendentes de validação formal | Aberto — antes de novos crawlers |
| DT-06 | Conversões de afiliado dependem de postback/API/CSV por parceiro | Aberto — Fase 2 |

---

## 16. Roadmap Faseado

### Fase 1 — MVP (Backend + Infra)

- Setup do repositório, Docker, Makefile, Lefthook
- Pipeline CI com GitHub Actions
- Models + migrations Alembic
- Fontes iniciais: Steam API + Nuuvem a validar entre feed/API/scraper
- Store compliance: `api`, `feed`, `scraper`, `manual`, `disabled`
- Normalização de nomes e slugs
- API REST: busca, listagem, detalhe, admin
- Outbound redirect afiliado + métricas de clique
- Autenticação: JWT local + Google + Discord + revogação
- RBAC: roles user/admin
- Rate limiting com slowapi

### Fase 1.5 — Frontend (MVP)

- Setup React SPA: Vite + TSX + SCSS + Zustand + Biome + Jest + pnpm
- Arquitetura mobile-ready: adapters em `src/platform/` para outbound, storage, auth redirect e APIs globais do browser
- Página de busca e listagem
- Páginas de login e registro
- Página de detalhe com comparação de preços e `outbound_url` interno
- Não adicionar React Native/Expo/Tauri/Capacitor/Rust/Android/iOS ao MVP sem issue e decisão registrada

### Fase 2 — Expansão

- Novas lojas autorizadas: GOG, Humble Bundle, Green Man Gaming, Fanatical após validação
- Admin panel
- Agendamento automático de crawlers
- Conversões de afiliado via postback/API/CSV quando disponível
- Wishlist e favoritos
- Limpeza de `revoked_tokens` (DT-01)

### Fase 2.5 — Mobile Apps (Android/iOS)

- Spike comparando React Native + Expo, Tauri v2 e Capacitor para Android/iOS
- Preferir React Native + Expo se o objetivo for UX mobile nativa, push notifications, storage seguro e evolução independente da web
- Considerar Tauri se desktop também for objetivo ou se reuso máximo da SPA for prioridade
- Considerar Capacitor se o objetivo for WebView mobile com menor custo operacional
- Compartilhar contratos e lógica entre SPA e app mobile quando fizer sentido: tipos TypeScript, schemas Zod, services de API, auth e outbound
- Implementar deep links para OAuth Google/Discord
- Implementar storage seguro para tokens
- Validar política de lojas, afiliados e privacidade para app stores
- Criar CI separado para builds Android/iOS

### Fase 3 — Features Avançadas

- Histórico de preços e gráficos
- Alertas de preço
- Suporte a consoles
- G2A/Eneba/Kinguin (experimental, com UX de marketplace)
- API pública com API Key

---

## 17. Riscos e Débitos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Crawler quebra por mudança de HTML | Alta | Alto | Health checks + testes de contrato + fallback |
| Termos não permitem scraping/comparação | Média | Crítico | Validar `docs/affiliate_store_strategy.md` antes de implementar loja |
| Afiliado sem `subid/click_id` | Média | Médio | Registrar clique interno e tratar conversão como não reconciliável |
| Marketplace com key problemática | Média | Alto | Adiar G2A/Eneba/Kinguin até UX de risco, região e vendedor |
| Normalização cria duplicatas | Média | Médio | `canonical_name` editável |
| Vazamento de credenciais | Baixa | Crítico | `.env` no gitignore, Secret Scanning |
| Bloqueio de IP por scraping | Média | Alto | Rate limiting, User-Agent rotation, robots.txt |
| Schema quebra sem migration | Média | Alto | Alembic obrigatório |
| Rate limiting ineficaz com Cloudflare | Média | Alto | `get_real_ip()` lê `CF-Connecting-IP` |

---

## 18. Glossário

| Termo | Definição |
|---|---|
| **Canonical Name** | Nome normalizado de um jogo para deduplicação |
| **Crawler** | Script que extrai dados de lojas externas |
| **DTO** | Schema Pydantic sem `Table=True` para I/O da API |
| **Feed** | Arquivo/API oficial de produtos fornecido por loja ou rede de afiliados |
| **Ingestion Source** | Fonte permitida de dados da loja: `api`, `feed`, `scraper`, `manual`, `disabled` |
| **Outbound Redirect** | Endpoint interno que registra clique e redireciona para a loja |
| **SubID / Click ID** | Identificador enviado ao afiliado para reconciliar clique e conversão |
| **Upsert** | Insert se não existe, update se já existe |
| **MCP** | Model Context Protocol — LLMs chamam ferramentas externas |
| **RBAC** | Role-Based Access Control |
| **Slug** | Versão URL-friendly de um nome |
| **scraped_at** | Timestamp da última coleta bem-sucedida |

---

## 19. Regras para Agentes

### Personalidade

Seja **direto ao ponto**. Respostas objetivas, sem explicações desnecessárias. Foque em: o que foi feito, o que foi verificado, próximo passo.

### Antes de Agir

1. Leia este arquivo (`AGENTS.md`)
2. Leia a skill relevante: `ai/lootprice-backend-developer/SKILL.md`, `ai/lootprice-frontend-developer/SKILL.md`, ou `ai/lootprice-scrum-master/SKILL.md`
3. Leia `docs/affiliate_store_strategy.md` ao tocar lojas, crawlers, preços, frontend de ofertas, redirects ou issues de novas lojas
4. Leia `docs/frontend_mobile_strategy.md` ao tocar setup frontend, auth, storage, links externos, arquitetura de services, responsividade ou mobile futuro
5. Verifique o estado real do repositório (árvore de arquivos, Makefile, CI)

### Regras Invioláveis

- **Nunca faça push direto na `master`** — sempre crie branch nova
- **Nunca interaja com PR fechado/mergeado** — verifique `state` e `merged` via `gh pr view <N> --json state,merged` antes
- **Nunca reutilize branch de PR fechado**
- **Nunca commite sem branch** — `git checkout -b <prefixo>/<descricao>` primeiro
- **Sempre use Conventional Commits**
- **Atualize `AGENTS.md` §15** ao criar/remover arquivos, concluir issues ou tomar decisões técnicas
- **Nunca crie crawler de loja nova sem registrar fonte permitida e compliance**
- **Nunca exponha link afiliado externo direto no frontend quando existir `outbound_url` interno**
- **Nunca misture marketplace de keys com loja autorizada sem sinalização explícita**
- **Nunca adicione React Native/Expo/Tauri/Capacitor ou dependências mobile ao MVP frontend sem issue e decisão registrada**

### Hierarquia de Autoridade

1. Arquivos reais do repositório
2. Este arquivo (`AGENTS.md`)
3. Skill específica (`ai/*/SKILL.md`)
4. Conhecimento geral da IA

Se algo existir apenas neste documento e não no código, trate como **planejado** (não implementado).

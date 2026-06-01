# LootPrice — Architecture Document

> **Versão:** 0.1.0-MVP
> **Status:** Planejamento Ativo
> **Última atualização:** 2026-05
> **Audiência:** Desenvolvedor, LLMs de apoio (GitHub Copilot, Claude, Cursor, etc.)

---

## Índice

1. [Visão Geral do Produto](#1-visão-geral-do-produto)
2. [Avaliação Crítica do Projeto](#2-avaliação-crítica-do-projeto)
3. [Decisão de Arquitetura: Monorepo vs. Multi-repo](#3-decisão-de-arquitetura-monorepo-vs-multi-repo)
4. [Escopo do MVP](#4-escopo-do-mvp)
5. [Stack Tecnológica](#5-stack-tecnológica)
6. [Estrutura do Repositório](#6-estrutura-do-repositório)
7. [Modelagem de Dados](#7-modelagem-de-dados)
8. [Fluxo de Dados](#8-fluxo-de-dados)
9. [API REST — Contratos](#9-api-rest--contratos)
10. [Autenticação e Autorização](#10-autenticação-e-autorização)
11. [Crawler Engine](#11-crawler-engine)
12. [Fluxo de Desenvolvimento com IA (MCP Toolchain)](#12-fluxo-de-desenvolvimento-com-ia-mcp-toolchain)
13. [CI/CD e Qualidade de Código](#13-cicd-e-qualidade-de-código)
14. [Roadmap Faseado](#14-roadmap-faseado)
15. [Riscos e Débitos Técnicos](#15-riscos-e-débitos-técnicos)
16. [Glossário](#16-glossário)

---

## 1. Visão Geral do Produto

**LootPrice** é um agregador e comparador de preços de chaves de jogos digitais. O sistema realiza scraping automatizado de múltiplas lojas, normaliza os dados coletados e expõe uma interface onde o usuário final encontra onde o jogo está mais barato — em tempo real ou com base no último snapshot coletado.

### Proposta de Valor

```
Usuário busca jogo → LootPrice consulta N lojas → Resultado: lista ordenada do menor ao maior preço
```

### Personas

| Persona | Necessidade |
|---|---|
| Gamer casual | Encontrar o menor preço rapidamente |
| Gamer frequente | Acompanhar variação de preço ao longo do tempo (Fase 3) |
| Admin do sistema | Gerenciar lojas cadastradas, forçar re-scraping, monitorar saúde dos crawlers |

---

## 2. Avaliação Crítica do Projeto

> Esta seção existe para apontar riscos reais. Não é pessimismo — é o que qualquer revisor técnico sênior diria antes de aprovar o planejamento.

### ✅ Pontos Fortes do Plano Inicial

- Escopo de MVP bem delimitado (apenas PC, apenas 2 lojas)
- Escolha de FastAPI + SQLModel é adequada e produtiva para Python
- Monorepo com contexto centralizado acelera o uso de LLMs no desenvolvimento
- Conventional Commits + Lefthook = base sólida de qualidade desde o dia 1

### ⚠️ Riscos e Problemas Identificados

#### 2.1 — Scraping é frágil por natureza

Lojas como Nuuvem, G2A e Eneba modificam seu HTML sem aviso. Um deploy delas pode quebrar 100% do seu crawler silenciosamente. Você precisa de:

- **Health checks** nos crawlers com alertas de falha
- **Testes de contrato** (asserting que campos obrigatórios existem no HTML parseado)
- **Fallback gracioso**: se o crawler falha, exibir o último preço coletado com timestamp visível

#### 2.2 — Normalização de nomes de jogos é o problema mais difícil

"Cyberpunk 2077", "Cyberpunk 2077 - PC", "Cyberpunk 2077™" e "Cyberpunk 2077 (GOG)" são o mesmo jogo. Sua lógica de normalização **vai falhar em edge cases**. Estratégia recomendada para o MVP:

- Normalização básica com regex (remove sufixos, símbolos especiais, lowercase)
- Campo `canonical_name` na tabela `games` editável pelo Admin
- Slug único gerado no backend — não confiar apenas no título

#### 2.3 — Você é desenvolvedor frontend sênior com backend básico

Isso não é problema, mas exige consciência:

- **Não subestime a autenticação JWT.** Refresh tokens, revogação, expiração — são muitos detalhes. Use uma biblioteca consolidada (`python-jose`, `passlib`) e siga exatamente a documentação do FastAPI para auth.
- **Migrations de banco.** O SQLModel não gera migrations automaticamente. Adicione **Alembic** desde o início. Alterar schema depois sem Alembic = dor de cabeça.
- **Validação de dados do scraping.** Nunca persista dados brutos. Toda entrada do crawler passa por Pydantic antes de tocar o banco.

#### 2.4 — G2A/Eneba estão fora do MVP — e devem continuar assim

Estes marketplaces cinzas possuem proteção anti-bot mais agressiva (Cloudflare, CAPTCHAs, rate limiting). Integrá-los exige proxies rotativos, Playwright headless e possíveis implicações legais dos termos de uso. Mantenha no roadmap, mas **não toque antes da Fase 3**.

#### 2.5 — Sem rate limiting na API = risco de abuso

Mesmo no MVP, adicione `slowapi` (rate limiting para FastAPI) antes do primeiro deploy público. Uma rota de busca sem throttling é um vetor de custo fácil.

---

## 3. Decisão de Arquitetura: Monorepo vs. Multi-repo

### Decisão: **Manter Monorepo**

#### Justificativa

| Critério | Monorepo | Multi-repo |
|---|---|---|
| Contexto para LLMs | ✅ Toda a base num lugar só | ❌ LLM precisa trocar de contexto entre repos |
| Complexidade operacional | ✅ 1 CI/CD, 1 board, 1 clone | ❌ Coordenação entre repos é custosa |
| Tamanho atual do time | ✅ 1 desenvolvedor — monorepo é ideal | Multi-repo é para times grandes com domínios separados |
| Deploys independentes | ❌ Mais difícil isolar | ✅ Cada serviço tem seu ciclo |
| Separação de concerns | Alcançável via estrutura de pastas | Estrutural por design |

**Conclusão:** Para um projeto MVP conduzido por um desenvolvedor com apoio intensivo de IA, o monorepo elimina fricção sem perder nada relevante. A separação de concerns será garantida pela estrutura de diretórios, não por repos separados.

> **Revisitar esta decisão** quando o projeto tiver: mais de 2 desenvolvedores ativos OU o crawler precisar de infraestrutura própria de escala (filas, workers distribuídos).

---

## 4. Escopo do MVP

### Em Escopo

| Área | Entregável |
|---|---|
| Alvo | Jogos de PC apenas |
| Lojas Fase 1 | Nuuvem (scraper) e Steam (API pública) |
| Atualização | Manual via CLI ou agendamento local (Makefile) |
| Auth | JWT + Login Social (Google, Discord) + Login Local |
| Perfis | RBAC com roles `user` e `admin` |
| Backend | API REST: busca, listagem, comparação de preços, gestão de usuários |
| Frontend | SPA: busca de jogos, comparação de preços, autenticação |
| Tooling | Conventional Commits, Lefthook, Ruff, Pytest, Alembic |

### Fora de Escopo (Fases Futuras)

- Wishlist e favoritos por usuário
- Alertas de preço por e-mail ou Discord
- Histórico e gráficos de variação de preço
- Integração com G2A, Eneba e outros marketplaces cinzas
- Suporte a jogos não-PC (console, mobile)
- Customização avançada de perfil
- Recomendações e rankings editoriais

---

## 5. Stack Tecnológica

### Backend & Crawler

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Linguagem | Python 3.11+ | Maturidade no ecossistema de scraping; compatibilidade total com FastAPI |
| Framework Web | FastAPI | Performance, tipagem nativa, OpenAPI automático |
| ORM | SQLModel + Alembic | SQLModel para modelos, Alembic para migrations controladas |
| Validação | Pydantic v2 | Já incluso no SQLModel; valida entradas do crawler e da API |
| Scraping | HTTPX (async) + BeautifulSoup4 | HTTPX para requests assíncronas; BS4 para parsing HTML |
| Linter/Formatter | Ruff | Substitui Black + isort + Flake8 com uma ferramenta só |
| Testes | Pytest + pytest-asyncio + httpx | Testes unitários e de integração da API |
| Autenticação | python-jose + passlib | JWT com bcrypt; amplamente utilizado no ecossistema FastAPI |
| Rate Limiting | slowapi | Middleware de throttling nativo para FastAPI |
| Ambiente | WSL2 Ubuntu (dev) | Conforme preferência do desenvolvedor |

### Banco de Dados & Infraestrutura

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Banco de Dados | PostgreSQL 15+ | Relacional, confiável, suporte nativo a JSONB para dados extras |
| Container | Docker + Docker Compose | Banco isolado, reproduzível entre máquinas |
| Migrations | Alembic | Controle de versão do schema, obrigatório desde o dia 1 |

### Frontend

| Camada | Tecnologia |
|---|---|
| Framework | React 18+ (TypeScript) |
| Build | Vite.js |
| Estilo | TailwindCSS |
| HTTP Client | Axios |
| Validação de Formulários | React Hook Form + Zod |
| State Management | Zustand (leve, adequado para MVP) |

### Tooling & DevOps

| Ferramenta | Finalidade |
|---|---|
| Makefile | Atalhos: `make dev`, `make test`, `make crawl`, `make migrate` |
| Lefthook | Git hooks: lint + commit message no pre-commit |
| GitHub Actions | CI: lint, testes, build a cada push/PR |
| GitHub Projects | Gestão de tarefas e backlog |
| Jira (opcional) | Alternativa ao GitHub Projects com integração MCP |

---

## 6. Estrutura do Repositório

```
lootprice/                          # Raiz do Monorepo
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # Lint + Testes em cada Push/PR
│   │   └── pr-review.yml           # Gatilho para revisão automática via MCP
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docs/
│   ├── architecture.md             # Este documento
│   ├── database_schema.md          # Modelagem detalhada do banco
│   ├── api_contracts.md            # Exemplos de request/response de cada rota
│   └── crawler_guide.md            # Como adicionar um novo crawler
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── games.py        # GET /games, GET /games/{id}
│   │   │   │   ├── prices.py       # GET /prices?game_id=
│   │   │   │   ├── search.py       # GET /search?q=
│   │   │   │   └── auth.py         # POST /auth/login, /auth/register, /auth/refresh
│   │   │   └── router.py           # Agregador de rotas
│   │   │
│   │   ├── core/
│   │   │   ├── config.py           # Settings via pydantic-settings (.env)
│   │   │   ├── database.py         # Engine e sessão do SQLModel
│   │   │   ├── security.py         # JWT encode/decode, hash de senha
│   │   │   └── dependencies.py     # get_current_user, get_db (FastAPI Depends)
│   │   │
│   │   ├── models/                 # Tabelas do banco (SQLModel Table=True)
│   │   │   ├── game.py
│   │   │   ├── price.py
│   │   │   ├── store.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/                # DTOs Pydantic (sem Table=True)
│   │   │   ├── game.py             # GameRead, GameWithPrices
│   │   │   ├── price.py            # PriceRead
│   │   │   └── auth.py             # TokenResponse, LoginRequest
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
│   │   └── conftest.py
│   │
│   ├── .env.example                # Template de variáveis de ambiente
│   ├── main.py                     # Ponto de entrada FastAPI
│   ├── requirements.txt
│   └── ruff.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/               # Funções Axios por domínio
│   │   ├── store/                  # Zustand stores
│   │   └── types/                  # Tipos TypeScript alinhados com schemas do backend
│   ├── .env.example
│   ├── vite.config.ts
│   └── package.json
│
├── docker-compose.yml              # PostgreSQL + (futuro) Redis
├── Makefile                        # Atalhos de desenvolvimento
├── lefthook.yml                    # Git hooks
├── .gitignore
└── README.md
```

### Regras do `.gitignore`

```gitignore
# Ambiente
.env
*.env.local
.venv/
__pycache__/
*.pyc

# Build
dist/
build/
*.egg-info/

# Node
node_modules/
frontend/dist/

# Banco (volumes locais)
pgdata/

# IDE
.vscode/
.idea/

# Testes / Coverage
.pytest_cache/
htmlcov/
.coverage
```

---

## 7. Modelagem de Dados

> Documento completo em `docs/database_schema.md`. Abaixo, o essencial para contexto de LLMs.

### Diagrama Entidade-Relacionamento (Simplificado)

```
users
  id (PK)
  email (UNIQUE)
  hashed_password (nullable — login social não tem senha)
  role: enum('user', 'admin')
  provider: enum('local', 'google', 'discord')
  created_at

stores
  id (PK)
  name              -- "Steam", "Nuuvem"
  slug              -- "steam", "nuuvem"
  base_url
  is_active: bool
  crawler_class     -- "steam.SteamCrawler"

games
  id (PK)
  title             -- Nome original (ex: "Cyberpunk 2077™")
  canonical_name    -- Nome normalizado (ex: "cyberpunk 2077")
  slug              -- "cyberpunk-2077"
  cover_url (nullable)
  created_at
  updated_at

prices
  id (PK)
  game_id (FK → games.id)
  store_id (FK → stores.id)
  price_brl         -- NUMERIC(10,2)
  original_price_brl (nullable)  -- Para calcular % de desconto
  discount_percent (nullable)
  url               -- Link direto para compra (afiliado futuro)
  is_available: bool
  scraped_at        -- Timestamp da última coleta

UNIQUE(game_id, store_id)  -- Um registro de preço por jogo por loja
```

### Decisões de Design

- `canonical_name` é editável pelo admin para corrigir falsos negativos da normalização automática
- `prices` guarda apenas o **preço atual** no MVP. Histórico será uma tabela `price_history` na Fase 3
- `price_brl` em NUMERIC, nunca FLOAT — dinheiro não tolera imprecisão de ponto flutuante
- `scraped_at` permite exibir "Atualizado há X minutos" no frontend sem expor problemas de crawler

---

## 8. Fluxo de Dados

### Pipeline de Ingestão (Crawler → Banco)

```
┌─────────────────────────────────────────────────┐
│                  Crawler Runner                  │
│  (executado via: make crawl / cron / CLI)        │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
NuuvemCrawler        SteamCrawler
(HTTPX + BS4)        (API pública)
    │                     │
    └──────────┬──────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Pydantic Validation  │
    │  (RawGameData schema) │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   Name Normalizer    │  ← remove símbolos, sufixos de plataforma,
    │                      │    gera canonical_name e slug
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Upsert no PostgreSQL│  ← INSERT OR UPDATE em games e prices
    └──────────────────────┘
```

### Fluxo de Consumo (Frontend → API)

```
[React SPA]
    │
    │  GET /api/v1/search?q=cyberpunk
    ▼
[FastAPI]
    │
    │  SELECT games JOIN prices JOIN stores
    │  WHERE canonical_name LIKE '%cyberpunk%'
    │  ORDER BY prices.price_brl ASC
    ▼
[PostgreSQL]
    │
    ▼
[FastAPI]  →  JSON response: { game, prices: [{store, price, url}] }
    │
    ▼
[React SPA]  →  Renderiza card com preços ordenados
```

---

## 9. API REST — Contratos

> Todos os endpoints são prefixados com `/api/v1/`.
> Documentação interativa gerada automaticamente em `/docs` (Swagger) e `/redoc`.

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/search?q={query}` | Não | Busca jogos por nome |
| GET | `/games` | Não | Lista jogos com paginação |
| GET | `/games/{slug}` | Não | Detalhe de um jogo com todos os preços |
| GET | `/prices?game_id={id}` | Não | Preços de um jogo específico |
| POST | `/auth/register` | Não | Cadastro local |
| POST | `/auth/login` | Não | Login local — retorna JWT |
| POST | `/auth/refresh` | JWT | Renova access token |
| GET | `/auth/me` | JWT | Dados do usuário autenticado |
| GET | `/auth/google` | Não | Inicia OAuth Google |
| GET | `/auth/discord` | Não | Inicia OAuth Discord |
| POST | `/admin/crawl` | JWT (admin) | Força execução dos crawlers |
| GET | `/admin/stores` | JWT (admin) | Lista lojas cadastradas |
| PATCH | `/admin/stores/{id}` | JWT (admin) | Ativa/desativa uma loja |
| PATCH | `/admin/games/{id}` | JWT (admin) | Edita canonical_name de um jogo |

### Exemplo de Response — `GET /games/{slug}`

```json
{
  "id": 1,
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
      "url": "https://nuuvem.com/...",
      "is_available": true,
      "scraped_at": "2026-05-31T14:00:00Z"
    },
    {
      "store": "Steam",
      "price_brl": 79.99,
      "original_price_brl": 199.99,
      "discount_percent": 60,
      "url": "https://store.steampowered.com/...",
      "is_available": true,
      "scraped_at": "2026-05-31T14:00:00Z"
    }
  ]
}
```

---

## 10. Autenticação e Autorização

### Fluxo JWT (Login Local)

```
POST /auth/login  {email, password}
    │
    ▼
Verifica hash (passlib/bcrypt)
    │
    ▼
Gera access_token (JWT, expira em 30min)
    +  refresh_token (JWT opaco, expira em 7 dias, salvo em DB)
    │
    ▼
Retorna {access_token, refresh_token, token_type: "bearer"}
```

### Fluxo OAuth (Google / Discord)

```
GET /auth/google
    │
    ▼
Redirect para provider (Google OAuth2)
    │
    ▼
Callback → recebe code → troca por user_info
    │
    ▼
Upsert user (cria se não existe, atualiza se existe)
    │
    ▼
Retorna JWT (mesmo formato do login local)
```

### RBAC (Roles)

| Role | Permissões |
|---|---|
| `user` | Buscar jogos, visualizar preços, gerenciar próprio perfil |
| `admin` | Tudo do `user` + forçar crawl, gerenciar lojas, editar games |

### Variáveis de Ambiente Obrigatórias

```env
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/lootprice
SECRET_KEY=<gerado com: openssl rand -hex 32>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
```

---

## 11. Crawler Engine

### Classe Base (Contrato)

Todo crawler deve herdar de `BaseCrawler` e implementar o método `fetch()`:

```python
# backend/app/crawlers/base.py

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import AsyncGenerator

class RawGameData(BaseModel):
    title: str
    price_brl: float
    original_price_brl: float | None = None
    url: str
    is_available: bool = True

class BaseCrawler(ABC):
    store_slug: str  # Obrigatório nas subclasses

    @abstractmethod
    async def fetch(self) -> AsyncGenerator[RawGameData, None]:
        """Yields dados brutos de jogos. Cada yield = 1 jogo."""
        ...
```

### Adicionando um Novo Crawler

1. Crie `backend/app/crawlers/{loja}.py`
2. Herde de `BaseCrawler` e defina `store_slug`
3. Implemente `fetch()` — use HTTPX async, valide com `RawGameData`
4. Registre no `runner.py`
5. Escreva pelo menos 1 teste em `tests/test_crawlers/test_{loja}.py`
6. Documente em `docs/crawler_guide.md`

### Critérios de Saúde do Crawler

- Se `fetch()` lançar exceção, o runner loga o erro e continua os demais crawlers
- Um crawler que retorna 0 resultados em 2 execuções consecutivas gera log `WARNING`
- Campo `scraped_at` é atualizado apenas em coleta bem-sucedida

---

## 12. Fluxo de Desenvolvimento com IA (MCP Toolchain)

Esta seção descreve como as ferramentas de IA são integradas ao workflow de desenvolvimento do LootPrice. O objetivo é manter alta velocidade sem sacrificar qualidade.

### Visão Geral da Toolchain

```
┌──────────────────────────────────────────────────────────────┐
│                    DESENVOLVIMENTO LOCAL                      │
│                                                              │
│  Editor (Cursor / VS Code)                                   │
│   └── Claude MCP: autocompletar, refatorar, documentar       │
│                                                              │
│  Terminal                                                    │
│   └── make dev | make test | make crawl | make migrate       │
└──────────────────────────────────────────────────────────────┘
              │  git push / open PR
              ▼
┌──────────────────────────────────────────────────────────────┐
│                       GITHUB                                 │
│                                                              │
│  MCP GitHub (claude.ai / Cursor)                            │
│   ├── Criar e fechar Issues diretamente via chat             │
│   ├── Revisar PRs: analisa diff + comenta no PR              │
│   ├── Consultar histórico de commits por contexto            │
│   └── Criar branches a partir de tarefas                     │
│                                                              │
│  GitHub Actions (CI)                                         │
│   ├── Lint (Ruff)                                            │
│   ├── Testes (Pytest)                                        │
│   └── Build check (Frontend)                                 │
└──────────────────────────────────────────────────────────────┘
              │  integração bidirecional
              ▼
┌──────────────────────────────────────────────────────────────┐
│                    GESTÃO DE TAREFAS                         │
│                                                              │
│  MCP Jira (ou GitHub Projects via MCP)                      │
│   ├── Criar cards de tarefa via prompt de chat               │
│   ├── Mover cards entre colunas (Backlog → In Progress)      │
│   ├── Vincular PR a card automaticamente                     │
│   └── Gerar release notes a partir de cards concluídos       │
└──────────────────────────────────────────────────────────────┘
              │  desenvolvimento frontend
              ▼
┌──────────────────────────────────────────────────────────────┐
│                 DESENVOLVIMENTO FRONTEND                     │
│                                                              │
│  MCP DevTools (Browser)                                     │
│   ├── Inspecionar elementos e estilos em tempo real          │
│   ├── Ler erros do console e repassar para o LLM             │
│   ├── Executar queries de acessibilidade (axe-core)          │
│   └── Validar responsive layout via screenshot               │
└──────────────────────────────────────────────────────────────┘
```

### MCP: GitHub

**Casos de uso práticos:**

```
Prompt: "Cria uma issue para adicionar suporte ao crawler da Fanatical, 
         label 'crawler', milestone 'Fase 2'"

Prompt: "Revisa o PR #14 e aponta problemas de segurança ou ausência de testes"

Prompt: "Lista todos os PRs abertos e me diz quais estão sem reviewer"
```

**Setup necessário:** Token de acesso pessoal do GitHub com permissões `repo` + MCP Server configurado no Cursor/Claude Desktop.

### MCP: Jira

**Casos de uso práticos:**

```
Prompt: "Cria um card no projeto LootPrice: 
         título 'Implementar crawler Nuuvem', 
         tipo Task, prioridade High, sprint atual"

Prompt: "Move o card LP-42 para 'In Review'"

Prompt: "Gera o resumo da sprint atual com todos os cards concluídos"
```

> **Alternativa ao Jira:** GitHub Projects funciona via MCP GitHub e pode ser suficiente para o MVP sem custo adicional. Recomendado começar com GitHub Projects e migrar para Jira apenas se o backlog crescer muito.

### MCP: DevTools (Browser)

**Casos de uso práticos:**

```
Prompt: "Inspeciona o componente de card de jogo e me diz 
         por que o preço está quebrando em mobile"

Prompt: "Lê os erros atuais do console da aba aberta"

Prompt: "Tira screenshot do estado atual e analisa o contraste de cores"
```

**Setup:** MCP Browser Tools (ex: `@modelcontextprotocol/server-puppeteer` ou extensão Playwright MCP).

### MCP: Futuras Integrações (Roadmap)

| MCP | Finalidade |
|---|---|
| Sentry MCP | Consultar erros de produção via chat |
| Slack MCP | Enviar alertas de crawler quebrado para canal |
| Postgres MCP | Executar queries exploratórias via chat (ambiente dev apenas) |
| Notion MCP | Sincronizar documentação técnica |

### Regras de Uso de IA no Projeto

1. **Todo código gerado por IA passa pelo CI** — nenhuma exceção
2. **Commits de código gerado por IA seguem Conventional Commits** — o LLM deve saber isso
3. **LLMs usam este arquivo como contexto primário** — mantenha-o atualizado a cada mudança de arquitetura
4. **Revisões de PR por IA são complementares, não substituem o entendimento humano**

---

## 13. CI/CD e Qualidade de Código

### Pipeline CI (GitHub Actions)

```yaml
# .github/workflows/ci.yml — estrutura simplificada

on: [push, pull_request]

jobs:
  backend:
    steps:
      - Checkout
      - Setup Python 3.11
      - Install dependencies
      - Ruff check (lint)
      - Ruff format --check
      - Pytest (com banco em memória / SQLite para testes unitários)

  frontend:
    steps:
      - Checkout
      - Setup Node 20
      - npm ci
      - TypeScript check (tsc --noEmit)
      - ESLint
      - Vite build
```

### Git Hooks (Lefthook)

```yaml
# lefthook.yml
pre-commit:
  commands:
    lint-backend:
      glob: "backend/**/*.py"
      run: ruff check {staged_files} && ruff format --check {staged_files}
    lint-frontend:
      glob: "frontend/src/**/*.{ts,tsx}"
      run: cd frontend && npx eslint {staged_files}

commit-msg:
  commands:
    conventional:
      run: npx commitlint --edit {1}
```

### Conventional Commits — Padrão do Projeto

```
feat(crawler): adiciona suporte ao scraper da Fanatical
fix(auth): corrige expiração do refresh token
docs(architecture): atualiza seção de MCP toolchain
chore(deps): atualiza FastAPI para 0.115
test(api): adiciona testes para rota de busca
refactor(normalizer): extrai lógica de slug para utilitário separado
```

---

## 14. Roadmap Faseado

### Fase 1 — MVP (Escopo Atual)

- [ ] Setup do repositório, Docker, Makefile, Lefthook
- [ ] Migrations iniciais com Alembic (models: games, prices, stores, users)
- [ ] Crawler: Steam (API)
- [ ] Crawler: Nuuvem (scraper)
- [ ] Normalização de nomes e geração de slugs
- [ ] API REST: busca, listagem, detalhe
- [ ] Autenticação: JWT local + Google + Discord
- [ ] RBAC: roles user/admin
- [ ] Frontend: busca + comparação de preços + auth
- [ ] CI/CD: GitHub Actions (lint + testes)
- [ ] MCP setup: GitHub + DevTools

### Fase 2 — Expansão de Lojas

- [ ] Crawler: GOG, Humble Bundle, Green Man Gaming
- [ ] Admin panel: gerenciar lojas, forçar re-scraping, editar canonical_names
- [ ] Agendamento automático de crawlers (Celery + Redis ou APScheduler)
- [ ] Wishlist e favoritos por usuário
- [ ] MCP: Jira para gestão de backlog

### Fase 3 — Features Avançadas

- [ ] Histórico de preços e gráficos de variação
- [ ] Alertas de preço por e-mail e Discord webhook
- [ ] Suporte a consoles (PS Store, Xbox, Nintendo — somente preços digitais)
- [ ] Integração experimental com G2A/Eneba (requer solução de anti-bot)
- [ ] API pública com autenticação por API Key
- [ ] MCP: Sentry para monitoramento de erros em produção

---

## 15. Riscos e Débitos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Crawler quebra por mudança de HTML | Alta | Alto | Health checks + testes de contrato + fallback de dados antigos |
| Normalização errada cria jogos duplicados | Média | Médio | Campo `canonical_name` editável pelo admin |
| Vazamento de credenciais no repositório | Baixa | Crítico | `.env` no gitignore, `.env.example` sem valores reais, GitHub Secret Scanning |
| Bloqueio de IP por scraping agressivo | Média | Alto | Rate limiting nos crawlers, User-Agent rotation, respeitar robots.txt |
| Schema do banco quebra sem migration | Média | Alto | Alembic obrigatório desde o dia 1 — nunca alterar models sem migration |
| Refresh tokens sem revogação | Baixa | Alto | Implementar tabela `revoked_tokens` ou usar Redis para blacklist |

---

## 16. Glossário

| Termo | Definição |
|---|---|
| **Canonical Name** | Nome normalizado e padronizado de um jogo, usado para deduplicação entre lojas |
| **Crawler** | Script que acessa lojas externas e extrai dados de jogos e preços |
| **DTO** | Data Transfer Object — schema Pydantic sem `Table=True`, usado para validação de I/O da API |
| **Upsert** | Operação de banco que insere um registro se não existe, ou atualiza se já existe |
| **MCP** | Model Context Protocol — protocolo que permite LLMs chamarem ferramentas externas (GitHub, Jira, etc.) |
| **RBAC** | Role-Based Access Control — controle de acesso baseado em papéis (roles) |
| **Slug** | Versão URL-friendly de um nome (ex: "cyberpunk 2077" → "cyberpunk-2077") |
| **scraped_at** | Timestamp da última coleta bem-sucedida de um preço |

---

> **Instrução para LLMs:** Este documento é a fonte de verdade de arquitetura do projeto LootPrice. Ao receber tarefas de desenvolvimento, consulte este arquivo para entender convenções de nomenclatura, estrutura de pastas, contratos de API e regras de negócio. Nunca assuma convenções que não estejam documentadas aqui. Em caso de conflito entre este documento e o código, sinalize a inconsistência antes de agir.

# LootPrice — Contexto Vivo para LLMs

> **INSTRUÇÃO PRIORITÁRIA PARA QUALQUER LLM QUE LER ESTE ARQUIVO:**
> Este é um documento vivo. Ao final de toda sessão de desenvolvimento, você DEVE atualizar as seções marcadas com `[ATUALIZÁVEL]` para refletir o estado real do projeto. Veja o protocolo completo na seção [Como Atualizar Este Arquivo](#-protocolo-de-atualização-obrigatório).

---

## Metadados do Documento

| Campo | Valor |
|---|---|
| **Versão** | 0.1.0 |
| **Última atualização** | 2026-05 |
| **Atualizado por** | Claude (planejamento inicial) |
| **Fase atual** | Planejamento — nenhum código implementado ainda |
| **Próximo card** | CARD-01: Setup inicial do repositório |

---

## 🚦 Protocolo de Atualização Obrigatório

**Este arquivo substitui memória entre sessões. Se não for mantido atualizado, o contexto se perde.**

### Quando atualizar

Ao final de **qualquer sessão** onde ocorreu pelo menos um dos seguintes:
- Um arquivo foi criado, editado ou deletado
- Um card foi iniciado, concluído ou bloqueado
- Uma decisão técnica foi tomada (mesmo que seja "decidimos não fazer X")
- Um bug relevante foi encontrado ou resolvido
- A stack, o schema ou os contratos de API mudaram

### O que atualizar

1. `Metadados do Documento` → versão, data, quem atualizou, próximo card
2. `Estado Atual do Projeto` → marcar o card como concluído, mover "em progresso"
3. `Arquivos Existentes no Repositório` → adicionar novos arquivos criados
4. `Decisões Tomadas` → registrar qualquer decisão relevante com data e motivo
5. `Problemas Conhecidos` → adicionar bugs/bloqueios encontrados
6. `Variáveis de Ambiente Necessárias` → se novas vars foram adicionadas

### Como atualizar (instrução direta para a LLM)

```
Ao final da sessão, gere o conteúdo atualizado deste arquivo com:
- Data de hoje no campo "Última atualização"
- Seu identificador no campo "Atualizado por" (ex: "Claude Sonnet", "Cursor", "GPT-4o")
- Cards concluídos marcados com ✅ na seção de Estado
- Novos arquivos adicionados na lista de arquivos
- Novas decisões registradas com data
- Problemas encontrados documentados

Apresente o arquivo atualizado completo para o desenvolvedor copiar e substituir.
Nunca atualize parcialmente — sempre entregue o arquivo inteiro.
```

---

## 1. Identidade do Projeto

**Nome:** LootPrice
**Tipo:** Agregador e comparador de preços de chaves de jogos digitais
**Objetivo:** Scraping de múltiplas lojas → normalização → interface mostrando onde o jogo está mais barato
**Repositório:** Monorepo
**Ambiente de dev:** WSL2 Ubuntu (Windows)
**Perfil do desenvolvedor:** Frontend sênior (React, Node.js), backend básico, Python intermediário

---

## 2. Stack Definitiva (Não alterar sem registrar em Decisões)

### Backend
| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| FastAPI | latest | Framework web assíncrono |
| SQLModel | latest | ORM (sobre SQLAlchemy) |
| Alembic | latest | Migrations de banco — obrigatório, nunca usar create_all em produção |
| Pydantic | v2 | Validação de dados e DTOs |
| HTTPX | latest | HTTP client assíncrono (crawlers e testes) |
| BeautifulSoup4 | latest | Parsing de HTML (Nuuvem scraper) |
| python-jose | latest | JWT encoding/decoding |
| passlib + bcrypt | latest | Hashing de senhas |
| slowapi | latest | Rate limiting para FastAPI |
| Ruff | latest | Linter + formatter (substitui Black/isort/Flake8) |
| Pytest + pytest-asyncio | latest | Testes unitários e de integração |

### Banco de Dados
| Tecnologia | Versão | Finalidade |
|---|---|---|
| PostgreSQL | 15+ | Banco principal |
| Docker Compose | latest | Containerização do banco |

### Frontend (parte do MVP)
React 18, TypeScript, Vite, TailwindCSS, Axios, Zod, React Hook Form, Zustand

### Tooling
Makefile, Lefthook, GitHub Actions, GitHub Projects (ou Jira), MCP GitHub, MCP Jira, MCP DevTools

---

## 3. Regras Rígidas de Comportamento (LLM: nunca violar)

### O que SEMPRE fazer
- Código Python com `async/await` em todas as rotas FastAPI e funções de I/O
- Type hints em todos os parâmetros e retornos de função Python
- Validação Pydantic em toda entrada de crawler antes de tocar o banco
- `NUMERIC(10, 2)` para campos monetários — nunca `float` ou `Float`
- Alembic para toda alteração de schema — nunca `SQLModel.metadata.create_all()` exceto em testes
- `try/except` com log explícito em todo bloco de scraping
- Testes unitários para toda nova funcionalidade (arquivo `tests/test_<módulo>.py`)
- Conventional Commits em toda sugestão de commit
- Variáveis sensíveis via `.env` e `pydantic-settings` — nunca hardcoded
- `logging` padrão do Python — nunca `print()` em código de produção

### O que NUNCA fazer
- Criar tabelas `price_history` ou `wishlists` (Fase 3)
- Implementar funcionalidades de wishlist, alertas de preço ou histórico
- Adicionar crawlers para G2A ou Eneba (Fase 3 — complexidade de anti-bot)
- Usar `requests` síncrono — sempre HTTPX async
- Usar `float` para dinheiro
- Alterar schema sem migration Alembic
- Retornar `hashed_password` em qualquer response de API
- Criar frontend antes do backend estar funcional
- Instalar dependências não listadas na stack sem registrar em Decisões Tomadas

---

## 4. Estrutura de Arquivos do Repositório

### Arquivos de Documentação (docs/)
```
docs/
├── architecture.md       ✅ Criado — visão arquitetural completa
├── database_schema.md    ✅ Criado — schema com todas as tabelas e constraints
├── llm_context.md        ✅ Este arquivo
└── project_cards.md      ✅ Criado — 21 cards do Jira com critérios de aceitação (7 épicos)
```

### [ATUALIZÁVEL] Arquivos do Backend
```
backend/
└── (nenhum arquivo criado ainda)
```

### [ATUALIZÁVEL] Arquivos de Infraestrutura
```
(nenhum arquivo criado ainda)
```

---

## 5. [ATUALIZÁVEL] Estado Atual do Projeto

### Cards em Progresso
```
(nenhum)
```

### Cards Concluídos
```
(nenhum — projeto em fase de planejamento)
```

### Próximo a Executar
```
CARD-01: chore(infra): setup inicial do repositório monorepo
  → Criar estrutura de pastas, docker-compose.yml, Makefile, lefthook.yml, .env.example, main.py vazio
  → Referência completa: docs/project_cards.md#CARD-01
```

### Cards Bloqueados
```
(nenhum)
```

---

## 6. Schema do Banco de Dados (Resumo Rápido)

> Documento completo: `docs/database_schema.md`

### Tabelas do MVP

**`stores`** — referência estática, populada via seed
- `id` (INT, PK), `name`, `slug`, `base_url`, `is_marketplace`, `crawler_class`, `is_active`
- Seed: Steam (`steam.SteamCrawler`) e Nuuvem (`nuuvem.NuuvemCrawler`)

**`games`** — um registro por jogo único
- `id` (UUID, PK), `title` (original), `canonical_name` (normalizado, editável), `slug` (único), `cover_url`
- `canonical_name` é o campo de deduplicação entre lojas

**`prices`** — snapshot atual, um por `(game_id, store_id)`
- `id` (UUID), `game_id` (FK), `store_id` (FK), `price_brl` (NUMERIC), `original_price_brl`, `discount_percent`, `affiliate_url`, `is_available`, `scraped_at`
- UNIQUE CONSTRAINT em `(game_id, store_id)` — crawler faz upsert, nunca insert puro

**`users`** — suporta local e OAuth
- `id` (UUID), `email` (único), `hashed_password` (nullable para OAuth), `role` ('user'|'admin'), `auth_provider` ('local'|'google'|'discord'), `provider_user_id`
- CHECK CONSTRAINT: `auth_provider = 'local'` implica `hashed_password IS NOT NULL`

### Ordem de Migration
```
1. stores → 2. games → 3. users → 4. prices
```

---

## 7. Contratos de API (Resumo Rápido)

> Prefixo de todas as rotas: `/api/v1/`
> Documentação interativa: `GET /docs` (Swagger)

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/search?q=` | — | Busca por canonical_name (ILIKE) |
| GET | `/games` | — | Listagem paginada |
| GET | `/games/{slug}` | — | Detalhe com preços ordenados por price_brl ASC |
| POST | `/auth/register` | — | Cadastro local |
| POST | `/auth/login` | — | Login → retorna access_token + refresh_token |
| POST | `/auth/refresh` | JWT | Renova access_token |
| GET | `/auth/me` | JWT | Dados do usuário autenticado (sem hashed_password) |
| GET | `/auth/google` | — | Inicia OAuth Google |
| GET | `/auth/discord` | — | Inicia OAuth Discord |
| POST | `/admin/crawl` | JWT admin | Força execução dos crawlers |
| PATCH | `/admin/games/{id}` | JWT admin | Edita canonical_name |
| GET | `/admin/stores` | JWT admin | Lista lojas |
| PATCH | `/admin/stores/{id}` | JWT admin | Ativa/desativa loja |

---

## 8. Crawler Engine (Contrato)

Todo crawler herda de `BaseCrawler` (em `backend/app/crawlers/base.py`):

```python
class RawGameData(BaseModel):
    title: str
    price_brl: Decimal          # Nunca float
    original_price_brl: Decimal | None = None
    affiliate_url: str
    is_available: bool = True
    store_slug: str             # "steam" | "nuuvem"

class BaseCrawler(ABC):
    store_slug: str

    @abstractmethod
    async def fetch(self) -> AsyncGenerator[RawGameData, None]: ...
    # Yields um item por vez — nunca retorna lista inteira
```

**Normalização de títulos (em `backend/app/core/normalizer.py`):**
- Remove: `™`, `®`, `©`, sufixos ` - PC`, `(PC)`, `(Steam)`
- Lowercase, strip, espaços normalizados
- `generate_slug()` → substitui espaços por `-`, remove caracteres especiais

---

## 9. [ATUALIZÁVEL] Decisões Tomadas

| Data | Decisão | Motivo | Alternativa Descartada |
|---|---|---|---|
| 2026-05 | Monorepo | 1 dev + LLM-assisted development; contexto unificado | Multi-repo descartado |
| 2026-05 | Alembic obrigatório desde o dia 1 | Evitar debt de schema sem rastreamento | SQLModel.create_all descartado para produção |
| 2026-05 | `prices` como snapshot (sem histórico) | Simplicidade no MVP; histórico é Fase 3 | Tabela append-only descartada para MVP |
| 2026-05 | `canonical_name` editável pelo admin | Normalização automática falha em edge cases | Deduplicação só automática descartada |
| 2026-05 | GitHub Projects no MVP (não Jira) | Sem custo adicional; suficiente para 1 dev | Migrar para Jira se backlog crescer |
| 2026-05 | `NUMERIC(10,2)` para preços | Precisão exata para dinheiro | `Float` descartado |
| 2026-05 | `slowapi` para rate limiting desde o MVP | API pública sem throttle é risco imediato | Sem rate limiting descartado |

---

## 10. [ATUALIZÁVEL] Problemas Conhecidos e Débitos Técnicos

| ID | Problema | Impacto | Status |
|---|---|---|---|
| — | Nenhum registrado ainda | — | — |

---

## 11. Variáveis de Ambiente

```env
# backend/.env.example — valores obrigatórios para o MVP

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
```

---

## 12. Comandos Frequentes (Referência Rápida)

```bash
make install                            # Instala deps + configura Lefthook
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

---

## 13. Contexto de Sessão Anterior

> Esta seção é preenchida pela LLM ao encerrar uma sessão. Resume o que foi feito para que a próxima sessão comece com contexto completo sem precisar reler toda a conversa.

### Última Sessão

**Data:** 2026-05
**LLM:** Claude Sonnet 4.6
**Duração:** Planejamento completo

**O que foi feito:**
- Definida e documentada a arquitetura completa do MVP (`docs/architecture.md`)
- Schema do banco de dados especificado com todas as tabelas, constraints e decisões de design (`docs/database_schema.md`)
- 16 cards do Jira criados com critérios de aceitação, dependências e contratos de API inline (`docs/project_cards.md`)
- README reescrito com comandos, estrutura e badges (`README.md`)
- Este arquivo `llm_context.md` criado como documento vivo

**Decisões tomadas nesta sessão:**
- Monorepo mantido (justificativa documentada na seção 9)
- Alembic adicionado à stack (não estava no plano original)
- `slowapi` adicionado para rate limiting desde o MVP
- `canonical_name` como campo separado e editável

**Estado ao encerrar:** Nenhum código implementado. Toda a sessão foi de planejamento e documentação. Pronto para iniciar CARD-01.

**O que fazer na próxima sessão:**
1. Fornecer este arquivo + `docs/project_cards.md` como contexto
2. Executar CARD-01: setup do repositório
3. Criar `docker-compose.yml`, `Makefile`, `lefthook.yml`, estrutura de pastas, `main.py` vazio

### Sessão de Revisão

**Data:** 2026-06-01
**LLM:** Claude Opus 4.6
**Duração:** Revisão de documentação

**O que foi feito:**
- Revisão completa de todos os 5 documentos do projeto
- Corrigido `RawGameData.price_brl` de `float` para `Decimal` em architecture.md
- Corrigido campo `url` para `affiliate_url` em architecture.md (alinhado com database_schema.md)
- Adicionado campo `store_slug` ao `RawGameData` em architecture.md
- Corrigido `DATABASE_URL` para usar driver `asyncpg` em architecture.md
- Corrigida dependência do CARD-15 (removido CARD-10, rotas são públicas)
- Corrigida árvore de dependências no sumário
- Corrigidas URLs de placeholder `seu-usuario` para `RodrigoVieira06` no README.md
- Adicionado `router.py` aos entregáveis do CARD-07
- Criado CARD-17: rate limiting com slowapi (EPIC-6)
- Criados CARD-18 a CARD-21: frontend React SPA (EPIC-7)
- Total de cards atualizado de 16 para 21 (7 épicos)
- Frontend confirmado como parte do MVP (não Fase 2)

**Decisões tomadas nesta sessão:**
- Frontend é MVP (não Fase 2) — cards de frontend criados
- Rate limiting (slowapi) em card separado (CARD-17), não no CARD-01
- `router.py` criado no CARD-07 (quando primeiras rotas surgem)

**Estado ao encerrar:** Nenhum código implementado. Documentação revisada e corrigida. Pronto para iniciar CARD-01.

**O que fazer na próxima sessão:**
1. Fornecer este arquivo + `docs/project_cards.md` como contexto
2. Executar CARD-01: setup do repositório
3. Criar `docker-compose.yml`, `Makefile`, `lefthook.yml`, estrutura de pastas, `main.py` vazio

---

*Documento mantido pela LLM ativa na sessão. Nunca editar manualmente exceto para corrigir informações incorretas.*

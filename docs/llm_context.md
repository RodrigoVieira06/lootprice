# LootPrice — Contexto Vivo para LLMs

> **INSTRUÇÃO PRIORITÁRIA PARA QUALQUER LLM QUE LER ESTE ARQUIVO:**
> Este é um documento vivo. Ao final de toda sessão de desenvolvimento, você DEVE atualizar as seções marcadas com `[ATUALIZÁVEL]` para refletir o estado real do projeto. Veja o protocolo completo na seção [Como Atualizar Este Arquivo](#-protocolo-de-atualização-obrigatório).

---

## Metadados do Documento

| Campo | Valor |
|---|---|
| **Versão** | 0.1.4 |
| **Última atualização** | 2026-06-09 |
| **Atualizado por** | Claude Sonnet 4.6 (Thinking) via Antigravity IDE |
| **Fase atual** | Desenvolvimento — CARD-01 em andamento (não iniciado fisicamente) |
| **Próximo card** | CARD-01: Setup inicial do repositório (Aguardando implementação física) |

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
**Ambiente de dev:** Ubuntu nativo (i7 10ª geração, 8GB RAM) — acessado via SSH do PC principal
**Acesso remoto:** Tailscale (SSH seguro) + Cloudflare Tunnel (exposição da app para testes)
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
Makefile, Lefthook, GitHub Actions, Jira, MCP GitHub, MCP Jira, MCP DevTools

### CI/CD & Code Review
| Ferramenta | Finalidade |
|---|---|
| `.github/workflows/ci.yml` | Lint (Ruff) + Testes (Pytest) + Build frontend em cada PR |
| `.github/workflows/ai-review.yml` | Review automático por Gemini 2.0 Flash em cada PR — posta nota, bloqueios, sugestões |
| `.github/PULL_REQUEST_TEMPLATE.md` | Template de PR com checklist de qualidade preenchido pelo dev |
| GitHub Branch Protection | `master` requer PR + CI verde + ai-review antes de qualquer merge |

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

## 3.1 Git Workflow — Regra OBRIGATÓRIA para toda IA assistente

> **⚠️ INSTRUÇÃO PRIORITÁRIA — aplicável a Claude, Gemini, Copilot, Cursor e qualquer LLM que trabalhe neste projeto.**
> Qualquer IA que viole estas regras estará criando risco real de regressão e perda de rastreabilidade no projeto.

### Regras de branching (NUNCA violar)

- **NUNCA** sugerir `git push origin master`, `git commit` direto na `master` ou qualquer operação que bypasse o fluxo de PR
- **TODO** código novo deve ir para uma branch com nome no padrão abaixo
- **SEMPRE** instruir a abrir um PR após o desenvolvimento de um card
- **NUNCA** recomendar merge sem o workflow `ai-review` ter postado o comentário de revisão no PR do GitHub
- **NUNCA** recomendar merge sem o workflow `ci` ter passado (lint + testes)
- **SEMPRE** verificar a nota de qualidade (de 0 a 10) postada pelo revisor IA nos comentários do PR. A nota mínima recomendada para aprovação sem ressalvas é 8/10. Notas inferiores devem ser corrigidas e melhoradas.

### Padrão de nome de branch

```
feat/<card-id>-descricao-curta      # nova funcionalidade
fix/<card-id>-descricao-curta       # correção de bug
chore/<card-id>-descricao-curta     # configuração, tooling, build
docs/<card-id>-descricao-curta      # apenas documentação
refactor/<card-id>-descricao-curta  # refatoração sem mudança de comportamento
test/<card-id>-descricao-curta      # apenas testes
```

Exemplos reais do projeto:
```
feat/card-01-monorepo-setup
feat/card-03-postgresql-alembic
fix/card-07-auth-token-expiry
chore/card-24-ai-code-review
```

### Fluxo Obrigatório de Desenvolvimento e Ciclo de Vida do Card (Ordem Exata)

Toda IA assistente que iniciar uma tarefa DEVE executar e reportar os seguintes 9 passos nesta ordem exata:

1. **Mover o card no Jira para "Desenvolvendo"**:
   - Usar a ferramenta `transitionJiraIssue` no MCP do Jira para transicionar o card do status "Priorizado" para o status "Desenvolvendo" (transição ID `21`).
2. **Criar uma nova branch**:
   - Criar uma branch a partir de `master` seguindo o padrão de nomenclatura (ex: `feat/<card-id>-descricao-curta`).
3. **Desenvolver e commitar as alterações**:
   - Desenvolver o código com testes e documentação e fazer commits utilizando Conventional Commits.
4. **Realizar o push para a branch remota**:
   - Fazer o push da branch criada para o repositório remoto no GitHub.
5. **Abrir o Pull Request (PR)**:
   - Abrir o PR apontando para a branch `master` usando o template de PR do repositório.
6. **Mover o card no Jira para "Revisando"**:
   - Usar a ferramenta `transitionJiraIssue` no MCP do Jira para transicionar o card do status "Desenvolvendo" para o status "Revisando" (transição ID `31`).
7. **Executar/Aguardar o Code Review**:
   - Aguardar a execução automática do workflow `ai-review.yml` e a aprovação do CI (`ci.yml`). Em sessões de desenvolvimento com o Antigravity, o próprio assistente pode rodar ou simular o review e postar nos comentários do PR.
8. **Aprovar e Mergear o PR**:
   - Caso não haja bloqueios identificados no review da IA (nota geral de qualidade >= 8/10 e zero bloqueios), e todos os checks de status do CI passem, o PR deve ser aprovado e mergeado na branch `master`.
9. **Mover o card no Jira para "Deployed"**:
   - Usar a ferramenta `transitionJiraIssue` no MCP do Jira para transicionar o card para o status "Deployed" (transição ID `51`).

### Branch protection rules (configuradas no GitHub)

- `master` requer PR obrigatório — push direto é bloqueado pelas regras de Branch Protection do GitHub
- Status checks obrigatórios: `ci / Backend (Python)`, `ci / Frontend`, `AI Code Review — LootPrice`
- Stale reviews são descartados ao novo push

---

## 4. Estrutura de Arquivos do Repositório

### Arquivos de Documentação (docs/)
```
docs/
├── architecture.md       ✅ Criado — visão arquitetural completa
├── database_schema.md    ✅ Criado — schema com todas as tabelas (incl. revoked_tokens)
├── llm_context.md        ✅ Este arquivo
└── project_cards.md      ✅ Criado — 23 cards do Jira com critérios de aceitação (8 épicos)
                          ✅ CARD-22 criado no Jira como LP-30 | CARD-23 criado como LP-31
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
CARD-01: chore(infra): setup inicial do repositório monorepo [LP-12]
  → Iniciado em 2026-06-02. Próximo passo: criar estrutura física de pastas e arquivos base.
```

### Cards Concluídos
```
(nenhum — desenvolvimento iniciado)
```

### Próximo a Executar
```
CARD-02: chore(ci): configurar pipeline CI com GitHub Actions [LP-14] (Depende de CARD-01)
CARD-03: feat(database): configurar conexão com PostgreSQL e setup do Alembic [LP-9] (Depende de CARD-01)
CARD-05: feat(database): implementar model de users com suporte a OAuth e RBAC [LP-10] (Depende de CARD-03)
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
| 2026-05 | `NUMERIC(10,2)` para preços | Precisão exata para dinheiro | `Float` descartado |
| 2026-05 | `slowapi` para rate limiting desde o MVP | API pública sem throttle é risco imediato | Sem rate limiting descartado |
| 2026-06-01 | Migração do GitHub Projects para Jira | Gestão de backlog centralizada no espaço "Loot Price" solicitado, cards exportados e configurados usando Jira MCP Server. | GitHub Projects |
| 2026-06-03 | `revoked_tokens` no schema do MVP | Refresh tokens sem revogação são risco de segurança real; estava nos riscos do architecture.md sem card correspondente | Redis para blacklist descartado (desnecessário no MVP) |
| 2026-06-03 | Ambiente de dev é Ubuntu físico (não WSL2) | Máquina i7 10ª + 8GB RAM já disponível; hardware superior à maioria das VPS na faixa de preço | VPS paga descartada até necessidade de uptime garantido |
| 2026-06-03 | Tailscale + Cloudflare Tunnel como infra de acesso | Tailscale para SSH seguro sem IP fixo; Cloudflare Tunnel para expor a app sem abrir portas | DDNS + port forwarding descartado (menos seguro) |
| 2026-06-03 | Manter `python-jose` no MVP, monitorar migração | `PyJWT` + `authlib` são alternativas mais ativas; mas trocar no MVP adiciona risco sem benefício imediato | Migração imediata para PyJWT descartada para o MVP |
| 2026-06-03 | CARD-23 (Nginx + CF-Connecting-IP) como card obrigatório | Sem `get_real_ip()` no slowapi, rate limiting por IP falha com Cloudflare Tunnel na frente | Ignorar o gotcha descartado — impacto direto em segurança |
| 2026-06-03 | Frontend é MVP (não Fase 2) | Confirmado em sessão anterior (Claude Opus); já tinha cards CARD-18 a CARD-21; estava incorreto no README e no diagrama de arquitetura | Frontend como Fase 2 descartado |
| 2026-06-09 | Cloudflare Tunnel mantido na arquitetura futura, bloqueado agora | Sem domínio registrado, Cloudflare Tunnel não pode ser usado. Ferramenta certa para o momento errado. Manter no plano de produção | Remover Cloudflare da arquitetura descartado — ainda é a solução mais segura e gratuita para exposição pública futura |
| 2026-06-09 | CARD-23 rebaixado para prioridade Low; `get_real_ip()` movida para CARD-17 | Sem Cloudflare ativo, CARD-23 não pode ser testado. A função `get_real_ip()` é útil para qualquer proxy e deve ser implementada no CARD-17 | Executar CARD-23 agora descartado — depende de domínio |
| 2026-06-10 | Sistema de AI Code Review via GitHub Actions implementado | Necessidade de garantir qualidade e rastreabilidade com desenvolvimento assistido por IA; nenhuma IA deve burlar o fluxo de PR | CodeRabbit SaaS descartado (repo privado = pago); Claude API descartada (sem key separada) — Gemini free tier suficiente |
| 2026-06-10 | CARD-24 criado: feat(ci): sistema de AI code review | Infra transversal criada via `ai-review.yml`, `ci.yml`, `branch-check.yml`, `PULL_REQUEST_TEMPLATE.md` e seção 3.1 em `llm_context.md` | Repo separado para o bot descartado — workflow dentro do projeto é o padrão da indústria |

---

## 10. [ATUALIZÁVEL] Problemas Conhecidos e Débitos Técnicos

| ID | Problema | Impacto | Status |
|---|---|---|---|
| DT-01 | Limpeza periódica de `revoked_tokens` expirados não implementada | Tabela cresce indefinidamente; sem impacto funcional no MVP, mas vira problema em produção com volume | Aberto — implementar `DELETE FROM revoked_tokens WHERE expires_at < NOW()` via cron na Fase 2 |
| DT-02 | `python-jose` com manutenção irregular no ecossistema | Pode ficar sem patches de segurança futuramente | Monitorar — migrar para `PyJWT` + `authlib` se inativo por 6+ meses |
| DT-03 | Sem validação de IPs Cloudflare no header `X-Forwarded-For` | Header pode ser forjado por cliente malicioso em ambiente não-Cloudflare | Aberto — para produção real, validar que o IP de origem do request é da lista de IPs do Cloudflare |
| DT-04 | CARD-23 bloqueado por ausência de domínio registrado | Cloudflare Tunnel não pode ser configurado sem domínio; rate limiting por IP real em produção fica pendente | Bloqueado — `get_real_ip()` implementada no CARD-17 como mitigação parcial; CARD-23 completo só após aquisição de domínio |

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

# Frontend (VITE_ prefix expõe para o cliente)
VITE_API_URL=http://localhost:8000/api/v1
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

### Sessão de Criação de Cards no Jira

**Data:** 2026-06-01
**LLM:** Gemini CLI
**Duração:** Importação de Backlog para Jira

**O que foi feito:**
- Os 7 épicos e 21 tarefas (cards) foram criados e configurados no espaço do Jira "Loot Price" do projeto usando MCP.
- Incluídas descrições detalhadas convertidas para o Atlassian Document Format.
- Epics, prioridades e tags configurados em cada card individual.
- Estrutura de dependência (Issue Links - `blocks`/`is blocked by`) foi implementada em todos os 21 cards.

**Decisões tomadas nesta sessão:**
- Migrar formalmente para Jira em vez do GitHub Projects, mantendo o controle total pelo Atlassian MCP.

**Estado ao encerrar:** Nenhum código implementado. O espaço do projeto no Jira está plenamente montado para o time iniciar o MVP.

### Sessão de Início de Desenvolvimento

**Data:** 2026-06-02
**LLM:** Gemini 3.5 Flash (High)
**Duração:** Análise e Início do CARD-01

**O que foi feito:**
- Analisados os arquivos `project_cards.md`, `architecture.md` e `llm_context.md`.
- Consultado o projeto Jira "Loot Price" (LP) usando Atlassian MCP.
- Identificado o CARD-01 (`LP-12` no Jira) como único card sem dependências ativas.
- Movido o status do CARD-01 (`LP-12`) no Jira de `Priorizado` para `Desenvolvendo` (In Progress).
- Atualizado o arquivo `llm_context.md` para refletir o início do desenvolvimento.

**Decisões tomadas nesta sessão:**
- Mover o status de LP-12 para "Desenvolvendo", marcando o início oficial do desenvolvimento do MVP do LootPrice.

**Estado ao encerrar:** CARD-01 (`LP-12`) em andamento. Estrutura básica de pastas e arquivos configurados no Jira para acompanhamento. Pronto para começar a escrever código.

**O que fazer na próxima sessão:**
1. Criar a estrutura inicial do monorepo (Makefile, Lefthook, docker-compose.yml, backend/app, main.py).
2. Garantir que os testes iniciais e linter (Ruff) passem localmente.
3. Concluir o card e movê-lo para a fase de revisão/teste.

### Sessão de Avaliação de Infraestrutura e Revisão do Plano

**Data:** 2026-06-03
**LLM:** Claude Sonnet 4.6 (Thinking) via Antigravity IDE
**Duração:** Revisão e avaliação

**O que foi feito:**
- Leitura e análise da conversa importada de Claude Sonnet 4.6 sobre VPS, Tailscale e Cloudflare Tunnel
- Cruzamento dessas propostas de infra com a arquitetura definida em `docs/architecture.md`
- Avaliação do plano geral do projeto do ponto de vista de um desenvolvedor frontend sênior entrando no mundo backend/infra

**Decisões tomadas nesta sessão:**
- Nenhuma nova decisão técnica de código — sessão de avaliação e contexto

**Estado ao encerrar:** Nenhum código implementado. CARD-01 ainda não foi executado fisicamente. Ambiente de desenvolvimento é a máquina Ubuntu local (i7 10ª + 8GB) acessada via SSH.

**Infraestrutura de dev confirmada (não documentada anteriormente):**
- Máquina dev: Ubuntu, i7 10ª geração, 8GB RAM
- Acesso: SSH do PC principal para a máquina Ubuntu
- Estratégia recomendada: Tailscale (SSH seguro) + Cloudflare Tunnel (exposição da app se necessário)
- Produção futura: migrar para VPS apenas quando houver necessidade de uptime garantido

**O que fazer na próxima sessão:**
1. Executar CARD-01: criar estrutura física do monorepo (`docker-compose.yml`, `Makefile`, `lefthook.yml`, pastas `backend/` e `frontend/`, `main.py` vazio)
2. Garantir que `ruff` e `lefthook` estejam funcionando localmente na máquina Ubuntu
3. Mover LP-12 para "Concluído" no Jira após setup

### Sessão de Análise de Infraestrutura — Cloudflare e Cards

**Data:** 2026-06-09
**LLM:** Claude Sonnet 4.6 (Thinking) via Antigravity IDE
**Duração:** Análise e tomada de decisão

**O que foi feito:**
- Analisado o impacto da ausência de domínio registrado na arquitetura planejada
- Verificado que o Cloudflare Tunnel requer domínio próprio para funcionar — sem ele, a ferramenta está bloqueada
- Avaliados os cards afetados por essa restrição atual
- Corrigidas edições indevidas do Gemini que havia removido decisões não relacionadas ao Cloudflare

**Decisões tomadas nesta sessão:**
- Cloudflare Tunnel **mantido** na arquitetura de produção futura — ferramenta certa, momento errado
- CARD-23 rebaixado para prioridade **Low** — não pode ser testado sem domínio
- Função `get_real_ip()` do CARD-23 absorvida pelo **CARD-17** (slowapi) — útil para qualquer proxy
- Novo débito técnico **DT-04** registrado sobre o bloqueio do CARD-23

**Cards impactados:**
- CARD-17 (slowapi): absorver `get_real_ip()` do CARD-23 — implementar na entrega do CARD-17
- CARD-23 (Nginx + CF-Connecting-IP): rebaixado para Low — executar apenas após aquisição de domínio

**Estado ao encerrar:** Nenhum código implementado. CARD-01 ainda não foi executado fisicamente. Análise de infra consolidada.

**O que fazer na próxima sessão:**
1. Executar CARD-01: criar estrutura física do monorepo (`docker-compose.yml`, `Makefile`, `lefthook.yml`, pastas `backend/` e `frontend/`, `main.py` vazio)
2. Garantir que `ruff` e `lefthook` estejam funcionando localmente na máquina Ubuntu
3. Mover LP-12 para "Concluído" no Jira após setup
4. No CARD-17, implementar `get_real_ip()` que lê `X-Forwarded-For` (preparado para proxy futuro)

---

*Documento mantido pela LLM ativa na sessão. Nunca editar manualmente exceto para corrigir informações incorretas.*
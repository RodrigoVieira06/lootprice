# LootPrice — Jira Project Cards (MVP)

> **Instrução para LLM que processar este arquivo:**
> Este documento define os cards do Jira para o MVP do LootPrice.
> Cada card contém: tipo, épico pai, descrição técnica precisa, critérios de aceitação mensuráveis, arquivos a criar/editar, dependências entre cards e o que explicitamente **não** fazer.
> Ao criar um card no Jira via MCP, use o campo `summary` para o título, `description` para o corpo completo em Markdown, `labels` para as labels e `priority` para a prioridade.
> **Não resumir, não omitir critérios de aceitação, não alterar os títulos.**
> **Total de cards: 23 (CARD-01 a CARD-23)**

---

## Estrutura de Épicos

| Épico | Chave Sugerida | Ordem |
|---|---|---|
| Infraestrutura Base | EPIC-1 | 1º — pré-requisito para tudo |
| Banco de Dados | EPIC-2 | 2º — pré-requisito para crawlers e auth |
| Autenticação | EPIC-3 | 3º — paralelo ao épico de crawlers |
| Crawlers e Ingestão | EPIC-4 | 4º — depende do banco |
| API REST | EPIC-5 | 5º — depende de banco + crawlers |
| Segurança e Middleware | EPIC-6 | 6º — rate limiting |
| Frontend | EPIC-7 | 7º — depende do backend funcional |

---

## EPIC-1 — Infraestrutura Base

---

### CARD-01

```
Tipo: Task
Épico: EPIC-1
Prioridade: Highest
Labels: infra, setup, backend
Summary: chore(infra): setup inicial do repositório monorepo
```

**Descrição:**

Configurar a estrutura base do repositório conforme o `docs/architecture.md`. Este card é o pré-requisito absoluto de todos os outros — nenhum outro card pode ser iniciado antes deste ser concluído.

**Arquivos a criar:**

```
lootprice/
├── .github/
│   └── workflows/
│       └── ci.yml              ← pipeline de lint + testes
├── docs/
│   ├── architecture.md         ← já existe
│   ├── database_schema.md      ← já existe
│   ├── llm_context.md          ← já existe
│   └── project_cards.md        ← este arquivo
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/__init__.py
│   │   ├── core/__init__.py
│   │   ├── models/__init__.py
│   │   ├── schemas/__init__.py
│   │   └── crawlers/__init__.py
│   ├── tests/
│   │   └── __init__.py
│   ├── .env.example
│   ├── main.py                 ← instância do FastAPI, sem rotas ainda
│   ├── requirements.txt
│   └── ruff.toml
├── docker-compose.yml          ← somente PostgreSQL por ora
├── Makefile
├── lefthook.yml
├── .gitignore
└── README.md
```

**Critérios de Aceitação:**

- [ ] `docker compose up -d` sobe o PostgreSQL sem erros
- [ ] `make install` instala dependências do backend sem erros
- [ ] `make dev` inicia o servidor FastAPI em `localhost:8000`
- [ ] `GET /docs` retorna o Swagger UI do FastAPI
- [ ] `make lint` executa Ruff sem erros no código inicial
- [ ] `make test` executa Pytest e retorna 0 testes (sem falha)
- [ ] Lefthook instalado e ativo: commit com mensagem inválida é bloqueado
- [ ] `.env` está no `.gitignore`; `.env.example` está no repositório com chaves mas sem valores

**Não fazer:**
- Não criar nenhuma rota de negócio ainda (games, prices, auth)
- Não criar models de banco ainda
- Não instalar Redis, Celery ou qualquer dependência além do MVP

---

### CARD-02

```
Tipo: Task
Épico: EPIC-1
Prioridade: Highest
Labels: infra, ci
Summary: chore(ci): configurar pipeline CI com GitHub Actions
Depende de: CARD-01
```

**Descrição:**

Criar o workflow do GitHub Actions que roda automaticamente a cada `push` e `pull_request` para a branch `main`. O pipeline é o guardião de qualidade do projeto.

**Arquivos a criar/editar:**

- `.github/workflows/ci.yml`

**Estrutura esperada do `ci.yml`:**

```yaml
# Jobs obrigatórios:
# 1. backend-lint: ruff check + ruff format --check
# 2. backend-test: pytest com banco SQLite in-memory
# 3. frontend-check: tsc --noEmit (quando frontend existir — preparar o job disabled por ora)

# Trigger: push e pull_request para main e develop
# Python version: 3.11
# Cache: pip dependencies via actions/cache
```

**Critérios de Aceitação:**

- [ ] Pipeline executa automaticamente em todo push para `main`
- [ ] Pipeline executa automaticamente em todo PR aberto contra `main`
- [ ] Job `backend-lint` falha se Ruff reportar erros
- [ ] Job `backend-test` falha se qualquer teste falhar
- [ ] Badge de status do CI visível no `README.md`
- [ ] Pipeline completo roda em menos de 3 minutos

**Não fazer:**
- Não configurar deploy automático (CD) ainda
- Não adicionar secrets de banco de dados reais no CI (usar SQLite in-memory nos testes)

---

## EPIC-2 — Banco de Dados

---

### CARD-03

```
Tipo: Task
Épico: EPIC-2
Prioridade: Highest
Labels: backend, database
Summary: feat(database): configurar conexão com PostgreSQL e setup do Alembic
Depende de: CARD-01
```

**Descrição:**

Configurar a camada de conexão com o banco de dados usando SQLModel + Alembic. O Alembic é **obrigatório desde o início** — nunca alterar o schema sem migration.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── core/
│       ├── config.py        ← Settings via pydantic-settings
│       ├── database.py      ← engine, session, get_db dependency
│       └── dependencies.py  ← get_db exportado para uso nas rotas
├── migrations/
│   ├── env.py               ← configurado para usar os models SQLModel
│   ├── script.py.mako
│   └── versions/            ← vazio inicialmente
└── alembic.ini
```

**Padrão obrigatório para `database.py`:**

```python
# Usar AsyncEngine com asyncpg
# DATABASE_URL lida de Settings (pydantic-settings)
# get_db deve ser um async generator para uso com FastAPI Depends
# Não usar create_all() do SQLModel — Alembic gerencia o schema
```

**Critérios de Aceitação:**

- [ ] `make migrate-create msg="initial"` gera arquivo de migration em `migrations/versions/`
- [ ] `make migrate` aplica a migration sem erros
- [ ] `make migrate-rollback` reverte a última migration sem erros
- [ ] FastAPI inicia sem erros com banco rodando
- [ ] FastAPI exibe erro claro e não crasha se banco estiver offline (startup check)
- [ ] `DATABASE_URL` lida exclusivamente do `.env`, nunca hardcoded

**Não fazer:**
- Não usar `SQLModel.metadata.create_all()` em produção — apenas em testes
- Não commitar `alembic.ini` com a DATABASE_URL preenchida

---

### CARD-04

```
Tipo: Task
Épico: EPIC-2
Prioridade: High
Labels: backend, database
Summary: feat(database): implementar models de stores, games e prices
Depende de: CARD-03
```

**Descrição:**

Criar os models SQLModel para as três tabelas centrais do sistema. Seguir exatamente o schema definido em `docs/database_schema.md`. Criar a migration correspondente e o seed de stores.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── models/
│       ├── __init__.py      ← exportar todos os models (necessário para Alembic detectar)
│       ├── store.py         ← model Store
│       ├── game.py          ← model Game com relacionamentos
│       └── price.py         ← model Price com UNIQUE constraint (game_id, store_id)
├── migrations/
│   └── versions/
│       └── XXXX_create_stores_games_prices.py  ← gerado via Alembic
└── tests/
    └── test_models/
        └── test_game_model.py   ← testes básicos de criação e relacionamento
```

**Critérios de Aceitação:**

- [ ] Migration cria as três tabelas com todos os campos conforme `database_schema.md`
- [ ] UNIQUE constraint `(game_id, store_id)` em `prices` existe e é testada
- [ ] Campo `price_brl` é `NUMERIC(10,2)`, nunca `FLOAT`
- [ ] Seed popula `stores` com Steam e Nuuvem após `make db-seed`
- [ ] Relacionamentos SQLModel funcionam: `game.prices` retorna lista de preços
- [ ] Testes unitários passam: criar game, criar price vinculado, consultar via relacionamento

**Não fazer:**
- Não criar a tabela `users` aqui (é CARD-05)
- Não criar a tabela `price_history` (Fase 3)
- Não usar `Float` ou `str` para campos monetários

---

### CARD-05

```
Tipo: Task
Épico: EPIC-2
Prioridade: High
Labels: backend, database, auth
Summary: feat(database): implementar model de users com suporte a OAuth e RBAC
Depende de: CARD-03
```

**Descrição:**

Criar o model `User` com suporte a login local e OAuth (Google, Discord). O model deve ser flexível o suficiente para os dois fluxos sem duplicar lógica.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── models/
│       └── user.py          ← model User conforme database_schema.md
├── migrations/
│   └── versions/
│       └── XXXX_create_users.py
└── tests/
    └── test_models/
        └── test_user_model.py
```

**Critérios de Aceitação:**

- [ ] Migration cria tabela `users` com todos os campos do schema
- [ ] `CHECK CONSTRAINT` garante que `auth_provider = 'local'` implica `hashed_password IS NOT NULL`
- [ ] Index em `(auth_provider, provider_user_id)` criado para lookup OAuth eficiente
- [ ] Campo `role` aceita apenas `'user'` ou `'admin'` (enum ou check constraint)
- [ ] Testes: criar usuário local (com senha), criar usuário OAuth (sem senha), validar constraint

**Não fazer:**
- Não implementar lógica de autenticação aqui (é CARD-07)
- Não criar endpoints de auth aqui

---

## EPIC-3 — Autenticação

---

### CARD-06

```
Tipo: Task
Épico: EPIC-3
Prioridade: High
Labels: backend, auth, security
Summary: feat(auth): implementar utilitários de segurança (JWT e hashing)
Depende de: CARD-05
```

**Descrição:**

Criar as funções utilitárias de segurança: hashing de senha com `passlib/bcrypt` e geração/validação de JWT com `python-jose`. Estas funções são a base de todos os endpoints de auth.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── core/
│       └── security.py      ← hash_password, verify_password, create_token, decode_token
└── tests/
    └── test_core/
        └── test_security.py
```

**Padrão obrigatório:**

```python
# security.py deve expor:
# - hash_password(plain: str) -> str
# - verify_password(plain: str, hashed: str) -> bool
# - create_access_token(data: dict, expires_delta: timedelta | None) -> str
# - create_refresh_token(user_id: UUID) -> str
# - decode_token(token: str) -> dict  ← lança HTTPException 401 se inválido

# Configurações (SECRET_KEY, algoritmo, expiração) lidas de Settings
# Algoritmo: HS256
```

> **⚠️ Nota de dependência:** `python-jose` é a biblioteca atualmente listada na stack. O ecossistema FastAPI migrou parcialmente para `PyJWT` + `authlib` como alternativas mais ativamente mantidas. Para o MVP, manter `python-jose`. Monitorar e registrar decisão de migração se a biblioteca ficar sem manutenção por mais de 6 meses.

**Critérios de Aceitação:**

- [ ] `hash_password` + `verify_password` funcionam corretamente (bcrypt)
- [ ] `create_access_token` gera JWT com `sub`, `exp` e `role`
- [ ] `decode_token` valida assinatura, expiração e retorna payload
- [ ] `decode_token` lança `HTTPException(401)` para token inválido ou expirado
- [ ] `SECRET_KEY` lida do `.env`, nunca hardcoded
- [ ] Testes unitários cobrem: token válido, token expirado, token adulterado

**Não fazer:**
- Não armazenar tokens no banco aqui (refresh token persistence é CARD-07)
- Não criar rotas de auth aqui

---

### CARD-07

```
Tipo: Task
Épico: EPIC-3
Prioridade: High
Labels: backend, auth, api
Summary: feat(api): criar endpoints de registro e login local
Depende de: CARD-06
```

**Descrição:**

Implementar os endpoints de autenticação local: registro de novo usuário e login com retorno de access + refresh token.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── auth.py      ← POST /auth/register, POST /auth/login, POST /auth/refresh
│   │   └── router.py        ← Agregador de rotas (importa e inclui todos os routers de v1/)
│   └── schemas/
│       └── auth.py          ← RegisterRequest, LoginRequest, TokenResponse
└── tests/
    └── test_api/
        └── test_auth.py
```

**Contratos de API:**

```
POST /api/v1/auth/register
  Body: { email: str, password: str }
  Response 201: { message: "User created" }
  Response 409: { detail: "Email already registered" }

POST /api/v1/auth/login
  Body: { email: str, password: str }
  Response 200: { access_token: str, refresh_token: str, token_type: "bearer" }
  Response 401: { detail: "Invalid credentials" }

POST /api/v1/auth/refresh
  Header: Authorization: Bearer <refresh_token>
  Response 200: { access_token: str, token_type: "bearer" }
  Response 401: { detail: "Invalid or expired refresh token" }
```

**Critérios de Aceitação:**

- [ ] Registro cria usuário com senha hasheada (nunca plain text no banco)
- [ ] Registro retorna 409 se email já existe
- [ ] Login retorna access_token (30min) e refresh_token (7 dias)
- [ ] Refresh retorna novo access_token sem exigir login novamente
- [ ] Testes: registro bem-sucedido, email duplicado, login correto, login errado, refresh válido

**Não fazer:**
- Não implementar OAuth aqui (CARD-08 e CARD-09)
- Não implementar `GET /auth/me` aqui (CARD-10)

---

### CARD-08

```
Tipo: Task
Épico: EPIC-3
Prioridade: Medium
Labels: backend, auth, external-api
Summary: feat(auth): implementar login social via Google OAuth2
Depende de: CARD-07
```

**Descrição:**

Implementar o fluxo OAuth2 Authorization Code com Google. Ao final do fluxo, o usuário recebe o mesmo JWT do login local.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── api/
│       └── v1/
│           └── auth.py      ← adicionar GET /auth/google e GET /auth/google/callback
```

**Fluxo esperado:**

```
GET /auth/google
  → redirect para accounts.google.com/o/oauth2/v2/auth

GET /auth/google/callback?code=XXX
  → troca code por access_token Google
  → busca user_info (email, nome, foto)
  → upsert em users (cria se não existe, atualiza provider_user_id se existe)
  → retorna { access_token, refresh_token, token_type: "bearer" }
```

**Critérios de Aceitação:**

- [ ] `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` lidos do `.env`
- [ ] Primeiro login com Google cria usuário com `auth_provider = 'google'`
- [ ] Login repetido com mesmo Google account atualiza `updated_at`, não cria duplicata
- [ ] Email já existente (cadastro local) recebe erro 409 com mensagem clara
- [ ] Testes com mock do provider Google (não chamar API real nos testes)

**Não fazer:**
- Não exigir senha para usuários Google
- Não implementar Discord aqui (CARD-09)

---

### CARD-09

```
Tipo: Task
Épico: EPIC-3
Prioridade: Medium
Labels: backend, auth, external-api
Summary: feat(auth): implementar login social via Discord OAuth2
Depende de: CARD-07
```

**Descrição:**

Implementar o fluxo OAuth2 com Discord. Capturar username e avatar do usuário Discord. Estrutura idêntica ao CARD-08, mas com endpoints do Discord.

**Arquivos a criar/editar:**

```
backend/
└── app/
    └── api/
        └── v1/
            └── auth.py      ← adicionar GET /auth/discord e GET /auth/discord/callback
```

**Critérios de Aceitação:**

- [ ] `DISCORD_CLIENT_ID` e `DISCORD_CLIENT_SECRET` lidos do `.env`
- [ ] Avatar do Discord salvo em `profile_picture_url`
- [ ] Username do Discord salvo em `username`
- [ ] Mesmo comportamento de deduplicação do CARD-08
- [ ] Testes com mock do provider Discord

---

### CARD-10

```
Tipo: Task
Épico: EPIC-3
Prioridade: Medium
Labels: backend, auth, api
Summary: feat(auth): criar dependências de segurança e endpoint /auth/me
Depende de: CARD-07
```

**Descrição:**

Criar as funções de dependência (FastAPI `Depends`) para proteger rotas e o endpoint que retorna dados do usuário autenticado.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── core/
│       └── dependencies.py  ← get_current_user, require_admin
└── tests/
    └── test_core/
        └── test_dependencies.py
```

**Padrão obrigatório:**

```python
# dependencies.py deve expor:
# - get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User
#   Decodifica JWT, busca user no banco, lança 401 se não encontrar
#
# - require_admin(current_user: User = Depends(get_current_user)) -> User
#   Lança 403 se user.role != 'admin'
#
# Uso nas rotas:
# @router.get("/me")
# async def get_me(user: User = Depends(get_current_user)): ...
#
# @router.post("/admin/crawl")
# async def force_crawl(admin: User = Depends(require_admin)): ...
```

**Critérios de Aceitação:**

- [ ] `GET /auth/me` retorna dados do usuário autenticado (sem `hashed_password`)
- [ ] Rota sem token retorna 401
- [ ] Rota com token expirado retorna 401
- [ ] Rota de admin com usuário `role = 'user'` retorna 403
- [ ] `hashed_password` nunca aparece em nenhuma response da API

---

## EPIC-4 — Crawlers e Ingestão

---

### CARD-11

```
Tipo: Task
Épico: EPIC-4
Prioridade: High
Labels: backend, crawler
Summary: feat(crawlers): criar classe base e contrato de crawler
Depende de: CARD-04
```

**Descrição:**

Criar a abstração base que todos os crawlers devem seguir. Define o contrato de interface e o schema de dado bruto, garantindo que qualquer novo crawler seja intercambiável.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── crawlers/
│       ├── base.py          ← BaseCrawler (ABC) + RawGameData (Pydantic)
│       └── runner.py        ← orquestra todos os crawlers registrados
└── tests/
    └── test_crawlers/
        └── test_base.py     ← testa contrato da classe base com mock
```

**Schema obrigatório:**

```python
class RawGameData(BaseModel):
    title: str                            # Nome original da loja
    price_brl: Decimal                    # Usar Decimal, nunca float
    original_price_brl: Decimal | None = None
    affiliate_url: str
    is_available: bool = True
    store_slug: str                       # Identificador da loja: "steam", "nuuvem"

class BaseCrawler(ABC):
    store_slug: str  # Obrigatório nas subclasses

    @abstractmethod
    async def fetch(self) -> AsyncGenerator[RawGameData, None]: ...
    # Yields um RawGameData por vez — nunca retorna lista inteira de uma vez
```

**Critérios de Aceitação:**

- [ ] `BaseCrawler` é abstrata — instanciar diretamente lança `TypeError`
- [ ] Subclasse sem `fetch()` lança `TypeError`
- [ ] `runner.py` executa todos os crawlers registrados em paralelo com `asyncio.gather`
- [ ] Runner loga erro e **continua** se um crawler individual falhar
- [ ] Runner registra `scraped_at` apenas para coletas bem-sucedidas

**Não fazer:**
- Não implementar lógica de normalização aqui (CARD-12)
- Não hardcodar lista de crawlers no runner — usar registro dinâmico

---

### CARD-12

```
Tipo: Task
Épico: EPIC-4
Prioridade: High
Labels: backend, crawler
Summary: feat(crawlers): implementar normalizer de nomes de jogos
Depende de: CARD-11
```

**Descrição:**

Criar o utilitário de normalização que transforma `title` bruto em `canonical_name` e `slug`. Este é o componente mais crítico para evitar duplicatas no banco.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── core/
│       └── normalizer.py    ← normalize_title(), generate_slug()
└── tests/
    └── test_core/
        └── test_normalizer.py  ← cobrir edge cases
```

**Comportamento esperado:**

```python
normalize_title("Cyberpunk 2077™")          # → "cyberpunk 2077"
normalize_title("Cyberpunk 2077 - PC")      # → "cyberpunk 2077"
normalize_title("Cyberpunk 2077 (Steam)")   # → "cyberpunk 2077"
normalize_title("Grand Theft Auto V")       # → "grand theft auto v"
normalize_title("  ELDEN RING™  ")          # → "elden ring"

generate_slug("cyberpunk 2077")             # → "cyberpunk-2077"
generate_slug("grand theft auto v")         # → "grand-theft-auto-v"
```

**Regras de normalização (obrigatórias):**

1. Converter para lowercase
2. Remover símbolos: `™`, `®`, `©`
3. Remover sufixos de plataforma: ` - PC`, `(PC)`, `(Steam)`, `[PC]`
4. Remover espaços extras (strip + normalize)
5. Para slug: substituir espaços por `-`, remover caracteres não-alfanuméricos exceto `-`

**Critérios de Aceitação:**

- [ ] Todos os casos de exemplo acima passam nos testes
- [ ] Pelo menos 15 casos de teste cobrindo variações reais de títulos de jogos
- [ ] Slugs gerados são únicos para nomes diferentes
- [ ] Slugs não contêm caracteres especiais, acentos ou espaços
- [ ] Função é pura (sem side effects) e facilmente testável

---

### CARD-13

```
Tipo: Task
Épico: EPIC-4
Prioridade: High
Labels: backend, crawler, external-api
Summary: feat(crawlers): implementar integração com API pública da Steam
Depende de: CARD-11, CARD-12
```

**Descrição:**

Consumir a API pública da Steam para obter preços de jogos de PC. A Steam tem uma API relativamente estável, por isso deve ser implementada antes do Nuuvem.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── crawlers/
│       └── steam.py         ← SteamCrawler(BaseCrawler)
└── tests/
    └── test_crawlers/
        └── test_steam.py    ← com mock HTTP (não chamar API real)
```

**Endpoints Steam relevantes:**

```
# Lista de apps (para descoberta):
https://api.steampowered.com/ISteamApps/GetAppList/v2/

# Detalhes e preço de um app específico (cc=br para preço em BRL):
https://store.steampowered.com/api/appdetails?appids={app_id}&cc=br&l=pt
```

**Critérios de Aceitação:**

- [ ] Crawler retorna `RawGameData` válido com `store_slug = "steam"`
- [ ] Preço retornado em BRL (`cc=br`)
- [ ] Jogos `is_free = true` são tratados: `price_brl = 0.00`
- [ ] Jogos sem preço (não disponíveis no BR) têm `is_available = false`
- [ ] Rate limiting respeitado: no máximo 1 request por segundo para a API Steam
- [ ] Testes usam `httpx.MockTransport` — API real nunca chamada nos testes
- [ ] Timeout configurado: 10 segundos por request

**Não fazer:**
- Não buscar 100% do catálogo Steam no MVP — trabalhar com lista curada ou by demand
- Não armazenar `app_id` da Steam no schema do MVP (deixar para Fase 2)

---

### CARD-14

```
Tipo: Task
Épico: EPIC-4
Prioridade: High
Labels: backend, crawler, scraper
Summary: feat(crawlers): implementar scraper para Nuuvem
Depende de: CARD-11, CARD-12
```

**Descrição:**

Implementar o scraper da Nuuvem usando HTTPX + BeautifulSoup4. Este é o crawler mais frágil (scraping de HTML) e exige tratamento de erro robusto.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── crawlers/
│       └── nuuvem.py        ← NuuvemCrawler(BaseCrawler)
└── tests/
    └── test_crawlers/
        └── test_nuuvem.py   ← com HTML fixture, não request real
```

**Critérios de Aceitação:**

- [ ] Crawler retorna `RawGameData` válido com `store_slug = "nuuvem"`
- [ ] Preço extraído em BRL sem caracteres extras ("R$ 49,90" → `Decimal("49.90")`)
- [ ] Jogos em promoção extraem `original_price_brl` e `discount_percent` corretamente
- [ ] Jogos sem estoque retornam `is_available = false`
- [ ] Testes usam fixtures de HTML salvo — nunca acessar Nuuvem real durante testes
- [ ] `try/except` envolve o parsing de cada campo individualmente (falha em 1 campo não cancela o jogo inteiro)
- [ ] User-Agent realista nos headers do HTTPX

**Não fazer:**
- Não usar `requests` síncrono — usar HTTPX async
- Não logar HTML completo em caso de erro (vazar dados sensíveis de resposta)

---

## EPIC-5 — API REST

---

### CARD-15

```
Tipo: Task
Épico: EPIC-5
Prioridade: High
Labels: backend, api
Summary: feat(api): implementar endpoints de busca e listagem de jogos
Depende de: CARD-04, CARD-12
```

**Descrição:**

Criar os endpoints públicos de consumo de dados: listagem paginada de jogos e busca por nome. São as rotas centrais do produto.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── games.py     ← GET /games, GET /games/{slug}
│   │       └── search.py    ← GET /search?q=
│   └── schemas/
│       ├── game.py          ← GameRead, GameWithPrices
│       └── price.py         ← PriceRead
└── tests/
    └── test_api/
        └── test_games.py
```

**Contratos de API:**

```
GET /api/v1/games?page=1&limit=20
  Response 200: { items: [GameRead], total: int, page: int, pages: int }

GET /api/v1/games/{slug}
  Response 200: GameWithPrices  ← game + prices ordenados por price_brl ASC
  Response 404: { detail: "Game not found" }

GET /api/v1/search?q=cyberpunk&limit=10
  Response 200: { items: [GameRead], total: int }
  Response 422: se q ausente ou vazio
```

**Critérios de Aceitação:**

- [ ] Paginação funciona: `page` e `limit` com defaults (1 e 20)
- [ ] Busca usa `ILIKE` em `canonical_name` (case-insensitive)
- [ ] `GET /games/{slug}` retorna preços ordenados do menor para o maior
- [ ] Preços com `is_available = false` são incluídos mas marcados claramente
- [ ] `hashed_password` nunca vaza em nenhuma response
- [ ] Testes: busca com resultado, busca sem resultado, slug inválido, paginação

**Não fazer:**
- Não implementar full-text search com PostgreSQL ainda (ILIKE é suficiente para o MVP)
- Não adicionar filtros avançados (por loja, faixa de preço) no MVP

---

### CARD-16

```
Tipo: Task
Épico: EPIC-5
Prioridade: Medium
Labels: backend, api, admin
Summary: feat(api): implementar endpoints de administração
Depende de: CARD-10, CARD-13, CARD-14
```

**Descrição:**

Criar as rotas administrativas protegidas por `require_admin`. Permitem ao admin forçar re-scraping, gerenciar lojas e corrigir `canonical_name` de jogos.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   └── api/
│       └── v1/
│           └── admin.py     ← rotas /admin/*
└── tests/
    └── test_api/
        └── test_admin.py
```

**Contratos de API:**

```
POST /api/v1/admin/crawl
  Auth: Bearer (admin)
  Body: { store_slug?: str }  ← null = rodar todos os crawlers
  Response 202: { message: "Crawl job started", stores: [str] }

GET /api/v1/admin/stores
  Auth: Bearer (admin)
  Response 200: [StoreRead]

PATCH /api/v1/admin/stores/{id}
  Auth: Bearer (admin)
  Body: { is_active: bool }
  Response 200: StoreRead

PATCH /api/v1/admin/games/{id}
  Auth: Bearer (admin)
  Body: { canonical_name: str }
  Response 200: GameRead
```

**Critérios de Aceitação:**

- [ ] Todas as rotas retornam 403 para `role = 'user'`
- [ ] `POST /admin/crawl` executa crawlers de forma assíncrona (não bloqueia a response)
- [ ] `PATCH /admin/games/{id}` regenera o `slug` se `canonical_name` mudar
- [ ] Testes: acesso com admin, acesso negado com user, forçar crawl

---

## Sumário de Dependências

```
CARD-01 (Setup)
  └── CARD-02 (CI)
  └── CARD-03 (DB Connection)
        └── CARD-04 (Models: stores/games/prices)
        │     └── CARD-11 (Base Crawler)
        │           └── CARD-12 (Normalizer)
        │                 └── CARD-13 (Steam Crawler)
        │                 └── CARD-14 (Nuuvem Crawler)
        │                 └── CARD-15 (Games API)
        │                       └── CARD-16 (Admin API)
        └── CARD-05 (Model: users)
              └── CARD-06 (JWT + Security)
                    └── CARD-07 (Auth Endpoints + router.py)
                          └── CARD-08 (Google OAuth)
                          └── CARD-09 (Discord OAuth)
                          └── CARD-10 (Dependencies + /me)
                                └── CARD-16 (Admin API)
                                └── CARD-22 (Refresh Token Revogation)

CARD-16 (Admin API — todas as deps resolvidas)
  └── CARD-17 (Rate Limiting)
        └── CARD-23 (Nginx + Cloudflare IP Passthrough)

CARD-15 (Games API) + CARD-10 (Dependencies + /me)
  └── CARD-18 (Frontend Setup)
        └── CARD-19 (Search Page)
        └── CARD-20 (Auth Pages)
        └── CARD-21 (Game Detail Page)
```

---

## EPIC-3.5 — Segurança de Autenticação

---

### CARD-22

```
Tipo: Task
Épico: EPIC-3
Prioridade: High
Labels: backend, auth, security
Summary: feat(auth): implementar revogação de refresh tokens
Depende de: CARD-10
```

**Descrição:**

Refresh tokens com validade de 7 dias sem mecanismo de revogação são um risco de segurança real: tokens vazados permanecem válidos até expirar naturalmente. Este card implementa uma blacklist de tokens via tabela `revoked_tokens` no PostgreSQL. Redis não é necessário no MVP — a abordagem in-database é suficiente para o volume esperado e elimina uma dependência de infraestrutura.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   ├── models/
│   │   └── revoked_token.py     ← model RevokedToken
│   ├── core/
│   │   └── security.py          ← atualizar decode_token() para checar blacklist
│   └── api/
│       └── v1/
│           └── auth.py          ← adicionar POST /auth/logout
├── migrations/
│   └── versions/
│       └── XXXX_create_revoked_tokens.py
└── tests/
    └── test_api/
        └── test_auth_revocation.py
```

**Schema da tabela `revoked_tokens`:**

```sql
CREATE TABLE revoked_tokens (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_jti   VARCHAR(255) NOT NULL UNIQUE,  -- JWT ID (campo `jti` do payload)
    revoked_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at  TIMESTAMP NOT NULL             -- para limpeza periódica via cron
);
CREATE INDEX idx_revoked_tokens_jti ON revoked_tokens (token_jti);
```

**Contratos de API:**

```
POST /api/v1/auth/logout
  Header: Authorization: Bearer <refresh_token>
  Response 200: { message: "Logged out successfully" }
  Response 401: token inválido ou já revogado

# Comportamento:
# 1. Decodifica o refresh_token
# 2. Extrai o campo `jti` (JWT ID único por token)
# 3. Insere o jti na tabela revoked_tokens com expires_at = token.exp
# 4. Qualquer uso posterior do mesmo token retorna 401
```

**Critérios de Aceitação:**

- [ ] `create_refresh_token()` gera tokens com campo `jti` (UUID aleatório)
- [ ] `decode_token()` verifica o `jti` contra `revoked_tokens` após validar assinatura
- [ ] `POST /auth/logout` insere o jti na blacklist e retorna 200
- [ ] Usar o refresh token após logout retorna 401
- [ ] Token de outro usuário não pode ser revogado via logout (validação de ownership)
- [ ] Testes: logout bem-sucedido, uso de token revogado, token inválido

**Débito técnico a registrar no `llm_context.md`:**
```
- Implementar job periódico para limpar revoked_tokens expirados:
  DELETE FROM revoked_tokens WHERE expires_at < NOW()
  Pode ser um cron via GitHub Actions ou APScheduler na Fase 2
```

**Não fazer:**
- Não usar Redis para a blacklist no MVP (complexidade desnecessária)
- Não revogar access tokens (30min de validade é aceitável; só revogar refresh)

---

## EPIC-6 — Segurança e Middleware

---

### CARD-17

```
Tipo: Task
Épico: EPIC-6
Prioridade: High
Labels: backend, security, middleware
Summary: feat(security): implementar rate limiting com slowapi
Depende de: CARD-16
```

**Descrição:**

Adicionar rate limiting global na API usando `slowapi`. O rate limiting deve proteger todas as rotas públicas contra abuso e as rotas de admin contra brute force. Esta é uma camada de segurança obrigatória antes de qualquer deploy público.

**Arquivos a criar/editar:**

```
backend/
├── app/
│   ├── core/
│   │   └── rate_limit.py    ← configuração do slowapi (limiter, key_func)
│   └── main.py              ← registrar middleware do slowapi
└── tests/
    └── test_core/
        └── test_rate_limit.py
```

**Configuração esperada:**

```python
# Limites sugeridos:
# - Rotas públicas (search, games): 60 requests/minuto por IP
# - Rotas de auth (login, register): 10 requests/minuto por IP
# - Rotas de admin: 30 requests/minuto por IP
# - Rota de crawl: 2 requests/minuto por IP (admin only)

# Key function: usar IP do client (com suporte a X-Forwarded-For para proxy/nginx)
```

**Critérios de Aceitação:**

- [ ] `slowapi` integrado como middleware no FastAPI
- [ ] Rotas públicas limitadas a 60 req/min por IP
- [ ] Rotas de auth limitadas a 10 req/min por IP
- [ ] Response `429 Too Many Requests` retornado quando limite é excedido
- [ ] Header `X-RateLimit-Remaining` presente nas responses
- [ ] Testes: request dentro do limite, request excedendo limite

**Não fazer:**
- Não usar Redis para armazenamento de contadores no MVP (in-memory é suficiente)
- Não implementar rate limiting por usuário autenticado (apenas por IP no MVP)

---

## EPIC-7 — Frontend

---

### CARD-18

```
Tipo: Task
Épico: EPIC-7
Prioridade: High
Labels: frontend, setup
Summary: chore(frontend): setup inicial do React SPA com Vite + TypeScript
Depende de: CARD-15, CARD-10
```

**Descrição:**

Configurar o projeto frontend com React 18, TypeScript, Vite, TailwindCSS e Zustand. Criar a estrutura de pastas, configuração do Axios para comunicação com a API, e a base de navegação com React Router.

**Arquivos a criar/editar:**

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.tsx          ← layout base com header/footer
│   ├── pages/
│   │   └── Home.tsx            ← página inicial placeholder
│   ├── hooks/
│   │   └── useAuth.ts          ← hook de autenticação (store Zustand)
│   ├── services/
│   │   └── api.ts              ← instância Axios configurada com baseURL e interceptors
│   ├── store/
│   │   └── authStore.ts        ← Zustand store para auth state
│   ├── types/
│   │   ├── game.ts             ← tipos alinhados com schemas do backend
│   │   └── auth.ts             ← tipos de auth (TokenResponse, User)
│   ├── App.tsx                 ← React Router + routes
│   ├── main.tsx                ← entry point
│   └── index.css               ← TailwindCSS base
├── .env.example                ← VITE_API_URL=http://localhost:8000/api/v1
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── eslint.config.js
```

**Critérios de Aceitação:**

- [ ] `npm run dev` inicia o frontend em `localhost:5173` sem erros
- [ ] Axios configurado com `baseURL` lido de `VITE_API_URL`
- [ ] Interceptor de request adiciona `Authorization: Bearer` se token existir no store
- [ ] Interceptor de response trata 401 (limpa token e redireciona para login)
- [ ] React Router configurado com rotas: `/`, `/search`, `/games/:slug`, `/login`, `/register`
- [ ] Layout base renderiza header com logo e navegação
- [ ] `npm run build` gera bundle sem erros de TypeScript
- [ ] ESLint configurado e passando sem erros

**Não fazer:**
- Não implementar páginas completas aqui (apenas placeholders com routing)
- Não adicionar SSR ou Next.js — SPA puro com Vite
- Não instalar dependências além das listadas na stack

---

### CARD-19

```
Tipo: Task
Épico: EPIC-7
Prioridade: High
Labels: frontend, feature
Summary: feat(frontend): implementar página de busca e listagem de jogos
Depende de: CARD-18
```

**Descrição:**

Implementar a página principal do LootPrice: campo de busca com resultados em tempo real e listagem paginada de jogos. Cada card de jogo exibe título, imagem de capa, menor preço entre as lojas e badge de desconto.

**Arquivos a criar/editar:**

```
frontend/
└── src/
    ├── components/
    │   ├── SearchBar.tsx        ← input de busca com debounce
    │   ├── GameCard.tsx         ← card individual de jogo
    │   └── Pagination.tsx       ← componente de paginação
    ├── pages/
    │   ├── Home.tsx             ← listagem paginada com busca
    │   └── Search.tsx           ← resultados de busca
    └── services/
        └── gameService.ts       ← funções: searchGames(), listGames(), getGameBySlug()
```

**Critérios de Aceitação:**

- [ ] Campo de busca com debounce de 300ms (não dispara request a cada tecla)
- [ ] Resultados de busca exibem: título, capa, menor preço, loja do menor preço
- [ ] Paginação funcional com navegação entre páginas
- [ ] Estado de loading visível durante requests
- [ ] Estado de "nenhum resultado" exibido para buscas sem match
- [ ] Validação com Zod nos dados recebidos da API
- [ ] Layout responsivo (mobile-first)
- [ ] Cards clicáveis redirecionam para `/games/:slug`

**Não fazer:**
- Não implementar filtros avançados (por loja, faixa de preço) no MVP
- Não implementar infinite scroll — paginação tradicional é suficiente

---

### CARD-20

```
Tipo: Task
Épico: EPIC-7
Prioridade: High
Labels: frontend, auth, feature
Summary: feat(frontend): implementar páginas de login e registro
Depende de: CARD-18
```

**Descrição:**

Criar as páginas de autenticação: login local, registro e botões de login social (Google e Discord). Integrar com o Zustand auth store para gerenciar estado de sessão.

**Arquivos a criar/editar:**

```
frontend/
└── src/
    ├── pages/
    │   ├── Login.tsx            ← formulário de login + botões OAuth
    │   └── Register.tsx         ← formulário de registro
    ├── components/
    │   ├── AuthForm.tsx         ← formulário reutilizável (login/register)
    │   └── OAuthButtons.tsx     ← botões Google e Discord
    └── hooks/
        └── useAuth.ts           ← atualizar com funções login(), register(), logout()
```

**Critérios de Aceitação:**

- [ ] Formulário de login com validação client-side (React Hook Form + Zod)
- [ ] Formulário de registro com validação (email válido, senha mínima 8 caracteres)
- [ ] Botões de login social (Google, Discord) redirecionam para as rotas OAuth do backend
- [ ] Token armazenado no Zustand store e persistido em `localStorage`
- [ ] Refresh token gerenciado automaticamente (interceptor Axios)
- [ ] Feedback visual: erro de credenciais, email duplicado, sucesso
- [ ] Após login bem-sucedido, redireciona para a página anterior ou home
- [ ] Usuário autenticado vê seu email/nome no header em vez de "Login"

**Não fazer:**
- Não armazenar tokens em cookies (usar localStorage para simplicidade no MVP)
- Não implementar "esqueci minha senha" no MVP

---

### CARD-21

```
Tipo: Task
Épico: EPIC-7
Prioridade: High
Labels: frontend, feature
Summary: feat(frontend): implementar página de detalhe do jogo com comparação de preços
Depende de: CARD-19
```

**Descrição:**

Implementar a página de detalhe de um jogo (`/games/:slug`), exibindo todos os preços disponíveis ordenados do menor ao maior, com links diretos para compra em cada loja. Esta é a página que entrega a proposta de valor central do LootPrice.

**Arquivos a criar/editar:**

```
frontend/
└── src/
    ├── pages/
    │   └── GameDetail.tsx       ← detalhe do jogo com tabela de preços
    ├── components/
    │   ├── PriceTable.tsx        ← tabela/lista de preços por loja
    │   └── PriceBadge.tsx        ← badge visual de desconto (ex: "-75%")
    └── types/
        └── game.ts              ← atualizar GameWithPrices type
```

**Critérios de Aceitação:**

- [ ] Exibe título, capa e todos os preços do jogo
- [ ] Preços ordenados do menor para o maior (destaque visual no menor)
- [ ] Cada preço exibe: nome da loja, preço atual, preço original (se em desconto), % de desconto
- [ ] Botão "Comprar" em cada linha redireciona para a `affiliate_url` da loja (abre em nova aba)
- [ ] Exibe timestamp "Atualizado há X minutos" baseado no `scraped_at`
- [ ] Jogos indisponíveis (`is_available = false`) exibidos com visual de desabilitado
- [ ] Página retorna 404 amigável se slug não existir
- [ ] Layout responsivo

**Não fazer:**
- Não implementar gráfico de histórico de preços (Fase 3)
- Não implementar botão de "adicionar à wishlist" (Fase 2)

---

## EPIC-8 — Infraestrutura de Deploy

---

### CARD-23

```
Tipo: Task
Épico: EPIC-8
Prioridade: Medium
Labels: infra, deploy, security
Summary: chore(infra): configurar Nginx com suporte a Cloudflare IP passthrough
Depende de: CARD-17
```

**Descrição:**

Quando a aplicação está atrás do Cloudflare Tunnel + Nginx, o IP real do cliente não chega diretamente ao FastAPI — chega o IP do proxy Cloudflare. Sem tratamento correto, o `slowapi` aplicará rate limiting por IP do Cloudflare (não do cliente real), tornando o throttling ineficaz ou bloqueando todos os usuários ao mesmo tempo.

Este card configura o Nginx para extrair o IP real do header `CF-Connecting-IP` (enviado pelo Cloudflare) e o FastAPI/slowapi para usar esse IP como chave de rate limiting.

**Arquivos a criar/editar:**

```
lootprice/
├── nginx/
│   ├── nginx.conf              ← configuração principal do Nginx
│   └── sites/
│       └── lootprice.conf      ← virtual host com proxy_pass para FastAPI
└── docker-compose.yml          ← adicionar service nginx (opcional para dev, obrigatório para prod)
```

**Configuração Nginx obrigatória:**

```nginx
# nginx/sites/lootprice.conf
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass         http://backend:8000;
        proxy_set_header   Host $host;

        # Repassa o IP real do Cloudflare para o FastAPI
        proxy_set_header   X-Real-IP $http_cf_connecting_ip;
        proxy_set_header   X-Forwarded-For $http_cf_connecting_ip;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

**Configuração do slowapi (atualizar CARD-17):**

```python
# rate_limit.py — key_func deve ler X-Forwarded-For quando disponível
from slowapi.util import get_remote_address

def get_real_ip(request: Request) -> str:
    # CF-Connecting-IP já foi reescrito pelo Nginx para X-Forwarded-For
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return get_remote_address(request)
```

**Critérios de Aceitação:**

- [ ] Nginx configurado e documentado em `nginx/`
- [ ] `CF-Connecting-IP` repassado como `X-Real-IP` e `X-Forwarded-For` para o backend
- [ ] `slowapi` usa `get_real_ip()` como `key_func` (não `get_remote_address` padrão)
- [ ] Teste manual: logs do FastAPI exibem IP do cliente real, não IP do Cloudflare
- [ ] `docker-compose.yml` inclui service `nginx` apontando para o backend
- [ ] Documentado no `README.md` na seção de deploy

**Não fazer:**
- Não confiar cegamente em qualquer header `X-Forwarded-For` sem validar que vem do Cloudflare (para prod, usar lista de IPs do Cloudflare)
- Não adicionar configuração de SSL no Nginx — o Cloudflare Tunnel já gerencia HTTPS

> **📝 Nota para o desenvolvedor:** Este card é relevante mesmo usando a máquina Ubuntu local com Cloudflare Tunnel. Sem ele, o rate limiting funciona localmente mas falha em produção.

---

## Instrução Final para LLM (Jira MCP)

Ao processar este arquivo para criar cards no Jira:

1. Criar um Épico para cada seção `## EPIC-N` (total: 8 épicos)
2. Criar uma Issue do tipo `Task` para cada `### CARD-N` (total: 23 cards)
3. Preencher `summary` com o valor do campo `Summary:` no card
4. Preencher `description` com todo o conteúdo do card em Markdown
5. Definir `priority` conforme o campo `Prioridade:`
6. Definir `labels` conforme o campo `Labels:`
7. Usar o campo `Depende de:` para criar `issue links` do tipo `blocks/is blocked by`
8. Linkar cada Task ao seu Épico pai conforme o campo `Épico:`
9. **Não resumir a descrição** — o conteúdo completo dos critérios de aceitação deve estar no card

### Cards adicionados na revisão de 2026-06-03

| Card | Motivo da adição |
|---|---|
| CARD-22 | Refresh tokens sem revogação são risco de segurança documentado nos riscos do architecture.md mas sem card correspondente |
| CARD-23 | Gotcha crítico: Cloudflare Tunnel + Nginx sem `CF-Connecting-IP` torna rate limiting ineficaz por IP real |

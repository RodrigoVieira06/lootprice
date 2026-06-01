# LootPrice — Jira Project Cards (MVP)

> **Instrução para LLM que processar este arquivo:**
> Este documento define os cards do Jira para o MVP do LootPrice.
> Cada card contém: tipo, épico pai, descrição técnica precisa, critérios de aceitação mensuráveis, arquivos a criar/editar, dependências entre cards e o que explicitamente **não** fazer.
> Ao criar um card no Jira via MCP, use o campo `summary` para o título, `description` para o corpo completo em Markdown, `labels` para as labels e `priority` para a prioridade.
> **Não resumir, não omitir critérios de aceitação, não alterar os títulos.**

---

## Estrutura de Épicos

| Épico | Chave Sugerida | Ordem |
|---|---|---|
| Infraestrutura Base | EPIC-1 | 1º — pré-requisito para tudo |
| Banco de Dados | EPIC-2 | 2º — pré-requisito para crawlers e auth |
| Autenticação | EPIC-3 | 3º — paralelo ao épico de crawlers |
| Crawlers e Ingestão | EPIC-4 | 4º — depende do banco |
| API REST | EPIC-5 | 5º — depende de banco + crawlers |

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
│   │   └── v1/
│   │       └── auth.py      ← POST /auth/register, POST /auth/login, POST /auth/refresh
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
Depende de: CARD-04, CARD-10, CARD-12
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
        │                       └── CARD-16 (Admin API)
        └── CARD-05 (Model: users)
              └── CARD-06 (JWT + Security)
                    └── CARD-07 (Auth Endpoints)
                          └── CARD-08 (Google OAuth)
                          └── CARD-09 (Discord OAuth)
                          └── CARD-10 (Dependencies + /me)
                                └── CARD-15 (Games API)
                                └── CARD-16 (Admin API)
```

---

## Instrução Final para LLM (Jira MCP)

Ao processar este arquivo para criar cards no Jira:

1. Criar um Épico para cada seção `## EPIC-N`
2. Criar uma Issue do tipo `Task` para cada `### CARD-N`
3. Preencher `summary` com o valor do campo `Summary:` no card
4. Preencher `description` com todo o conteúdo do card em Markdown
5. Definir `priority` conforme o campo `Prioridade:`
6. Definir `labels` conforme o campo `Labels:`
7. Usar o campo `Depende de:` para criar `issue links` do tipo `blocks/is blocked by`
8. Linkar cada Task ao seu Épico pai conforme o campo `Épico:`
9. **Não resumir a descrição** — o conteúdo completo dos critérios de aceitação deve estar no card

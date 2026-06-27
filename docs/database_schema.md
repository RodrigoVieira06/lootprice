# LootPrice — Database Schema

> **Versão:** 0.3.0-MVP
> **Banco:** PostgreSQL 15+
> **ORM:** SQLModel + Alembic (migrations obrigatórias)
> **Última atualização:** 2026-06-26
> **Audiência:** Desenvolvedores e LLMs de apoio

---

## Objetivo

Este documento define o schema alvo do MVP e reserva pontos de evolução para fases futuras sem criar complexidade antes da hora.

O LootPrice precisa separar seis conceitos:

1. **Jogo canônico** (`games`): entidade normalizada usada na busca e comparação.
2. **Produto da loja** (`store_products`): listing específico de uma loja, com `external_id`, URL e título bruto.
3. **Preço atual** (`prices`): snapshot mais recente de um produto de loja.
4. **Política da loja** (`stores`): fonte de ingestão permitida, flags de afiliado/compliance e nível de risco.
5. **Execução de coleta** (`crawler_runs`): observabilidade de ingestão por loja.
6. **Clique afiliado** (`affiliate_clicks`): métrica interna antes do redirect para a loja.

Essa separação evita gaps comuns: Steam usa `app_id`, Nuuvem depende de URL/slug, marketplaces futuros podem ter múltiplas ofertas para o mesmo jogo, e a normalização automática pode precisar de correção manual.

Detalhes de negócio e risco por loja ficam em `docs/affiliate_store_strategy.md`.

---

## Decisões de Design

| Decisão | Escolha | Motivo |
|---|---|---|
| IDs principais | `UUID` | Evita enumeração e facilita evolução |
| IDs de lookup estático | `UUID` também | Mantém consistência entre modelos |
| Dinheiro | `NUMERIC(10,2)` | Nunca usar `FLOAT` para valores monetários |
| Moeda | `currency CHAR(3)` | MVP usa `BRL`, mas mantém base para expansão |
| Preço atual | `prices` como snapshot | Histórico fica fora do MVP |
| Produto por loja | `store_products` | Preserva `external_id`, URL, título bruto e vínculo canônico |
| Fonte por loja | `stores.ingestion_source` | Evita assumir crawler quando API/feed/manual é o caminho permitido |
| Afiliado | Redirect interno | Frontend usa `/api/v1/out/{price_id}`; URL externa não deve ser exposta direto |
| Métricas | `affiliate_clicks` no MVP | Cliques são necessários antes de medir conversão/comissão |
| Normalização | `games.canonical_name` editável | Corrige edge cases manualmente |
| Auth social | `oauth_accounts` separado de `users` | Evita acoplar usuário a um único provider |
| Revogação JWT | `revoked_tokens` | Logout real sem Redis no MVP |
| Auditoria básica | `created_at`, `updated_at` | Padrão mínimo para debug e evolução |

---

## Extensões PostgreSQL

Ativar na migration inicial:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
```

- `pgcrypto`: habilita `gen_random_uuid()`.
- `citext`: permite e-mail case-insensitive em `users.email`.

---

## Diagrama de Relacionamentos

```text
users ──(1:N)── oauth_accounts

users ──(N:N futuro)── games        via wishlists

stores ──(1:N)── store_products ──(1:1)── prices
games  ──(1:N)── store_products

stores ──(1:N)── crawler_runs ──(1:N futuro)── crawler_run_items

prices ──(1:N)── affiliate_clicks

prices ──(1:N futuro)── price_history
affiliate_clicks ──(1:N futuro)── affiliate_conversions
```

---

## Enums Lógicos

Implementar como `VARCHAR` com `CHECK` no MVP. Migrar para enum PostgreSQL só se houver ganho real.

```sql
user_role:        'user' | 'admin'
auth_provider:    'google' | 'discord'
crawler_status:   'running' | 'success' | 'partial_failure' | 'failed'
product_platform: 'pc' | 'playstation' | 'xbox' | 'nintendo' | 'mobile'
ingestion_source: 'api' | 'feed' | 'scraper' | 'manual' | 'disabled'
store_risk_level: 'low' | 'medium' | 'high'
store_compliance_status: 'unknown' | 'approved' | 'blocked' | 'needs_review'
affiliate_conversion_status: 'pending' | 'approved' | 'rejected' | 'paid'
```

No MVP, `product_platform` deve ser sempre `pc`.

---

## Tabelas MVP

### `users`

Conta principal do usuário. Login local e login social são suportados sem limitar o usuário a um único provider.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `email` | `CITEXT` | NOT NULL, UNIQUE | E-mail case-insensitive |
| `display_name` | `VARCHAR(120)` | NULLABLE | Nome exibível |
| `hashed_password` | `TEXT` | NULLABLE | Obrigatório apenas para login local |
| `avatar_url` | `TEXT` | NULLABLE | Avatar local ou do provider |
| `role` | `VARCHAR(20)` | NOT NULL, DEFAULT `'user'` | `user` ou `admin` |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT `true` | Desativação lógica |
| `last_login_at` | `TIMESTAMPTZ` | NULLABLE | Último login bem-sucedido |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

**Constraints e índices:**

```sql
ALTER TABLE users
  ADD CONSTRAINT chk_users_role
  CHECK (role IN ('user', 'admin'));

CREATE UNIQUE INDEX uq_users_email ON users (email);
```

**Regra de API:** `hashed_password` nunca aparece em schemas de response.

---

### `oauth_accounts`

Vínculos OAuth. Permite que o mesmo usuário conecte Google e Discord no futuro.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `user_id` | `UUID` | NOT NULL, FK `users.id` ON DELETE CASCADE | Dono da conta |
| `provider` | `VARCHAR(20)` | NOT NULL | `google` ou `discord` |
| `provider_user_id` | `VARCHAR(255)` | NOT NULL | ID no provider |
| `provider_email` | `CITEXT` | NULLABLE | E-mail retornado pelo provider |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

```sql
ALTER TABLE oauth_accounts
  ADD CONSTRAINT chk_oauth_provider
  CHECK (provider IN ('google', 'discord'));

ALTER TABLE oauth_accounts
  ADD CONSTRAINT uq_oauth_provider_user
  UNIQUE (provider, provider_user_id);

CREATE INDEX idx_oauth_accounts_user_id ON oauth_accounts (user_id);
```

---

### `revoked_tokens`

Blacklist de refresh tokens revogados. Necessária para logout real e resposta a token vazado.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `token_jti` | `UUID` | NOT NULL, UNIQUE | Campo `jti` do refresh token |
| `user_id` | `UUID` | NULLABLE, FK `users.id` ON DELETE SET NULL | Usuário associado, se disponível |
| `revoked_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Momento da revogação |
| `expires_at` | `TIMESTAMPTZ` | NOT NULL | Expiração original do token |

```sql
CREATE UNIQUE INDEX uq_revoked_tokens_jti ON revoked_tokens (token_jti);
CREATE INDEX idx_revoked_tokens_expires_at ON revoked_tokens (expires_at);
```

**Débito controlado:** limpeza periódica com `DELETE FROM revoked_tokens WHERE expires_at < NOW()` fica para Fase 2.

---

### `stores`

Lojas/fontes de dados. Populada via seed, administrável no painel.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `name` | `VARCHAR(100)` | NOT NULL | Nome exibível |
| `slug` | `VARCHAR(100)` | NOT NULL, UNIQUE | `steam`, `nuuvem` |
| `base_url` | `TEXT` | NOT NULL | URL base |
| `logo_url` | `TEXT` | NULLABLE | Uso futuro no frontend/admin |
| `crawler_key` | `VARCHAR(100)` | NULLABLE, UNIQUE | Chave lógica do crawler/importer: `steam`, `nuuvem` |
| `ingestion_source` | `VARCHAR(30)` | NOT NULL, DEFAULT `'disabled'` | `api`, `feed`, `scraper`, `manual` ou `disabled` |
| `allows_price_display` | `BOOLEAN` | NOT NULL, DEFAULT `false` | Termos permitem exibir preço no LootPrice |
| `allows_affiliate_deeplink` | `BOOLEAN` | NOT NULL, DEFAULT `false` | Termos permitem link direto para produto |
| `allows_tracking_subid` | `BOOLEAN` | NOT NULL, DEFAULT `false` | Programa permite `subid`, `click_id` ou equivalente |
| `allows_scraping` | `BOOLEAN` | NOT NULL, DEFAULT `false` | Termos/autorização permitem scraper |
| `affiliate_network` | `VARCHAR(100)` | NULLABLE | Rede/parceiro: direto, Awin, Impact, etc. |
| `affiliate_link_template` | `TEXT` | NULLABLE | Template seguro para gerar URL afiliada no redirect |
| `compliance_status` | `VARCHAR(30)` | NOT NULL, DEFAULT `'unknown'` | `unknown`, `approved`, `blocked`, `needs_review` |
| `risk_level` | `VARCHAR(20)` | NOT NULL, DEFAULT `'medium'` | `low`, `medium` ou `high` |
| `terms_url` | `TEXT` | NULLABLE | URL dos termos/programa validado |
| `compliance_notes` | `TEXT` | NULLABLE | Resumo da decisão e limitações |
| `is_marketplace` | `BOOLEAN` | NOT NULL, DEFAULT `false` | `true` para G2A/Eneba/Kinguin no futuro |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT `true` | Liga/desliga coleta e exibição |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

```sql
CREATE UNIQUE INDEX uq_stores_slug ON stores (slug);
CREATE UNIQUE INDEX uq_stores_crawler_key ON stores (crawler_key)
  WHERE crawler_key IS NOT NULL;

ALTER TABLE stores
  ADD CONSTRAINT chk_stores_ingestion_source
  CHECK (ingestion_source IN ('api', 'feed', 'scraper', 'manual', 'disabled'));

ALTER TABLE stores
  ADD CONSTRAINT chk_stores_compliance_status
  CHECK (compliance_status IN ('unknown', 'approved', 'blocked', 'needs_review'));

ALTER TABLE stores
  ADD CONSTRAINT chk_stores_risk_level
  CHECK (risk_level IN ('low', 'medium', 'high'));

CREATE INDEX idx_stores_ingestion_source ON stores (ingestion_source);
CREATE INDEX idx_stores_compliance_status ON stores (compliance_status);
CREATE INDEX idx_stores_risk_level ON stores (risk_level);
```

**Seed MVP:**

```sql
INSERT INTO stores (
  name,
  slug,
  base_url,
  crawler_key,
  ingestion_source,
  allows_price_display,
  allows_affiliate_deeplink,
  allows_tracking_subid,
  allows_scraping,
  compliance_status,
  risk_level,
  is_marketplace
) VALUES
  (
    'Steam',
    'steam',
    'https://store.steampowered.com',
    'steam',
    'api',
    true,
    false,
    false,
    false,
    'needs_review',
    'medium',
    false
  ),
  (
    'Nuuvem',
    'nuuvem',
    'https://www.nuuvem.com',
    'nuuvem',
    'disabled',
    false,
    false,
    false,
    false,
    'needs_review',
    'medium',
    false
  );
```

**Regra de compliance:** `ingestion_source = 'scraper'` só pode ser usado se `allows_scraping = true` e `compliance_status = 'approved'`. Para `feed` ou `api`, registrar `terms_url` e limitações em `compliance_notes`.

---

### `games`

Jogo canônico, independente da loja.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `title` | `VARCHAR(255)` | NOT NULL | Título exibível canônico |
| `canonical_name` | `VARCHAR(255)` | NOT NULL | Nome normalizado para deduplicação |
| `slug` | `VARCHAR(255)` | NOT NULL, UNIQUE | URL-friendly |
| `cover_url` | `TEXT` | NULLABLE | Capa principal |
| `platform` | `VARCHAR(30)` | NOT NULL, DEFAULT `'pc'` | MVP usa apenas `pc` |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT `true` | Ocultar sem deletar |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

```sql
ALTER TABLE games
  ADD CONSTRAINT chk_games_platform
  CHECK (platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile'));

CREATE UNIQUE INDEX uq_games_slug ON games (slug);
CREATE INDEX idx_games_canonical_name ON games (canonical_name);
CREATE INDEX idx_games_title ON games (title);
```

**Regra de negócio:** `canonical_name` pode ser editado por admin. `title` deve ser estável e exibível.

---

### `store_products`

Produto/listing de uma loja. Esta tabela absorve diferenças entre Steam, Nuuvem e fontes futuras.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `store_id` | `UUID` | NOT NULL, FK `stores.id` ON DELETE CASCADE | Loja origem |
| `game_id` | `UUID` | NOT NULL, FK `games.id` ON DELETE CASCADE | Jogo canônico |
| `external_id` | `VARCHAR(255)` | NULLABLE | Ex: Steam `app_id`; Nuuvem pode ser slug |
| `store_title` | `VARCHAR(255)` | NOT NULL | Título bruto da loja |
| `store_url` | `TEXT` | NOT NULL | URL do produto |
| `cover_url` | `TEXT` | NULLABLE | Capa específica da loja |
| `platform` | `VARCHAR(30)` | NOT NULL, DEFAULT `'pc'` | MVP usa apenas `pc` |
| `is_available` | `BOOLEAN` | NOT NULL, DEFAULT `true` | Produto disponível na loja |
| `first_seen_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Primeira coleta |
| `last_seen_at` | `TIMESTAMPTZ` | NULLABLE | Última coleta em que apareceu |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

```sql
ALTER TABLE store_products
  ADD CONSTRAINT chk_store_products_platform
  CHECK (platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile'));

CREATE UNIQUE INDEX uq_store_products_external_id
  ON store_products (store_id, external_id)
  WHERE external_id IS NOT NULL;

CREATE UNIQUE INDEX uq_store_products_url
  ON store_products (store_id, store_url);

CREATE INDEX idx_store_products_game_id ON store_products (game_id);
CREATE INDEX idx_store_products_store_id ON store_products (store_id);
```

**Regra de crawler:** todo dado bruto passa por schema Pydantic antes de upsert em `games`, `store_products` e `prices`.

---

### `prices`

Snapshot atual do preço de um produto de loja.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `store_product_id` | `UUID` | NOT NULL, UNIQUE, FK `store_products.id` ON DELETE CASCADE | Produto da loja |
| `price_brl` | `NUMERIC(10,2)` | NOT NULL | Preço atual em BRL |
| `original_price_brl` | `NUMERIC(10,2)` | NULLABLE | Preço sem desconto |
| `discount_percent` | `INTEGER` | NULLABLE | 0–100 |
| `currency` | `CHAR(3)` | NOT NULL, DEFAULT `'BRL'` | Moeda |
| `affiliate_url` | `TEXT` | NOT NULL | Campo legado/compatibilidade; frontend deve preferir redirect interno |
| `is_available` | `BOOLEAN` | NOT NULL, DEFAULT `true` | Disponibilidade no momento da coleta |
| `scraped_at` | `TIMESTAMPTZ` | NOT NULL | Momento da coleta |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Atualização |

```sql
ALTER TABLE prices
  ADD CONSTRAINT chk_prices_money_non_negative
  CHECK (price_brl >= 0 AND (original_price_brl IS NULL OR original_price_brl >= 0));

ALTER TABLE prices
  ADD CONSTRAINT chk_prices_discount_percent
  CHECK (discount_percent IS NULL OR discount_percent BETWEEN 0 AND 100);

CREATE UNIQUE INDEX uq_prices_store_product_id ON prices (store_product_id);
CREATE INDEX idx_prices_price_brl ON prices (price_brl);
CREATE INDEX idx_prices_scraped_at ON prices (scraped_at);
```

**Regra central:** crawler/importer deve fazer `UPSERT` por `store_product_id`. Histórico não é inserido no MVP.

**Regra de afiliado:** a API pública não deve expor `affiliate_url` externa como link primário. O frontend deve receber um `outbound_url` interno apontando para `/api/v1/out/{price_id}`.

---

### `crawler_runs`

Execuções de crawler por loja. Entra no MVP para observabilidade mínima e debugging de scraping.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `store_id` | `UUID` | NOT NULL, FK `stores.id` ON DELETE CASCADE | Loja coletada |
| `status` | `VARCHAR(30)` | NOT NULL | `running`, `success`, `partial_failure`, `failed` |
| `started_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Início |
| `finished_at` | `TIMESTAMPTZ` | NULLABLE | Fim |
| `items_found` | `INTEGER` | NOT NULL, DEFAULT `0` | Produtos encontrados |
| `items_updated` | `INTEGER` | NOT NULL, DEFAULT `0` | Produtos/preços atualizados |
| `error_message` | `TEXT` | NULLABLE | Erro agregado, sem HTML bruto extenso |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Criação |

```sql
ALTER TABLE crawler_runs
  ADD CONSTRAINT chk_crawler_runs_status
  CHECK (status IN ('running', 'success', 'partial_failure', 'failed'));

CREATE INDEX idx_crawler_runs_store_started ON crawler_runs (store_id, started_at DESC);
CREATE INDEX idx_crawler_runs_status ON crawler_runs (status);
```

**Regra:** falha em uma loja não deve impedir execução das demais.

---

### `affiliate_clicks`

Cliques de saída para lojas. Entra no MVP monetizado para medir CTR, intenção de compra e permitir reconciliação futura de conversões.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Identificador interno |
| `click_id` | `UUID` | NOT NULL, UNIQUE | ID enviado como `subid`/tracking quando permitido |
| `store_id` | `UUID` | NOT NULL, FK `stores.id` ON DELETE CASCADE | Loja destino |
| `store_product_id` | `UUID` | NOT NULL, FK `store_products.id` ON DELETE CASCADE | Produto clicado |
| `price_id` | `UUID` | NULLABLE, FK `prices.id` ON DELETE SET NULL | Snapshot de preço usado no clique |
| `game_id` | `UUID` | NOT NULL, FK `games.id` ON DELETE CASCADE | Jogo canônico |
| `user_id` | `UUID` | NULLABLE, FK `users.id` ON DELETE SET NULL | Usuário autenticado, se existir |
| `session_id` | `VARCHAR(120)` | NULLABLE | Identificador anônimo de sessão, sem dado sensível |
| `placement` | `VARCHAR(80)` | NOT NULL | Origem visual: `search_result`, `game_detail`, `price_card`, etc. |
| `position` | `INTEGER` | NULLABLE | Posição da oferta na lista no momento do clique |
| `price_brl` | `NUMERIC(10,2)` | NOT NULL | Preço exibido quando o usuário clicou |
| `destination_url` | `TEXT` | NOT NULL | URL final gerada para redirect |
| `referrer` | `TEXT` | NULLABLE | Header ou rota anterior, se seguro armazenar |
| `user_agent` | `TEXT` | NULLABLE | User-Agent para análise agregada |
| `ip_hash` | `VARCHAR(128)` | NULLABLE | Hash do IP; não armazenar IP bruto sem decisão explícita |
| `clicked_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT `NOW()` | Momento do clique |

```sql
CREATE UNIQUE INDEX uq_affiliate_clicks_click_id
  ON affiliate_clicks (click_id);

CREATE INDEX idx_affiliate_clicks_store_clicked
  ON affiliate_clicks (store_id, clicked_at DESC);

CREATE INDEX idx_affiliate_clicks_game_clicked
  ON affiliate_clicks (game_id, clicked_at DESC);

CREATE INDEX idx_affiliate_clicks_product_clicked
  ON affiliate_clicks (store_product_id, clicked_at DESC);
```

**Regra de privacidade:** `ip_hash` deve ser hash irreversível com salt de ambiente. Não gravar IP bruto, token afiliado secreto ou dados pessoais desnecessários.

**Regra de redirect:** se `stores.compliance_status != 'approved'`, `stores.is_active = false`, `prices.is_available = false` ou a loja não permitir deep link, `/api/v1/out/{price_id}` deve retornar erro controlado em vez de redirecionar.

---

## Queries Esperadas no MVP

### Busca de jogos com menor preço

```sql
SELECT
  g.id,
  g.title,
  g.slug,
  g.cover_url,
  MIN(p.price_brl) AS best_price_brl
FROM games g
JOIN store_products sp ON sp.game_id = g.id
JOIN stores s ON s.id = sp.store_id
JOIN prices p ON p.store_product_id = sp.id
WHERE g.is_active = true
  AND p.is_available = true
  AND s.is_active = true
  AND s.compliance_status = 'approved'
  AND s.allows_price_display = true
  AND g.canonical_name ILIKE '%' || :query || '%'
GROUP BY g.id
ORDER BY best_price_brl ASC;
```

### Detalhe do jogo com preços ordenados

```sql
SELECT
  s.name AS store_name,
  s.slug AS store_slug,
  sp.store_title,
  p.price_brl,
  p.original_price_brl,
  p.discount_percent,
  '/api/v1/out/' || p.id::text AS outbound_url,
  p.scraped_at
FROM games g
JOIN store_products sp ON sp.game_id = g.id
JOIN stores s ON s.id = sp.store_id
JOIN prices p ON p.store_product_id = sp.id
WHERE g.slug = :slug
  AND s.is_active = true
  AND p.is_available = true
  AND s.compliance_status = 'approved'
  AND s.allows_price_display = true
ORDER BY p.price_brl ASC;
```

### Cliques por loja nos últimos 7 dias

```sql
SELECT
  s.slug,
  s.name,
  COUNT(ac.id) AS clicks
FROM affiliate_clicks ac
JOIN stores s ON s.id = ac.store_id
WHERE ac.clicked_at >= NOW() - INTERVAL '7 days'
GROUP BY s.id
ORDER BY clicks DESC;
```

---

## Ordem de Migrations

Migration inicial recomendada:

```text
1. PostgreSQL extensions
2. users
3. oauth_accounts
4. revoked_tokens
5. stores
6. games
7. store_products
8. prices
9. crawler_runs
10. affiliate_clicks
```

Comando real deve ser confirmado no `Makefile`. Enquanto `make migrate-create` não existir:

```bash
cd backend && alembic revision --autogenerate -m "create initial schema"
```

---

## Padrão SQLModel

```python
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255)
    canonical_name: str = Field(max_length=255, index=True)
    slug: str = Field(max_length=255, unique=True, index=True)
    cover_url: str | None = None
    platform: str = Field(default="pc", max_length=30)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    store_products: list["StoreProduct"] = Relationship(back_populates="game")
```

Regras:

- Models com `table=True` ficam em `backend/app/models/`.
- DTOs Pydantic/SQLModel sem tabela ficam em `backend/app/schemas/`.
- Campos monetários usam `Decimal`, nunca `float`.
- Alterações de schema exigem migration Alembic no mesmo PR.

---

## Fases Futuras

Estas tabelas não devem ser criadas no MVP sem nova decisão registrada em `AGENTS.md` §15.

### Fase 2

#### `wishlists`

Usuários seguindo jogos para receber alertas e montar lista pessoal.

```sql
CREATE TABLE wishlists (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  target_price_brl NUMERIC(10,2),
  notify_enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, game_id)
);
```

#### `price_alerts`

Fila/registro de alertas disparados para evitar notificações duplicadas.

```sql
CREATE TABLE price_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  price_brl NUMERIC(10,2) NOT NULL,
  channel VARCHAR(30) NOT NULL,
  sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### `crawler_run_items`

Detalhe por produto em cada execução, útil para diagnóstico de crawler.

```sql
CREATE TABLE crawler_run_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  crawler_run_id UUID NOT NULL REFERENCES crawler_runs(id) ON DELETE CASCADE,
  store_product_id UUID REFERENCES store_products(id) ON DELETE SET NULL,
  status VARCHAR(30) NOT NULL,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Fase 3

#### `price_history`

Histórico append-only para gráficos e análise de variação.

```sql
CREATE TABLE price_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  store_product_id UUID NOT NULL REFERENCES store_products(id) ON DELETE CASCADE,
  price_brl NUMERIC(10,2) NOT NULL,
  original_price_brl NUMERIC(10,2),
  discount_percent INTEGER,
  currency CHAR(3) NOT NULL DEFAULT 'BRL',
  is_available BOOLEAN NOT NULL DEFAULT true,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### `affiliate_conversions`

Conversões/comissões reportadas por rede de afiliados, postback ou importação CSV. Fica fora do MVP porque depende do suporte de cada parceiro.

```sql
CREATE TABLE affiliate_conversions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  click_id UUID REFERENCES affiliate_clicks(click_id) ON DELETE SET NULL,
  store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
  external_order_id_hash VARCHAR(128),
  commission_brl NUMERIC(10,2),
  order_value_brl NUMERIC(10,2),
  status VARCHAR(30) NOT NULL,
  converted_at TIMESTAMPTZ,
  reported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### `api_keys`

Autenticação para API pública futura.

```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(120) NOT NULL,
  key_hash TEXT NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT true,
  last_used_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### Marketplaces cinzas

G2A/Eneba/Kinguin podem exigir campos adicionais em `store_products` ou tabela específica de ofertas:

- vendedor/merchant
- reputação do vendedor
- região de ativação
- risco/observações de marketplace
- região de ativação
- múltiplas ofertas para o mesmo `game_id` e `store_id`

Não modelar agora. A tabela `store_products` já reduz o custo da futura adaptação.

---

## Fora de Escopo Deliberado no MVP

- `price_history`
- `wishlists`
- alertas de preço
- `affiliate_conversions`
- API keys públicas
- suporte a consoles
- G2A/Eneba/Kinguin
- dados extensos de catálogo como gêneros, publishers, requisitos mínimos e tags

---

## Nota de Ambiente

O PostgreSQL roda via Docker Compose exposto apenas em `127.0.0.1:5432`. Em desenvolvimento, `DATABASE_URL` aponta para o banco local da máquina Ubuntu. Secrets ficam em `.env`; nunca hardcoded em código, migrations ou seeds.

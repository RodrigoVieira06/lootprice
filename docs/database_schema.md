# LootPrice — Database Schema

> **Versão:** 0.1.1-MVP
> **Banco:** PostgreSQL 15+
> **ORM:** SQLModel + Alembic (migrations obrigatórias)
> **Última atualização:** 2026-06-03
> **Audiência:** Desenvolvedor, LLMs de apoio

---

## Decisões de Design

| Decisão | Escolha | Motivo |
|---|---|---|
| Tipo de ID | `UUID` em entidades principais | Evita enumeração e facilita futura distribuição |
| Tipo monetário | `NUMERIC(10, 2)` | Nunca usar `FLOAT` para dinheiro |
| Histórico de preços | **Fora do MVP** — `prices` guarda apenas o snapshot atual | Tabela `price_history` entra na Fase 3 |
| Normalização de nomes | Campo `canonical_name` separado de `title` | Permite correção manual pelo admin sem alterar o título original |
| Timestamps | `created_at` imutável + `updated_at` auto-atualizado | Padrão auditável |

---

## Diagrama de Relacionamentos

```
users
 └─(1:N via FK)──> (sem relação direta no MVP — preparado para wishlist na Fase 2)

stores ──(1:N)──> prices
games  ──(1:N)──> prices

games.id  + stores.id  →  UNIQUE CONSTRAINT em prices
```

---

## Tabelas

### `stores`

Tabela de referência estática. Populada via seed, não via crawler.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `INTEGER` | PK, AUTOINCREMENT | ID numérico simples para FK eficiente |
| `name` | `VARCHAR(100)` | NOT NULL, UNIQUE | Nome exibível: "Steam", "Nuuvem" |
| `slug` | `VARCHAR(100)` | NOT NULL, UNIQUE | Identificador URL-safe: "steam", "nuuvem" |
| `base_url` | `VARCHAR(255)` | NOT NULL | URL base da loja |
| `is_marketplace` | `BOOLEAN` | NOT NULL, DEFAULT false | `true` para G2A, Eneba (chaves cinzas) |
| `crawler_class` | `VARCHAR(100)` | NULLABLE | Classe Python responsável: "steam.SteamCrawler" |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | Desativar sem deletar |
| `created_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | |

**Seed inicial (MVP):**
```sql
INSERT INTO stores (name, slug, base_url, crawler_class) VALUES
  ('Steam',  'steam',  'https://store.steampowered.com', 'steam.SteamCrawler'),
  ('Nuuvem', 'nuuvem', 'https://www.nuuvem.com',         'nuuvem.NuuvemCrawler');
```

---

### `games`

Um registro por jogo único, independente de loja.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT gen_random_uuid() | |
| `title` | `VARCHAR(255)` | NOT NULL | Nome original como scraped: "Cyberpunk 2077™" |
| `canonical_name` | `VARCHAR(255)` | NOT NULL, INDEX | Nome normalizado: "cyberpunk 2077". Editável pelo admin para deduplicação |
| `slug` | `VARCHAR(255)` | NOT NULL, UNIQUE, INDEX | URL-friendly: "cyberpunk-2077" |
| `cover_url` | `TEXT` | NULLABLE | URL da imagem de capa |
| `created_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | Auto-atualizado via trigger ou ORM |

**Índices:**
```sql
CREATE INDEX idx_games_canonical_name ON games (canonical_name);
CREATE UNIQUE INDEX idx_games_slug ON games (slug);
```

**Nota de negócio:** `canonical_name` é gerado automaticamente pelo normalizer no momento do scraping, mas pode ser editado pelo admin via `PATCH /admin/games/{id}`. É o campo usado para deduplicação entre lojas.

---

### `prices`

Snapshot atual de preço por jogo por loja. **Uma linha por par `(game_id, store_id)`.**

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT gen_random_uuid() | |
| `game_id` | `UUID` | NOT NULL, FK → games.id ON DELETE CASCADE | |
| `store_id` | `INTEGER` | NOT NULL, FK → stores.id | |
| `price_brl` | `NUMERIC(10, 2)` | NOT NULL | Preço atual em BRL |
| `original_price_brl` | `NUMERIC(10, 2)` | NULLABLE | Preço sem desconto (para calcular %) |
| `discount_percent` | `INTEGER` | NULLABLE | Percentual de desconto (0–100) |
| `affiliate_url` | `TEXT` | NOT NULL | Link direto para compra na loja |
| `is_available` | `BOOLEAN` | NOT NULL, DEFAULT true | `false` se o jogo saiu de catálogo |
| `scraped_at` | `TIMESTAMP` | NOT NULL | Timestamp da última coleta bem-sucedida |

**Constraint de unicidade (regra central do sistema):**
```sql
ALTER TABLE prices ADD CONSTRAINT uq_prices_game_store UNIQUE (game_id, store_id);
```

**Nota de negócio:** O crawler deve executar um `UPSERT` nesta tabela — nunca um `INSERT` puro. Se o par `(game_id, store_id)` já existir, atualiza `price_brl`, `original_price_brl`, `discount_percent` e `scraped_at`. Histórico de preços é escopo da Fase 3 (tabela `price_history`).

---

### `users`

Suporta login local e OAuth social (Google, Discord). Campos de senha são nulos para login social.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT gen_random_uuid() | |
| `email` | `VARCHAR(255)` | NOT NULL, UNIQUE | Identificador principal |
| `username` | `VARCHAR(100)` | NULLABLE | Opcional no MVP |
| `hashed_password` | `TEXT` | NULLABLE | `NULL` para usuários OAuth |
| `profile_picture_url` | `TEXT` | NULLABLE | Avatar vindo do provider OAuth |
| `role` | `VARCHAR(20)` | NOT NULL, DEFAULT 'user' | Valores: `'user'` \| `'admin'` |
| `auth_provider` | `VARCHAR(20)` | NOT NULL, DEFAULT 'local' | Valores: `'local'` \| `'google'` \| `'discord'` |
| `provider_user_id` | `VARCHAR(255)` | NULLABLE, INDEX | ID do usuário no provider OAuth (para lookup) |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | Soft disable de conta |
| `created_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | |

**Índices:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_provider ON users (auth_provider, provider_user_id);
```

**Constraint de integridade:**
```sql
-- Garante que login local sempre tem senha
ALTER TABLE users ADD CONSTRAINT chk_local_password
  CHECK (auth_provider != 'local' OR hashed_password IS NOT NULL);
```

---

### `revoked_tokens`

Blacklist de refresh tokens revogados. Usada para implementar logout real e revogação de tokens vazados sem depender de Redis no MVP.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `UUID` | PK, DEFAULT gen_random_uuid() | |
| `token_jti` | `VARCHAR(255)` | NOT NULL, UNIQUE | Campo `jti` do JWT (UUID único gerado em `create_refresh_token()`) |
| `revoked_at` | `TIMESTAMP` | NOT NULL, DEFAULT NOW() | Momento da revogação |
| `expires_at` | `TIMESTAMP` | NOT NULL | Cópia do `exp` do token — para limpeza periódica via cron |

**Índices:**
```sql
CREATE INDEX idx_revoked_tokens_jti ON revoked_tokens (token_jti);
```

**Nota de negócio:** O endpoint `POST /auth/logout` insere o `jti` do refresh token nesta tabela. A função `decode_token()` em `security.py` verifica a presença do `jti` aqui antes de aceitar o token como válido. Registros expirados (`expires_at < NOW()`) devem ser limpos periodicamente — débito técnico para a Fase 2.

## Estrutura SQLModel (Referência para LLMs)

```python
# Padrão obrigatório: herdar de SQLModel com table=True APENAS nos models/
# Schemas (DTOs) em schemas/ herdam de SQLModel com table=False (padrão)

# models/game.py
class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    canonical_name: str = Field(max_length=255, index=True)
    slug: str = Field(max_length=255, unique=True, index=True)
    cover_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    prices: list["Price"] = Relationship(back_populates="game")
```

---

## Ordem de Criação das Migrations (Alembic)

A ordem importa por causa das foreign keys:

```
1. stores           (sem dependências)
2. games            (sem dependências)
3. users            (sem dependências)
4. prices           (depende de games e stores)
5. revoked_tokens   (sem dependências — executa após users por clareza de contexto)
```

**Comando de referência:**
```bash
make migrate-create msg="create initial tables"
# ou
cd backend && alembic revision --autogenerate -m "create initial tables"
```

---

## Fora do Schema MVP (Fase 3)

```sql
-- price_history: registra cada coleta para gráficos de variação
CREATE TABLE price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES games(id),
    store_id INT NOT NULL REFERENCES stores(id),
    price_brl NUMERIC(10, 2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- wishlists: relação N:N entre users e games
CREATE TABLE wishlists (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, game_id)
);
```

> **Nota de ambiente:** O banco roda em Docker na máquina Ubuntu local (i7 10ª + 8GB RAM) acessada via SSH. Não confundir com WSL2 — é uma instância Ubuntu nativa, sem as peculiaridades de networking do WSL2. O `DATABASE_URL` em desenvolvimento aponta para `localhost:5432` quando acessado dentro da máquina Ubuntu.

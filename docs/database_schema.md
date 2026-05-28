# Schema do Banco de Dados - Game Price Tracker

## Entidades

### 1. `games`
Armazena o registro único do jogo (independente da loja).
* `id`: UUID (Primary Key)
* `title`: VARCHAR(255) (Nome oficial normalizado)
* `slug`: VARCHAR(255) (Para a URL do frontend, ex: "grand-theft-auto-v")
* `image_url`: TEXT
* `created_at`: TIMESTAMP

### 2. `stores`
Tabela estática com as lojas suportadas.
* `id`: INT (Primary Key)
* `name`: VARCHAR(100) (Ex: "Nuuvem", "G2A")
* `base_url`: VARCHAR(255)
* `is_marketplace`: BOOLEAN (Para diferenciar lojas oficiais de chaves cinzas)

### 3. `prices`
A tabela que o crawler vai alimentar constantemente. Guarda o histórico ou o preço atual.
* `id`: UUID (Primary Key)
* `game_id`: UUID (Foreign Key -> games.id)
* `store_id`: INT (Foreign Key -> stores.id)
* `current_price`: DECIMAL(10, 2)
* `original_price`: DECIMAL(10, 2) (Para calcular a % de desconto)
* `affiliate_url`: TEXT (Link direto para a página de compra do jogo na loja)
* `updated_at`: TIMESTAMP (Saber quando o crawler atualizou esse preço pela última vez)

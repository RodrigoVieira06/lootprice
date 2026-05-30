# Sugestões de Cards para GitHub Projects - LootPrice

Aqui estão as issues sugeridas para organizar o desenvolvimento inicial, com foco na infraestrutura de Autenticação e Banco de Dados.

## 🟢 Épico: Infraestrutura e Autenticação (MVP)

### 1. Setup de Modelos de Usuário e RBAC
- **Título:** `feat(auth): implementar modelos de usuário e perfis (User/Admin)`
- **Descrição:** Criar as tabelas `users` e `roles` utilizando SQLModel. Definir os campos base (email, username, hashed_password, profile_picture) e a relação com roles.
- **Labels:** `backend`, `database`, `auth`

### 2. Implementação de JWT e Hashing
- **Título:** `feat(auth): configurar JWT e utilitários de segurança`
- **Descrição:** Instalar e configurar `python-jose` e `passlib`. Criar utilitários para geração de tokens, verificação de expiração e hashing de senhas.
- **Labels:** `backend`, `auth`

### 3. Endpoints de Registro e Login Local
- **Título:** `feat(api): criar endpoints de registro e login local`
- **Descrição:** Implementar `/auth/register` e `/auth/login` (OAuth2 Password Flow). Garantir validação de email único e hashing de senha.
- **Labels:** `backend`, `api`, `auth`

### 4. Integração OAuth2: Google
- **Título:** `feat(auth): implementar login social via Google`
- **Descrição:** Configurar o fluxo de redirecionamento e callback para autenticação com Google. Vincular ao modelo de usuário existente ou criar um novo.
- **Labels:** `backend`, `auth`, `external-api`

### 5. Integração OAuth2: Discord
- **Título:** `feat(auth): implementar login social via Discord`
- **Descrição:** Configurar o fluxo de autenticação via Discord. Capturar o username e avatar do usuário durante o primeiro login.
- **Labels:** `backend`, `auth`, `external-api`

### 6. Dependency Injection para Rotas Protegidas
- **Título:** `feat(auth): criar dependências de segurança (get_current_user, get_admin_user)`
- **Descrição:** Criar funções de dependência do FastAPI para proteger rotas e validar o perfil do usuário (RBAC).
- **Labels:** `backend`, `auth`

## 🟡 Épico: Ingestão de Dados (Crawlers)

### 7. Crawler Base e Abstração
- **Título:** `feat(crawlers): criar estrutura base e utilitários de scraping`
- **Descrição:** Definir a classe base para crawlers, configurar o `HTTPX` com headers realistas e tratamento de erros global.
- **Labels:** `backend`, `scraper`

### 8. Implementação Crawler Nuuvem
- **Título:** `feat(crawlers): implementar scraper para Nuuvem`
- **Descrição:** Desenvolver o parser para a loja Nuuvem utilizando BeautifulSoup4. Normalizar nomes de jogos.
- **Labels:** `backend`, `scraper`

### 9. Integração API Steam
- **Título:** `feat(crawlers): integrar com API pública da Steam`
- **Descrição:** Consumir os endpoints de preço da Steam para jogos de PC. Implementar cache local se necessário.
- **Labels:** `backend`, `api`, `external-api`

## 🔵 Épico: Banco de Dados e API

### 10. Modelagem de Preços e Jogos
- **Título:** `feat(database): implementar modelos de games e prices`
- **Descrição:** Criar tabelas para armazenar os dados agregados. Garantir que um jogo possa ter múltiplos preços de lojas diferentes.
- **Labels:** `backend`, `database`

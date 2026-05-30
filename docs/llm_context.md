# Contexto do Projeto para IA (LLM System Context)

## 1. Visão Geral da Aplicação
* **Nome do Projeto:** LootPrice
* **Objetivo:** Um agregador e comparador de preços de chaves de jogos digitais.
* **Fase Atual:** Desenvolvimento Inicial do Backend (Foco em Infraestrutura Local, Banco de Dados e Ingestão).

---

## 2. Restrições e Escopo do MVP (NÃO DESVIAR)
Para evitar "scope creep" (aumento descontrolado de escopo), a IA deve sugerir códigos focados **estritamente** nas seguintes regras:

* **Plataforma Alvo:** Apenas jogos de PC.
* **Lojas Suportadas no MVP:** Nuuvem (via Web Scraping/Parser) e Steam (via API Pública).
* **Lojas Proibidas no MVP (Não insistir):** Eneba e G2A.
* **Autenticação:** JWT com suporte a OAuth2 (Google e Discord) e Login Local.
* **Perfis:** Suporte inicial para perfis `User` e `Admin` (RBAC).
* **Escopo Global:** O projeto não deve ser limitado apenas ao mercado brasileiro, visando escalabilidade global.
* **Roadmap Futuro (Não implementar agora):** Wishlists, Alertas de Preço, Histórico de Preços.
* **Testes:** Priorizar a criação de testes unitários com Pytest para novas funcionalidades.

---

## 3. Stack Tecnológica Definitiva

### Backend & Ingestão
* **Ambiente de Dev:** Python 3.10+ executado em ambiente **WSL2 (Ubuntu)** no Windows.
* **Framework API:** **FastAPI** com servidores assíncronos.
* **Segurança:** **Python-jose** (JWT) e **Passlib** (Hashing de senhas).
* **ORM / Banco:** **SQLModel**.
* **Validação / DTOs:** **Pydantic** (V2).
* **Ferramentas de Scraping:** **BeautifulSoup4** e **HTTPX**.
* **Qualidade de Código:** **Ruff** (Linter/Formatter), **Pytest** (Testes Unitários) e **Lefthook** (Git Hooks).
* **Orquestração:** **Makefile**.

### Banco de Dados & Infraestrutura Local
* **Banco Principal:** **PostgreSQL 15+** via **Docker Compose**.
* **CI/CD:** **GitHub Actions** rodando testes e linters.

### Frontend (Fase Posterior - Não gerar código para isso ainda)
* React.js (TypeScript), Vite.js, TailwindCSS, Axios, Zod, React Hook Form.

---

## 4. Estrutura de Pastas do Repositório (Monorepo)
A IA deve sempre gerar caminhos de arquivos e imports baseados na estrutura abaixo:

```text
lootprice/                  # Raiz do Repositório
├── .github/
│   └── workflows/          # Workflows do GitHub Actions
├── docs/                   # Documentação em Markdown
│   ├── architecture.md     # Visão geral arquitetural
│   ├── database_schema.md  # Modelagem de dados
│   └── llm_context.md      # Este arquivo de contexto
├── backend/                # Todo o projeto Python
│   ├── app/
│   │   ├── api/            # Endpoints (v1/games, v1/prices)
│   │   ├── core/           # Configurações globais e conexão de Banco
│   │   ├── models/         # Modelos SQLModel (Tabelas do Banco)
│   │   ├── schemas/        # Schemas Pydantic (Validação de entrada/saída)
│   │   └── crawlers/       # Scripts de raspagem (nuuvem.py, steam.py)
│   ├── tests/              # Testes unitários e de integração
│   ├── requirements.txt    # Dependências do Pip
│   ├── ruff.toml           # Configuração do Ruff Linter
│   └── main.py             # Ponto de entrada do FastAPI
├── Makefile                # Comandos de orquestração
└── lefthook.yml            # Configuração de Git Hooks
```

## 5. Diretrizes para Geração de Código pela IA (Instruções para você, IA)
Quando o desenvolvedor solicitar a criação de código neste projeto, siga rigidamente estas regras:

1. Escreva código assíncrono (async/await) nas rotas do FastAPI e nas requisições do crawler.

2. Utilize Tipagem Estrita: Todo parâmetro e retorno de função em Python deve conter Type Hints claros.

3. Padrão SQLModel: Prefira os métodos nativos do SQLModel.

4. Segurança: Implemente OAuth2PasswordBearer para rotas protegidas e utilize scopes para controle de acesso (Admin/User).

5. Testes Unitários: Ao criar novos modelos, serviços ou crawlers, sugira sempre um arquivo de teste correspondente na pasta `backend/tests/`.

6. Scraping Resiliente: Utilize blocos try/except robustos com BeautifulSoup4.

7. Logs: Utilize o módulo padrão logging do Python.

8. Conventional Commits: Sugira mensagens de commit seguindo o padrão (ex: `feat: add steam crawler`, `fix: handle null prices`).

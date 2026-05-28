Plaintext
# 💰 LootPrice

O **LootPrice** é um agregador e comparador de preços de chaves de jogos digitais focado no mercado brasileiro. O sistema realiza a raspagem de dados (web scraping) e consome APIs de diversas lojas de jogos, normaliza as informações e exibe em uma interface única onde o jogo está mais barato.

---

## 🗺️ Arquitetura Global do Sistema
```text
 ┌────────────────────────────────────────────────────────┐
 │                   CAMADA DE INGESTÃO                   │
 │  ┌────────────────────────┐    ┌────────────────────┐  │
 │  │ Nuuvem Web Scraper     │    │ Steam Public API   │  │
 │  │ (HTTPX + BeautifulSoup)│    │ (HTTPX Async)      │  │
 │  └───────────┬────────────┘    └─────────┬──────────┘  │
 └──────────────┼───────────────────────────┼─────────────┘
                │                           │
                ▼                           ▼
 ┌────────────────────────────────────────────────────────┐
 │                    BACKEND CORE                        │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ Data Normalization Engine (Python)               │  │
 │  │ - Limpeza de títulos e agrupamento de jogos       │  │
 │  └───────────────────────┬──────────────────────────┘  │
 │                          │                             │
 │                          ▼                             │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ SQLModel (ORM)                                   │  │
 │  └───────────────────────┬──────────────────────────┘  │
 └──────────────────────────┼─────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │                  BANCO DE DADOS (Docker)               │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ PostgreSQL 15+                                   │  │
 │  │ - Tabelas: games, stores, prices                 │  │
 │  └───────────────────────┬──────────────────────────┘  │
 └──────────────────────────┼─────────────────────────────┘
                            │ (Leitura / Query Assíncrona)
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │                    WEB API (FastAPI)                   │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ Endpoints RESTful (JSON)                         │  │
 │  │ - GET /api/v1/games                              │  │
 │  └───────────────────────┬──────────────────────────┘  │
 └──────────────────────────┼─────────────────────────────┘
                            │
                            ▼ (Axios HTTP Requests)
 ┌────────────────────────────────────────────────────────┐
 │                   FRONTEND (React SPA)                 │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ React + TypeScript + Vite + TailwindCSS          │  │
 │  │ - Busca, filtros e ordenação por menor preço      │  │
 │  └──────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────┘
```
---

## 📁 Estrutura do Repositório (Monorepo)

O projeto adota uma estratégia de repositório único para facilitar o gerenciamento e garantir contexto completo para desenvolvimento auxiliado por IA (LLMs).

*   `docs/`: Contratos de API, schemas de banco de dados e manuais de contexto para IA.
*   `backend/`: API REST desenvolvida em FastAPI e motores de Web Scraping.
*   `frontend/`: Interface Single Page Application (SPA) em React com TypeScript.

---

## 🛠️ Como Iniciar o Desenvolvimento

### Pré-requisitos
*   Ambiente **WSL2 (Ubuntu)** instalado (caso esteja no Windows).
*   **Python 3.10+** instalado no ambiente Linux.
*   **Docker** & **Docker Compose** configurados.

---

### 🚀 Configurando o Backend (Local)

**1. Navegue até a pasta do backend:**
cd backend

**2. Crie e ative o ambiente virtual (venv):**
python3 -m venv .venv
source .venv/bin/activate
*(Você verá o prefixo `(.venv)` no terminal confirmando a ativação).*

**3. Instale todas as dependências:**
pip install -r requirements.txt

**4. Suba o Banco de Dados (PostgreSQL):**
Certifique-se de que o Docker está rodando e execute o comando na raiz do projeto (onde está o `docker-compose.yml`):
docker-compose up -d

**5. Execute o servidor de desenvolvimento da API:**
uvicorn main:app --reload

A API estará disponível em `[http://127.0.0.1:8000](http://127.0.0.1:8000)` e a documentação interativa (Swagger) em `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`.

---

## 🧪 Qualidade de Código & Testes

Mantemos o código limpo e testado utilizando ferramentas modernas do ecossistema Python.

*   **Run Linter/Formatter (Ruff):**
    ruff check .    # Para checar erros
    ruff format .   # Para auto-formatar o código

*   **Executar Testes Unitários (Pytest):**
    pytest

---

## 🤖 Uso de Inteligência Artificial (LLMs)

Se você estiver desenvolvendo ou estendendo este projeto utilizando LLMs (como o Antigravity), sempre forneça os arquivos da pasta `docs/` como contexto inicial da sessão, especialmente o `docs/llm_context.md`. Isso garante que a IA siga estritamente o escopo definido do MVP e as escolhas de arquitetura.
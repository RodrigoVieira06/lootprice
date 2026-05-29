# 💰 LootPrice

O **LootPrice** é um agregador e comparador de preços de chaves de jogos digitais. O sistema realiza a raspagem de dados (web scraping) e consome APIs de diversas lojas de jogos, normaliza as informações e exibe em uma interface única onde o jogo está mais barato.

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
*   **Lefthook** instalado globalmente.

---

### 🚀 Configurando o Projeto

Utilizamos um **Makefile** para simplificar os comandos comuns. Os comandos devem ser executados na raiz do projeto.

**1. Instale as dependências e configure os hooks de commit:**
```bash
make install
```

**2. Suba o Banco de Dados e inicie o servidor de desenvolvimento:**
```bash
make dev
```

A API estará disponível em `http://127.0.0.1:8000` e a documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

---

## 🧪 Qualidade de Código & Testes

Mantemos o código limpo e testado utilizando ferramentas modernas do ecossistema Python e Git Hooks.

*   **Lint/Format:** `make lint` ou `make format`
*   **Testes:** `make test`

Os testes unitários são executados automaticamente no GitHub Actions a cada push. O **Lefthook** garante que o código esteja formatado e os commits sigam o padrão antes mesmo de subir para o repositório.

---

## 🤖 Uso de Inteligência Artificial (LLMs)

Se você estiver desenvolvendo ou estendendo este projeto utilizando LLMs, sempre forneça os arquivos da pasta `docs/` como contexto inicial da sessão, especialmente o `docs/llm_context.md`. Isso garante que a IA siga estritamente o escopo definido do MVP e as escolhas de arquitetura.

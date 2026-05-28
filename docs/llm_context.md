# Contexto do Projeto para IA (LLM System Context)

## 1. Visão Geral da Aplicação
* **Nome do Projeto:** LootPrice
* **Objetivo:** Um agregador e comparador de preços de chaves de jogos digitais focado no mercado brasileiro (estilo Buscapé/Zoom/IsThereAnyDeal).
* **Fase Atual:** Desenvolvimento Inicial do Backend (Foco em Infraestrutura Local, Banco de Dados e Ingestão).

---

## 2. Restrições e Escopo do MVP (NÃO DESVIAR)
Para evitar "scope creep" (aumento descontrolado de escopo), a IA deve sugerir códigos focados **estritamente** nas seguintes regras:

* **Plataforma Alvo:** Apenas jogos de PC.
* **Lojas Suportadas no MVP:** Nuuvem (via Web Scraping/Parser) e Steam (via API Pública).
* **Lojas Proibidas no MVP (Não insistir):** Eneba e G2A (deixadas para a Fase 2 devido a bloqueios complexos de Cloudflare/Akamai).
* **Autenticação/Usuários:** Fora do escopo. Não criar tabelas de usuários, senhas ou sistemas de login (OAuth/JWT) por enquanto.
* **Histórico de Preços:** Fora do escopo. O sistema deve armazenar e atualizar apenas o **preço atual**.

---

## 3. Stack Tecnológica Definitiva

### Backend & Ingestão
* **Ambiente de Dev:** Python 3.10+ executado em ambiente **WSL2 (Ubuntu)** no Windows.
* **Framework API:** **FastAPI** com servidores assíncronos (Uvicorn).
* **ORM / Banco:** **SQLModel** (junção nativa de SQLAlchemy + Pydantic).
* **Validação / DTOs:** **Pydantic** (V2).
* **Ferramentas de Scraping:** **BeautifulSoup4** (para parsing de HTML) e **HTTPX** (para requisições HTTP assíncronas).
* **Qualidade de Código:** **Ruff** (como linter e formatter unificado) e **Pytest** (para testes unitários básicos e de integração).

### Banco de Dados & Infraestrutura Local
* **Banco Principal:** **PostgreSQL 15+** rodando em container isolado via **Docker Compose**.
* **CI/CD:** **GitHub Actions** rodando testes e linters a cada Git Push.

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
│   ├── requirements.txt    # Dependências do Pip
│   ├── ruff.toml           # Configuração do Ruff Linter
│   └── main.py             # Ponto de entrada do FastAPI
└── frontend/               # Futuro projeto React (Vazio atualmente)
```

## 5. Diretriz5es para Geração de Código pela IA (Instruções para você, IA)
Quando o desenvolvedor solicitar a criação de código neste projeto, siga rigidamente estas regras:

1. Escreva código assíncrono (async/await) nas rotas do FastAPI e nas requisições do crawler (usando HTTPX).

2. Utilize Tipagem Estrita: Todo parâmetro e retorno de função em Python deve conter Type Hints claros.

3. Padrão SQLModel: Não misture sintaxe pura do SQLAlchemy se for possível resolver com os métodos nativos do SQLModel.

4. Scraping Resiliente: Ao gerar parsers com BeautifulSoup4, utilize blocos try/except robustos para evitar que alterações sutis no HTML das lojas quebrem o loop de execução do crawler.

5. Logs: Utilize o módulo padrão logging do Python em vez de print() para debugar o fluxo dos crawlers.

---
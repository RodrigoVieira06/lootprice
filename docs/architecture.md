# Arquitetura do Sistema - LootPrice

O **LootPrice** é um agregador e comparador de preços de chaves de jogos focado no público brasileiro. O sistema realiza a raspagem de dados (web scraping) de diversas lojas, normaliza as informações e exibe para o usuário final onde o jogo está mais barato.

---

## 1. Escopo do MVP (Mínimo Produto Viável)

Para garantir a entrega ágil e mitigar a complexidade inicial, o escopo está estritamente fechado nos seguintes entregáveis:

### Em Escopo
* **Alvo:** Apenas jogos de PC.
* **Lojas Suportadas (Fase 1):** Nuuvem (via Scraper) e Steam (via API pública).
* **Frequência de Atualização:** Execução manual ou agendamento local simples (CLI script).
* **Backend:** API REST para listagem e busca de jogos com seus respectivos preços agregados.
* **Frontend:** Interface SPA simples para busca e comparação de preços.

### Fora de Escopo (Fases Futuras)
* Autenticação de usuários, favoritos e listas de desejos.
* Histórico e gráficos de variação de preço ao longo do tempo.
* Alertas de preço por e-mail ou Discord.
* Integração com marketplaces cinzas complexos (Eneba, G2A) devido a bloqueios de Cloudflare.

---

## 2. Stack Tecnológica

### Backend & Ingestão
* **Linguagem:** Python 3.10+ (Executado em ambiente WSL2 Ubuntu).
* **Framework Web:** FastAPI (com Pydantic para validação de dados).
* **ORM:** SQLModel (Abstração baseada em SQLAlchemy e Pydantic).
* **Qualidade de Código:** Ruff (Linter/Formatter) e Pytest (Testes unitários).
* **Scraping:** BeautifulSoup4 e HTTPX (para requisições assíncronas).

### Banco de Dados & Infraestrutura Local
* **Banco de Dados:** PostgreSQL 15+ (Relacional, rodando via Docker).
* **CI/CD:** GitHub Actions (Validação de Lint e execução de Testes a cada Push).

### Frontend (Fase Posterior)
* React.js (TypeScript), Vite.js, TailwindCSS, Axios, Zod, React Hook Form.

---

## 3. Estrutura do Repositório (Monorepo)

O projeto adota uma estratégia de repositório único para centralizar o contexto do projeto, facilitando o desenvolvimento assistido por IA (LLMs) e unificando o gerenciamento de demandas no GitHub Projects.

```text
lootprice/                  # Raiz do Repositório
├── .github/
│   └── workflows/          # Esteiras de CI/CD (GitHub Actions)
├── docs/                   # Documentação em Markdown para as LLMs
│   ├── architecture.md     # Este documento
│   └── database_schema.md  # Modelagem do banco de dados
├── backend/                # Ecossistema Python / FastAPI / Crawlers
│   ├── app/
│   │   ├── api/            # Rotas e Endpoints da API
│   │   ├── core/           # Configurações globais e conexão com Banco
│   │   ├── models/         # Modelos do SQLModel (Tabelas do Banco)
│   │   ├── schemas/        # Validações Pydantic (DTOs)
│   │   └── crawlers/       # Scripts de Scraping por loja (nuuvem.py, steam.py)
│   ├── requirements.txt    # Dependências do projeto Python
│   ├── ruff.toml           # Configurações do Linter/Formatter
│   └── main.py             # Ponto de entrada da aplicação FastAPI
└── frontend/               # Ecossistema React / TypeScript (Fase 2)
```

### Regras do .gitignore (Raiz do Projeto)
Arquivos locais de ambiente, binários de navegadores de testes, caches de linters e a pasta .venv do backend nunca devem ser commitados.

## 4. Fluxo de Dados (Data Pipeline)
```text
[ Lojas: Nuuvem / Steam ]
           │
           ▼ (HTTPX / BeautifulSoup4)
   [ Crawler Engine ] ──(Normalização de Nomes)──> [ Banco PostgreSQL ]
                                                            │
                                                            ▼ (SQLModel)
[ Frontend (React) ] <──────(JSON)─────── [ Web API (FastAPI) ]
```

1. Ingestão: O script de scraping acessa as lojas parceiras.
2. Normalização: O backend limpa o título do jogo (ex: remove "PC - Steam" ou caracteres especiais) para garantir que o mesmo jogo de lojas diferentes aponte para o mesmo registro na tabela games.
3. Persistência: Os preços atuais e os links de afiliados são salvos/atualizados na tabela prices.
4. Consumo: O Frontend consome a rota do FastAPI, que entrega o jogo combinado com um array de preços ordenado do menor para o maior.


---
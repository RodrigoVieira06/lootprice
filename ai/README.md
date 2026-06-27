# LootPrice — AI Tooling

> Este diretório contém as **skills** e ferramentas de IA do projeto LootPrice.
> Cada skill instrui uma IA CLI (Antigravity IDE, Claude Code, Gemini CLI, Cursor, Copilot) a desempenhar um papel específico neste projeto.

---

## Skills disponíveis

### 🧑‍💻 [`lootprice-backend-developer/SKILL.md`](./lootprice-backend-developer/SKILL.md)
**Quando usar:** Tarefas de backend, API, banco, crawlers, autenticação, CI backend ou infra backend.

Transforma qualquer IA CLI em um **desenvolvedor backend sênior do LootPrice** — conhece FastAPI, SQLModel, Alembic, PostgreSQL, crawlers, testes Python e regras de segurança do backend.
Também conhece a estratégia de lojas/afiliados: fonte permitida por loja, redirect interno, métricas de clique e riscos de marketplaces.

### 🎨 [`lootprice-frontend-developer/SKILL.md`](./lootprice-frontend-developer/SKILL.md)
**Quando usar:** Tarefas de React, TypeScript/TSX, Vite, SCSS, Biome, Jest, pnpm, UX, acessibilidade, integração com a API ou mobile futuro.

Transforma qualquer IA CLI em um **desenvolvedor frontend sênior do LootPrice** — conhece a stack planejada, respeita contratos da API e não assume estrutura React antes de existir.
Para ofertas, usa `outbound_url` interno e trata marketplaces, riscos e estados bloqueados sem expor link afiliado direto.
Também segue `docs/frontend_mobile_strategy.md`: SPA web-first, mobile-ready, sem React Native/Expo/Tauri/Capacitor no MVP, com adapters para outbound, storage, auth redirect e APIs de plataforma.
Para a fase mobile, considera React Native + Expo como preferencial se mobile nativo virar prioridade, mantendo Tauri e Capacitor como alternativas conforme objetivo de reuso/desktop/WebView.

### 🔍 [`lootprice-reviewer/SKILL.md`](./lootprice-reviewer/SKILL.md)
**Quando usar:** Para revisar um Pull Request aberto.

Transforma qualquer IA CLI em um **revisor de código especializado** do LootPrice. Busca o PR via `gh`/MCP GitHub, analisa o diff com o checklist do projeto e posta um review estruturado como comentário no PR.
O checklist inclui conformidade de afiliados, crawler, store compliance e tracking.

```
@reviewer revisar PR #42
@reviewer revisar https://github.com/RodrigoVieira06/lootprice/pull/42
```

### 📋 [`lootprice-scrum-master/SKILL.md`](./lootprice-scrum-master/SKILL.md)
**Quando usar:** Para gerenciar issues, priorizar backlog, mover cards entre colunas ou gerar resumos de sprint.

Transforma qualquer IA CLI em **Scrum Master do LootPrice**. Gerencia GitHub Issues como cards do projeto usando `gh` e prefixos de coluna no título (`[Backlog]`, `[Developing]`, `[Code Review]`, `[Done]`, etc.).
Issues de novas lojas/crawlers devem incluir fonte de dados, termos, risco e estratégia de afiliado.

```
@scrum criar issue para implementar crawler Fanatical
@scrum mover issue #5 para Developing
@scrum resumo da sprint atual
```

---

## Template de Pull Request

O template de PR está em **`.github/PULL_REQUEST_TEMPLATE.md`** — localização obrigatória para o GitHub preencher automaticamente.

Quando uma IA abre um PR via `gh pr create`, deve usar o conteúdo deste template como base e incluir `Closes #XX` para vincular a issue.

---

## Estrutura

```
ai/
├── README.md                         ← Este arquivo
├── lootprice-backend-developer/
│   └── SKILL.md                      ← Skill: backend sênior LootPrice
├── lootprice-frontend-developer/
│   └── SKILL.md                      ← Skill: frontend sênior LootPrice
├── lootprice-reviewer/
│   ├── SKILL.md                      ← Skill: revisor de código LootPrice
│   └── resources/
│       ├── checklist.md              ← Checklist de conformidade (B-01..G-05)
│       └── review_format.md          ← Formato exato do review
└── lootprice-scrum-master/
    └── SKILL.md                      ← Skill: scrum master LootPrice
```

---

## Contexto do Projeto

Para entender o estado atual do projeto:
- **[`AGENTS.md`](../AGENTS.md)** — contexto unificado (arquitetura, estado, regras, decisões)
- **[`docs/affiliate_store_strategy.md`](../docs/affiliate_store_strategy.md)** — estratégia de lojas, afiliados, fontes de dados e riscos
- **[`docs/frontend_mobile_strategy.md`](../docs/frontend_mobile_strategy.md)** — estratégia frontend mobile-ready e fase futura Android/iOS
- **[`docs/database_schema.md`](../docs/database_schema.md)** — schema completo do banco
- **[`docs/issues_mvp.md`](../docs/issues_mvp.md)** — issues detalhadas para o MVP

# LootPrice — AI Tooling

> Este diretório contém as **skills** e ferramentas de IA do projeto LootPrice.
> Cada skill instrui uma IA CLI (Antigravity IDE, Claude Code, Gemini CLI, Cursor, Copilot) a desempenhar um papel específico neste projeto.

---

## Skills disponíveis

### 🧑‍💻 [`backend-developer/SKILL.md`](./backend-developer/SKILL.md)
**Quando usar:** Tarefas de backend, API, banco, crawlers, autenticação, CI backend ou infra backend.

Transforma qualquer IA CLI em um **desenvolvedor backend sênior do LootPrice** — conhece FastAPI, SQLModel, Alembic, PostgreSQL, crawlers, testes Python e regras de segurança do backend.

### 🎨 [`frontend-developer/SKILL.md`](./frontend-developer/SKILL.md)
**Quando usar:** Tarefas de React, TypeScript/TSX, Vite, SCSS, Biome, Jest, pnpm, UX, acessibilidade ou integração com a API.

Transforma qualquer IA CLI em um **desenvolvedor frontend sênior do LootPrice** — conhece a stack planejada, respeita contratos da API e não assume estrutura React antes de existir.

Se a skill `caveman` estiver ativa junto com backend ou frontend, use as regras técnicas da skill LootPrice e o formato curto do Caveman.

### 🔍 [`reviewer/SKILL.md`](./reviewer/SKILL.md)
**Quando usar:** Para revisar um Pull Request aberto.

Transforma qualquer IA CLI em um **revisor de código especializado** do LootPrice. Busca o PR via MCP GitHub, analisa o diff com o checklist do projeto e posta um review estruturado como comentário no PR.

```
@reviewer revisar PR #42
@reviewer revisar https://github.com/RodrigoVieira06/lootprice/pull/42
```

---

## Template de Pull Request

O template de PR está em **`.github/PULL_REQUEST_TEMPLATE.md`** — essa localização é obrigatória para o GitHub preencher o template automaticamente ao abrir PRs pela UI ou pela API.

Quando uma IA abre um PR via MCP GitHub, ela deve usar o conteúdo deste template como base para o corpo do PR.

---

## Estrutura

```
ai/
├── README.md                         ← Este arquivo
├── backend-developer/
│   └── SKILL.md                      ← Skill: backend sênior LootPrice
├── frontend-developer/
│   └── SKILL.md                      ← Skill: frontend sênior LootPrice
└── reviewer/
    ├── SKILL.md                      ← Skill: revisor de código LootPrice
    └── resources/
        ├── checklist.md              ← Referência: checklist de conformidade (B-01..G-05)
        └── review_format.md          ← Referência: formato exato do review em markdown
```

---

## Contexto do Projeto

Para entender o estado atual do projeto (cards, decisões, última sessão):
- **[`docs/project_state.md`](../docs/project_state.md)** — estado vivo (cards, decisões, débitos técnicos)
- **[`docs/architecture.md`](../docs/architecture.md)** — arquitetura, stack, contratos de API
- **[`docs/database_schema.md`](../docs/database_schema.md)** — schema completo do banco

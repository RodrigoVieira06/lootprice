# LootPrice — AI Tooling

> Este diretório contém as **skills** e ferramentas de IA do projeto LootPrice.
> Cada skill instrui uma IA CLI (Antigravity IDE, Claude Code, Gemini CLI, Cursor, Copilot) a desempenhar um papel específico neste projeto.

---

## Skills disponíveis

### 🧑‍💻 [`developer/SKILL.md`](./developer/SKILL.md)
**Quando usar:** Ao iniciar qualquer sessão de desenvolvimento no LootPrice.

Transforma qualquer IA CLI em um **desenvolvedor sênior especialista do LootPrice** — conhece a stack, respeita as regras rígidas do projeto, segue o workflow de 9 passos e usa os MCPs disponíveis corretamente.

```
Toda IA que trabalhar no LootPrice DEVE carregar esta skill primeiro.
```

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
├── developer/
│   ├── SKILL.md                      ← Skill: desenvolvedor sênior LootPrice
│   └── resources/
│       ├── stack.md                  ← Referência: stack completa + variáveis de ambiente
│       └── workflow.md               ← Referência: workflow de 9 passos + padrões de branch/commit
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

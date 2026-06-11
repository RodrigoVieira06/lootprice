# LootPrice — Referência: Workflow de Desenvolvimento

> Referência técnica para uso das skills. Sem instruções — só dados e exemplos.

---

## Fluxo de 9 Passos — Ciclo de Vida do Card

| Passo | Ação | Ferramenta |
|---|---|---|
| 1 | Mover card → **"Desenvolvendo"** | `transitionJiraIssue` — transição ID `21` |
| 2 | Criar branch a partir de `master` | `git checkout -b <prefixo>/<card-id>-descricao` |
| 3 | Desenvolver com commits convencionais incrementais | Git local |
| 4 | Push para branch remota | `git push origin <branch>` |
| 5 | Abrir PR para `master` com template | MCP GitHub `create_pull_request` |
| 6 | Mover card → **"Revisando"** | `transitionJiraIssue` — transição ID `31` |
| 7 | Executar review via skill `ai/reviewer/SKILL.md` | Skill de review |
| 8 | Notificar dev para merge manual (após CI verde + review aprovado) | Chat |
| 9 | Após merge: mover card → **"Deployed"** | `transitionJiraIssue` — transição ID `51` |

---

## Padrão de Nome de Branch

```
feat/<card-id>-descricao-curta      # nova funcionalidade
fix/<card-id>-descricao-curta       # correção de bug
chore/<card-id>-descricao-curta     # configuração, tooling, build
docs/<card-id>-descricao-curta      # apenas documentação
refactor/<card-id>-descricao-curta  # refatoração sem mudança de comportamento
test/<card-id>-descricao-curta      # apenas testes
```

**Exemplos reais do projeto:**
```
feat/card-01-monorepo-setup
feat/card-03-postgresql-alembic
fix/card-07-auth-token-expiry
chore/card-24-ai-code-review
```

---

## Conventional Commits — Padrão do Projeto

**Formato:** `tipo(escopo): descrição em minúsculas`

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `refactor` | Refatoração sem mudança de comportamento |
| `chore` | Configuração, build, tooling, dependências |
| `docs` | Documentação |
| `test` | Adição ou correção de testes |
| `perf` | Melhoria de performance |
| `ci` | Mudanças no pipeline de CI/CD |

**Exemplos reais:**
```
feat(crawler): adiciona suporte ao scraper da Fanatical
fix(auth): corrige expiração do refresh token
docs(architecture): atualiza seção de MCP toolchain
chore(deps): atualiza FastAPI para 0.115
test(api): adiciona testes para rota de busca
refactor(normalizer): extrai lógica de slug para utilitário separado
```

---

## Transições do Jira (IDs)

| Ação | ID de transição |
|---|---|
| Priorizado → Desenvolvendo | `21` |
| Desenvolvendo → Revisando | `31` |
| Revisando → Deployed | `51` |

**Projeto Jira:** `LP` (Loot Price)
**URL base:** `https://lootprice.atlassian.net/browse/LP-<numero>`

---

## Branch Protection Rules (GitHub — `master`)

- PR obrigatório — push direto bloqueado
- Status checks obrigatórios: `ci / Backend (Python)`, `ci / Frontend (React/TypeScript)`
- Stale reviews descartados ao novo push
- Merge: **sempre manual** pelo desenvolvedor humano

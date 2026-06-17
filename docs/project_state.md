# LootPrice — Estado do Projeto

> **Para qualquer LLM que ler este arquivo:** Este é o documento de estado vivo do projeto.
> Contém apenas dados — o que foi feito, o que está em progresso e decisões tomadas.
> As **instruções de como se comportar** estão nas skills de escopo em `ai/backend-developer/SKILL.md` e `ai/frontend-developer/SKILL.md`.
> Atualize este arquivo ao encerrar qualquer sessão onde arquivos foram criados, cards movidos ou decisões tomadas.

---

## Metadados

| Campo | Valor |
|---|---|
| **Versão** | 0.2.0 |
| **Última atualização** | 2026-06-12 |
| **Atualizado por** | Codex GPT-5 via CLI |
| **Fase atual** | Desenvolvimento — CARD-01 em andamento |
| **Próximos cards** | CARD-02 (CI), CARD-03 (PostgreSQL + Alembic), CARD-05 (model users) |

---

## Como atualizar este arquivo

Ao final de qualquer sessão onde ocorreu ao menos um dos itens abaixo, atualize as seções marcadas:

- Arquivo criado, editado ou deletado → **Estrutura de Arquivos**
- Card iniciado, concluído ou bloqueado → **Estado dos Cards**
- Decisão técnica tomada → **Decisões Tomadas**
- Bug ou bloqueio encontrado → **Débitos e Problemas**
- Sessão encerrada → **Última Sessão**

---

## Estado dos Cards

### Em Progresso
```
CARD-01 [LP-12] chore(infra): setup inicial do repositório monorepo
  Branch: chore/card-01-monorepo-setup
  Desde: 2026-06-02
  Status: Estrutura física criada e testada localmente. Docker pendente.
```

### Concluídos
```
(nenhum)
```

### Bloqueados
```
CARD-23 [LP-31] chore(infra): Nginx + CF-Connecting-IP
  Motivo: Requer domínio registrado para Cloudflare Tunnel. Ver DT-04.
  Prioridade rebaixada para Low.
```

### Próximos (sem bloqueio ativo)
```
CARD-02 [LP-14] chore(ci): pipeline CI com GitHub Actions
CARD-03 [LP-9]  feat(database): PostgreSQL + Alembic setup
CARD-05 [LP-10] feat(database): model users com OAuth e RBAC
```

---

## Estrutura de Arquivos Atual

```
lootprice/
├── .github/
│   ├── workflows/ci.yml              ✅ Lint (Ruff) + Pytest
│   └── PULL_REQUEST_TEMPLATE.md      ✅ Template para IAs que abrem PRs
│
├── ai/
│   ├── README.md                     ✅ Mapa das ferramentas de IA
│   ├── backend-developer/SKILL.md    ✅ Skill: backend sênior LootPrice
│   ├── frontend-developer/SKILL.md   ✅ Skill: frontend sênior LootPrice
│   └── reviewer/
│       ├── SKILL.md                  ✅ Skill: revisor de código
│       └── resources/
│           ├── checklist.md          ✅ Checklist de conformidade
│           └── review_format.md      ✅ Formato do review
│
├── docs/
│   ├── architecture.md               ✅ Arquitetura completa
│   ├── database_schema.md            ✅ Schema com todas as tabelas
│   ├── project_state.md              ✅ Este arquivo
│   └── project_cards.md              ⏳ Planejado; cards ativos estão no Jira
│
├── backend/
│   ├── app/
│   │   ├── __init__.py, api/, core/, models/, schemas/, crawlers/  ✅
│   ├── tests/__init__.py, test_main.py  ✅
│   ├── .env.example                  ✅
│   ├── main.py                       ✅
│   ├── requirements.txt              ✅
│   └── ruff.toml                     ✅
│
├── frontend/.gitkeep                  ⏳ Placeholder; SPA ainda não implementada
├── AGENTS.md                         ✅ Guia de contribuição para humanos e agentes
├── docker-compose.yml                ✅ PostgreSQL 15 em 127.0.0.1
├── Makefile                          ✅
├── lefthook.yml                      ✅
└── README.md                         ✅
```

---

## Decisões Tomadas

| Data | Decisão | Motivo | Alternativa Descartada |
|---|---|---|---|
| 2026-05 | Monorepo | 1 dev + LLM-assisted; contexto unificado | Multi-repo |
| 2026-05 | Alembic obrigatório desde o dia 1 | Evitar debt de schema sem rastreamento | `create_all` em produção |
| 2026-05 | `prices` como snapshot (sem histórico) | Simplicidade MVP; histórico é Fase 3 | Tabela append-only |
| 2026-05 | `canonical_name` editável pelo admin | Normalização automática falha em edge cases | Só dedup automático |
| 2026-05 | `NUMERIC(10,2)` para preços | Precisão exata para dinheiro | `Float` |
| 2026-05 | `slowapi` para rate limiting desde o MVP | API pública sem throttle é risco imediato | Sem rate limiting |
| 2026-06-01 | Migração para Jira | Gestão de backlog centralizada | GitHub Projects |
| 2026-06-03 | `revoked_tokens` no schema do MVP | Refresh tokens sem revogação são risco real | Redis para blacklist |
| 2026-06-03 | Ubuntu físico como dev (não VPS) | i7 10ª + 8GB — hardware superior a VPS nessa faixa | VPS paga |
| 2026-06-03 | Tailscale + Cloudflare Tunnel como infra | SSH seguro sem IP fixo; HTTPS sem abrir portas | DDNS + port forwarding |
| 2026-06-03 | Manter `python-jose` no MVP | Trocar adiciona risco sem benefício imediato | Migração imediata para PyJWT |
| 2026-06-09 | CARD-23 rebaixado para Low | Cloudflare Tunnel bloqueado sem domínio. `get_real_ip()` absorvida pelo CARD-17 | Executar CARD-23 agora |
| 2026-06-10 | PostgreSQL bound em `127.0.0.1` no compose | Segurança: banco não escuta em todos os IPs | Expor na porta pública |
| 2026-06-10 | AI Review via Skill em vez de GitHub Actions | `ai-review.yml` com erros persistentes. Skill via MCP GitHub tem contexto superior e zero infraestrutura de Actions | Manter `ai-review.yml` |
| 2026-06-10 | `llm_context.md` decomposto em `ai/developer/SKILL.md` + `docs/project_state.md` | Arquivo único de 650+ linhas misturava instruções e estado, causando falhas de contexto | Manter arquivo monolítico |
| 2026-06-10 | PostHog para Métricas e Analytics | Centraliza Product Analytics, Session Replay e Feature Flags com esforço mínimo e plano gratuito amplo | Umami + Sentry + Admin Dashboard próprio |
| 2026-06-12 | Fonte de verdade operacional definida para IAs | Evitar que skills executem comandos/pastas ainda planejados na arquitetura | Tratar arquitetura como estado implementado |
| 2026-06-12 | Skill genérica de developer separada por escopo | Reduzir ambiguidade entre backend implementado e frontend planejado | Manter `ai/developer/SKILL.md` única |
| 2026-06-12 | Stack frontend atualizada para SCSS + Biome + Jest + pnpm | Evitar TailwindCSS e padronizar tooling antes da criação da base frontend | TailwindCSS, ESLint e npm como padrões frontend |
| 2026-06-12 | Schema separa `games`, `store_products` e `prices` | Evitar acoplamento entre jogo canônico e produto específico de loja; preparar Steam app_id, URLs da Nuuvem e lojas futuras | `prices` referenciar diretamente `(game_id, store_id)` |


---

## Débitos Técnicos e Problemas Conhecidos

| ID | Problema | Impacto | Status |
|---|---|---|---|
| DT-01 | Limpeza periódica de `revoked_tokens` expirados não implementada | Tabela cresce indefinidamente — sem impacto funcional no MVP | Aberto — `DELETE WHERE expires_at < NOW()` via cron na Fase 2 |
| DT-02 | `python-jose` com manutenção irregular | Pode ficar sem patches de segurança | Monitorar — migrar para `PyJWT` + `authlib` se inativo 6+ meses |
| DT-03 | Sem validação de IPs Cloudflare no header `X-Forwarded-For` | Header pode ser forjado em ambiente não-Cloudflare | Aberto — validar IPs Cloudflare em produção |
| DT-04 | CARD-23 bloqueado por ausência de domínio | Cloudflare Tunnel não funciona sem domínio; `get_real_ip()` implementada no CARD-17 como mitigação | Bloqueado — executar após aquisição de domínio |

---

## Última Sessão

**Data:** 2026-06-12
**LLM:** Codex GPT-5 via CLI

**O que foi feito:**
- Criado `AGENTS.md` com guia de contribuição específico do repositório
- Documentados estrutura atual, comandos reais do Makefile, padrões de código, testes, commits, PRs e instruções para agentes
- Alinhadas skills em `ai/` com `docs/architecture.md` e com o estado real do repositório
- Separados comandos ativos de comandos planejados nas skills backend/frontend e na documentação
- Ajustadas regras de CI/review para refletir backend ativo e frontend ainda desabilitado
- Removida a skill genérica `ai/developer`
- Criadas `ai/backend-developer/SKILL.md` e `ai/frontend-developer/SKILL.md`
- Atualizadas referências para combinar backend/frontend com a skill `caveman` quando habilitada
- Atualizada stack frontend planejada: React mais recente, TypeScript/TSX, Vite, SCSS, Axios, Zod, React Hook Form, Zustand, Biome, Jest e pnpm
- Refeito `docs/database_schema.md` para o MVP com visão de evolução por fases

**O que fazer na próxima sessão:**
- Executar CARD-01 se pendente (Docker no host Ubuntu)
- Abrir PR do CARD-01 e usar `ai/reviewer/SKILL.md` para validar o review em produção
- Avançar para CARD-02 (pipeline CI) ou CARD-03 (PostgreSQL + Alembic)

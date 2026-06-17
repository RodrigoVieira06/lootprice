# Checklist de Conformidade — LootPrice

> Este checklist é a fonte de verdade para o revisor de código.
> Cada item deve ser verificado no diff do PR. Se não se aplica ao diff, marque N/A.

---

## 🐍 Backend (Python / FastAPI)

| # | Regra | Como verificar |
|---|---|---|
| B-01 | Rotas FastAPI usam `async def` + `await` em todas as chamadas de I/O | Procurar `def ` (sem async) em arquivos de `app/api/` |
| B-02 | Type hints em todos os parâmetros e retornos de função | Procurar funções sem anotação de tipo: `def foo(x):` |
| B-03 | Campos monetários usam `Decimal` ou `NUMERIC(10,2)` — nunca `float` ou `Float` | Buscar `float` em modelos, schemas e crawlers |
| B-04 | Alterações de schema têm migration Alembic correspondente | Se `models/` foi alterado, checar se há arquivo novo em `migrations/versions/` |
| B-05 | `hashed_password` nunca é retornado em responses | Checar schemas de response (`schemas/`) — campo não deve aparecer |
| B-06 | Sem variáveis sensíveis hardcoded | Procurar strings longas aleatórias, URLs com credenciais, chaves de API hardcoded |
| B-07 | `logging` padrão do Python — nunca `print()` em código de produção | Buscar `print(` fora de arquivos de teste |
| B-08 | Validação Pydantic em toda entrada de crawler antes de tocar o banco | Crawlers devem usar `RawGameData` antes de qualquer operação de banco |
| B-09 | `try/except` com log explícito em todo bloco de scraping | Funções `fetch()` dos crawlers devem ter tratamento de exceção |
| B-10 | Nunca usar `requests` síncrono — sempre HTTPX async | Buscar `import requests` em código de produção |
| B-11 | `SQLModel.metadata.create_all()` apenas em testes — nunca em produção | Verificar se aparece fora de `conftest.py` ou arquivos de teste |
| B-12 | Testes escritos para nova funcionalidade | Se há novo código em `app/`, checar se há arquivo correspondente em `tests/` |

---

## ⚛️ Frontend (React / TypeScript)

| # | Regra | Como verificar |
|---|---|---|
| F-01 | TypeScript estrito — sem `any` explícito | Buscar `: any` ou `as any` no diff |
| F-02 | Componentes novos têm tipos corretos nas props | Props de componentes devem ter interface ou type declarado |
| F-03 | Nenhum dado sensível no `localStorage` sem criptografia | Buscar `localStorage.setItem` e verificar o que está sendo armazenado |
| F-04 | Estilos usam SCSS, sem TailwindCSS | Buscar `tailwind`, classes utilitárias extensas ou dependências Tailwind |
| F-05 | Biome é usado para lint/format/imports | Checar `biome.json` e scripts de `package.json` |
| F-06 | Testes frontend usam Jest | Checar scripts e arquivos `*.test.ts`/`*.test.tsx` |
| F-07 | Gerenciador frontend é pnpm | Checar `pnpm-lock.yaml` e evitar `package-lock.json`/`yarn.lock` |

---

## 🔒 Segurança

| # | Regra | Como verificar |
|---|---|---|
| S-01 | Sem SQL injection | Verificar queries — devem usar ORM (SQLModel) ou parâmetros bindados |
| S-02 | Sem XSS em responses | Strings de usuário não devem ser inseridas em HTML sem sanitização |
| S-03 | Sem credenciais ou secrets no código | Procurar padrões de chaves (ex: `sk-`, `ghp_`, UUIDs hardcoded como segredos) |
| S-04 | JWT implementado corretamente | Usar `core/security.py` — não reimplementar lógica JWT inline |
| S-05 | `hashed_password` não exposta em responses de API | Nenhum schema de response deve incluir esse campo |
| S-06 | Rate limiting preservado | Novas rotas públicas devem usar o decorator `@limiter.limit(...)` do slowapi |

---

## 📝 Geral

| # | Regra | Como verificar |
|---|---|---|
| G-01 | Título do PR segue Conventional Commits | Formato: `tipo(escopo): descrição` — ex: `feat(auth): adiciona refresh token` |
| G-02 | Branch segue o padrão do projeto | Formato: `feat/card-XX-descricao`, `fix/card-XX-descricao`, etc. |
| G-03 | `docs/project_state.md` atualizado se houve decisão técnica | Se o PR muda arquitetura, stack ou processo — o arquivo deve refletir |
| G-04 | Sem código comentado (dead code) | Blocos comentados que não são documentação devem ser removidos |
| G-05 | CI passou (lint + testes) | Verificar via `get_pull_request_status` — checar `CI — Lint & Tests / Backend (Python)`; frontend só é obrigatório após o job ser reativado |

---

## 🚦 Legenda de Status

| Status | Significado |
|---|---|
| ✅ | Conforme — sem problemas |
| ❌ | Não conforme — deve ser corrigido |
| ⚠️ | Atenção — risco potencial ou sugestão de melhoria |
| N/A | Não aplicável a este PR |

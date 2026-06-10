## 📋 Card Relacionado

<!-- Obrigatório: vincule o card do Jira -->
- Jira: [LP-XX](https://lootprice.atlassian.net/browse/LP-XX)
- Card: CARD-XX — Descrição breve do card

---

## 🧾 O que foi feito

<!-- Descreva em linguagem simples o que este PR implementa ou corrige -->

-
-
-

---

## 🔗 Tipo de Mudança

<!-- Marque com [x] o que se aplica -->

- [ ] `feat` — Nova funcionalidade
- [ ] `fix` — Correção de bug
- [ ] `refactor` — Refatoração sem mudança de comportamento
- [ ] `chore` — Configuração, build, tooling
- [ ] `docs` — Documentação
- [ ] `test` — Testes
- [ ] `perf` — Melhoria de performance
- [ ] `ci` — Mudanças no pipeline de CI/CD

---

## ✅ Checklist do Desenvolvedor

**Antes de abrir o PR, confirme:**

### Backend (Python/FastAPI)
- [ ] Rotas FastAPI usam `async/await`
- [ ] Type hints em todas as funções
- [ ] Nenhum campo monetário usa `float` (usar `Decimal` / `NUMERIC`)
- [ ] Alterações de schema têm migration Alembic (`make migrate-create`)
- [ ] Nenhuma senha (`hashed_password`) retornada em responses de API
- [ ] Nenhuma variável sensível hardcoded (usar `.env` + `pydantic-settings`)
- [ ] `logging` usado, nunca `print()` em código de produção
- [ ] Testes escritos para a nova funcionalidade (`tests/test_<módulo>.py`)

### Frontend (React/TypeScript)
- [ ] TypeScript estrito — sem `any` explícito
- [ ] Componentes novos têm tipos corretos nas props
- [ ] Nenhum dado sensível no `localStorage` sem criptografia

### Geral
- [ ] Título do PR segue Conventional Commits (`feat(auth): ...`)
- [ ] CI passou (lint + testes)
- [ ] `docs/llm_context.md` atualizado se houve decisão técnica nova
- [ ] Revisão da IA concluída com nota (grade) registrada nos comentários do PR
- [ ] Nota de qualidade do PR é satisfatória (desejável >= 8/10) e todos os bloqueios da IA resolvidos

---

## 🤖 Nota para a IA Revisora

<!-- NÃO EDITAR — instrução automática para o bot de review -->
> Este PR deve ser revisado pelo workflow `ai-review.yml`.
> O review automático acontecerá em instantes após a abertura do PR.
> Verifique os comentários automáticos antes de solicitar aprovação humana.

---

## 📸 Evidências (opcional)

<!-- Screenshots, logs de teste, output do terminal — se aplicável -->

---

## 💬 Contexto Adicional

<!-- Qualquer informação que o revisor (humano ou IA) deva saber -->

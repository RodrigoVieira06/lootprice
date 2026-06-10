<!--
  ╔══════════════════════════════════════════════════════════════════╗
  ║  INSTRUÇÃO PARA IAs QUE ESTÃO ABRINDO ESTE PR                  ║
  ║                                                                  ║
  ║  Antes de enviar, preencha TODOS os campos abaixo com base     ║
  ║  no trabalho realizado. Não deixe campos vazios ou com valores  ║
  ║  de placeholder. Remova os comentários HTML após preencher.    ║
  ╚══════════════════════════════════════════════════════════════════╝
-->

## 📋 Card Relacionado

<!-- Obrigatório: vincule o card do Jira e do GitHub Issue correspondente -->
- Jira: [LP-XX](https://lootprice.atlassian.net/browse/LP-XX)
- Card: CARD-XX — Descrição breve do card

---

## 🧾 O que foi feito

<!-- Descreva em linguagem simples o que este PR implementa ou corrige.
     Use bullet points. Seja específico: mencione arquivos criados, funções implementadas,
     decisões tomadas e o motivo de cada uma. Não use linguagem vaga como "melhorias gerais". -->

-
-
-

---

## 🔗 Tipo de Mudança

<!-- Marque com [x] o que se aplica — pode ser mais de um -->

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

<!-- Marque com [x] cada item verificado. Se um item não se aplica a este PR, marque [x] e escreva N/A após. -->

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
- [ ] `docs/project_state.md` atualizado se houve decisão técnica nova

---

## 📸 Evidências (opcional)

<!-- Screenshots, logs de teste, output do terminal — se aplicável -->

---

## 💬 Contexto Adicional

<!-- Qualquer informação que o revisor humano deva saber:
     trade-offs considerados, alternativas descartadas, débitos técnicos criados,
     dependências de outros cards, etc. -->

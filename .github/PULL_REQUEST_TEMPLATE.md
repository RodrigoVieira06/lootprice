<!--
  ╔══════════════════════════════════════════════════════════════════╗
  ║  INSTRUÇÃO PARA ABERTURA ESTE PR                                 ║
  ║                                                                  ║
  ║  Antes de enviar, preencha TODOS os campos abaixo com base       ║
  ║  no trabalho realizado. Não deixe campos vazios ou com valores   ║
  ║  de placeholder. Remova os comentários HTML após preencher.      ║
  ╚══════════════════════════════════════════════════════════════════╝
-->

## 📋 Issue Relacionada

<!-- Obrigatório: vincule a issue do GitHub -->
Closes #XX

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
- [ ] Alterações de schema têm migration Alembic
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
- [ ] `AGENTS.md` §15 atualizado se houve decisão técnica nova

---

## 📸 Evidências (opcional)

<!-- Screenshots, logs de teste, output do terminal — se aplicável -->

---

## 💬 Contexto Adicional

<!-- Qualquer informação que o revisor humano deva saber:
     trade-offs considerados, alternativas descartadas, débitos técnicos criados,
     dependências de outros cards, etc. -->

# Formato do Review — LootPrice AI Reviewer

> Este arquivo define o formato **exato** que o review deve seguir.
> Copie a estrutura abaixo e preencha cada seção. Não omita seções — se não houver conteúdo,
> escreva a mensagem padrão indicada em cada seção.

---

## Template

```markdown
## 🤖 AI Code Review — LootPrice

**PR #<NÚMERO> — <TÍTULO DO PR>**
**Revisor:** <identificador da IA — ex: "Claude Sonnet 4.6" ou "Gemini 2.0 Flash"> | **Data:** <data atual em dd/mm/aaaa>

---

### 📊 Nota Geral: X/10

> <Justificativa resumida da nota em 1–2 frases.>

---

### ✅ Pontos Positivos

<Liste o que foi bem feito — código limpo, boas práticas seguidas, testes presentes, etc.>
<Se nada se destacar positivamente, escreva: *Nenhum ponto positivo de destaque identificado.*>

---

### 🚨 Bloqueios — Devem ser corrigidos ANTES do merge

<Liste problemas críticos que impedem o merge.>
<Para cada bloqueio, use o formato:>

**[B-X] Título do problema**
- **Arquivo:** `caminho/do/arquivo.py` (linha X)
- **Problema:** Descrição clara do problema.
- **Sugestão:** Como corrigir.

<Se não houver bloqueios, escreva: *Nenhum bloqueio identificado.*>

---

### ⚠️ Sugestões — Não bloqueantes, mas recomendadas

<Melhorias de qualidade, legibilidade, performance, boas práticas.>
<Para cada sugestão, use o formato:>

**[S-X] Título da sugestão**
- **Arquivo:** `caminho/do/arquivo.py` (linha X)
- **Sugestão:** Descrição da melhoria e motivo.

<Se não houver sugestões, escreva: *Nenhuma sugestão adicional.*>

---

### ❓ Questionamentos

<Perguntas para o autor do PR sobre decisões de design, trade-offs ou intenções não claras.>
<Se não houver questionamentos, escreva: *Sem questionamentos.*>

---

### 🔒 Segurança

<Avaliação dos itens de segurança do checklist (S-01 a S-06).>
<Se não há arquivos de segurança alterados no diff, escreva: *Nenhum vetor de segurança identificado no diff.*>

---

### 📋 Conformidade com os Padrões do Projeto

| # | Regra | Status |
|---|---|---|
| B-01 | Rotas FastAPI usam `async/await` | ✅ / ❌ / N/A |
| B-02 | Type hints em todas as funções Python | ✅ / ❌ / N/A |
| B-03 | Campos monetários usam `Decimal`/`NUMERIC` | ✅ / ❌ / N/A |
| B-04 | Alterações de schema têm migration Alembic | ✅ / ❌ / N/A |
| B-05 | `hashed_password` não exposta em responses | ✅ / ❌ / N/A |
| B-06 | Sem variáveis sensíveis hardcoded | ✅ / ❌ / N/A |
| B-07 | `logging` usado (sem `print()` em produção) | ✅ / ❌ / N/A |
| B-08 | Validação Pydantic nas entradas de crawler | ✅ / ❌ / N/A |
| B-12 | Testes para funcionalidade nova | ✅ / ❌ / N/A |
| F-01 | TypeScript estrito — sem `any` explícito | ✅ / ❌ / N/A |
| F-02 | Componentes novos têm props tipadas | ✅ / ❌ / N/A |
| F-03 | Sem dados sensíveis inseguros no `localStorage` | ✅ / ❌ / N/A |
| F-04 | Estilos usam SCSS, sem TailwindCSS | ✅ / ❌ / N/A |
| F-05 | Biome usado para lint/format/imports | ✅ / ❌ / N/A |
| F-06 | Testes frontend usam Jest | ✅ / ❌ / N/A |
| F-07 | Gerenciador frontend é pnpm | ✅ / ❌ / N/A |
| G-01 | Conventional Commits no título do PR | ✅ / ❌ |
| G-02 | Padrão de nome de branch correto | ✅ / ❌ |
| G-03 | `AGENTS.md` §15 atualizado | ✅ / ❌ / N/A |
| G-05 | CI passou (lint + testes) | ✅ / ❌ / ⏳ Pendente |

---

### 🏁 Veredicto Final

- [ ] **APROVADO** — Pode ser mergeado
- [ ] **APROVADO COM RESSALVAS** — Pode ser mergeado, mas as sugestões devem ser tratadas em seguida
- [ ] **REPROVADO** — Corrija os bloqueios antes do merge

---

*Review gerado pela skill `ai/reviewer/SKILL.md`. Dúvidas sobre o review? Fale com o mantenedor do repositório.*
```

---

## Notas sobre preenchimento

- **Nota numérica:** Seja justo e criterioso. Uma nota 10 é rara — reservada para código verdadeiramente impecável.
- **Calibragem da nota:** Se houver veredicto **APROVADO COM RESSALVAS**, a nota máxima é **8/10**. Se houver qualquer item `⚠️` em regra obrigatória do checklist, a nota máxima é **8/10**. Se a ressalva estiver ligada a regra obrigatória do projeto, use **7/10** ou **8/10**, conforme impacto. Se houver bloqueio, a nota máxima é **6/10**.
- **Justificativa da nota:** Quando a nota for menor que 10, cite o principal fator que limitou a nota.
- **Bloqueios vs Sugestões:** Bloqueios são problemas que causam bugs, violam regras do projeto ou criam riscos de segurança. Sugestões são melhorias de qualidade de vida que não impedem o funcionamento.
- **Tabela de conformidade:** Preencha todos os itens. N/A é válido para regras que não se aplicam ao diff (ex: B-03 se o PR não toca campos monetários).
- **Veredicto:** Marque apenas **um** com `[x]`. Se há qualquer bloqueio, o veredicto é obrigatoriamente REPROVADO.
- **Idioma:** O review deve ser sempre em **português brasileiro**, incluindo descrições de problemas e sugestões.

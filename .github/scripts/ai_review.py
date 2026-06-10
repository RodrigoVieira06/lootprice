#!/usr/bin/env python3
"""Script de AI Code Review para LootPrice.
Chamado pelo workflow .github/workflows/ai-review.yml.
"""

import os
import json
import sys
import requests


def main():
    # Lê variáveis de ambiente
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("❌ GEMINI_API_KEY não configurada. Verifique os secrets do repositório.")
        sys.exit(1)

    pr_title = os.environ.get("PR_TITLE", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    pr_author = os.environ.get("PR_AUTHOR", "")
    pr_body = os.environ.get("PR_BODY", "")
    pr_base = os.environ.get("PR_BASE_BRANCH", "")
    pr_head = os.environ.get("PR_HEAD_BRANCH", "")
    diff_size = int(os.environ.get("DIFF_SIZE", "0"))

    # Lê arquivos gerados nos steps anteriores
    with open("/tmp/pr_diff_truncated.txt", "r", encoding="utf-8", errors="replace") as f:
        diff_content = f.read()

    with open("/tmp/llm_context_trunc.txt", "r", encoding="utf-8", errors="replace") as f:
        llm_context = f.read()

    with open("/tmp/architecture_trunc.txt", "r", encoding="utf-8", errors="replace") as f:
        architecture = f.read()

    truncated_note = ""
    if diff_size > 15000:
        truncated_note = (
            f"\n> ⚠️ *Diff truncado: {diff_size} bytes totais, "
            f"analisados os primeiros 15.000 bytes.*\n"
        )

    prompt = (
        "Você é um revisor de código sênior do projeto **LootPrice**.\n\n"
        "Seu papel é revisar Pull Requests com rigor técnico, segurança e alinhamento "
        "com as regras do projeto.\n"
        "A resposta DEVE ser em **português brasileiro**.\n\n"
        "## Contexto do Projeto\n\n"
        "### Arquivo llm_context.md (resumo):\n"
        f"{llm_context}\n\n"
        "### Arquivo architecture.md (resumo):\n"
        f"{architecture}\n\n"
        "---\n\n"
        "## Pull Request a Revisar\n\n"
        f"- **PR #{pr_number}:** {pr_title}\n"
        f"- **Autor:** {pr_author}\n"
        f"- **Branch:** `{pr_head}` → `{pr_base}`\n"
        "- **Descrição do PR:**\n"
        f"{pr_body if pr_body else '(sem descrição)'}\n\n"
        "## Diff das Alterações:\n"
        "```diff\n"
        f"{diff_content}\n"
        "```\n"
        f"{truncated_note}\n"
        "---\n\n"
        "## Sua Tarefa\n\n"
        "Analise o diff acima e produza um review estruturado EXATAMENTE no formato abaixo.\n"
        "Seja direto, técnico e construtivo. Se algo estiver correto, diga que está correto.\n"
        "Se houver problemas graves, aponte claramente como BLOQUEIO.\n\n"
        "### Critério de Nota (Controle de Qualidade):\n"
        "Atribua uma nota de 0 a 10 para o PR:\n"
        "- **10/10**: Código impecável, sem sugestões ou bloqueios.\n"
        "- **8/10 a 9/10**: Código bom, funcional, sem bloqueios, com pequenas sugestões não-impeditivas.\n"
        "- **7/10**: Código aceitável, mas com sugestões importantes de melhoria.\n"
        "- **Abaixo de 7/10**: Código com problemas significativos, bugs potenciais ou descumprimento de regras.\n\n"
        "---\n\n"
        "## Formato do Review (use EXATAMENTE esta estrutura em markdown):\n\n"
        "## 🤖 AI Code Review — LootPrice\n\n"
        f"**PR #{pr_number} — {pr_title}**\n"
        "**Revisor:** Gemini AI | **Data:** (data atual)\n\n"
        "---\n\n"
        "### 📊 Nota Geral: X/10\n\n"
        "> Justificativa resumida da nota em 1-2 frases.\n\n"
        "---\n\n"
        "### ✅ Pontos Positivos\n\n"
        "(Liste o que foi bem feito. Se nada se destacar positivamente, omita esta seção.)\n\n"
        "---\n\n"
        "### 🚨 Bloqueios — Devem ser corrigidos ANTES do merge\n\n"
        "(Liste problemas críticos que impedem o merge. Inclua: linha do arquivo, "
        "problema e sugestão de correção.\n"
        "Se não houver bloqueios, escreva: *Nenhum bloqueio identificado.*)\n\n"
        "---\n\n"
        "### ⚠️ Sugestões — Não bloqueantes, mas recomendadas\n\n"
        "(Melhorias de qualidade, legibilidade, performance, boas práticas. "
        "Não são obrigatórias para o merge.)\n\n"
        "---\n\n"
        "### ❓ Questionamentos\n\n"
        "(Perguntas para o autor do PR sobre decisões de design, trade-offs ou "
        "intenções não claras no código.)\n\n"
        "---\n\n"
        "### 🔒 Segurança\n\n"
        "(Avalie: SQL injection, XSS, dados sensíveis expostos, JWT mal implementado, "
        "hashed_password em responses, variáveis hardcoded, etc.)\n\n"
        "---\n\n"
        "### 📋 Conformidade com as Regras do Projeto\n\n"
        "| Regra | Status |\n"
        "|---|---|\n"
        "| Rotas FastAPI usam `async/await` | ✅ / ❌ / N/A |\n"
        "| Type hints em todas as funções Python | ✅ / ❌ / N/A |\n"
        "| Campos monetários usam `Decimal`/`NUMERIC`, não `float` | ✅ / ❌ / N/A |\n"
        "| Alterações de schema têm migration Alembic | ✅ / ❌ / N/A |\n"
        "| `hashed_password` não exposta em responses | ✅ / ❌ / N/A |\n"
        "| Sem variáveis sensíveis hardcoded | ✅ / ❌ / N/A |\n"
        "| Conventional Commits no título do PR | ✅ / ❌ |\n"
        "| Testes para funcionalidade nova | ✅ / ❌ / N/A |\n"
        "| `logging` usado (sem `print()` em produção) | ✅ / ❌ / N/A |\n\n"
        "---\n\n"
        "### 🏁 Veredicto Final\n\n"
        "- [ ] **APROVADO** — Pode ser mergeado\n"
        "- [ ] **APROVADO COM RESSALVAS** — Pode ser mergeado, mas as sugestões devem ser tratadas\n"
        "- [ ] **REPROVADO** — Corrija os bloqueios antes do merge\n\n"
        "---\n"
        "*Review gerado automaticamente pelo workflow `ai-review.yml`. "
        "Questões sobre o review? Fale com o mantenedor do repositório.*\n"
    )

    # Chama a API do Gemini
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
        },
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    review_text = result["candidates"][0]["content"]["parts"][0]["text"]

    # Salva o review para o próximo step
    with open("/tmp/ai_review.md", "w", encoding="utf-8") as f:
        f.write(review_text)

    print("✅ Review gerado com sucesso.")
    print(f"Tamanho do review: {len(review_text)} chars")


if __name__ == "__main__":
    main()

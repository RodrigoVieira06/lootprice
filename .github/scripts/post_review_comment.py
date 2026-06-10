#!/usr/bin/env python3
"""Script que posta o review gerado como comentário no PR do GitHub."""

import json
import os
import sys
import requests


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    repo = os.environ.get("REPO", "")

    if not token or not pr_number or not repo:
        print("❌ Variáveis de ambiente obrigatórias ausentes: GITHUB_TOKEN, PR_NUMBER, REPO")
        sys.exit(1)

    with open("/tmp/ai_review.md", "r", encoding="utf-8") as f:
        review_body = f.read()

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {"body": review_body}

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    print(f"✅ Comentário postado no PR #{pr_number}: {response.json()['html_url']}")


if __name__ == "__main__":
    main()

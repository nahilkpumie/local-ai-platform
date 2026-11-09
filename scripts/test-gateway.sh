#!/usr/bin/env bash
# Teste la passerelle LiteLLM : santé, modèles, réponse d'un modèle
set -euo pipefail
cd "$(dirname "$0")/.."
set -a
# shellcheck source=/dev/null
source .env
set +a

URL="http://localhost:4000"
MODEL="${1:-gemini-flash}"

echo "== 1. Santé de LiteLLM"
curl -sf "$URL/health/liveliness" && echo

echo "== 2. Modèles visibles avec la clé Open WebUI"
curl -sf "$URL/v1/models" -H "Authorization: Bearer $WEBUI_LITELLM_KEY" \
  | python3 -c 'import sys,json; [print(" -", m["id"]) for m in json.load(sys.stdin)["data"]]'

echo "== 3. Question au modèle $MODEL"
curl -sf "$URL/v1/chat/completions" \
  -H "Authorization: Bearer $WEBUI_LITELLM_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Réponds en une phrase : à quoi sert une passerelle LLM ?\"}]}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["choices"][0]["message"]["content"])'

echo "== OK"

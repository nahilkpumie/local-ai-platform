#!/usr/bin/env bash
# Démontre les contrôles de sécurité de LiteLLM :
#  1. restriction des modèles par clé
#  2. limite de requêtes par minute (rate limit)
#  3. suivi des dépenses par clé
set -euo pipefail
cd "$(dirname "$0")/.."
set -a
# shellcheck source=/dev/null
source .env
set +a

URL="http://localhost:4000"
ADMIN=(-H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json")

echo "== Création d'une clé de test : 1 seul modèle local, 2 requêtes/minute max"
TEST_KEY=$(curl -sf "$URL/key/generate" "${ADMIN[@]}" \
  -d '{"key_alias":"demo-quota","models":["local-llama"],"rpm_limit":2,"max_budget":1,"duration":"1h"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["key"])')
echo "Clé créée : ${TEST_KEY:0:10}..."

ask() {
  curl -s -o /dev/null -w "%{http_code}" "$URL/v1/chat/completions" \
    -H "Authorization: Bearer $TEST_KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"$1\",\"messages\":[{\"role\":\"user\",\"content\":\"Dis OK\"}],\"max_tokens\":5}"
}

echo
echo "== Test 1 : modèle non autorisé (gemini-flash) -> attendu : 403 (refusé)"
echo "Code HTTP : $(ask gemini-flash)"

echo
echo "== Test 2 : 4 requêtes rapides sur local-llama -> attendu : 200, 200, puis 429"
for i in 1 2 3 4; do
  echo "Requête $i : $(ask local-llama)"
done

echo
echo "== Test 3 : dépenses et usage de la clé"
curl -sf "$URL/key/info?key=$TEST_KEY" "${ADMIN[@]}" \
  | python3 -c 'import sys,json; i=json.load(sys.stdin)["info"]; print("alias:", i.get("key_alias"), "| dépensé:", i.get("spend"), "| budget max:", i.get("max_budget"), "| rpm:", i.get("rpm_limit"))'

echo
echo "== Nettoyage : suppression de la clé de test"
curl -sf "$URL/key/delete" "${ADMIN[@]}" -d "{\"keys\":[\"$TEST_KEY\"]}" > /dev/null && echo "Clé supprimée"

#!/usr/bin/env bash
# Run map SQL on NAS via one-shot Dockge stack.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PUT="$ROOT/.cursor/skills/truenas-scale/scripts/tn-put.mjs"
DOCKGE="$ROOT/.cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs"
REMOTE="${POSTIZ_APPLY_DIR:-/mnt/apps/dockge/postiz-apply-map}"
SQL="$ROOT/instance/postiz/postiz-apply.sql"
ENVF="$ROOT/instance/postiz/.env"

if [[ ! -f "$SQL" ]]; then
  echo "missing $SQL — run instance/maps/map-postiz/apply.py" >&2
  exit 1
fi

# shellcheck disable=SC1090
set -a
source "$ENVF"
set +a
if [[ -z "${POSTGRES_USER:-}" || -z "${POSTGRES_DB:-}" ]]; then
  echo "missing POSTGRES_USER/POSTGRES_DB in instance/postiz/.env" >&2
  exit 1
fi

tmp="$(mktemp)"
printf 'POSTGRES_USER=%s\nPOSTGRES_DB=%s\n' "$POSTGRES_USER" "$POSTGRES_DB" >"$tmp"
node "$PUT" "$ROOT/postiz/scripts/host-apply-map.compose.yaml" "$REMOTE/compose.yaml"
node "$PUT" "$SQL" "$REMOTE/apply.sql"
node "$PUT" "$tmp" "$REMOTE/.env"
rm -f "$tmp"

node "$DOCKGE" start postiz-apply-map
echo "map SQL applied"

#!/usr/bin/env bash
# Postiz MCP (church org). Key from instance/postiz/.env
set -euo pipefail
# shellcheck disable=SC1091
source "$(dirname "$0")/path.sh"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$ROOT/instance/caddy/.env"
# shellcheck disable=SC1091
source "$ROOT/instance/postiz/.env"
set +a

if [[ -z "${POSTIZ_DOMAIN:-}" ]]; then
  echo "POSTIZ_DOMAIN missing in instance/caddy/.env" >&2
  exit 1
fi
if [[ -z "${POSTIZ_CHURCH_API_KEY:-}" ]]; then
  echo "POSTIZ_CHURCH_API_KEY missing — run python3 instance/maps/map-postiz/apply.py" >&2
  exit 1
fi

NPX="$(command -v npx || true)"
if [[ -z "$NPX" ]]; then
  echo "npx not found. Install Node 22+." >&2
  exit 1
fi
exec "$NPX" -y mcp-remote "https://${POSTIZ_DOMAIN}/mcp" --header "Authorization: Bearer ${POSTIZ_CHURCH_API_KEY}"

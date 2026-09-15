#!/usr/bin/env bash
# Home MCP (/api/mcp). Token from instance/home/.env
set -euo pipefail
# shellcheck disable=SC1091
source "$(dirname "$0")/path.sh"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$ROOT/instance/home/.env"
set +a

base="${HOME_URL:-}"
if [[ -z "$base" ]]; then
  echo "HOME_URL missing in instance/home/.env" >&2
  exit 1
fi
if [[ "$base" != http://* && "$base" != https://* ]]; then
  base="http://${base}"
fi
base="${base%/}"

if [[ -z "${HOME_MCP_TOKEN:-}" ]]; then
  echo "HOME_MCP_TOKEN missing in instance/home/.env" >&2
  exit 1
fi

NPX="$(command -v npx || true)"
if [[ -z "$NPX" ]]; then
  echo "npx not found. Install Node 22+ (Homebrew: /opt/homebrew/bin or /usr/local/bin)." >&2
  exit 1
fi
exec "$NPX" -y mcp-remote "${base}/api/mcp" --header "Authorization: Bearer ${HOME_MCP_TOKEN}"

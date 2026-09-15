#!/usr/bin/env bash
# stdio Gitea MCP. Token+host from instance/gitea/.env
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
# shellcheck disable=SC1091
set -a
source "$ROOT/instance/gitea/.env"
set +a
BIN="$ROOT/.cursor/mcp/bin/gitea-mcp"
if [[ ! -x "$BIN" ]]; then
  echo "missing $BIN — run: bash .cursor/mcp/install-gitea-mcp.sh" >&2
  exit 1
fi
if [[ -z "${GITEA_HOST:-}" ]]; then
  echo "GITEA_HOST missing in instance/gitea/.env" >&2
  exit 1
fi
exec "$BIN" -t stdio --host "$GITEA_HOST"

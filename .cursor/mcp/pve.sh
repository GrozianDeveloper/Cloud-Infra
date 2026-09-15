#!/usr/bin/env bash
# stdio Proxmox VE MCP. Creds from instance/proxmox/.env
set -euo pipefail
# shellcheck disable=SC1091
source "$(dirname "$0")/path.sh"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$ROOT/instance/proxmox/.env"
set +a
export PVE_VERIFY_SSL="${PVE_VERIFY_SSL:-false}"

NPX="$(command -v npx || true)"
if [[ -z "$NPX" ]]; then
  echo "npx not found. Install Node 22+ (Homebrew: /opt/homebrew/bin or /usr/local/bin)." >&2
  exit 1
fi
exec "$NPX" -y @samik081/mcp-pve

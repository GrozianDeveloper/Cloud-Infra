#!/usr/bin/env bash
# HUP `caddy` on TrueNAS via one-shot Dockge stack (docker.sock). No recreate.
# Usage: bash caddy/scripts/reload.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PUT="$ROOT/.cursor/skills/truenas-scale/scripts/tn-put.mjs"
DOCKGE="$ROOT/.cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs"
REMOTE="${CADDY_HUP_DIR:-/mnt/apps/dockge/caddy-hup}"

node "$PUT" "$ROOT/caddy/scripts/hup.compose.yaml" "$REMOTE/compose.yaml"
printf '# caddy-hup\n' > /tmp/caddy-hup.env
node "$PUT" /tmp/caddy-hup.env "$REMOTE/.env"
rm -f /tmp/caddy-hup.env

node "$DOCKGE" start caddy-hup
echo "caddy HUP requested"

#!/usr/bin/env bash
# Upload repo Caddy stack files to Dockge dir on TrueNAS.
# Usage: bash caddy/scripts/push.sh [--no-env]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PUT="$ROOT/.cursor/skills/truenas-scale/scripts/tn-put.mjs"
REMOTE="${CADDY_STACK_DIR:-/mnt/apps/dockge/caddy}"
SKIP_ENV=0
for a in "$@"; do
  [[ "$a" == "--no-env" ]] && SKIP_ENV=1
done

put() {
  node "$PUT" "$1" "$2"
}

put "$ROOT/caddy/Caddyfile" "$REMOTE/Caddyfile"
put "$ROOT/caddy/docker-compose.yml" "$REMOTE/compose.yaml"
put "$ROOT/caddy/crowdsec/acquis.yaml" "$REMOTE/crowdsec/acquis.yaml"
put "$ROOT/caddy/crowdsec/profiles.yaml" "$REMOTE/crowdsec/profiles.yaml"
put "$ROOT/caddy/crowdsec/whitelist.yaml" "$REMOTE/crowdsec/whitelist.yaml"
if [[ "$SKIP_ENV" -eq 0 ]]; then
  put "$ROOT/instance/caddy/.env" "$REMOTE/.env"
fi
echo "pushed → $REMOTE"

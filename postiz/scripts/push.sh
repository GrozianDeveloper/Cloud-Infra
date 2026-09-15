#!/usr/bin/env bash
# Upload Postiz stack to Dockge dir.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PUT="$ROOT/.cursor/skills/truenas-scale/scripts/tn-put.mjs"
REMOTE="${POSTIZ_STACK_DIR:-/mnt/apps/dockge/postiz}"

python3 "$ROOT/postiz/scripts/ensure-env.py"

node "$PUT" "$ROOT/postiz/docker-compose.yml" "$REMOTE/compose.yaml"
node "$PUT" "$ROOT/postiz/dynamicconfig/development-sql.yaml" "$REMOTE/dynamicconfig/development-sql.yaml"
node "$PUT" "$ROOT/instance/postiz/.env" "$REMOTE/.env"
echo "pushed → $REMOTE"

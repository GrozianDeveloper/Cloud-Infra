#!/bin/sh
# Gitea 1.27 has no /api/v1/admin/auths. Use CLI. Name must stay `authentik`.
set -eu
: "${GITEA_OIDC_CLIENT_ID:?}"
: "${GITEA_OIDC_CLIENT_SECRET:?}"
: "${GITEA_OIDC_DISCOVERY:?}"

cid=$(docker ps --format '{{.ID}} {{.Names}}' | awk 'BEGIN{IGNORECASE=1} /gitea/ && !/act-runner/ && !/runner/ {print $1; exit}')
if [ -z "$cid" ]; then
  echo "gitea container not found" >&2
  exit 1
fi

gitea() { docker exec -u git "$cid" gitea "$@"; }
# rootless image may run as default user
if ! docker exec "$cid" gitea --version >/dev/null 2>&1; then
  gitea() { docker exec "$cid" gitea "$@"; }
fi

list=$(gitea admin auth list 2>/dev/null || true)
echo "$list"
id=$(echo "$list" | awk 'BEGIN{IGNORECASE=1} $0 ~ /authentik/ {print $1; exit}')
if [ -n "$id" ]; then
  gitea admin auth update-oauth \
    --id "$id" \
    --name authentik \
    --provider openidConnect \
    --key "$GITEA_OIDC_CLIENT_ID" \
    --secret "$GITEA_OIDC_CLIENT_SECRET" \
    --auto-discover-url "$GITEA_OIDC_DISCOVERY" \
    --scopes "email profile"
  echo "updated gitea auth authentik id=$id"
  exit 0
fi
gitea admin auth add-oauth \
  --name authentik \
  --provider openidConnect \
  --key "$GITEA_OIDC_CLIENT_ID" \
  --secret "$GITEA_OIDC_CLIENT_SECRET" \
  --auto-discover-url "$GITEA_OIDC_DISCOVERY" \
  --scopes "email profile"
echo "created gitea auth authentik"

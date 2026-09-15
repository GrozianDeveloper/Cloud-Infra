#!/usr/bin/env bash
# Session TTLs only (existing user_oidc install).
set -euo pipefail
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
occ() { docker exec -u 33 "$NC" php occ "$@"; }
occ config:app:set user_oidc store_login_token --value=1
occ config:system:set session_lifetime --type=integer --value=3024000
occ config:system:set remember_login_cookie_lifetime --type=integer --value=3024000
occ config:app:get user_oidc store_login_token
occ config:system:get session_lifetime

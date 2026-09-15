#!/usr/bin/env bash
# user_oidc + session. Run on the TrueNAS host after AIO Start (nextcloud-aio-nextcloud exists).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
for f in \
  "$DIR/../../.env.oidc" \
  "$DIR/../../.env.nextcloud-oidc" \
  "$DIR/../.env.nextcloud-oidc" \
  "$DIR/.env.nextcloud-oidc" \
  "$(cd "$DIR/../../.." && pwd)/instance/master-nextcloud-aio/.env.oidc"; do
  if [[ -f "$f" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$f"
    set +a
    break
  fi
done
: "${NC_OIDC_CLIENT_ID:?}"
: "${NC_OIDC_CLIENT_SECRET:?}"
: "${NC_OIDC_DISCOVERY:?}"
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
occ() { docker exec -u 33 "$NC" php occ "$@"; }

occ app:install user_oidc || true
occ app:enable user_oidc
occ user_oidc:provider church \
  --clientid="$NC_OIDC_CLIENT_ID" \
  --clientsecret="$NC_OIDC_CLIENT_SECRET" \
  --discoveryuri="$NC_OIDC_DISCOVERY" \
  --scope="openid profile email entitlements nextcloud offline_access" \
  --unique-uid=0 \
  --mapping-uid="user_id" \
  --mapping-display-name="name" \
  --mapping-email="email" \
  --mapping-groups="entitlements" \
  --group-provisioning=1 \
  --mapping-phone=phone \
  --mapping-organisation=organisation \
  --mapping-role=role \
  --mapping-locale=locale \
  --mapping-language=language \
  --mapping-region=region \
  --mapping-locality=locality \
  --mapping-country=country \
  --mapping-birthdate=birthdate \
  --mapping-quota=quota \
  --resolve-nested-claims=1 \
  --send-id-token-hint=1 \
  --endsessionendpointuri="${NC_OIDC_ENDSESSION}" \
  --postlogouturi="${NC_OIDC_POST_LOGOUT}"
occ config:app:set --value=0 user_oidc allow_multiple_user_backends
occ config:app:set user_oidc store_login_token --value=1
occ config:system:set session_lifetime --type=integer --value=3024000
occ config:system:set remember_login_cookie_lifetime --type=integer --value=3024000
occ app:disable sociallogin || true
occ user_oidc:providers

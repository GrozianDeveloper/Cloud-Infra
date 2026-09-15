#!/usr/bin/env bash
# SMTP from instance/email/.env (or next to this script).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
for f in \
  "$(cd "$DIR/../.." && pwd)/instance/email/.env" \
  "$DIR/.env.email_server"; do
  if [[ -f "$f" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$f"
    set +a
    break
  fi
done
: "${SMTP_HOST:?}"
: "${SMTP_PORT:?}"
: "${SMTP_USERNAME:?}"
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
occ() { docker exec -u 33 "$NC" php occ "$@"; }

from_local="${SMTP_USERNAME%%@*}"
from_domain="${SMTP_USERNAME#*@}"
sec="$(echo "${SMTP_Security:-ssl}" | tr '[:upper:]' '[:lower:]')"
case "$sec" in
  ssl|tls|smtps) smtp_secure=ssl ;;
  starttls|star) smtp_secure=tls ;;
  none|"") smtp_secure="" ;;
  *) smtp_secure="$sec" ;;
esac

occ config:system:set mail_smtpmode --value=smtp
occ config:system:set mail_sendmailmode --value=smtp
occ config:system:set mail_from_address --value="$from_local"
occ config:system:set mail_domain --value="$from_domain"
occ config:system:set mail_smtphost --value="$SMTP_HOST"
occ config:system:set mail_smtpport --value="$SMTP_PORT"
occ config:system:set mail_smtpauth --type=boolean --value=true
occ config:system:set mail_smtpname --value="$SMTP_USERNAME"
if [[ -n "${SMTP_PASSWORD:-}" ]]; then
  occ config:system:set mail_smtppassword --value="$SMTP_PASSWORD"
fi
if [[ -n "$smtp_secure" ]]; then
  occ config:system:set mail_smtpsecure --value="$smtp_secure"
fi

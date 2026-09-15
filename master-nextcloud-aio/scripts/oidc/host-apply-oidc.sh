#!/bin/sh
# NAS one-shot: user_oidc then SMTP. Needs docker.sock + stack scripts/env.
set -eu
STACK="${STACK_DIR:-/stack}"
sh "$STACK/scripts/oidc/apply-oidc.sh"
sh "$STACK/scripts/apply-mail.sh"

#!/bin/sh
# Manual: wait for occ, apply ClamAV keys.
set -eu
OUT="${OUT_DIR:-/out}"
STACK="${STACK_DIR:-/stack}"
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
exec >"$OUT/apply-optimizations.log" 2>&1
echo START "$(date -u +%FT%TZ)"

i=0
while [ "$i" -lt 180 ]; do
  if docker exec -u 33 "$NC" php occ status >/dev/null 2>&1; then
    echo nextcloud_up
    break
  fi
  i=$((i + 1))
  sleep 4
done

sh "$STACK/scripts/optimizations/apply-optimizations.sh"
echo DONE "$(date -u +%FT%TZ)"

#!/bin/sh
# Full Clam scan for files >500MB after upload (upload stream already stopped).
set -eu
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
DATA="${NEXTCLOUD_DATADIR:-/mnt/church_tank/nc-data}"
MIN_BYTES="${NC_AV_UPLOAD_BYTES:-524288000}"
STALE_SEC="${NC_AV_STALE_SEC:-120}"

occ() { docker exec -u 33 "$NC" php occ "$@"; }

if ! docker exec -u 33 "$NC" php occ status >/dev/null 2>&1; then
  echo "nextcloud not ready"
  exit 0
fi

now=$(date +%s)
# Host paths; skip in-flight .part and uploads/
find "$DATA" \( -path '*/files/*' -o -path '*/__groupfolders/*' \) \
  -type f -size +"${MIN_BYTES}c" \
  ! -name '*.part' \
  ! -path '*/uploads/*' \
  ! -path '*/files_trashbin/*' \
  ! -path '*/files_versions/*' \
  ! -path '*/__groupfolders/versions/*' \
  ! -path '*/__groupfolders/trash/*' \
  -print |
while IFS= read -r host; do
  mtime=$(stat -c %Y "$host")
  if [ $((now - mtime)) -lt "$STALE_SEC" ]; then
    continue
  fi
  rel=${host#"$DATA"/}
  ncpath="/$rel"
  echo "scan $ncpath"
  occ files_antivirus:mark "$ncpath" unscanned >/dev/null 2>&1 || true
  occ files_antivirus:scan "$ncpath" || echo "scan failed $ncpath"
done

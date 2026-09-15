#!/bin/sh
# ClamAV: stop upload stream after 500MB. Lives in NC DB (survives reboot/update).
set -eu
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
LIMIT="${NC_AV_UPLOAD_BYTES:-524288000}"

occ() { docker exec -u 33 "$NC" php occ "$@"; }

echo START "$(date -u +%FT%TZ)"
occ config:app:set files_antivirus av_scan_first_bytes --value="$LIMIT"
occ config:app:set files_antivirus av_max_file_size --value=-1
occ config:app:set files_antivirus av_background_scan --value=true
occ config:app:set files_antivirus av_block_unscannable --value=false
occ config:app:get files_antivirus av_scan_first_bytes
occ config:app:get files_antivirus av_max_file_size
occ config:app:get files_antivirus av_background_scan
echo DONE "$(date -u +%FT%TZ)"

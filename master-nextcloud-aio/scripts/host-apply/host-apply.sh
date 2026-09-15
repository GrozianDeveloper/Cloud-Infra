#!/bin/sh
# One-shot on NAS: remount AIO at /mnt, FAST+ARCHIVE Local, Deck import.
set -eu
OUT="${OUT_DIR:-/out}"
STACK="${STACK_DIR:-/stack}"
HOST_OUT="${HOST_OUT:-/mnt/apps/dockge/nc-aio-apply}"
HOST_STACK="${HOST_STACK:-/mnt/apps/dockge/master-nextcloud-aio}"
exec >"$OUT/host-apply.log" 2>&1
cleanup() { rm -f "$OUT/deck-import-token.txt"; }
trap cleanup EXIT
echo START "$(date -u +%FT%TZ)"

mount_env=$(docker inspect nextcloud-aio-mastercontainer --format '{{range .Config.Env}}{{println .}}{{end}}' 2>/dev/null | grep '^NEXTCLOUD_MOUNT=' || true)
echo "current $mount_env"
if [ "$mount_env" != "NEXTCLOUD_MOUNT=/mnt" ]; then
  sed 's/^apps:/services:/' "$STACK/compose.yaml" > /tmp/aio-compose.yaml
  docker compose -p master-nextcloud-aio -f /tmp/aio-compose.yaml --env-file "$STACK/.env" up -d --force-recreate
  echo mastercontainer_recreated
  i=0
  while [ "$i" -lt 90 ]; do
    docker inspect -f '{{.State.Running}}' nextcloud-aio-mastercontainer 2>/dev/null | grep -q true && break
    i=$((i + 1))
    sleep 2
  done
fi

nc_bind=$(docker inspect nextcloud-aio-nextcloud --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' 2>/dev/null || true)
echo "$nc_bind"
if ! echo "$nc_bind" | grep -q '^/mnt -> /mnt'; then
  if docker inspect nextcloud-aio-nextcloud >/dev/null 2>&1; then
    docker rm -f nextcloud-aio-nextcloud
    echo nextcloud_removed
  fi
  echo starting_aio_containers
  docker exec -e START_CONTAINERS=1 nextcloud-aio-mastercontainer /daily-backup.sh \
    || echo start_containers_failed
  echo start_containers_done
fi

i=0
while [ "$i" -lt 180 ]; do
  if docker exec -u 33 nextcloud-aio-nextcloud php occ status >/dev/null 2>&1; then
    echo nextcloud_up
    break
  fi
  i=$((i + 1))
  sleep 4
done

echo "--- mounts ---"
docker inspect nextcloud-aio-nextcloud --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' || true

sh "$STACK/scripts/apply-external-storage.sh"

i=0
while [ "$i" -lt 60 ]; do
  docker inspect -f '{{.State.Running}}' nextcloud-aio-apache 2>/dev/null | grep -q true && break
  i=$((i + 1))
  sleep 2
done

docker cp "$STACK/scripts/create-app-token.php" nextcloud-aio-nextcloud:/tmp/create-app-token.php
docker exec nextcloud-aio-nextcloud chmod 644 /tmp/create-app-token.php
docker exec -u 33 -w /var/www/html nextcloud-aio-nextcloud php /tmp/create-app-token.php admin deck-import >"$OUT/deck-import-token.txt"
docker exec nextcloud-aio-nextcloud rm -f /tmp/create-app-token.php
echo token_written

if [ -f "$OUT/deck-export.tgz" ]; then
  mkdir -p "$OUT/deck-src"
  tar -xzf "$OUT/deck-export.tgz" -C "$OUT/deck-src"
  echo deck_extracted
fi
cp "$STACK/scripts/import-deck.py" "$OUT/import-deck.py"

docker run --rm --network nextcloud-aio \
  -e PYTHONUNBUFFERED=1 \
  -e NC_BASE=http://nextcloud-aio-apache:11000 \
  -e NC_HOST=cloud.internal-church.gleeze.com \
  -e NC_DECK_USER=admin \
  -e NC_DECK_TOKEN_FILE=/secret/token \
  -e DECK_SRC=/data/nextcloud-deck \
  -v "$HOST_OUT/deck-import-token.txt:/secret/token:ro" \
  -v "$HOST_OUT/deck-src:/data:ro" \
  -v "$HOST_OUT/import-deck.py:/import.py:ro" \
  python:3.12-alpine python -u /import.py
echo deck_import_done

rm -f "$OUT/deck-import-token.txt"
echo DONE "$(date -u +%FT%TZ)"

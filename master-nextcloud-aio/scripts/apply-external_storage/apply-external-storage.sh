#!/bin/sh
# Local files_external create/update. Never delete.
set -eu
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
OUT="${OUT_DIR:-}"
if [ -n "$OUT" ]; then
  mkdir -p "$OUT"
  exec >"$OUT/apply-external-storage.log" 2>&1
fi
echo START "$(date -u +%FT%TZ)"

occ() { docker exec -u 33 -w /var/www/html "$NC" php occ "$@"; }

i=0
while [ "$i" -lt 90 ]; do
  occ status >/dev/null 2>&1 && break
  i=$((i + 1))
  sleep 2
done
occ app:enable files_external >/dev/null 2>&1 || true
occ group:add church-media >/dev/null 2>&1 || true

find_id() {
  name="$1"
  docker exec -u 33 -w /var/www/html "$NC" php -r '
    $name = trim($argv[1], "/");
    $raw = shell_exec("php occ files_external:list --output=json 2>/dev/null");
    $data = json_decode($raw ?: "{}", true);
    if (!is_array($data)) exit(0);
    $items = array_is_list($data) ? $data : array_values($data);
    foreach ($items as $it) {
      if (!is_array($it)) continue;
      $mp = trim((string)($it["mount_point"] ?? $it["mountPoint"] ?? ""), "/");
      $id = $it["mount_id"] ?? $it["id"] ?? "";
      if ($mp === $name && $id !== "") { echo $id; exit(0); }
    }
  ' -- "$name"
}

ensure() {
  name="$1"
  datadir="$2"
  group="${3:-}"
  id="$(find_id "$name" || true)"
  if [ -z "$id" ]; then
    id="$(occ files_external:create "$name" local null::null -c "datadir=$datadir" --output=json)"
    id="$(printf '%s' "$id" | tr -d '[:space:]"')"
    echo created "$name" "$id"
  else
    occ files_external:config "$id" datadir "$datadir" >/dev/null 2>&1 || true
    echo update "$name" "$id"
  fi
  if [ -n "$group" ] && [ -n "$id" ]; then
    occ files_external:applicable --add-group="$group" "$id" || true
    echo applicable "$name" "$group"
  fi
}

# FAST / ARCHIVE: all users. Map mounts: group only.
ensure FAST /mnt/apps
ensure ARCHIVE /mnt/church_tank
ensure "Медиа в Работе" /mnt/fast/media_work church-media

echo "--- ls ---"
docker exec -u 33 "$NC" ls -la /mnt/fast/media_work || echo "ls_failed"
echo "--- occ list ---"
occ files_external:list

echo DONE "$(date -u +%FT%TZ)"

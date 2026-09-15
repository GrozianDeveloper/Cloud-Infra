#!/bin/sh
# occ: NC groups + Team Folders. Collectives/Talk/Deck: apply-groups-acl.py → permissions map.
set -eu
NC="${NC_CONTAINER:-nextcloud-aio-nextcloud}"
echo "docker ps"
docker ps --format '{{.Names}}'
occ() { docker exec -u 33 "$NC" php occ "$@"; }
echo "occ status"
occ status || echo "occ status failed"

GROUPS="
everybody presentation announcements desktop_workspace full_text_search
giphy youtube mail ai talk sharing postiz fileflows handbrake
jdownloader nocodb home cctv freeshow netbird n8n gitea
teaching_instruments teaching_instruments-library teaching_instruments-library-read
operator -recipes home church-info teacher parishioner
guest guest-teacher sunday church church-teacher church-lead presbyter
tech-common tech tech-lead media music music-lead youth youth-lead
volleyball blesstime blesstime-media blesstime-teacher blesstime-lead
real_estate real_estate-geo real_estate-vpn-geo real_estate-lawyer
"

for g in $GROUPS; do
  echo "group $g"
  occ group:add "$g" >/dev/null 2>&1 || true
done
echo "groups ok"

list=$(occ groupfolders:list --output=json 2>/dev/null || occ groupfolders:list 2>/dev/null || true)
create_folder() {
  name="$1"
  occ groupfolders:create "$name" >/dev/null 2>&1 || true
}

create_folder "Bless Time"
create_folder "Презентация"
list=$(occ groupfolders:list --output=json 2>/dev/null || occ groupfolders:list 2>/dev/null || true)
echo "$list"

fid_of() {
  echo "$list" | sed 's/},{/}\n{/g' | grep -F "$1" | sed 's/.*"id":\([0-9][0-9]*\).*/\1/' | head -n 1
}

bt=$(fid_of "Bless Time")
pr=$(fid_of "Презентация")
[ -z "$bt" ] && bt=8
[ -z "$pr" ] && pr=9
echo "fid Bless Time=$bt Презентация=$pr"
if [ -n "$bt" ]; then
  occ groupfolders:group "$bt" blesstime || true
  occ groupfolders:group "$bt" blesstime-lead || true
  occ groupfolders:permissions "$bt" --group blesstime-lead -1 >/dev/null 2>&1 || \
    occ groupfolders:group "$bt" blesstime-lead write share delete || true
fi
if [ -n "$pr" ]; then
  occ groupfolders:group "$pr" presentation || true
fi
echo "folders ok"

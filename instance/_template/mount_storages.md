| Piece | State |
|---|---|
| Dataset `fast/media_work` | `quota=300G`, `recordsize=1M` (`convert/`, `converted/`) |
| FileFlows `/media/work` | `/mnt/fast/media_work` |
| HandBrake `/video` | `/mnt/fast/media_work` |
| POSIX ACL | owner **568** (`apps`), extra **uid 33** (NC), inherit. No `chown -R 33` |
| NC Local | **Медиа в Работе** → `/mnt/fast/media_work`, group `church-media` |
| `NEXTCLOUD_MOUNT` | Nextcloud mounts `/mnt`; so no remount |

# `fast/media_work`

| App | Path |
|---|---|
| FileFlows | `/media/work` |
| HandBrake | `/video` |
| Nextcloud Local | **Медиа в Работе** → `/mnt/fast/media_work`, group `church-media` |

In-progress media on pool `fast` (NVMe, no redundancy). Quota **300G**. Not in `nc-data`.

ACL: uid **568** + **33**. Disk loss loses work files only.

## Apply

```bash
python3 instance/maps/permissions/apply-permissions-map.py church:teams
# then occ (Dockge one-shot nc-aio-extstorage, or on NAS): (update script - when mount storage changed)
sh master-nextcloud-aio/scripts/apply-external_storage/apply-external-storage.sh
```

Map: `instance/maps/permissions/map-church-teams.yaml` → `external_storage`. occ is the Local mount path (`files_external` HTTP needs password confirm). Never delete. Do not mount whole `fast/`.

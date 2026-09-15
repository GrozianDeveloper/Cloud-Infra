# Pools and datasets

Fill [instance/truenas/Readme.md](../../instance/truenas/Readme.md) pool table. Disks: [instance/hardware.md](../../instance/hardware.md).

## Roles

| Pool | Disk | For |
|---|---|---|
| `apps` | SSD | App data, Docker (`apps/ix-apps`) |
| archive HDD | HDD | Nextcloud/user files |
| optional `fast` | NVMe | In-progress **media files** only |

Stripe vs mirror = user. No redundancy on `fast` = lost work files only.

## Datasets

```bash
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh SPEC [SPEC...]
# SPEC: dataset  or  dataset:uid:gid:mode
```

HostPath per `{app}/README.md`. FileFlows/HandBrake: `{fastest}/media_work` (`recordsize=1M`, ACL uid **568** + **33**). Not a database. Postiz Postgres stays on `apps`.

HTTP/3 buffers:

```bash
python3 truenas/scripts/apply-tunables.py \
  net.core.rmem_max=2500000 net.core.rmem_default=2500000
```

Media mounts: [instance/mount_storages.md](../../instance/mount_storages.md).

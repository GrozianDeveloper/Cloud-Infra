# This infra instance

## Installed on Proxmox VE

| VM Name | VID |
|---|---|
| TrueNAS | 100 |
| home | 120 |

## MoC

| file | Contents |
|---|---|
| [`apps.md`](apps.md) | installed apps → `instance/{app}/Readme.md` |
| `maps/index.md` | sources of truth for app data & permissions |
| `{app}/` | this NAS docs + secrets (`.env`, `.env.oidc`) |
| `mount_storages.md` | mounted storages, TrueNAS shared datasets |
| [`authentik/Readme.md`](authentik/Readme.md) | apps, providers |
| [`truenas/Readme.md`](truenas/Readme.md) | TrueNAS instance info |
| `hardware.md` | instance hardware |

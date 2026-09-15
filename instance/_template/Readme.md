# New instance files

Copy into `instance/` **only** for a new NAS. Never overwrite a live `instance/` that already has `TRUENAS_API_KEY`.

This tree is a snapshot of **this infra’s apps + maps** (HostPath, ports, Authentik slugs, group YAML). Fill hardware + `.env`. Then apply maps.

## Copy

From repo root. Do **not** copy `.env` / `.env.oidc`. Do **not** overwrite `instance/maps/**/apply*.py` or `map_lib.py` (scripts stay in `instance/maps/`).

| From `_template/` | To |
|---|---|
| `Readme-instance.md` | `instance/Readme.md` |
| `hardware.md` | `instance/hardware.md` (fill disks/MAC/GPU) |
| `apps.md` | `instance/apps.md` |
| `mount_storages.md` | `instance/mount_storages.md` |
| `{app}/Readme.md` | `instance/{app}/Readme.md` |
| `maps/**/*.yaml` + `maps/**/*.md` | `instance/maps/` |
| `first-install-state.yaml` | `instance/first-install-state.yaml` |

Then create empty `instance/{app}/.env` (keys listed in each Readme). User pastes values. Never print secrets.

## After copy

1. Edit `hardware.md`, pool names in `truenas/Readme.md` if disks differ.
2. Edit `netbird/map.yaml` `lan_ip` / FQDNs to this LAN (YAML is the old snapshot).
3. `{APP}_DOMAIN` / `{APP}_UPSTREAM` in `instance/caddy/.env` for chosen apps.
4. Maps: keep YAML to recreate this org tree, **or** rename groups before apply (step 10). Scripts never delete.
5. GPU PCI in FileFlows/HandBrake Readmes → match `hardware.md`.

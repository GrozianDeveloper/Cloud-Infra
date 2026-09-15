# TrueNAS SCALE

Goal: NAS + Apps host. Operate via API (never ad-hoc from memory).

## Docs

- [Instance](../instance/truenas/Readme.md)
- Skill: `.cursor/skills/truenas-scale/SKILL.md`

## Installation

- Secrets: [instance/truenas/.env](../instance/truenas/.env)
- UI on **880 / 8443** so Caddy owns **80 / 443**
- HostPath, not IxVolumes

## Scripts

| Path | What |
|---|---|
| `scripts/apply-tunables.py` | Upsert SYSCTL `VAR=VALUE` |
| `scripts/set-nameservers.py` | `NS1 [NS2 [NS3]]` — ns1 = AdGuard |
| `scripts/apps-status.py` | Catalog states; named apps must be RUNNING |

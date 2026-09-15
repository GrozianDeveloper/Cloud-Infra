# Postiz workspaces

## Goal

Postiz organizations + customer groups (channel folders). Authentik who-can-login stays in [`auth_apps`](../auth_apps/Readme.md) (`postiz`). Who-joins-which-org: later n8n; not this map.

## Files

[`map.yaml`](map.yaml). Secrets: keys in YAML, values in `instance/postiz/.env`.

## How to read

| Field | What |
|-------|------|
| `orgs[].name` | Postiz organization (workspace). Scripts match by this. Do not rename in UI. |
| `orgs[].slug` | Stable id for env keys (`church` / `blesstime`) |
| `from_authentik` | Authentik group that *should* live in this org (docs + future sync) |
| `groups[].name` | Postiz customer (channel group) |

## Apply

Never delete. Needs running stack `postiz` (SQL inside `postiz-postgres`).

```bash
python3 instance/maps/map-postiz/apply.py
python3 instance/maps/map-postiz/apply.py church
```

Creates missing orgs/groups. Sets `apiKey` only when empty. Writes missing keys to `instance/postiz/.env`; never overwrites existing.

## Effects

Two workspaces: **Бахчисарайская Церковь**, **Bless Time**. Each has customer **Все Аккаунты**. First OIDC login may still create a leftover personal org (delete only via deletion workflow).

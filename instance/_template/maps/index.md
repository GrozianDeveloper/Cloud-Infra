# Maps (after copy → `instance/maps/`)

YAML here = this infra’s groups / apps / NetBird / Postiz. Apply with scripts that **stay** in `instance/maps/` (not in `_template`).

• Rule: [`.cursor/rules/maps.mdc`](../../../.cursor/rules/maps.mdc)

| Doc | Owns | Apply |
|-----|------|-------|
| [permissions](permissions/Readme.md) | Authentik groups, entitlements, NC surfaces | `python3 instance/maps/permissions/apply.py` then `apply-permissions-map.py` |
| [auth_apps](auth_apps/Readme.md) | Authentik Application + Provider | `python3 instance/maps/auth_apps/apply.py` |
| [netbird](netbird/Readme.md) | NetBird groups, networks, resources, policies | `python3 instance/maps/netbird/apply.py` |
| [map-postiz](map-postiz/Readme.md) | Postiz orgs + customer groups | `python3 instance/maps/map-postiz/apply.py` |

No args = whole file. Never delete.

```bash
python3 instance/maps/permissions/apply.py
python3 instance/maps/permissions/apply-permissions-map.py
python3 instance/maps/auth_apps/apply.py
python3 instance/maps/netbird/apply.py
python3 instance/maps/map-postiz/apply.py
```

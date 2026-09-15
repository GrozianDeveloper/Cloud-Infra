# Verify

After each wave: fail closed. Then handoff.

## Catalog

```bash
python3 truenas/scripts/apps-status.py
python3 truenas/scripts/apps-status.py adguardhome dockge authentik
```

## Edge

```bash
python3 caddy/scripts/check.py
```

LAN: `dig +short {APP}_DOMAIN` = `TRUENAS_LAN`. WAN: [01 verify](01-router-portforward.md#verify) from a hotspot.

## SSO

- Authentik library = bound apps only ([02.4](02-authentik-apps-auth/02.4-groups-map.md)).
- Nextcloud login + groups; FA 403 for outsiders.
- WP / Gitea: login with Authentik.

Leftover non-blocking work → `todo/{app}/`. Mark `instance/first-install-state.yaml` `step: done`.

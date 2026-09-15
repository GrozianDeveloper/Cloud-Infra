# AdGuard Home

Goal: Rewrite local infra domains to this host
Eg `*.infra-domain.org` → `TRUENAS_LAN`

## Docs

- [Instance](../instance/adguardhome/Readme.md)

## Installation

- TrueNAS App: `adguardhome`
- WebUI + DNS. Host Network=false, DHCP=false, HTTPS Probe=false
- `TRUENAS_LAN` in `instance/truenas/.env`
- Wildcards from domains in `instance/caddy/.env`

## Scripts

```bash
python3 adguardhome/scripts/apply-rewrites.py
```

Needs `instance/adguardhome/.env`: `ADGUARD_URL`, `ADGUARD_USER`, `ADGUARD_PASSWORD`. Answer = `TRUENAS_LAN`. Never deletes.

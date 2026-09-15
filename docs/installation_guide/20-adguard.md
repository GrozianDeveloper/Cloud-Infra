# AdGuard Home

Catalog app. Start **before** any other `app.start` (TrueNAS `nameserver1` will point here).

## Install

- [adguardhome/README.md](../../adguardhome/README.md)
- HostPath `apps/adguardhome` (+ work dir). WebUI + DNS. Host Network=false, DHCP=false.
- LAN IP: `TRUENAS_LAN` in `instance/truenas/.env`.

## Rewrites

Wildcards + extra hosts from `{APP}_DOMAIN` in `instance/caddy/.env` → `TRUENAS_LAN`.

```bash
python3 adguardhome/scripts/apply-rewrites.py
```

Hostname outside the main wildcard: own rewrite **and** public A/AAAA ([networking.md](../networking.md)).

Then [TrueNAS nameservers](12-truenas.md).

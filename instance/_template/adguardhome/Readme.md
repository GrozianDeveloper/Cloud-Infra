# AdGuard Home

- WebUI `30004`, DNS `53`
- Config=`apps/adguardhome`, WorkDir=`apps/adguardhome/work`
- `TRUENAS_LAN` from `instance/truenas/.env`
- Wildcards from domains in `instance/caddy/.env`
- Rewrites: `python3 adguardhome/scripts/apply-rewrites.py` (`.env` keys `ADGUARD_URL`, `ADGUARD_USER`, `ADGUARD_PASSWORD`)

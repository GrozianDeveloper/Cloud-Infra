# NetBird Server

## Authentik

- slug = `netbird`
- bind group = `netbird`
- Keep `embedded_idp=true`. Extra Generic OIDC in NetBird UI. Disable local login.
- Redirects: `/nb-auth`, `/nb-silent-auth`
- Creds: `instance/netbird-server/.env.oidc`

## This NAS

- WebUI `30415`, Management `30416`, STUN `30417`
- Data=`apps/netbird_s/data`, Config=`apps/netbird_s/config`
- PAT for map apply: `NETBIRD_API_TOKEN` in `instance/netbird-server/.env` (create if missing)
- Map: [`../maps/netbird`](../maps/netbird/Readme.md)

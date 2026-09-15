# Nextcloud MCP

- Dockge stack `nextcloud-mcp`. LAN `:31800` only — not Caddy.
- Creds: `instance/nextcloud-mcp/.env` (`NEXTCLOUD_MCP_LOGIN` / `NEXTCLOUD_MCP_PASSWORD`)
- HostPath `apps/nextcloud-mcp` → `/app/data` (uid 1000)
- `NEXTCLOUD_HOST` = `https://{NEXTCLOUD_DOMAIN}` from `instance/caddy/.env`

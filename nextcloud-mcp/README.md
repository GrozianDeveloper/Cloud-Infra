# Nextcloud MCP

Goal: MCP tools for this Nextcloud, used from Cursor

## Docs

- [Deploy](docs/deploy.md)
- [MCP](MCP.md)
- [Instance](../instance/nextcloud-mcp/Readme.md)
- Upstream: [cbcoutinho/nextcloud-mcp-server](https://github.com/cbcoutinho/nextcloud-mcp-server)

## Installation

- Dockge stack `nextcloud-mcp`
- Mode: single-user BasicAuth (`MCP_DEPLOYMENT_MODE=single_user_basic`). LAN only — **not** Caddy.
- Secrets: [instance/nextcloud-mcp/.env](../instance/nextcloud-mcp/.env)
- Nextcloud URL: `NEXTCLOUD_HOST` = `https://{NEXTCLOUD_DOMAIN}` from `instance/caddy/.env`

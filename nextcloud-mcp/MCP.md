# Nextcloud MCP — instance

Upstream: https://github.com/cbcoutinho/nextcloud-mcp-server

URL: `http://{TrueNAS LAN}:{MCP_PORT}/mcp`  
Health: `/health/live`, `/health/ready`

## Connect

- Config: `.cursor/mcp.json` server `nextcloud`. Type `streamable-http` (not `http`).
- Do not put this MCP in `~/.cursor/mcp.json`.
- After stack start: reload MCP in Cursor.
- Creds stay in the container env (Nextcloud app password). Client does not send them.

## Do not

Expose `:31800` on the router or via Caddy. Single-user mode has no MCP client auth.

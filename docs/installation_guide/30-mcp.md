# MCP

Only after that app is up. Tokens stay in `instance/{app}/.env`. Never in `.cursor/mcp.json`.

AI edits `.cursor/mcp.json` (no render script). Skip servers for skipped apps. Then reload Cursor MCP.

| App | Config |
|---|---|
| Gitea | `bash .cursor/mcp/install-gitea-mcp.sh` · stdio `.cursor/mcp/gitea.sh` |
| n8n | `streamable-http` `https://{N8N_DOMAIN}/mcp-server/http` ([n8n/MCP.md](../../n8n/MCP.md)) |
| Nextcloud | `streamable-http` `http://{TRUENAS_LAN}:31800/mcp` after nextcloud-mcp ([nextcloud-mcp/MCP.md](../../nextcloud-mcp/MCP.md)) |
| PVE | `.cursor/mcp/pve.sh` if Proxmox ([proxmox/MCP.md](../../proxmox/MCP.md)) |
| HA | `.cursor/mcp/home.sh` (or extra VM wrapper) |
| Postiz | `.cursor/mcp/postiz.sh` |

Project `.cursor/mcp.json` only — not `~/.cursor/mcp.json`.

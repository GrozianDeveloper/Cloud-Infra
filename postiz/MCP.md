# Postiz MCP — instance

Upstream: https://docs.postiz.com/mcp/setup

Postiz MCP is **per organization API key**. Stock server cannot see both workspaces in one connection.

This Cursor project uses **one** MCP (`postiz`) = org **Бахчисарайская Церковь** (`POSTIZ_CHURCH_API_KEY`). Bless Time: Postiz UI org switcher, or scripts with `POSTIZ_BLESSTIME_API_KEY`.

## Connect

- Config: `.cursor/mcp.json` server `postiz` → `.cursor/mcp/postiz.sh` (`mcp-remote` + Bearer).
- URL: `https://{POSTIZ_DOMAIN}/mcp` (key not in git).
- Keys: `instance/postiz/.env`. After first map apply: reload MCP in Cursor.

## Verify

Ask: list connected social media accounts → tool `integrationList`.

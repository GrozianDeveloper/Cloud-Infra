# Proxmox VE MCP

Upstream: https://github.com/Samik081/mcp-pve (`npx @samik081/mcp-pve`)

## Connect

- Config: `.cursor/mcp.json` server `pve` (stdio). Wrapper `.cursor/mcp/pve.sh` → `npx @samik081/mcp-pve`.
- PATH: Cursor MCP spawn has no Homebrew. Wrapper sources `.cursor/mcp/path.sh` (`/opt/homebrew/bin`, `/usr/local/bin`). Symptom if missing: `exec: npx: not found`.
- Auth: `instance/proxmox/.env` (`PVE_URL`, `PVE_TOKEN_ID`, `PVE_TOKEN_SECRET`). Self-signed: `PVE_VERIFY_SSL=false`.
- Token: PVE UI → Datacenter → Permissions → API Tokens. **Privilege Separation off** (inherit root). If privsep stays on, add ACL path `/` role Administrator for `root@pam!mcp`. Empty ACL → `permissions: {}` → VM/PCI calls fail.
- After first add: reload MCP in Cursor.

## Use when

Nodes, QEMU VMs (list/status/config, power, snapshots), storage, cluster, tasks, backups, network.

## Cannot

Host kernel/vfio, IOMMU groups, `lspci`, PCI `hostpci*` (tool `pve_update_qemu_config` has no hostpci field). GPU passthrough host bind = SSH. VM PCI attach = `qm set` / UI.

## Do not

Put the token in `mcp.json` or docs.

# docs/

Shareable. Same procedures for every instance.

- Values (`{APP}_DOMAIN`, `{APP}_UPSTREAM`): `instance/caddy/.env`. Per-app secrets: `instance/{app}/.env` / `.env.oidc`. SMTP: `instance/email/.env`. TrueNAS API: `instance/truenas/.env`.
- This instance (groups, users, leftover apply, extra VMs): `instance/`
- New NAS stubs: `instance/_template/`
- Per-app install notes: `{app}/README.md`

# Installation guide

Flow: `.cursor/skills/first-install/SKILL.md`

| Page | What |
|---|---|
| [00](installation_guide/00-clone-skills.md) | Clone, skills, abort-if-live |
| [01](installation_guide/01-router-portforward.md) | Router forwards |
| [10](installation_guide/10-hardware.md) | Hardware intake |
| [11](installation_guide/11-proxmox.md) | Optional PVE |
| [12](installation_guide/12-truenas.md) | SCALE + our ports |
| [13](installation_guide/13-pools-datasets.md) | Pools, datasets, tunables |
| [14](installation_guide/14-email.md) | SMTP keys |
| [15](installation_guide/15-app-picker.md) | Presets |
| [20](installation_guide/20-adguard.md) | AdGuard + rewrites |
| [21](installation_guide/21-dockge.md) | Dockge |
| [22](installation_guide/22-caddy.md) | Caddy |
| [23](installation_guide/23-authentik.md) | Authentik |
| [02.1–02.4](installation_guide/02-authentik-apps-auth/02.1-authentik-netbird-oidc.md) | SSO / maps |
| [30](installation_guide/30-mcp.md) | MCP |
| [90](installation_guide/90-verify.md) | Verify |

# Instance Maps

Source of truth for applications data, permissions (groups, Authentik apps, NetBird, Nextcloud...) Edit YAML. Scripts only create/update - **Never delete.**

• [Rule](.cursor/rules/maps.mdc)
• [Maps index](instance/maps/index.md)
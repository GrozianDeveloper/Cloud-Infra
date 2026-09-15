# App picker

Write [instance/apps.md](../../instance/apps.md) from [instance/_template/apps.md](../../instance/_template/apps.md). Delete rows for skipped apps. Domains: `instance/caddy/.env`.

## Presets

| Preset | Apps |
|---|---|
| `church-core` | AdGuard, Dockge, Caddy, Authentik, Nextcloud AIO + MCP, n8n, Gitea + runner |
| `church+media` | core + FileFlows, HandBrake, `media_work` |
| `church+family` | core + extra HA OS VM, Tandoor, HomeBox, Gramps |
| `full` | all apps in [Readme mermaid](../../Readme.md) |

Any public preset: CrowdSec, router TCP 80 + TCP/UDP 443 ([01](01-router-portforward.md)).

Extras (yes/no): Netbird, WordPress, NocoDB, Postiz, FreeShow stub, second HA (`home`).

Install how-to stays in `{app}/README.md` + `{app}/docs/deploy.md`.

---
name: first-install
description: >
  First-time install of this infra on new hardware. Follow when the user pastes
  the Readme first-install prompt or says new instance / new NAS.
---

# First-install

Follow that flow: one step at a time — ask (use suggested answers), write instance/ docs, wait for my confirm, then implement that step. Resume from instance/first-install-state.yaml if it exists. Never print secrets. Do not treat the current live instance/ as a blank slate unless I say this is a new instance.

Start at step 0.

**Output:** this hardware runs the chosen apps, SSO, DNS, edge, maps, MCP, skills — as the user described.

**This file** = flow + rules. Per-app how-to: `docs/installation_guide/` and `{app}/docs/`.

**Not for this already-running NAS** unless the user says “new instance”. Existing `instance/` is live.

---

## How to run

1. User pastes the prompt from `Readme.md`.
2. Agent reads **this file**, then only the guide pages for the **current step**.
3. One step at a time: **ask → write `instance/` → user confirms → implement that step**.
4. Checkpoint: `instance/first-install-state.yaml` — **AI writes this YAML** (no script). Resume from it; do not re-ask done steps.
5. After each implement: `python3 truenas/scripts/apps-status.py` and/or `python3 caddy/scripts/check.py`, then next step.

Do **not** install after every single question. Do **not** skip confirm. Do **not** print secrets.

---

## Rules

| Rule | Why |
|---|---|
| HostPath, never IxVolumes | Survives app reinstall |
| Values only in `instance/{app}/.env` / `.env.oidc`, `instance/caddy/.env`, `instance/email/.env`, `instance/truenas/.env` | Docs stay shareable |
| Docs: `instance/{app}/Readme.md` = this hardware; `{app}/README.md` + `{app}/docs/` = reusable | MoC |
| Scripts only (TrueNAS `tn-*` / `catalog-install.py`, Authentik skill `scripts/`, map `apply.py`). Never ad-hoc curl | Repeatable |
| Maps never delete | [maps](docs/README.md#instance-maps) |
| Suggested answer on every question; say the **effect** | User knows the result |
| Official vendor install pages for OS; this repo for *our* choices | Less AI invention |
| Skills from `skills-lock.json` **before** app work (`npx skills experimental_install`) | Agent has tools |
| MCP only after that app is up; wrappers read `instance/` | No tokens in `mcp.json` |
| Parallel only inside a **wave** (table below). Never parallel across waves | AdGuard / Caddy / Authentik are gates |
| Abort if `instance/truenas/.env` has `TRUENAS_API_KEY` unless user said **new instance** | Protect this NAS |
| `apps` SSD = app DBs. Fastest pool = **media files in progress**, not Postiz/Postgres | Postiz DB ≠ media_work |

---

## Efficiency (less thinking)

- **Template** — `instance/_template/` is the full app+maps snapshot. Copy first; do not rewrite maps from memory.
- **Presets** (one pick, then only deltas): `church-core` · `church+media` · `church+family` · `full`. See [app picker](#14-app-picker--presets).
- **State file** — next chat continues without re-reading the whole install.
- **Read list per step** — only linked guide + `{app}/README.md` + `instance/{app}/` for apps in this step. Do not load all skills at once; load TrueNAS / Dockge / Authentik when that wave starts.
- **Catalog values JSON** from `instance/` + `{app}/docs/deploy.md` — do not invent chart keys.
- **Verify** after each wave (`apps-status.py`, `caddy/scripts/check.py`) — fail the step, do not continue.
- **Docs-only mode** — fill `instance/` and stop (no API). Useful on a laptop before the NAS exists.

---

## Waves (install order)

Serial gates, then parallel **inside** a wave (TrueNAS pulls still share disk — cap 2–3 catalog jobs).

| Wave | What | Parallel? |
|---|---|---|
| 0 | Clone, skills, state file | no |
| 1 | Intake → `instance/` docs (no hardware yet) | no |
| 2 | Proxmox (optional) → TrueNAS up → API key | no |
| 3 | Pools, datasets, tunables, GPU passthrough | no |
| 4 | Router + public DNS | can overlap 3 if IPs known |
| 5 | AdGuard → TrueNAS nameserver1 → Dockge → Caddy | **no** (AdGuard before any other `app.start`) |
| 6 | Authentik | no |
| 7 | Nextcloud AIO (slow) ‖ n8n ‖ Gitea | AIO vs catalog: **yes** (2–3) |
| 8 | Chosen extra apps (WP, NocoDB, Netbird, FileFlows, HandBrake, Postiz, Tandoor, HomeBox, Gramps, …) | **yes**, 2–3 |
| 9 | HA OS VM(s) if wanted | after PVE |
| 10 | Maps + OIDC/FA + host-apply | mostly serial (Authentik → apps → NC ACL) |
| 11 | MCP for installed apps + Cursor reload | yes (binaries) |
| 12 | Verify + leftover `todo/` | no |

---

# Steps

Each **Ask** block = questions for that step (suggested default in *italics*). Then write `instance/`, confirm, implement.

---

## 0. Repo + skills

Guide: [00-clone-skills.md](docs/installation_guide/00-clone-skills.md)

**Ask**

- New hardware / new church instance, or continue this repo’s live `instance/`? → *new instance = copy `instance/_template/` (apps + maps YAML); live = abort*
- Agent machine has Node 18+, Python 3, `npx`? → *yes*

**Do**

1. If `instance/truenas/.env` already has `TRUENAS_API_KEY` and the user did **not** say new instance → **abort**.
2. New instance: copy [instance/_template/](instance/_template/Readme.md) into `instance/` — all `{app}/Readme.md` + `maps/**/*.yaml`. Do **not** overwrite `.env` or `instance/maps/**/apply*.py` / `map_lib.py`.
3. `npx skills experimental_install` from `skills-lock.json` (no `-g`). Custom skills in `.cursor/skills/` — do not reinstall.
4. AI writes `instance/first-install-state.yaml` (shape: `_template/first-install-state.yaml`). No script.

---

## 1. Prepare `instance/` (intake)

Start from `_template` (already copied in step 0). Fill hardware + `.env` keys. Stop so the user can read `instance/`.

### 1.1 Hardware

Guide: [10-hardware.md](docs/installation_guide/10-hardware.md) · [instance/_template/hardware.md](instance/_template/hardware.md)

**Ask:** CPU, RAM, NICs, disks (size/type/serial), GPU (passthrough?). *Fill `instance/hardware.md`.*

**Effect:** later pool layout and GPU to FileFlows/HandBrake.

### 1.2 Hypervisor (Proxmox)

Guide: [11-proxmox.md](docs/installation_guide/11-proxmox.md) · [proxmox/README.md](proxmox/README.md)

**Ask:** Proxmox already installed?

| Answer | Then |
|---|---|
| Yes | Collect `PVE_URL`, token → `instance/proxmox/.env`. Note VMID plan. Enable MCP `pve` after creds. |
| No | Install **only if** user wants extra VMs (HA OS, more guests) **or** later several physical nodes. Else *bare-metal TrueNAS* — fewer layers, GPU simpler. |

If installing PVE: point to official Proxmox ISO; this repo only: disks split, IOMMU, VM IDs, GPU vfio. Do not invent a full PVE textbook in chat.

### 1.3 TrueNAS

Guide: [12-truenas.md](docs/installation_guide/12-truenas.md) · [truenas/README.md](truenas/README.md)

**Ask:** TrueNAS already installed?

| Answer | Then |
|---|---|
| Yes | `TRUENAS_URL`, API key, LAN IP → `instance/truenas/.env`. UI must be **880/8443** (Caddy owns 80/443). |
| No + wants guide | Follow [12-truenas.md](docs/installation_guide/12-truenas.md): *prefer bare metal if no Proxmox*. If PVE: one VM, disks passed through, UI ports. Official SCALE install + **our** ports/HostPath/tunables only. |
| No + no guide | User installs SCALE themselves; we wait for API key. |

**Ask:** timezone, `HOST_LAN_IP` / MAC for DHCP reservation.

### 1.4 Pools & datasets

Guide: [13-pools-datasets.md](docs/installation_guide/13-pools-datasets.md) · [instance/truenas/Readme.md](instance/truenas/Readme.md)

**Ask:** which disks → `apps` (SSD, app data + Docker) · archive HDD · optional NVMe `fast`.

**Effect:** `ensure-datasets.sh` later. Stripe vs mirror = user (no redundancy on `fast` = lost in-progress media only).

**If FileFlows and/or HandBrake:** create `{fastest}/media_work` (quota, `recordsize=1M`, ACL 568+33). *Not* a database. Postiz Postgres/Redis/Temporal stay on `apps`.

### 1.5 Network & domains

Guide: [01-router-portforward.md](docs/installation_guide/01-router-portforward.md) · [docs/networking.md](docs/networking.md)

**Ask:** public zone + wildcard; LAN DNS strategy (*AdGuard on this host, split-horizon*); router model if known.

Write `instance/caddy/.env` keys `{APP}_DOMAIN` / `{APP}_UPSTREAM` for **chosen** apps only.

### 1.6 Email

Guide: [14-email.md](docs/installation_guide/14-email.md) · [instance/email/Readme.md](instance/email/Readme.md)

**Ask:** SMTP for Authentik/NC/Gitea/n8n/Postiz/ACME. *One `instance/email/.env`.*

### 1.7 App picker + presets

Guide: [15-app-picker.md](docs/installation_guide/15-app-picker.md) · [_template/apps.md](instance/_template/apps.md)

**Ask:** preset, then extras. Default for “recreate this infra”: *`full` — keep `_template/apps.md` as-is.*

Delete rows / skip install for apps the user does not want. Do not invent HostPaths — copy from `_template/{app}/Readme.md`.

| Preset | Apps |
|---|---|
| `church-core` | AdGuard, Dockge, Caddy, Authentik, Nextcloud AIO + MCP, n8n, Gitea + runner |
| `church+media` | core + FileFlows, HandBrake, `media_work` |
| `church+family` | core + extra HA OS VM, Tandoor, HomeBox, Gramps (family domains) |
| `full` | all apps in [Readme mermaid](Readme.md) |

Always-on with any preset that is public: Caddy CrowdSec, router 80/443 TCP+UDP.

Per extra app: yes/no. Netbird, WordPress, NocoDB, Postiz, FreeShow stub, second HA (`home`).

### 1.8 Maps / orgs / people

Guide: [02.4-groups-map.md](docs/installation_guide/02-authentik-apps-auth/02.4-groups-map.md) · [_template/maps](instance/_template/maps/index.md)

**Ask:** keep this org tree (church / bless-time / home) or rename? *Keep YAML; only edit names the user rejects.*

Maps YAML is already in `instance/maps/` from step 0. Do **not** start from empty maps. Apply in step 10 (`apply.py` already in `instance/maps/`, not in `_template`).

**Stop.** User reads `instance/`. Fix docs before wave 2.

---

## 2. Hypervisor + TrueNAS on metal

Guides: [11-proxmox.md](docs/installation_guide/11-proxmox.md) · [12-truenas.md](docs/installation_guide/12-truenas.md)
Implement only what step 1 decided. GPU: PVE vfio → TrueNAS VM; guest NVIDIA if FileFlows/HandBrake.

Verify: TrueNAS API `system.info`; PVE MCP if PVE.

---

## 3. Storage

Guide: [13-pools-datasets.md](docs/installation_guide/13-pools-datasets.md)

```bash
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh …
python3 truenas/scripts/apply-tunables.py \
  net.core.rmem_max=2500000 net.core.rmem_default=2500000
```

Write [instance/mount_storages.md](instance/mount_storages.md) for media_work.

---

## 4. Router + public DNS

Guide: [01-router-portforward.md](docs/installation_guide/01-router-portforward.md)

DHCP reservation → forwards in [networking.md](docs/networking.md#router-port-forwarding). A/AAAA for zone. Verify **after Caddy exists** (step 5).

---

## 5. Edge: AdGuard → Dockge → Caddy

Guides: [20-adguard.md](docs/installation_guide/20-adguard.md) · [21-dockge.md](docs/installation_guide/21-dockge.md) · [22-caddy.md](docs/installation_guide/22-caddy.md) · [adguardhome/README.md](adguardhome/README.md) · [dockge/README.md](dockge/README.md) · [caddy/docs/deploy.md](caddy/docs/deploy.md)

1. Catalog AdGuard. `python3 adguardhome/scripts/apply-rewrites.py`
2. `python3 truenas/scripts/set-nameservers.py <AdGuard LAN> <router>` — **then** other apps.
3. Catalog Dockge. HostPath `apps/dockge`.
4. `bash caddy/scripts/push.sh`; CrowdSec healthy; `80/443` tcp+udp.

Verify: `python3 caddy/scripts/check.py`; LAN `dig` = `TRUENAS_LAN`.

---

## 6. Authentik

Guides: [23-authentik.md](docs/installation_guide/23-authentik.md) · [authentik/README.md](authentik/README.md) · skill `.cursor/skills/authentik/SKILL.md`

Catalog Authentik, SMTP from `instance/email/.env`, API token → `instance/authentik/.env`. First admin user.

---

## 7–8. Apps (waves 7–8)

Per app: `{app}/README.md` + `{app}/docs/deploy.md` if present + **`instance/_template/{app}/Readme.md`** then `instance/{app}/Readme.md`.

Catalog: `python3 .cursor/skills/truenas-scale/scripts/catalog-install.py --app … --values …`  
Dockge: compose + `caddy/scripts/push.sh` pattern / app `scripts/push.sh`.

| App | Guide / deploy |
|---|---|
| Nextcloud AIO | [master-nextcloud-aio/docs/deploy.md](master-nextcloud-aio/docs/deploy.md) |
| Nextcloud MCP | [nextcloud-mcp/docs/deploy.md](nextcloud-mcp/docs/deploy.md) |
| n8n | [n8n/README.md](n8n/README.md) |
| Gitea + runner | [gitea/README.md](gitea/README.md) |
| Netbird | [02.1](docs/installation_guide/02-authentik-apps-auth/02.1-authentik-netbird-oidc.md) *(OIDC in step 10)* |
| WordPress | [wordpress/README.md](wordpress/README.md) |
| NocoDB | [nocodb/README.md](nocodb/README.md) |
| FileFlows / HandBrake | [fileflows/README.md](fileflows/README.md) · [handbrake/README.md](handbrake/README.md) |
| Postiz | [postiz/docs/deploy.md](postiz/docs/deploy.md) |
| Tandoor / HomeBox / Gramps | `{app}/docs/deploy.md` |

Wave 8: only **chosen** apps. 2–3 catalog installs at a time. AIO Start is long — do not block other catalog jobs.

---

## 9. Extra VMs (HA OS)

Guide: [02.3](docs/installation_guide/02-authentik-apps-auth/02.3-authentik-home-assistant-sso.md) *(SSO in 10)* · [11-proxmox.md](docs/installation_guide/11-proxmox.md)

If no PVE: skip, or say HA OS needs a VM/host.

---

## 10. Maps + SSO + FA

Guides:

- [02.4-groups-map.md](docs/installation_guide/02-authentik-apps-auth/02.4-groups-map.md)
- [02.2 Nextcloud SSO](docs/installation_guide/02-authentik-apps-auth/02.2-authentik-nextcloud-sso.md)
- [02.1 Netbird](docs/installation_guide/02-authentik-apps-auth/02.1-authentik-netbird-oidc.md)
- [02.3 HA SSO](docs/installation_guide/02-authentik-apps-auth/02.3-authentik-home-assistant-sso.md)
- per-app `{app}/docs/sso.md`

Order in 02.4: groups → entitlements → users → OIDC/FA apps → host-apply → NC ACL. Users re-login.

NetBird Dex stays; Generic OIDC in UI (not fully scripted).

---

## 11. MCP

Guide: [30-mcp.md](docs/installation_guide/30-mcp.md) · app `MCP.md` files

Only for **installed** apps:

| App | How |
|---|---|
| Gitea | `bash .cursor/mcp/install-gitea-mcp.sh` · `.cursor/mcp/gitea.sh` |
| n8n | `.cursor/mcp.json` `streamable-http` `https://{N8N_DOMAIN}/mcp-server/http` |
| Nextcloud | LAN `http://{TRUENAS_LAN}:31800/mcp` after nextcloud-mcp stack |
| PVE | `.cursor/mcp/pve.sh` if Proxmox |
| HA | `.cursor/mcp/home.sh` (or extra VM wrapper) |
| Postiz | `.cursor/mcp/postiz.sh` |

Do not put tokens in `mcp.json`. AI edits `.cursor/mcp.json` from `instance/` (no render script). Reload Cursor MCP. Skip servers for skipped apps.

---

## 12. Verify + handoff

Guide: [90-verify.md](docs/installation_guide/90-verify.md)

- `python3 truenas/scripts/apps-status.py` · `python3 caddy/scripts/check.py`
- [01 verify](docs/installation_guide/01-router-portforward.md#verify) from hotspot
- Authentik library = bound apps only
- NC login + groups; FA 403 for outsiders
- `todo/{app}/` left for non-blocking work

AI sets state `step: done`.

Suggest to remove `instance/_template` after done

---

# Decisions

| Topic | Decision |
|---|---|
| Abort if live | If `instance/truenas/.env` has `TRUENAS_API_KEY` and user did not say **new instance** → abort. No `--force-new` script. |
| `mcp.json` | AI edits `.cursor/mcp.json`. Wrappers read `instance/`. No render script. |
| Presets | `church-core` · `church+media` · `church+family` · `full` |
| State file | AI-only YAML. No script. Gitignored. |
| Scaffold | Copy `instance/_template/` apps + maps YAML into `instance/`. Keep `apply*.py` / `map_lib.py`. No first-install scripts. |
| n8n seed / backup | Out of first-install unless user asks |

# Scripts

Reusable only (`{app}/scripts` or TrueNAS). No first-install-only helpers.

| Script | When |
|---|---|
| `npx skills experimental_install` | Step 0 |
| `.cursor/skills/truenas-scale/scripts/tn-ws.mjs` · `tn.py` · `catalog-install.py` · `ensure-datasets.sh` · `tn-put.mjs` | TrueNAS |
| `truenas/scripts/apply-tunables.py` | SYSCTL upsert |
| `truenas/scripts/set-nameservers.py` | DNS ns1=AdGuard |
| `truenas/scripts/apps-status.py` | Catalog RUNNING |
| `.cursor/skills/truenas-scale/scripts/dockge-list.mjs` · `dockge-update.mjs` | Dockge images |
| `.cursor/skills/…dockge…/scripts/dockge-start.mjs` | list/start/status |
| `.cursor/skills/authentik/scripts/*.py` | SSO, never curl |
| `instance/maps/*/apply.py` | Step 10 |
| `caddy/scripts/ensure-env.py` · `push.sh` · `reload.sh` · `check.py` | Edge |
| `adguardhome/scripts/apply-rewrites.py` | Split-horizon DNS |
| `{app}/scripts/ensure-env.py` · `install-catalog.py` · `push.sh` | Catalog/Dockge apps |
| `master-nextcloud-aio/scripts/**` | OIDC, mail, ACL, ext-storage |
| `.cursor/mcp/install-gitea-mcp.sh` | Step 11 |

Idempotent. Maps never delete.

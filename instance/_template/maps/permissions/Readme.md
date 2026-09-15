# Permissions

## Goal

Authentik groups, entitlements, user paths, Nextcloud surfaces (Collectives / Talk / Deck / folders).

## Files

```
map.yaml                         # quota, paths, links to categories
map-{category}.yaml              # links to subs, or groups if no sub
map-{category}-{sub}.yaml        # groups
map-home.yaml                    # category without sub
map-blesstime.yaml
map-teaching_instruments.yaml    # apps sub (filename without apps- prefix)
```

| Category | Sub | File |
|----------|-----|------|
| `church` | `teams` | `map-church-teams.yaml` |
| | `youth` | `map-church-youth.yaml` |
| | `volleyball` | `map-church-volleyball.yaml` |
| | `guest` | `map-church-guest.yaml` |
| | `tech` | `map-church-tech.yaml` |
| | `infra` | `map-church-infra.yaml` |
| `home` | — | `map-home.yaml` |
| `apps` | `cloud` | `map-apps-cloud.yaml` |
| | `instruments` | `map-apps-instruments.yaml` |
| | `teaching_instruments` | `map-teaching_instruments.yaml` |
| `family` | `family` | `map-name-family.yaml` |
| | `real_estate` | `map-real_estate.yaml` |
| `services` | — | `map-services.yaml` |

Target: `church:teams,youth` `church:infra` `home`. Bare category = all its files.

## How to read

| Field | What |
|-------|------|
| `name` | Authentik group (people). Do not rename. Scripts match by this. |
| `parents` | Authentik `name`s (add-only). YAML list **or** comma-string. No commas in names. |
| `nextcloud.entitlement` | App permission + Nextcloud group slug (English) |
| `nextcloud.team` | Optional. Main Collective name = this group’s Circle in Nextcloud. See below. |
| `quota` | On entitlement. OIDC **sums** matched quotas |
| `via` | Who gets ACL. Defaults omitted from YAML. |
| `decks.permissions` | Deck flags for that team. Default omitted. |
| `external_storage` | NC Local mount. `name` = folder, `dataset` = HostPath (`/mnt/{dataset}`). Applicable = that row’s entitlement. Not a Team Folder |
| `netbird.group` | NetBird user group (map `from_authentik`) |
| `netbird.network` | NetBird Network name. `*-vpn` = overlay only, no app policy |

`services` built-in groups (`authentik Admins`, …): ensure exist, never recreate.

Defaults are **not** written in maps. Write a field only when it is not the default.

| Surface | Default `via` | Write `via` when |
|---------|---------------|------------------|
| `collectives` | `group` (NC group = entitlement) | `via: collective-team` |
| `decks` / `talk` / `folders` | `collective-team` (that Collective’s Circle) | `via: group` |

Circle for `collective-team`: `item.collective` → else `nextcloud.team` → else `item.name`.

### `nextcloud.team`

Main identifier of the group in Nextcloud. Value = Collective title.

Apply: ensure that Collective exists; add entitlement as **member** (unless the same name is listed under `collectives` with another `role`). Do **not** repeat that Collective as a member-only row.

`team` is the default Circle for decks / talk / folders. Set `collective:` on a surface only when it is not the team.

### `nextcloud.decks.permissions`

What that Circle (or group, if `via: group`) can do on the board. `see` is implied by any ACL row.

| YAML | Deck ACL |
|------|----------|
| *(omit)* | `edit, manage` |
| `see` | read only |
| `edit, manage` | same as omit |
| `edit, share` | cards + share, no manage |
| `edit, manage, share` | all |

Do not use decks `access` / `role` for ACL. Folders still use `access: full`. Talk still uses `role`.

## Examples

`map-church-teams.yaml` — parents comma-string; team; omit defaults:

```yaml
- name: Церковь
  idea: Член церкви
  parents: Информация о Церкови, cloud/full-text-search, cloud/giphy, cloud/youtube, cloud/talk, cloud/sharing
  nextcloud:
    entitlement: church
    quota: 45GB
    organization: Бахчисарайская Церковь
    team: Церковь

- name: Церковь/Учитель
  nextcloud:
    entitlement: church-teacher
    team: Церковь - Учитель
    decks:
      - name: Проповеди
        permissions: edit, share

- name: Церковь/Лидер
  nextcloud:
    entitlement: church-lead
    team: Церковь - Лидеры
    collectives:
      - name: Церковь
        role: manager
      - name: Активности Церкви
        role: admin
    decks:
      - name: Планы Покупок
      - name: Пресвитерское Общение

- name: Церковь/Пресвитер
  nextcloud:
    entitlement: presbyter
    team: Пресвитерский Совет
    collectives:
      - name: Церковь
        role: manager
      - name: Церковь - Лидеры
        role: admin
      - name: О Церкви
        role: admin
      - name: Учительство в церкви
        role: admin
    decks:
      - name: Планы Покупок
        permissions: edit, manage, share
      - name: Пресвитерское Общение
        permissions: edit, manage, share
    talk:
      - name: Пресвитерский Совет

- name: Церковь/Медиа
  nextcloud:
    entitlement: church-media
    team: Медиа Команда
    folders:
      - name: Медиа
```

Keep `via: group` when the ACL principal is the entitlement, not the Circle (`talk` Воскресное, `folders` Презентация, deck Bless Time - Проповеди).

## Apply

Never delete. Creds: `instance/authentik/.env` + `instance/caddy/.env` (Authentik); `instance/nextcloud-mcp/.env` (Nextcloud).

```bash
python3 instance/maps/permissions/apply.py
python3 instance/maps/permissions/apply.py church:tech,guest
python3 instance/maps/permissions/apply-permissions-map.py bless-time
```

| Script | Does |
|--------|------|
| [`apply.py`](apply.py) | Authentik: groups, parents (add), NC entitlements + attrs, bindings, user paths |
| [`apply-permissions-map.py`](apply-permissions-map.py) | Nextcloud: groups, Collectives via **group**, Talk/Deck/folders via **Collective team** (unless `via: group`), Local `external_storage`. Deck ACL flags from `permissions`. Create/update mapped ACL; never delete extra live ACL |

User `path` = max priority in group closure (`paths:` in `map.yaml`). Never change `goauthentik.io/*`.

## Effects

Users get NC groups on next OIDC login. Extra live groups / ACL (e.g. old `Медиа`, leftover `church-teacher` on Проповеди) stay until a separate delete approval.

Tandoor: SSO via Group Binding `tandoor-recipes`. Spaces/households are created in Tandoor UI (owner = `space.created_by`), not this map.

HomeBox: SSO via Group Binding `homebox`. Shared inventory = invite in HomeBox UI.

Gramps: SSO via Group Binding `gramps`. One OIDC user = one tree. Trees created in Gramps, not this map.

`name/Админ` entitlement slug is `name-admin`.

Comma-string `parents` without a parser split would treat each character as a parent — apply must split.

## Related

[Maps index](../index.md) · [auth_apps](../auth_apps/Readme.md) · [user-managment](../../../.cursor/rules/user-managment.mdc) · [maps rule](../../../.cursor/rules/maps.mdc) · [Authentik skill](../../../.cursor/skills/authentik/SKILL.md)

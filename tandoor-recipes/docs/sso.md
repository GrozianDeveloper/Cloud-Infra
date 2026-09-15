# Tandoor ↔ Authentik (OIDC)

- Login: Authentik OIDC (`provider_id` **must** be `authentik`; button name **Authentik**). Gate = Group Binding `tandoor-recipes`. Form hidden (`HIDE_LOGIN_FORM=1`). Break-glass: `/accounts/login/?form=1`. Not `SOCIALACCOUNT_ONLY` (breaks migrate on 2.6.15 + `allauth.mfa`).

Official path: django-allauth OpenID Connect. [authentik Tandoor](https://integrations.goauthentik.io/documentation/tandoor/). Tandoor docs: [authentication](https://docs.tandoor.dev/features/authentication/).

Do **not** use Caddy forward-auth / `REMOTE_USER_AUTH` (Tandoor still has users/spaces; a loose `REMOTE_USER` lets anyone pick a username).

## Authentik

App slug `tandoor-recipes`. Bind group `tandoor-recipes` only. Map: [`auth_apps/map.yaml`](../../instance/maps/auth_apps/map.yaml).



## Tandoor env

Catalog `recipes.additional_envs` (values from secrets, never in git):

| Name | Why |
|------|-----|
| `SOCIAL_PROVIDERS` | `allauth.socialaccount.providers.openid_connect` |
| `SOCIALACCOUNT_PROVIDERS` | JSON: provider_id `authentik`, display name `Authentik`, client + discovery from `instance/tandoor-recipes/.env.oidc` |
| `HIDE_LOGIN_FORM` | `1` — hide local form. Break-glass: `/accounts/login/?form=1` |
| `SOCIALACCOUNT_LOGIN_ON_GET` | `1` |
| `SOCIALACCOUNT_AUTO_SIGNUP` | `1` — first OIDC login creates the Django user |
| `ENABLE_SIGNUP` | `0` — local form only; does not block social |
| `SOCIAL_DEFAULT_ACCESS` | `0` — do not dump everyone into the first space |
| `CSRF_TRUSTED_ORIGINS` | `https://{TANDOOR_RECIPES_DOMAIN}` |
| `ACCOUNT_DEFAULT_HTTP_PROTOCOL` | `https` |

`ALLOWED_HOSTS` = domain + `127.0.0.1` + `localhost` (catalog healthcheck hits `127.0.0.1:30290/openapi`).

Do **not** set `SOCIALACCOUNT_ONLY=1` on Tandoor **2.6.15**: `allauth.mfa` is always installed; Django system check then fails (`SOCIALACCOUNT_ONLY` vs MFA / `ACCOUNT_EMAIL_VERIFICATION`). `boot.sh` has no `set -e`, so migrate is skipped and postgres stays empty (`auth_user` missing). Use `HIDE_LOGIN_FORM` instead.

Do not set `SOCIAL_DEFAULT_ACCESS=1`: next SSO user is dumped into the first existing space.

## Spaces / households

Tandoor does **not** treat Django `is_superuser` as space owner. Household + invite APIs require `space.created_by == current user` (`CustomIsSpaceOwner`). Space **admin** group is not enough.

Instance owner: Богдан (`79785894579`) — Django superuser + staff, `max_owned_spaces=100`. Break-glass local: `tandoor-apply` (Django admin only).

A request with **zero** UserSpace auto-creates `{username}'s Space` owned by that user. Create extra spaces / households / invite links in the UI after that. Relogin if the UI still 403s (stale active space).

After first catalog boot, Django `Site.domain` must be the recipes host (default is `example.com`). Set via `manage.py shell` in the recipes container (`/opt/recipes/venv/bin/python`).

## email_verified

Authentik ≥2025.10 may send `email_verified=false`. Tandoor email-matching then skips. New users still auto-create. If a local user must link, set Authentik email verified or a scope mapping.

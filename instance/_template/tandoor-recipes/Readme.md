# Authentik

## Application

- slug = `tandoor-recipes`
- bind group = `tandoor-recipes`

## Provider

- Redirect (strict): `https://{TANDOOR_RECIPES_DOMAIN}/accounts/oidc/authentik/login/callback/`
- `provider_id` in Tandoor **must** be `authentik` (path segment)
- grant_types = `authorization_code`, `refresh_token`
- Scopes: `openid email profile`
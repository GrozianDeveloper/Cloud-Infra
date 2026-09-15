# WordPress

## Authentik

- slug = `wordpress`
- Bind group `wordpress/admin_panel`
- Plugin: OpenID Connect Generic
- Redirect: `https://{WORDPRESS_DOMAIN}/wp-admin/admin-ajax.php?action=openid-connect-authorize`
- Creds: `instance/wordpress/.env.oidc`

## This NAS

- WebUI `30180`
- Data=`apps/wordpress/data`, MariaDB=`apps/wordpress/mariadb`

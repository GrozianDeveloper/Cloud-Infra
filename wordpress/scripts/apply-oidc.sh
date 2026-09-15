#!/bin/sh
# Install OpenID Connect Generic Client. Host: wordpress:cli sidecar. In-app: wp-cli.
set -eu
wp_in() { wp-cli "$@" --allow-root --path=/var/www/html; }

run_wp() {
  if command -v wp-cli >/dev/null 2>&1; then
    wp_in "$@"
    return
  fi
  if command -v wp >/dev/null 2>&1; then
    wp "$@" --allow-root --path=/var/www/html
    return
  fi
  echo "wp-cli missing" >&2
  exit 1
}

apply_settings() {
  : "${WP_OIDC_CLIENT_ID:?}"
  : "${WP_OIDC_CLIENT_SECRET:?}"
  : "${WP_OIDC_LOGIN:?}"
  : "${WP_OIDC_USERINFO:?}"
  : "${WP_OIDC_TOKEN:?}"
  : "${WP_OIDC_ENDSESSION:?}"
  run_wp eval "
\$s = get_option('openid_connect_generic_settings', array());
if (!is_array(\$s)) { \$s = array(); }
\$s['login_type'] = 'button';
\$s['client_id'] = getenv('WP_OIDC_CLIENT_ID');
\$s['client_secret'] = getenv('WP_OIDC_CLIENT_SECRET');
\$s['scope'] = 'email profile openid offline_access';
\$s['endpoint_login'] = getenv('WP_OIDC_LOGIN');
\$s['endpoint_userinfo'] = getenv('WP_OIDC_USERINFO');
\$s['endpoint_token'] = getenv('WP_OIDC_TOKEN');
\$s['endpoint_end_session'] = getenv('WP_OIDC_ENDSESSION');
\$s['identity_key'] = 'sub';
\$s['nickname_key'] = 'preferred_username';
\$s['email_format'] = '{email}';
\$s['displayname_format'] = '{name}';
\$s['link_existing_users'] = 1;
\$s['create_if_does_not_exist'] = 1;
\$s['enforce_privacy'] = 0;
update_option('openid_connect_generic_settings', \$s, false);
echo 'wp oidc settings saved';
"
}

if [ "${1:-}" = "host" ] || [ -n "${WP_CONTAINER:-}" ]; then
  wpcid="${WP_CONTAINER:-}"
  if [ -z "$wpcid" ]; then
    wpcid=$(docker ps --format '{{.ID}} {{.Names}}' | awk 'BEGIN{IGNORECASE=1} /wordpress/ && !/mariadb/ && !/cli/ {print $1; exit}')
  fi
  if [ -z "$wpcid" ]; then
    echo "wordpress container not found" >&2
    exit 1
  fi
  envf=/tmp/wp-oidc.env
  docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$wpcid" | grep '^WORDPRESS_' >"$envf"
  docker run --rm --user 0 --entrypoint wp \
    --volumes-from "$wpcid" \
    --network "container:$wpcid" \
    --env-file "$envf" \
    -e WP_OIDC_CLIENT_ID -e WP_OIDC_CLIENT_SECRET \
    -e WP_OIDC_LOGIN -e WP_OIDC_USERINFO -e WP_OIDC_TOKEN -e WP_OIDC_ENDSESSION \
    wordpress:cli plugin install daggerhart-openid-connect-generic --activate --allow-root
  docker run --rm --user 0 --entrypoint wp \
    --volumes-from "$wpcid" \
    --network "container:$wpcid" \
    --env-file "$envf" \
    -e WP_OIDC_CLIENT_ID -e WP_OIDC_CLIENT_SECRET \
    -e WP_OIDC_LOGIN -e WP_OIDC_USERINFO -e WP_OIDC_TOKEN -e WP_OIDC_ENDSESSION \
    wordpress:cli eval "
\$s = get_option('openid_connect_generic_settings', array());
if (!is_array(\$s)) { \$s = array(); }
\$s['login_type'] = 'button';
\$s['client_id'] = getenv('WP_OIDC_CLIENT_ID');
\$s['client_secret'] = getenv('WP_OIDC_CLIENT_SECRET');
\$s['scope'] = 'email profile openid offline_access';
\$s['endpoint_login'] = getenv('WP_OIDC_LOGIN');
\$s['endpoint_userinfo'] = getenv('WP_OIDC_USERINFO');
\$s['endpoint_token'] = getenv('WP_OIDC_TOKEN');
\$s['endpoint_end_session'] = getenv('WP_OIDC_ENDSESSION');
\$s['identity_key'] = 'sub';
\$s['nickname_key'] = 'preferred_username';
\$s['email_format'] = '{email}';
\$s['displayname_format'] = '{name}';
\$s['link_existing_users'] = 1;
\$s['create_if_does_not_exist'] = 1;
\$s['enforce_privacy'] = 0;
update_option('openid_connect_generic_settings', \$s, false);
echo 'wp oidc settings saved';
" --allow-root
  echo "wordpress oidc ok"
  exit 0
fi

run_wp plugin install daggerhart-openid-connect-generic --activate || run_wp plugin activate daggerhart-openid-connect-generic
if [ -n "${WP_OIDC_CLIENT_ID:-}" ]; then
  apply_settings
else
  echo "Set Settings → OpenID Connect Client from instance/wordpress/.env.oidc"
  echo "Discovery: WP_OIDC_DISCOVERY  Client: WP_OIDC_CLIENT_ID / WP_OIDC_CLIENT_SECRET"
  echo "Scope: email profile openid offline_access"
  echo "Link existing users + create if missing. Enforce Privacy off."
fi

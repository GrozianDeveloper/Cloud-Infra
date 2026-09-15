# Print Site + OIDC app shape. No secrets.
from django.conf import settings
from django.contrib.sites.models import Site

s = Site.objects.get(id=settings.SITE_ID)
print("site", s.id, s.domain, s.name)
print("hosts", settings.ALLOWED_HOSTS)
print("csrf", settings.CSRF_TRUSTED_ORIGINS)
print("http_proto", getattr(settings, "ACCOUNT_DEFAULT_HTTP_PROTOCOL", None))
apps = (settings.SOCIALACCOUNT_PROVIDERS.get("openid_connect") or {}).get("APPS") or []
print("n_apps", len(apps))
for a in apps:
    su = (a.get("settings") or {}).get("server_url") or ""
    host = su.split("/")[2] if "://" in su else ""
    print(
        "app",
        a.get("provider_id"),
        a.get("name"),
        "cid",
        bool(a.get("client_id")),
        "secret",
        bool(a.get("secret")),
        "url_host",
        host,
        "token_auth",
        (a.get("settings") or {}).get("token_auth_method"),
    )
print("ok")

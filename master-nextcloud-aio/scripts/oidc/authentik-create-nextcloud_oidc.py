#!/usr/bin/env python3
"""Idempotent Authentik OIDC app+provider for Nextcloud user_oidc."""
from __future__ import annotations

import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# path-setup: skill lib lives outside this stack
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env, paginate as ak_paginate, request, resolve_creds

INST = ROOT / "instance"
OIDC_ENV = INST / "master-nextcloud-aio" / ".env.oidc"

APP_SLUG = "nextcloud"
APP_NAME = "Nextcloud"
PROVIDER_NAME = "nextcloud"
SCOPE_NAME = "nextcloud"
SCOPE_DISPLAY = "Nextcloud profile"

ENTITLEMENT_PRIORITY = [
    "presbyter",
    "church-lead",
    "church",
]

ENTITLEMENT_ATTRS = {
    "church": {"organization": "Бахчисарайская Церковь"},
    "church-info": {"organization": "Бахчисарайская Церковь"},
    "church-teacher": {"organization": "Бахчисарайская Церковь"},
    "church-lead": {"organization": "Бахчисарайская Церковь"},
    "presbyter": {"organization": "Бахчисарайская Церковь"},
}

EXPRESSION = r'''
from authentik.core.models import Application, ApplicationEntitlement
from authentik.policies.models import PolicyBinding

ENTITLEMENT_PRIORITY = ["presbyter", "church-lead", "church"]

def _parse_quota(raw):
    if raw is None:
        return 0
    s = str(raw).strip().upper().replace(" ", "")
    if not s:
        return 0
    mul = 1
    for suffix, m in (("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024), ("T", 1024**4), ("G", 1024**3), ("M", 1024**2), ("K", 1024)):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            mul = m
            break
    try:
        return int(float(s) * mul)
    except ValueError:
        return 0

def _fmt_quota(n):
    gb = 1024 ** 3
    if n >= gb and n % gb == 0:
        return f"{n // gb} GB"
    if n >= 1024 ** 2 and n % (1024 ** 2) == 0:
        return f"{n // (1024 ** 2)} MB"
    return f"{n} B"

def _app():
    try:
        a = getattr(provider, "application", None)
        if a:
            return a
    except Exception:
        pass
    return Application.objects.filter(slug="nextcloud").first()

user = request.user
attrs = user.attributes or {}
info = attrs.get("info") or {}
settings = attrs.get("settings") or {}

uid = attrs.get("nextcloud_user_id") or f"church-{user.uuid.hex}"

phone = None
uname = user.username or ""
digits = "".join(c for c in uname if c.isdigit())
if len(digits) >= 10:
    phone = digits if uname.startswith("8") else (uname if uname.startswith("+") else f"+{uname}")

def _closure_pks(u):
    seen = set()
    stack = list(u.ak_groups.all())
    while stack:
        g = stack.pop()
        if g.pk in seen:
            continue
        seen.add(g.pk)
        stack.extend(g.parents.all())
    return {str(x) for x in seen}

matched = []
app = _app()
if app:
    from authentik.policies.engine import PolicyEngine
    http_req = getattr(request, "http_request", None) or request
    pks = _closure_pks(user)
    for ent in ApplicationEntitlement.objects.filter(app=app):
        hit = False
        try:
            engine = PolicyEngine(ent, user, http_req)
            engine.build()
            hit = engine.result.passing
        except Exception:
            hit = False
        if not hit:
            for b in PolicyBinding.objects.filter(target=ent):
                gid = getattr(b, "group_id", None)
                if gid is not None and str(gid) in pks:
                    hit = True
                    break
        if hit:
            matched.append(ent)

role = None
for name in ENTITLEMENT_PRIORITY:
    for ent in matched:
        r = (ent.attributes or {}).get("role")
        if ent.name == name and r:
            role = r
            break
    if role:
        break
if role is None:
    for ent in matched:
        r = (ent.attributes or {}).get("role")
        if r:
            role = r
            break

org = None
for ent in matched:
    o = (ent.attributes or {}).get("organization")
    if o:
        org = o
        break

qsum = 0
for ent in matched:
    qsum += _parse_quota((ent.attributes or {}).get("quota"))

ent_names = {ent.name for ent in matched}
org = info.get("organization") or org
role = info.get("role") or role
country = info.get("country")
birthday = info.get("birthday") or info.get("birthdate")
language = settings.get("language") or "ru"
locale = settings.get("locale") or "ru-RU"
region = settings.get("region")
if not region and ("church" in ent_names or "church-info" in ent_names):
    region = "Бахчисарай"
locality = None
if region == "Бахчисарай":
    locality = "Simferopol"

out = {
    "user_id": uid,
    "phone": phone,
    "organisation": org,
    "role": role,
    "quota": _fmt_quota(qsum) if qsum else None,
    "locale": locale,
    "language": language,
    "region": region,
    "locality": locality,
    "country": country,
    "birthdate": birthday,
}
return {k: v for k, v in out.items() if v not in (None, "")}
'''.lstrip()


_DOMAIN = ""


def req(method: str, url: str, token: str, body=None):
    return 200, request(method, url, token, _DOMAIN, body)


def paginate(_base: str, token: str, path: str, params: dict | None = None):
    return ak_paginate(path, token, _DOMAIN, params)


def main() -> int:
    global _DOMAIN
    token, _DOMAIN = resolve_creds()
    caddy = load_env(INST / "caddy" / ".env")
    nc_domain = caddy.get("NEXTCLOUD_DOMAIN")
    if not nc_domain:
        print("need NEXTCLOUD_DOMAIN in instance/caddy/.env", file=sys.stderr)
        return 1
    auth_domain = _DOMAIN
    base = f"https://{auth_domain}/api/v3"
    nc_https = f"https://{nc_domain}"
    auth_https = f"https://{auth_domain}"

    flows = {f["slug"]: f["pk"] for f in paginate(base, token, "/flows/instances/")}
    certs = {c["name"]: c["pk"] for c in paginate(base, token, "/crypto/certificatekeypairs/")}
    scopes = paginate(base, token, "/propertymappings/provider/scope/")
    scope_by_name = {s["scope_name"]: s for s in scopes}

    needed_scopes = ["openid", "profile", "email", "entitlements", "offline_access"]
    mapping_pks = [scope_by_name[n]["pk"] for n in needed_scopes if n in scope_by_name]

    existing_nc = next((s for s in scopes if s.get("scope_name") == SCOPE_NAME), None)
    scope_body = {
        "name": SCOPE_DISPLAY,
        "scope_name": SCOPE_NAME,
        "expression": EXPRESSION,
        "description": "Nextcloud user_oidc claims (user_id, profile, quota)",
    }
    if existing_nc:
        req("PATCH", f"{base}/propertymappings/provider/scope/{existing_nc['pk']}/", token, scope_body)
        nc_scope_pk = existing_nc["pk"]
        print("updated scope mapping", SCOPE_DISPLAY)
    else:
        _, created = req("POST", f"{base}/propertymappings/provider/scope/", token, scope_body)
        nc_scope_pk = created["pk"]
        print("created scope mapping", SCOPE_DISPLAY)
    mapping_pks.append(nc_scope_pk)

    signing = certs.get("authentik Self-signed Certificate")
    if not signing:
        print("missing signing cert", file=sys.stderr)
        return 1

    existing_oidc = load_env(OIDC_ENV)
    client_id = existing_oidc.get("NC_OIDC_CLIENT_ID") or secrets.token_urlsafe(24)
    client_secret = existing_oidc.get("NC_OIDC_CLIENT_SECRET") or secrets.token_urlsafe(48)

    redirect_uris = [
        {"matching_mode": "strict", "url": f"{nc_https}/apps/user_oidc/code", "redirect_uri_type": "authorization"},
        {"matching_mode": "strict", "url": f"{nc_https}/index.php/apps/user_oidc/code", "redirect_uri_type": "authorization"},
        {"matching_mode": "strict", "url": f"{auth_https}/if/user/", "redirect_uri_type": "logout"},
    ]

    provider_payload = {
        "name": PROVIDER_NAME,
        "authentication_flow": flows["default-authentication-flow"],
        "authorization_flow": flows["default-provider-authorization-explicit-consent"],
        "invalidation_flow": flows["default-invalidation-flow"],
        "client_type": "confidential",
        "client_id": client_id,
        "client_secret": client_secret,
        "include_claims_in_id_token": True,
        "signing_key": signing,
        "encryption_key": None,
        "property_mappings": mapping_pks,
        "redirect_uris": redirect_uris,
        "sub_mode": "user_id",
        "access_token_validity": "minutes=15",
        "refresh_token_validity": "days=35",
        "refresh_token_threshold": "days=17",
        "access_code_validity": "minutes=1;seconds=30",
        "logout_method": "backchannel",
        "logout_uri": f"{nc_https}/apps/user_oidc/backchannel-logout/1",
    }

    providers = paginate(base, token, "/providers/oauth2/")
    found_p = next((p for p in providers if p["name"] == PROVIDER_NAME), None)
    if found_p:
        pk = found_p["pk"]
        if found_p.get("client_id"):
            client_id = found_p["client_id"]
            provider_payload["client_id"] = client_id
        req("PATCH", f"{base}/providers/oauth2/{pk}/", token, provider_payload)
        print("updated provider", PROVIDER_NAME)
        provider_pk = pk
    else:
        _, created = req("POST", f"{base}/providers/oauth2/", token, provider_payload)
        provider_pk = created["pk"]
        client_id = created.get("client_id") or client_id
        client_secret = created.get("client_secret") or client_secret
        print("created provider", PROVIDER_NAME)

    apps = paginate(base, token, "/core/applications/")
    found_a = next((a for a in apps if a["slug"] == APP_SLUG), None)
    app_body = {
        "name": APP_NAME,
        "slug": APP_SLUG,
        "provider": provider_pk,
        "meta_launch_url": nc_https,
        "open_in_new_tab": False,
    }
    if found_a:
        req("PATCH", f"{base}/core/applications/{found_a['slug']}/", token, app_body)
        app_pk = found_a["pk"]
        print("updated application", APP_NAME)
    else:
        _, created = req("POST", f"{base}/core/applications/", token, app_body)
        app_pk = created["pk"]
        print("created application", APP_NAME)

    ents = paginate(base, token, "/core/application_entitlements/", {"app": app_pk})
    by_name = {e["name"]: e for e in ents}
    for name, attributes in ENTITLEMENT_ATTRS.items():
        body = {"name": name, "app": app_pk, "attributes": attributes}
        if name in by_name:
            eid = by_name[name].get("pk") or by_name[name].get("pbm_uuid")
            req("PATCH", f"{base}/core/application_entitlements/{eid}/", token, body)
            print("updated entitlement", name)
        else:
            req("POST", f"{base}/core/application_entitlements/", token, body)
            print("created entitlement", name)

    login_stages = paginate(base, token, "/stages/user_login/")
    login = next((s for s in login_stages if s["name"] == "default-authentication-login"), None)
    if login:
        req(
            "PATCH",
            f"{base}/stages/user_login/{login['pk']}/",
            token,
            {"session_duration": "days=35", "remember_me_offset": "seconds=0"},
        )
        print("login stage session 35d")

    OIDC_ENV.write_text(
        "# Nextcloud user_oidc ↔ Authentik. Not for the AIO mastercontainer.\n"
        f"NC_OIDC_CLIENT_ID={client_id}\n"
        f"NC_OIDC_CLIENT_SECRET={client_secret}\n"
        f"NC_OIDC_DISCOVERY={auth_https}/application/o/{APP_SLUG}/.well-known/openid-configuration\n"
        f"NC_OIDC_ENDSESSION={auth_https}/application/o/{APP_SLUG}/end-session/\n"
        f"NC_OIDC_POST_LOGOUT={auth_https}/if/user/\n"
    )
    print("wrote", OIDC_ENV.relative_to(ROOT), "(client secret not printed)")
    print("set Authentik user attribute nextcloud_user_id=admin for the NC admin account")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

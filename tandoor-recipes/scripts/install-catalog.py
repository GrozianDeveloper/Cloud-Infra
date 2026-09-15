#!/usr/bin/env python3
"""Install/update TrueNAS catalog app tandoor-recipes. HostPath only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from ak_lib import load_env
from tn import host_path, tn, upsert_catalog

APP = "tandoor-recipes"


def _values(
    tandoor: dict,
    oidc: dict,
    caddy: dict,
    tz: str,
    static: str,
    media: str,
    db: str,
    port: int,
) -> dict:
    domain = caddy["TANDOOR_RECIPES_DOMAIN"]
    hosts = [domain, "127.0.0.1", "localhost"]
    disc = oidc.get("TANDOOR_RECIPES_OIDC_DISCOVERY") or ""
    cid = oidc.get("TANDOOR_RECIPES_OIDC_CLIENT_ID") or ""
    secret = oidc.get("TANDOOR_RECIPES_OIDC_CLIENT_SECRET") or ""
    if not all([disc, cid, secret]):
        raise SystemExit("missing OIDC keys — run instance/maps/auth_apps/apply.py tandoor-recipes")
    providers = {
        "openid_connect": {
            "APPS": [
                {
                    "provider_id": "authentik",
                    "name": "Authentik",
                    "client_id": cid,
                    "secret": secret,
                    "settings": {"server_url": disc},
                }
            ]
        }
    }
    envs = [
        {"name": "SOCIAL_PROVIDERS", "value": "allauth.socialaccount.providers.openid_connect"},
        {"name": "SOCIALACCOUNT_PROVIDERS", "value": json.dumps(providers, separators=(",", ":"))},
        {"name": "HIDE_LOGIN_FORM", "value": "1"},
        {"name": "SOCIALACCOUNT_LOGIN_ON_GET", "value": "1"},
        {"name": "SOCIALACCOUNT_AUTO_SIGNUP", "value": "1"},
        {"name": "ENABLE_SIGNUP", "value": "0"},
        {"name": "SOCIAL_DEFAULT_ACCESS", "value": "0"},
        {"name": "CSRF_TRUSTED_ORIGINS", "value": f"https://{domain}"},
        {"name": "ACCOUNT_DEFAULT_HTTP_PROTOCOL", "value": "https"},
    ]
    return {
        "TZ": tz,
        "recipes": {
            "postgres_image_selector": "postgres_18_image",
            "db_password": tandoor["DATABASE_PASSWORD"],
            "secret_key": tandoor["SECRET_KEY"],
            "allowed_hosts": hosts,
            "additional_envs": envs,
        },
        "network": {
            "web_port": {"bind_mode": "published", "port_number": port, "host_ips": []},
            "networks": [],
        },
        "storage": {
            "staticfiles": host_path(static),
            "mediafiles": host_path(media),
            "postgres_data": host_path(db, auto_perm=True),
            "additional_storage": [],
        },
    }


def _tz() -> str:
    g = tn("system.general.config", [])
    tz = g.get("timezone") if isinstance(g, dict) else None
    if not tz:
        raise SystemExit("missing timezone from system.general.config")
    return str(tz)


def main() -> int:
    p = argparse.ArgumentParser(description="Install Tandoor catalog app.")
    p.add_argument("--train", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--static", required=True, help="HostPath staticfiles")
    p.add_argument("--media", required=True, help="HostPath mediafiles")
    p.add_argument("--db", required=True, help="HostPath postgres_data")
    p.add_argument("--port", required=True, type=int)
    args = p.parse_args()
    inst = ROOT / "instance"
    tandoor = load_env(inst / "tandoor-recipes" / ".env")
    oidc = load_env(inst / "tandoor-recipes" / ".env.oidc")
    caddy = load_env(inst / "caddy" / ".env")
    if not tandoor.get("DATABASE_PASSWORD") or not tandoor.get("SECRET_KEY"):
        raise SystemExit("missing DATABASE_PASSWORD/SECRET_KEY in instance/tandoor-recipes/.env")
    if not caddy.get("TANDOOR_RECIPES_DOMAIN"):
        raise SystemExit("missing TANDOOR_RECIPES_DOMAIN in instance/caddy/.env")
    values = _values(
        tandoor, oidc, caddy, _tz(), args.static, args.media, args.db, args.port
    )
    upsert_catalog(APP, args.train, args.version, values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

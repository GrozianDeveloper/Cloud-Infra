#!/usr/bin/env python3
"""Install/update TrueNAS catalog app gramps-web. HostPath only."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from ak_lib import load_env, request, resolve_creds
from tn import host_path, tn, upsert_catalog

APP = "gramps-web"


def _issuer(discovery: str) -> str:
    token, domain = resolve_creds()
    data = request("GET", discovery, token, domain)
    iss = data.get("issuer") if isinstance(data, dict) else None
    if not iss:
        raise SystemExit("discovery missing issuer")
    return str(iss)


def _tz() -> str:
    g = tn("system.general.config", [])
    tz = g.get("timezone") if isinstance(g, dict) else None
    if not tz:
        raise SystemExit("missing timezone from system.general.config")
    return str(tz)


def _values(
    app: dict,
    oidc: dict,
    caddy: dict,
    tz: str,
    users: str,
    index: str,
    thumbs: str,
    cache: str,
    media: str,
    db: str,
    port: int,
) -> dict:
    domain = caddy.get("GRAMPS_DOMAIN") or ""
    disc = oidc.get("GRAMPS_OIDC_DISCOVERY") or ""
    cid = oidc.get("GRAMPS_OIDC_CLIENT_ID") or ""
    secret = oidc.get("GRAMPS_OIDC_CLIENT_SECRET") or ""
    redis = app.get("REDIS_PASSWORD") or ""
    key = app.get("SECRET_KEY") or ""
    if not domain:
        raise SystemExit("missing GRAMPS_DOMAIN in instance/caddy/.env")
    if not redis or not key:
        raise SystemExit("missing REDIS_PASSWORD/SECRET_KEY — run gramps-web/scripts/ensure-env.py")
    if len(key) < 32:
        raise SystemExit("SECRET_KEY must be at least 32 characters")
    if not all([disc, cid, secret]):
        raise SystemExit("missing OIDC keys — run instance/maps/auth_apps/apply.py gramps")
    issuer = _issuer(disc)
    envs = [
        {"name": "GRAMPSWEB_BASE_URL", "value": f"https://{domain}"},
        {"name": "GRAMPSWEB_OIDC_ENABLED", "value": "true"},
        {"name": "GRAMPSWEB_OIDC_ISSUER", "value": issuer},
        {"name": "GRAMPSWEB_OIDC_CLIENT_ID", "value": cid},
        {"name": "GRAMPSWEB_OIDC_CLIENT_SECRET", "value": secret},
        {"name": "GRAMPSWEB_OIDC_NAME", "value": "Authentik"},
        {"name": "GRAMPSWEB_OIDC_SCOPES", "value": "openid email profile groups"},
        {"name": "GRAMPSWEB_OIDC_ROLE_CLAIM", "value": "groups"},
        {"name": "GRAMPSWEB_OIDC_GROUP_OWNER", "value": "gramps"},
        {"name": "GRAMPSWEB_OIDC_AUTO_REDIRECT", "value": "true"},
        {"name": "GRAMPSWEB_OIDC_DISABLE_LOCAL_AUTH", "value": "false"},
    ]
    return {
        "TZ": tz,
        "gramps": {
            "redis_password": redis,
            "multi_tree": True,
            "disable_telemetry": False,
            "app_key": key,
            "additional_envs": envs,
        },
        "network": {
            "web_port": {"bind_mode": "published", "port_number": port, "host_ips": []},
            "networks": [],
        },
        "storage": {
            "users": host_path(users),
            "index": host_path(index),
            "thumbnail_cache": host_path(thumbs),
            "cache": host_path(cache),
            "media": host_path(media),
            "grampsdb": host_path(db),
            "additional_storage": [],
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Install Gramps Web catalog app.")
    p.add_argument("--train", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--users", required=True)
    p.add_argument("--index", required=True)
    p.add_argument("--thumbs", required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--media", required=True)
    p.add_argument("--db", required=True)
    p.add_argument("--port", required=True, type=int)
    args = p.parse_args()
    inst = ROOT / "instance"
    values = _values(
        load_env(inst / "gramps-web" / ".env"),
        load_env(inst / "gramps-web" / ".env.oidc"),
        load_env(inst / "caddy" / ".env"),
        _tz(),
        args.users,
        args.index,
        args.thumbs,
        args.cache,
        args.media,
        args.db,
        args.port,
    )
    upsert_catalog(APP, args.train, args.version, values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

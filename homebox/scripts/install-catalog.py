#!/usr/bin/env python3
"""Install/update TrueNAS catalog app homebox. HostPath only."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from ak_lib import load_env, request, resolve_creds
from tn import host_path, tn, upsert_catalog

APP = "homebox"


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


def _values(app: dict, oidc: dict, caddy: dict, tz: str, data: str, port: int) -> dict:
    domain = caddy.get("HOMEBOX_DOMAIN") or ""
    disc = oidc.get("HOMEBOX_OIDC_DISCOVERY") or ""
    cid = oidc.get("HOMEBOX_OIDC_CLIENT_ID") or ""
    secret = oidc.get("HOMEBOX_OIDC_CLIENT_SECRET") or ""
    pepper = app.get("API_KEY_PEPPER") or ""
    if not domain:
        raise SystemExit("missing HOMEBOX_DOMAIN in instance/caddy/.env")
    if not pepper:
        raise SystemExit("missing API_KEY_PEPPER — run homebox/scripts/ensure-env.py")
    if not all([disc, cid, secret]):
        raise SystemExit("missing OIDC keys — run instance/maps/auth_apps/apply.py homebox")
    issuer = _issuer(disc)
    envs = [
        {"name": "HBOX_OIDC_ENABLED", "value": "true"},
        {"name": "HBOX_OIDC_ISSUER_URL", "value": issuer},
        {"name": "HBOX_OIDC_CLIENT_ID", "value": cid},
        {"name": "HBOX_OIDC_CLIENT_SECRET", "value": secret},
        {"name": "HBOX_OPTIONS_TRUST_PROXY", "value": "true"},
        {"name": "HBOX_OPTIONS_HOSTNAME", "value": domain},
        {"name": "HBOX_OIDC_AUTO_REDIRECT", "value": "true"},
        {"name": "HBOX_OPTIONS_ALLOW_LOCAL_LOGIN", "value": "false"},
    ]
    return {
        "TZ": tz,
        "homebox": {
            "api_key_pepper": pepper,
            "additional_envs": envs,
        },
        "run_as": {"user": 568, "group": 568},
        "network": {
            "host_network": False,
            "web_port": {"bind_mode": "published", "port_number": port, "host_ips": []},
            "networks": [],
        },
        "storage": {
            "data": host_path(data),
            "additional_storage": [],
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Install HomeBox catalog app.")
    p.add_argument("--train", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--data", required=True, help="HostPath data")
    p.add_argument("--port", required=True, type=int)
    args = p.parse_args()
    inst = ROOT / "instance"
    values = _values(
        load_env(inst / "homebox" / ".env"),
        load_env(inst / "homebox" / ".env.oidc"),
        load_env(inst / "caddy" / ".env"),
        _tz(),
        args.data,
        args.port,
    )
    upsert_catalog(APP, args.train, args.version, values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

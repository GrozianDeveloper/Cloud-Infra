#!/usr/bin/env python3
"""Create Gitea auth source `authentik` (OIDC). Idempotent."""
from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env

CTX = ssl._create_unverified_context()
INST = ROOT / "instance"


def req(method, url, token, body=None):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=60) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        raise SystemExit(f"{method} {url} -> {e.code}\n{err[:2000]}") from e


def main() -> int:
    gitea = load_env(INST / "gitea" / ".env")
    oidc = load_env(INST / "gitea" / ".env.oidc")
    host = (gitea.get("GITEA_HOST") or "").rstrip("/")
    token = gitea.get("GITEA_ACCESS_TOKEN")
    cid = oidc.get("GITEA_OIDC_CLIENT_ID")
    secret = oidc.get("GITEA_OIDC_CLIENT_SECRET")
    disc = oidc.get("GITEA_OIDC_DISCOVERY")
    if not all([host, token, cid, secret, disc]):
        print("missing gitea host/token or OIDC env", file=sys.stderr)
        return 1
    # Gitea 1.27 swagger has no /admin/auths — CLI: apply-oidc-host.sh
    auths = req("GET", f"{host}/api/v1/admin/auths", token)
    if not isinstance(auths, list):
        auths = auths.get("data") or []
    existing = next((a for a in auths if (a.get("name") or "").lower() == "authentik"), None)
    body = {
        "name": "authentik",
        "is_active": True,
        "is_sync_enabled": False,
        "type": 6,
        "config": {
            "provider": "openidConnect",
            "clientID": cid,
            "clientSecret": secret,
            "autoDiscoverUrl": disc,
            "scopes": "email profile",
            "iconUrl": "",
        },
    }
    if existing:
        aid = existing.get("id")
        req("PATCH", f"{host}/api/v1/admin/auths/{aid}", token, body)
        print("updated auth source authentik")
        return 0
    req("POST", f"{host}/api/v1/admin/auths", token, body)
    print("created auth source authentik")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

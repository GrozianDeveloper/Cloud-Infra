#!/usr/bin/env python3
"""Idempotent AdGuard rewrites: caddy *_DOMAIN → TRUENAS_LAN. Never delete."""
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


def _hosts(caddy: dict[str, str]) -> list[str]:
    out: list[str] = []
    for k, v in caddy.items():
        if not k.endswith("_DOMAIN"):
            continue
        h = v.strip().rstrip(".")
        if h:
            out.append(h.lower())
    return sorted(set(out))


def _rewrites(hosts: list[str]) -> list[str]:
    """Exact FQDN + *.parent (strip leftmost label)."""
    names: set[str] = set(hosts)
    for h in hosts:
        parts = h.split(".")
        if len(parts) >= 3:
            names.add("*." + ".".join(parts[1:]))
    return sorted(names)


def _req(url: str, method: str, body: dict | None, cookie: str | None) -> tuple[int, bytes, str | None]:
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if cookie:
        r.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
            set_c = resp.headers.get("Set-Cookie")
            return resp.status, resp.read(), set_c
    except urllib.error.HTTPError as e:
        set_c = e.headers.get("Set-Cookie") if e.headers else None
        return e.code, e.read() if e.fp else b"", set_c


def _cookie(set_c: str | None) -> str | None:
    if not set_c:
        return None
    return set_c.split(";", 1)[0].strip()


def main() -> int:
    agh = load_env(ROOT / "instance" / "adguardhome" / ".env")
    tn = load_env(ROOT / "instance" / "truenas" / ".env")
    caddy = load_env(ROOT / "instance" / "caddy" / ".env")
    lan = tn.get("TRUENAS_LAN") or tn.get("HOST_LAN_IP") or ""
    user = agh.get("ADGUARD_USER") or ""
    password = agh.get("ADGUARD_PASSWORD") or ""
    base = (agh.get("ADGUARD_URL") or "").rstrip("/")
    if not lan:
        raise SystemExit("missing TRUENAS_LAN / HOST_LAN_IP")
    if not user or not password:
        raise SystemExit("missing ADGUARD_USER / ADGUARD_PASSWORD in instance/adguardhome/.env")
    if not base:
        raise SystemExit("missing ADGUARD_URL in instance/adguardhome/.env")
    code, _, set_c = _req(
        f"{base}/control/login",
        "POST",
        {"name": user, "password": password},
        None,
    )
    cookie = _cookie(set_c)
    if code >= 400 or not cookie:
        raise SystemExit(f"adguard login failed HTTP {code}")
    code, raw, _ = _req(f"{base}/control/rewrite/list", "GET", None, cookie)
    if code >= 400:
        raise SystemExit(f"rewrite list HTTP {code}")
    existing = json.loads(raw.decode() or "[]")
    have = {
        (str(x.get("domain") or "").lower(), str(x.get("answer") or ""))
        for x in existing
        if isinstance(x, dict)
    }
    added = 0
    for domain in _rewrites(_hosts(caddy)):
        key = (domain.lower(), lan)
        if key in have:
            continue
        code, _, _ = _req(
            f"{base}/control/rewrite/add",
            "POST",
            {"domain": domain, "answer": lan},
            cookie,
        )
        if code >= 400:
            raise SystemExit(f"rewrite add {domain} HTTP {code}")
        print("add", domain)
        added += 1
        have.add(key)
    print("rewrites ok", added)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

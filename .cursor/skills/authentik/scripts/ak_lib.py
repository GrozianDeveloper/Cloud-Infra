#!/usr/bin/env python3
"""Authentik API helpers. Creds: --token/--domain > env > instance/{app}/.env."""
from __future__ import annotations

import argparse
import http.client
import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

CTX = ssl._create_unverified_context()
_OPENER: urllib.request.OpenerDirector | None = None


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "instance").is_dir() and (parent / "Readme.md").is_file():
            return parent
    raise SystemExit("repo root not found (need instance/ + Readme.md)")


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def normalize_domain(raw: str) -> str:
    d = raw.strip().rstrip("/")
    for p in ("https://", "http://"):
        if d.lower().startswith(p):
            d = d[len(p) :]
            break
    return d.rstrip("/")


def _tcp_ok(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout):
            return True
    except OSError:
        return False


def _truenas_lan_host() -> str | None:
    url = load_env(repo_root() / "instance" / "truenas" / ".env").get("TRUENAS_URL")
    if url:
        return urlparse(url).hostname
    return None


def pick_connect_host(domain: str, override: str | None = None) -> str:
    if override:
        return override.split("/")[0].split(":")[0]
    lan = _truenas_lan_host()
    # LAN first: public DNS to AUTH_DOMAIN often hangs from this network
    if lan and _tcp_ok(lan, 443, 2.0):
        return lan
    if _tcp_ok(domain, 443, 2.0):
        return domain
    return domain


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    tcp_host: str | None = None
    sni_host: str | None = None

    def connect(self) -> None:
        sock = socket.create_connection((self.tcp_host or self.host, self.port), self.timeout)
        self.sock = CTX.wrap_socket(sock, server_hostname=self.sni_host or self.host)


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, tcp_host: str, sni_host: str):
        super().__init__(context=CTX)
        self._tcp = tcp_host
        self._sni = sni_host

    def https_open(self, req):
        def conn(host, **kw):
            c = _PinnedHTTPSConnection(host, context=CTX, **kw)
            c.tcp_host = self._tcp
            c.sni_host = self._sni
            return c

        return self.do_open(conn, req)


def install_opener(domain: str, connect_host: str | None = None) -> str:
    """Pin TCP to LAN Caddy when public DNS does not reach AUTH_DOMAIN. Returns tcp host."""
    global _OPENER
    tcp = pick_connect_host(domain, connect_host)
    _OPENER = urllib.request.build_opener(_PinnedHTTPSHandler(tcp, domain))
    return tcp


def resolve_creds(
    token: str | None = None,
    domain: str | None = None,
    connect_host: str | None = None,
) -> tuple[str, str]:
    inst = repo_root() / "instance"
    ak = load_env(inst / "authentik" / ".env")
    caddy = load_env(inst / "caddy" / ".env")
    tok = token or os.environ.get("AUTHENTIK_TOKEN") or ak.get("AUTHENTIK_TOKEN")
    dom = (
        domain
        or os.environ.get("AUTH_DOMAIN")
        or ak.get("AUTH_DOMAIN")
        or caddy.get("AUTH_DOMAIN")
        or ak.get("AUTHENTIK_URL")
    )
    if not tok:
        raise SystemExit("AUTHENTIK_TOKEN missing (--token, env, or instance/authentik/.env)")
    if not dom:
        raise SystemExit("AUTH_DOMAIN missing (--domain, env, or instance/caddy/.env)")
    host = normalize_domain(dom)
    install_opener(host, connect_host or os.environ.get("AUTH_CONNECT_HOST"))
    return tok, host


def api_base(domain: str) -> str:
    return f"https://{normalize_domain(domain)}/api/v3"


def add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--token", help="override AUTHENTIK_TOKEN")
    p.add_argument("--domain", help="override AUTH_DOMAIN (host or URL)")
    p.add_argument("--connect-host", help="TCP host for Caddy (default: AUTH_DOMAIN, else TrueNAS LAN)")


def creds_from_args(args: argparse.Namespace) -> tuple[str, str]:
    return resolve_creds(
        getattr(args, "token", None),
        getattr(args, "domain", None),
        getattr(args, "connect_host", None),
    )


def dump(obj: Any) -> None:
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def request(
    method: str,
    path: str,
    token: str,
    domain: str,
    body: Any = None,
) -> Any:
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        rel = path if path.startswith("/") else f"/{path}"
        url = f"{api_base(domain)}{rel}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    opener = _OPENER or urllib.request.build_opener(urllib.request.HTTPSHandler(context=CTX))
    try:
        with opener.open(req, timeout=60) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        raise SystemExit(f"{method.upper()} {url} -> {e.code}\n{err[:4000]}") from e


def paginate(path: str, token: str, domain: str, params: dict | None = None) -> list:
    q = urllib.parse.urlencode({"page_size": 100, **(params or {})})
    rel = path if path.startswith("/") else f"/{path}"
    url = f"{api_base(domain)}{rel}?{q}"
    out: list = []
    while url:
        data = request("GET", url, token, domain)
        if isinstance(data, list):
            return data
        out.extend(data.get("results") or [])
        nxt = (data.get("pagination") or {}).get("next")
        if not nxt:
            url = None
        elif isinstance(nxt, int):
            parsed = urllib.parse.urlparse(url)
            q = dict(urllib.parse.parse_qsl(parsed.query))
            q["page"] = str(nxt)
            url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(q)))
        else:
            url = nxt
    return out


def find_user(token: str, domain: str, ident: str) -> dict:
    users = paginate("/core/users/", token, domain, {"username": ident})
    exact = [u for u in users if u.get("username") == ident]
    if exact:
        return exact[0]
    if ident.isdigit():
        try:
            return request("GET", f"/core/users/{ident}/", token, domain)
        except SystemExit:
            pass
    users = paginate("/core/users/", token, domain, {"search": ident})
    if len(users) == 1:
        return users[0]
    if not users:
        raise SystemExit(f"user not found: {ident}")
    raise SystemExit(f"ambiguous user {ident}: {[u.get('username') for u in users[:10]]}")


def find_group(token: str, domain: str, ident: str) -> dict:
    groups = paginate("/core/groups/", token, domain)
    for g in groups:
        if g.get("pk") == ident or g.get("name") == ident:
            return g
    raise SystemExit(f"group not found: {ident}")


def deep_merge(base: dict, extra: dict) -> dict:
    out = dict(base)
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def parse_json_arg(raw: str | None) -> Any:
    if raw is None:
        return None
    return json.loads(raw)

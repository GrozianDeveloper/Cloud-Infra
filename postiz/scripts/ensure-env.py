#!/usr/bin/env python3
"""Create instance/postiz/.env (missing keys only). Never print secrets."""
from __future__ import annotations

import secrets
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env

INST = ROOT / "instance"
CADDY = INST / "caddy" / ".env"
MAIL = INST / "email" / ".env"
OIDC = INST / "postiz" / ".env.oidc"
OUT = INST / "postiz" / ".env"

PATHS = {
    "POSTIZ_CONFIG_DIR": "/mnt/apps/postiz/config",
    "POSTIZ_UPLOADS_DIR": "/mnt/apps/postiz/uploads",
    "POSTIZ_POSTGRES_DIR": "/mnt/apps/postiz/postgres",
    "POSTIZ_REDIS_DIR": "/mnt/apps/postiz/redis",
    "POSTIZ_TEMPORAL_PG_DIR": "/mnt/apps/postiz/temporal-pg",
    "POSTIZ_TEMPORAL_ES_DIR": "/mnt/apps/postiz/temporal-es",
}


def _set(env: dict[str, str], key: str, value: str | None) -> None:
    if not value:
        return
    if not env.get(key):
        env[key] = value


def _write(path: Path, env: dict[str, str], header: str) -> None:
    existing_order: list[str] = []
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip() or line.strip().startswith("#") or "=" not in line:
                continue
            existing_order.append(line.split("=", 1)[0].strip())
    order = list(existing_order)
    for k in env:
        if k not in order:
            order.append(k)
    lines = [header.rstrip()]
    for k in order:
        v = env.get(k)
        if v is None or v == "":
            continue
        lines.append(f"{k}={v}")
    path.write_text("\n".join(lines) + "\n")


def _ensure_caddy_upstream(caddy: dict[str, str]) -> None:
    if caddy.get("POSTIZ_UPSTREAM"):
        return
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "caddy/scripts/ensure-env.py"),
            "POSTIZ_UPSTREAM=postiz:5000",
        ],
        check=True,
    )


def main() -> int:
    caddy = load_env(CADDY)
    mail = load_env(MAIL)
    oidc = load_env(OIDC)
    env = load_env(OUT)
    domain = caddy.get("POSTIZ_DOMAIN")
    auth = caddy.get("AUTH_DOMAIN")
    if not domain:
        raise SystemExit("missing POSTIZ_DOMAIN in instance/caddy/.env")
    if not auth:
        raise SystemExit("missing AUTH_DOMAIN in instance/caddy/.env")

    _ensure_caddy_upstream(caddy)
    for k, v in PATHS.items():
        _set(env, k, v)
    _set(env, "POSTGRES_USER", "postiz-user")
    _set(env, "POSTGRES_DB", "postiz-db-local")
    _set(env, "POSTGRES_PASSWORD", secrets.token_urlsafe(24))
    _set(env, "JWT_SECRET", secrets.token_hex(32))
    base = f"https://{domain}"
    _set(env, "FRONTEND_URL", base)
    _set(env, "NEXT_PUBLIC_BACKEND_URL", f"{base}/api")
    _set(env, "NEXT_PUBLIC_UPLOAD_STATIC_DIRECTORY", f"{base}/uploads")
    _set(env, "MCP_URL", f"{base}/mcp")
    _set(env, "POSTIZ_OAUTH_URL", f"https://{auth}")
    _set(env, "POSTIZ_OAUTH_AUTH_URL", f"https://{auth}/application/o/authorize/")
    _set(env, "POSTIZ_OAUTH_TOKEN_URL", f"https://{auth}/application/o/token/")
    _set(env, "POSTIZ_OAUTH_USERINFO_URL", f"https://{auth}/application/o/userinfo/")
    _set(env, "POSTIZ_OAUTH_CLIENT_ID", oidc.get("POSTIZ_OIDC_CLIENT_ID"))
    _set(env, "POSTIZ_OAUTH_CLIENT_SECRET", oidc.get("POSTIZ_OIDC_CLIENT_SECRET"))
    _set(env, "EMAIL_HOST", mail.get("SMTP_HOST"))
    _set(env, "EMAIL_PORT", mail.get("SMTP_PORT") or "465")
    _set(env, "EMAIL_USER", mail.get("SMTP_USERNAME"))
    _set(env, "EMAIL_PASS", mail.get("SMTP_PASSWORD"))
    secure = (mail.get("SMTP_Security") or "SSL").upper()
    _set(env, "EMAIL_SECURE", "true" if secure in ("SSL", "TLS", "TRUE", "1") else "false")
    _set(env, "EMAIL_FROM_ADDRESS", mail.get("SMTP_USERNAME"))
    _set(env, "EMAIL_FROM_NAME", "Postiz")
    _write(OUT, env, "# Postiz. Do not commit.")
    print("ok", OUT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

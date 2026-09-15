#!/usr/bin/env python3
"""Create OAuth2/OIDC provider + application. Looks up flows, scopes, signing key."""
from __future__ import annotations

import argparse
import secrets
import sys

from ak_lib import add_common_args, creds_from_args, dump, paginate, request

CONSENT = {
    "explicit": "default-provider-authorization-explicit-consent",
    "implicit": "default-provider-authorization-implicit-consent",
}


def _by(items: list, key: str, value: str) -> dict:
    found = next((i for i in items if i.get(key) == value), None)
    if not found:
        raise SystemExit(f"{key}={value!r} not found")
    return found


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--name", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--launch-url", required=True)
    p.add_argument("--redirect-uri", action="append", required=True, help="repeatable")
    p.add_argument("--logout-uri", action="append", default=[], help="logout redirect URIs")
    p.add_argument("--consent", choices=list(CONSENT), default="implicit")
    p.add_argument("--scopes", default="openid,email,profile", help="comma-separated scope_name")
    p.add_argument("--signing-key", default="authentik Self-signed Certificate")
    p.add_argument("--client-id")
    p.add_argument("--client-secret")
    p.add_argument("--print-secret", action="store_true")
    args = p.parse_args()
    token, domain = creds_from_args(args)

    flows = {f["slug"]: f["pk"] for f in paginate("/flows/instances/", token, domain)}
    authz = flows.get(CONSENT[args.consent])
    invalidation = flows.get("default-invalidation-flow")
    if not authz or not invalidation:
        raise SystemExit("required flows missing")

    certs = paginate("/crypto/certificatekeypairs/", token, domain)
    signing = _by(certs, "name", args.signing_key)["pk"]

    scopes = paginate("/propertymappings/provider/scope/", token, domain)
    by_name = {s.get("scope_name"): s for s in scopes}
    mapping_pks = []
    for name in [s.strip() for s in args.scopes.split(",") if s.strip()]:
        if name not in by_name:
            raise SystemExit(f"scope mapping not found: {name}")
        mapping_pks.append(by_name[name]["pk"])

    client_id = args.client_id or secrets.token_urlsafe(24)
    client_secret = args.client_secret or secrets.token_urlsafe(48)
    redirect_uris = [
        {"matching_mode": "strict", "url": u, "redirect_uri_type": "authorization"}
        for u in args.redirect_uri
    ]
    redirect_uris += [
        {"matching_mode": "strict", "url": u, "redirect_uri_type": "logout"}
        for u in args.logout_uri
    ]

    provider_body = {
        "name": f"Provider for {args.slug}",
        "authorization_flow": authz,
        "invalidation_flow": invalidation,
        "client_type": "confidential",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uris": redirect_uris,
        "property_mappings": mapping_pks,
        "signing_key": signing,
        "include_claims_in_id_token": True,
    }
    auth_flow = flows.get("default-authentication-flow")
    if auth_flow:
        provider_body["authentication_flow"] = auth_flow

    provider = request("POST", "/providers/oauth2/", token, domain, provider_body)
    app = request(
        "POST",
        "/core/applications/",
        token,
        domain,
        {
            "name": args.name,
            "slug": args.slug,
            "provider": provider["pk"],
            "meta_launch_url": args.launch_url,
        },
    )
    out = {
        "application": {"pk": app.get("pk"), "name": app.get("name"), "slug": app.get("slug")},
        "provider": {"pk": provider.get("pk"), "name": provider.get("name"), "client_id": provider.get("client_id")},
        "discovery": f"https://{domain}/application/o/{args.slug}/.well-known/openid-configuration",
    }
    if args.print_secret:
        out["provider"]["client_secret"] = provider.get("client_secret") or client_secret
    dump(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

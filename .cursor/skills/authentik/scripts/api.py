#!/usr/bin/env python3
"""Generic Authentik API call. PATH is under /api/v3/."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ak_lib import add_common_args, creds_from_args, dump, paginate, parse_json_arg, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("method", help="GET POST PATCH PUT DELETE")
    p.add_argument("path", help="e.g. core/users/ or /core/users/me/")
    p.add_argument("body", nargs="?", help="JSON object/array string")
    p.add_argument("--file", help="JSON body from file (instead of positional body)")
    p.add_argument("--paginate", action="store_true", help="GET only: follow pagination.results")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    method = args.method.upper()
    body = None
    if args.file:
        body = json.loads(Path(args.file).read_text())
    elif args.body:
        body = parse_json_arg(args.body)
    if args.paginate:
        if method != "GET":
            raise SystemExit("--paginate only with GET")
        dump(paginate(args.path, token, domain))
        return 0
    dump(request(method, args.path, token, domain, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())

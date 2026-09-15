#!/usr/bin/env python3
"""Add a user to a group (add_user; does not replace the member list)."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, find_group, find_user, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--user", required=True, help="username or pk")
    p.add_argument("--group", required=True, help="group name or pk")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    user = find_user(token, domain, args.user)
    group = find_group(token, domain, args.group)
    dump(
        request(
            "POST",
            f"/core/groups/{group['pk']}/add_user/",
            token,
            domain,
            {"pk": user["pk"]},
        )
        or {"ok": True, "user": user["pk"], "group": group["pk"]}
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

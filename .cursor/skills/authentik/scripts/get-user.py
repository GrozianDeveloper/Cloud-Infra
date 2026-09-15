#!/usr/bin/env python3
"""Get one user by username or pk."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, find_user


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--user", required=True, help="username or pk")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    dump(find_user(token, domain, args.user))
    return 0


if __name__ == "__main__":
    sys.exit(main())

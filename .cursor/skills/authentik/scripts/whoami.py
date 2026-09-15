#!/usr/bin/env python3
"""GET /core/users/me/ — verify token."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    args = p.parse_args()
    token, domain = creds_from_args(args)
    dump(request("GET", "/core/users/me/", token, domain))
    return 0


if __name__ == "__main__":
    sys.exit(main())

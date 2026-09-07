"""Operator commands of the Backend package.

    python -m my_backend serve

Starts the API server on the host and port the Backend section of the
runtime configuration states, and serves until stopped.
"""

from __future__ import annotations

import argparse
import sys

import uvicorn

from .api import create_app
from .runtime import resolve_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="my_backend")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("serve", help="start the API server from the runtime configuration")
    args = parser.parse_args(argv)

    if args.command == "serve":
        settings = resolve_settings()
        uvicorn.run(create_app(settings), host=settings.host, port=settings.port, log_level="info")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

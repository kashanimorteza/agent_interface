"""Operator commands of the Database package.

    python -m my_database seed [--instance KEY]
    python -m my_database generate-key

Structure creation belongs to the migration tooling and is not a command here.
"""

from __future__ import annotations

import argparse
import sys

from . import Database, generate_encryption_key


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="my_database")
    commands = parser.add_subparsers(dest="command", required=True)
    seed = commands.add_parser("seed", help="apply every Model's declared initial data")
    seed.add_argument("--instance", default=None, help="Instance key; default Instance when omitted")
    commands.add_parser("generate-key", help="print a new key for the encrypted at-rest mode")
    args = parser.parse_args(argv)

    if args.command == "generate-key":
        print(generate_encryption_key())
        return 0

    db = Database()
    try:
        report = db.seed(instance=args.instance)
    finally:
        db.close()
    for model, count in report.inserted.items():
        print(f"inserted {count} {model}")
    for model, count in report.skipped.items():
        print(f"skipped  {count} {model} (already present)")
    if report.generated:
        print()
        print("Generated secrets, shown once and stored only in their at-rest form:")
        for item in report.generated:
            print(f"  {item.model} {item.record!r} {item.field}: {item.value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

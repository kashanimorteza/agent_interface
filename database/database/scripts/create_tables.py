"""Manual entry point: run the create_tables Lifecycle Command on the default Instance."""

import sys

from database.interface import Database, DatabaseError


def main() -> int:
    try:
        result = Database().create_tables()
    except DatabaseError as error:
        print(f"create_tables failed on the default Instance: {error}", file=sys.stderr)
        return 1
    print(f"{result.command} on {result.instance.name}: {result.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Manual entry point: run the insert_initial_data Lifecycle Command on the default Instance."""

import sys

from database.interface import Database, DatabaseError


def main() -> int:
    try:
        result = Database().insert_initial_data()
    except DatabaseError as error:
        print(
            f"insert_initial_data failed on the default Instance: {error}",
            file=sys.stderr,
        )
        return 1
    print(f"{result.command} on {result.instance.name}: {result.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

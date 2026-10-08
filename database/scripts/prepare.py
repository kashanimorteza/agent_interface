"""Create the Tables and insert the Initial Data on the default Instance."""

import sys

from database.interface import database_error, database_setup


def main() -> int:
    try:
        result = database_setup().prepare()
    except database_error.DatabaseError as error:
        print(f"prepare: failed - {error}", file=sys.stderr)
        return 1
    print(
        f"{result.command}: {'success' if result.success else 'failed'} - {result.message}"
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

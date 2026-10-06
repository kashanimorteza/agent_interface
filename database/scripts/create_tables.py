"""Manual entry point for the create_tables Lifecycle Command on the default Instance."""

import sys

from database.interface import Database


def main() -> int:
    result = Database().create_tables()
    print(result)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

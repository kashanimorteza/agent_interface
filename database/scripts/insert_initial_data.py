"""Manual entry point for the insert_initial_data Lifecycle Command on the default Instance."""

import sys

from database.interface import Database


def main() -> int:
    result = Database().insert_initial_data()
    print(result)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

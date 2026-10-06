"""Manual entry point for the prepare Lifecycle Command on the default Instance."""

import sys

from database.interface import Database


def main() -> int:
    result = Database().prepare()
    print(result)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

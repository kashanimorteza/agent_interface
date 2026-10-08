"""Creates the Table of every Entity by running the create_tables Setup Operation on the default Instance."""

import sys

from database import database_error, database_setup


def main() -> int:
    try:
        result = database_setup().create_tables()
    except database_error.DatabaseError as error:
        print(f"create_tables failed: {error}")
        return 1
    print(result.message)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

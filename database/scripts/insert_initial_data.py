"""Inserts the missing Initial Data by running the insert_initial_data Setup Operation on the default Instance."""

import sys

from database import database_error, database_setup


def main() -> int:
    try:
        result = database_setup().insert_initial_data()
    except database_error.DatabaseError as error:
        print(f"insert_initial_data failed: {error}")
        return 1
    print(result.message)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

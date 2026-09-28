"""Verify that an Instance holds the storage structure of every Entity that Model publishes.

Run `python -m database.verification` to verify the default Instance.
"""

import sys

from sqlalchemy import inspect

from database import data, structure


def missing_tables(instance: str | None = None) -> list[str]:
    """List the Entity Tables that an Instance lacks.

    Args:
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (list[str]): Names of the Tables the Instance does not contain.
    """
    present = set(inspect(data.resolve(instance).sql_engine).get_table_names())
    return sorted(set(structure.metadata.tables) - present)


def main() -> int:
    """Report whether the default Instance holds every required Table."""
    required = len(structure.metadata.tables)
    missing = missing_tables()
    print(
        f"{required - len(missing)} of {required} Tables found"
        + (f"; missing: {', '.join(missing)}" if missing else "")
    )
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

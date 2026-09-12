"""Public generic Model-driven data-access operations.

Canonical usage::

    import my_database
    my_database.operations.add(record)
"""

from my_database._pipeline import add, delete, edit, list_records, read, set_status

__all__ = ["add", "delete", "edit", "list_records", "read", "set_status"]

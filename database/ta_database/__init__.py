"""Database Component of Trading Assistant.

Layers: Database Interface -> Data Logic and Mapping -> Storage Adapter.
Consumers use only ``open_database()`` (or ``DatabaseInterface``) and ``errors``.
Importing this package never opens a database connection.
"""

from __future__ import annotations

from ta_database.database_interface import errors
from ta_database.database_interface.interface import DatabaseInterface

__version__ = "0.1.0"


def open_database() -> DatabaseInterface:
    """Return a DatabaseInterface bound to the configured database (from runtime settings)."""
    from ta_database.storage_adapter.engine import get_session_factory

    return DatabaseInterface(get_session_factory())


__all__ = ["open_database", "DatabaseInterface", "errors", "__version__"]

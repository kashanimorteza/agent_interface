"""Interface: the gateway other Logic Services import Storage from."""

from database import (
    database_error,
    database_instance,
    database_result,
    database_value,
)

from logic.services.storage.core import Storage

__all__ = [
    "Storage",
    "database_error",
    "database_instance",
    "database_result",
    "database_value",
]

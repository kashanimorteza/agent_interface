"""Database Component of Trading Assistant (package my_database).

Publishes one generic Database Interface — :class:`Database` from the nested database_interface
package — together with the error types consumers handle. The other nested packages, data_logic and
storage_adapter, and the settings module are internal and not part of the public surface.
"""

from my_database.database_interface import Database
from my_database.errors import (
    ConstraintViolationError,
    CredentialKeyMissingError,
    DatabaseError,
    InvalidActionError,
    RecordNotFoundError,
    UnknownFieldError,
    UnknownModelError,
    UnsupportedCredentialModeError,
    UnsupportedOperationError,
)

__version__ = "0.1.0"

__all__ = [
    "Database",
    "DatabaseError",
    "UnknownModelError",
    "UnknownFieldError",
    "RecordNotFoundError",
    "ConstraintViolationError",
    "InvalidActionError",
    "UnsupportedOperationError",
    "CredentialKeyMissingError",
    "UnsupportedCredentialModeError",
]

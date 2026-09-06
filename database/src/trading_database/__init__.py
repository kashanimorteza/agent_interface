"""Database Component of Trading Assistant.

Publishes one generic Database Interface — :class:`Database` — over the resolved SQLite storage,
together with the error types consumers handle. Nothing else (engine, sessions, mapped tables,
settings, migrations) is part of the public surface.
"""

from trading_database.errors import (
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
from trading_database.interface import Database

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

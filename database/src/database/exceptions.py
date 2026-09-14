"""Database's public exception types."""

from __future__ import annotations


class DatabaseError(Exception):
    """Base class for every error the Database Interface raises."""


class UnknownDatabaseInstance(DatabaseError):
    """Raised when an explicit Database Instance selection names no configured Instance."""


class ConnectionFailure(DatabaseError):
    """Raised when the Storage Adapter cannot establish or use a connection."""


class MigrationFailure(DatabaseError):
    """Raised when a Migration cannot be applied or the running structure drifts from it."""


class ConstraintViolation(DatabaseError):
    """Raised when a persistence constraint (uniqueness, required relationship) is violated."""


class TransactionConflict(DatabaseError):
    """Raised when a grouped unit of operations cannot commit due to a detected conflict."""


class ControlledCommandRejected(DatabaseError):
    """Raised when a controlled command route request is not an allow-listed, safe command."""

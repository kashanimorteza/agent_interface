"""Public Database error types (Database Interface, Database Principle 1)."""

from __future__ import annotations


class DatabaseError(Exception):
    """Base class for every error the Database Interface raises."""


class UnknownInstanceError(DatabaseError):
    """Raised when an explicit Instance selection does not name a configured Instance
    (Database Principle 9)."""


class NotFoundError(DatabaseError):
    """Raised when an operation requires an existing persisted record that does not exist."""


class DuplicateRecordError(DatabaseError):
    """Raised when a persist attempt would violate a Target-declared uniqueness constraint
    (Database Principle 10)."""


class ReferencedRecordMissingError(DatabaseError):
    """Raised when a persist attempt references a record that does not exist
    (Database Principle 10 — referenced-record existence)."""


class UnsupportedOperationError(DatabaseError):
    """Raised when a requested Model Operation is not applicable to the given Domain
    Definition (Development Principle 5), or a controlled command requests a structural,
    privilege, or Migration change it must reject (Database Principle 8)."""

"""Distinguishable outcomes the public Database interface can raise."""

from __future__ import annotations


class DatabaseError(Exception):
    """Base class for every Database-raised outcome."""


class UnknownInstanceError(DatabaseError):
    """An explicit Instance identity does not match a configured Instance."""


class NotFoundError(DatabaseError):
    """No record exists for the requested Model type and identifier."""


class ConstraintViolationError(DatabaseError):
    """A write would violate a declared persistence-level rule (a
    uniqueness rule, a required relationship, or a required field).
    """


class StatusNotSupportedError(DatabaseError):
    """The requested Model does not declare a ``status`` field."""


class TransactionConflictError(DatabaseError):
    """A transient conflict (serialization failure, lock timeout, or
    deadlock) occurred and may succeed if retried.
    """


class ControlledSQLRejectedError(DatabaseError):
    """A controlled SQL command attempted a structural change, a privilege
    change, a migration operation, or an identifier outside the allow-list.
    """

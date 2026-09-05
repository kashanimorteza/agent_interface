"""Shared error hierarchy raised by Data Logic and re-exported by the Database Interface."""

from __future__ import annotations


class DatabaseError(Exception):
    """Base class for every error raised by the Database Component."""


class UnknownModel(DatabaseError):
    """The Model key is not indexed in the shared Model configuration."""


class RecordNotFound(DatabaseError):
    """No record of the Model exists with the given primary key."""


class InvalidField(DatabaseError):
    """A key in the supplied data or criteria is not a field of the Model, or the command is invalid."""


class InvalidAction(DatabaseError):
    """The status action is not one of enable or disable."""


class UnsupportedOperation(DatabaseError):
    """The Model does not support the requested operation (for example, it has no status field)."""


class IntegrityViolation(DatabaseError):
    """A uniqueness or referential-integrity rule of the storage schema rejected the change."""


__all__ = [
    "DatabaseError", "UnknownModel", "RecordNotFound", "InvalidField",
    "InvalidAction", "UnsupportedOperation", "IntegrityViolation",
]

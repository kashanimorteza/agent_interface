"""Errors raised through the Database Interface (re-exported from Data Logic)."""

from ta_database.data_logic.errors import (
    DatabaseError,
    IntegrityViolation,
    InvalidAction,
    InvalidField,
    RecordNotFound,
    UnknownModel,
    UnsupportedOperation,
)

__all__ = [
    "DatabaseError", "UnknownModel", "RecordNotFound", "InvalidField",
    "InvalidAction", "UnsupportedOperation", "IntegrityViolation",
]

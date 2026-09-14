"""Database's public surface (Database Principle 1): the generic Database Interface, Instance
Registry, Transaction boundary, and error types. Everything else in this package is private."""

from database.adapter import StorageAdapter
from database.errors import (
    DatabaseError,
    DuplicateRecordError,
    NotFoundError,
    ReferencedRecordMissingError,
    UnknownInstanceError,
    UnsupportedOperationError,
)
from database.interface import DatabaseInterface
from database.registry import InstanceDescriptor, InstanceRegistry
from database.transaction import Transaction

__all__ = [
    "DatabaseError",
    "DatabaseInterface",
    "DuplicateRecordError",
    "InstanceDescriptor",
    "InstanceRegistry",
    "NotFoundError",
    "ReferencedRecordMissingError",
    "StorageAdapter",
    "Transaction",
    "UnknownInstanceError",
    "UnsupportedOperationError",
]

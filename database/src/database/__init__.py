"""Database's Public Interface: the generic Database Interface, Instance Registry, Transaction
boundary, controlled command route, and initial-data seeding for the Trading Assistant."""

from __future__ import annotations

from .db_interface import Database
from .exceptions import (
    ConnectionFailure,
    ConstraintViolation,
    ControlledCommandRejected,
    DatabaseError,
    MigrationFailure,
    TransactionConflict,
    UnknownDatabaseInstance,
)
from .registry import InstanceInfo, InstanceRegistry
from .seed import seed_initial_data
from .transaction import Transaction

__all__ = [
    "ConnectionFailure",
    "ConstraintViolation",
    "ControlledCommandRejected",
    "Database",
    "DatabaseError",
    "InstanceInfo",
    "InstanceRegistry",
    "MigrationFailure",
    "Transaction",
    "TransactionConflict",
    "UnknownDatabaseInstance",
    "seed_initial_data",
]

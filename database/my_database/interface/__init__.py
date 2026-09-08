"""Database Interface — the only boundary this package publishes.

The top of the three responsibilities inside this package, and the only one a
consumer ever meets. It reaches the mapping and operation responsibility below
it; a consumer reaches nothing but this.
"""

from .gateway import (
    DISABLE,
    ENABLE,
    CommandRefused,
    CommandResult,
    ConfigurationError,
    Database,
    OperationError,
    Transaction,
    TransactionCancelled,
)
from .registry import InstanceIdentity, InstanceRegistry

__all__ = [
    "DISABLE",
    "ENABLE",
    "CommandRefused",
    "CommandResult",
    "ConfigurationError",
    "Database",
    "InstanceIdentity",
    "InstanceRegistry",
    "OperationError",
    "Transaction",
    "TransactionCancelled",
]

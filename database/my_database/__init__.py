"""my_database: the persistence layer of the Trading Assistant.

This module is the package's single public interface: the ``Database``
gateway, the transaction boundary it publishes, the ``InstanceRegistry`` and
its ``Instance`` entries, the seeding report types, the credential mask, and
the errors the gateway raises. The adapter, mapping, connection, migration,
and configuration implementation are internal and never imported by
consumers.
"""

from .adapter.instances import Instance
from .errors import (
    ConfigurationError,
    ConnectionUnavailable,
    ConstraintViolation,
    DatabaseError,
    InvalidData,
    InvalidOperation,
    NotFound,
    UnknownInstance,
    UnsupportedRequirement,
)
from .interface.gateway import Database
from .interface.registry import InstanceRegistry
from .interface.transaction import Transaction, TransactionCancelled
from .logic.credentials import generate_encryption_key
from .logic.operations import CREDENTIAL_MASK
from .logic.seed import GeneratedSecret, SeedReport

__all__ = [
    "Database",
    "Transaction",
    "TransactionCancelled",
    "InstanceRegistry",
    "Instance",
    "SeedReport",
    "GeneratedSecret",
    "CREDENTIAL_MASK",
    "generate_encryption_key",
    "DatabaseError",
    "ConfigurationError",
    "UnknownInstance",
    "ConnectionUnavailable",
    "InvalidOperation",
    "InvalidData",
    "NotFound",
    "ConstraintViolation",
    "UnsupportedRequirement",
]

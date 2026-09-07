"""The Database package of Trading Assistant.

Consumers import only from this root: the ``Database`` gateway, the
``InstanceRegistry`` (with ``InstanceIdentity``), and ``DatabaseError`` with
its subclasses. The Engine, connections, mappings, tables, migrations, and
database files are internal.
"""

from .database_interface import Database, InstanceIdentity, InstanceRegistry
from .errors import (
    ConfigurationError,
    ConstraintError,
    CredentialKeyError,
    DatabaseError,
    NotFoundError,
    OperationError,
    StatementError,
    UnknownInstanceError,
    UnsupportedEngineError,
)

__all__ = [
    "Database",
    "InstanceIdentity",
    "InstanceRegistry",
    "DatabaseError",
    "ConfigurationError",
    "UnknownInstanceError",
    "UnsupportedEngineError",
    "CredentialKeyError",
    "OperationError",
    "NotFoundError",
    "ConstraintError",
    "StatementError",
]
__version__ = "0.1.0"

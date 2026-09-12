"""Public interface of the Trading Assistant's Database package.

Canonical usage::

    import my_database
    my_database.operations.add(record)

Public submodules are also re-exported at the package root as a convenience
for the most common operations; they never replace the module-qualified
interface above as the canonical usage pattern.
"""

from my_database import errors, instances, operations, seeding, sql, transactions
from my_database.errors import (
    ConstraintViolationError,
    ControlledSQLRejectedError,
    DatabaseError,
    NotFoundError,
    StatusNotSupportedError,
    TransactionConflictError,
    UnknownInstanceError,
)
from my_database.instances import InstanceIdentity
from my_database.instances import registry as instance_registry
from my_database.operations import add, delete, edit, list_records, read, set_status
from my_database.seeding import seed_initial_data
from my_database.sql import execute_controlled_sql
from my_database.transactions import transaction

__all__ = [  # noqa: RUF022 (grouped by submodules then root re-exports, not one flat sort)
    # public submodules
    "errors",
    "instances",
    "operations",
    "seeding",
    "sql",
    "transactions",
    # package-root convenience re-exports
    "add",
    "read",
    "list_records",
    "edit",
    "delete",
    "set_status",
    "transaction",
    "execute_controlled_sql",
    "seed_initial_data",
    "instance_registry",
    "InstanceIdentity",
    "DatabaseError",
    "UnknownInstanceError",
    "NotFoundError",
    "ConstraintViolationError",
    "StatusNotSupportedError",
    "TransactionConflictError",
    "ControlledSQLRejectedError",
]

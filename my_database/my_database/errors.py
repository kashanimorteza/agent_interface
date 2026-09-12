"""Public, distinguishable Database outcomes.

Canonical usage::

    import my_database
    try:
        ...
    except my_database.errors.NotFoundError:
        ...
"""

from my_database._errors import (
    ConstraintViolationError,
    ControlledSQLRejectedError,
    DatabaseError,
    NotFoundError,
    StatusNotSupportedError,
    TransactionConflictError,
    UnknownInstanceError,
)

__all__ = [
    "ConstraintViolationError",
    "ControlledSQLRejectedError",
    "DatabaseError",
    "NotFoundError",
    "StatusNotSupportedError",
    "TransactionConflictError",
    "UnknownInstanceError",
]

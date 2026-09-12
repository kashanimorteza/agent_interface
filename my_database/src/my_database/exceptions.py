"""Public result and failure types returned by the Database interface.

Every generic operation and the transaction boundary raise one of these
distinguishable types instead of a raw storage or driver error, so a consumer
can choose a safe response without seeing engine internals.
"""

from __future__ import annotations


class DatabaseError(Exception):
    """Base class for every public Database failure."""


class NotFound(DatabaseError):
    """No record matched the requested identifier."""


class ValidationFailed(DatabaseError):
    """The supplied payload does not satisfy the Model's own validation."""


class ConstraintViolation(DatabaseError):
    """A persistence constraint (uniqueness or referenced-record existence) was violated."""


class UnsupportedOperation(DatabaseError):
    """The requested operation is not available, such as status on a Model without one."""


class TransactionConflict(DatabaseError):
    """A concurrent transaction produced a serialization or locking conflict."""


class TransactionTimeout(DatabaseError):
    """The transaction could not complete within the resolved timeout."""


class ConnectionFailure(DatabaseError):
    """The Storage Adapter could not reach the selected Instance."""

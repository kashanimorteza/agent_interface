"""Error types raised by the Database Component.

Consumers handle these instead of SQLAlchemy or sqlite3 exceptions, which never cross the interface.
"""


class DatabaseError(Exception):
    """Base class of every error raised by the Database Component."""


class UnknownModelError(DatabaseError):
    """The given Model key is not a persistent Model."""


class UnknownFieldError(DatabaseError):
    """A field is not part of the Model, or may not be used in this operation."""


class RecordNotFoundError(DatabaseError):
    """No record of the Model has the given primary key."""


class ConstraintViolationError(DatabaseError):
    """A storage constraint (uniqueness, foreign key, referential action) rejected the operation."""


class InvalidActionError(DatabaseError):
    """The status operation received an action other than enable or disable."""


class UnsupportedOperationError(DatabaseError):
    """The Model does not support the requested operation (for example status without a status field)."""


class CredentialKeyMissingError(DatabaseError):
    """CREDENTIAL_ENCRYPTION_KEY is required for an encrypted credential but is not configured."""


class UnsupportedCredentialModeError(DatabaseError):
    """The at-rest credential mode is not one of plaintext, hash, or encrypted."""

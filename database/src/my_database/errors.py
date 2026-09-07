"""Errors raised across the Database boundary.

Every failure inside the package is reported as ``DatabaseError`` or one of its
subclasses; no driver or ORM exception escapes to a consumer.
"""


class DatabaseError(Exception):
    """Base of every error raised by the Database package."""


class ConfigurationError(DatabaseError):
    """The runtime settings delivered to Database are incomplete or invalid."""


class UnknownInstanceError(ConfigurationError):
    """A selected Instance key names no configured Instance."""


class UnsupportedEngineError(ConfigurationError):
    """A configured Instance binds an Engine this package does not implement."""


class CredentialKeyError(ConfigurationError):
    """The credential-encryption key is required but not available."""


class OperationError(DatabaseError):
    """An operation was requested with arguments the interface cannot serve."""


class NotFoundError(DatabaseError):
    """The addressed record does not exist."""


class ConstraintError(DatabaseError):
    """The Engine rejected the change because a constraint would be violated."""


class StatementError(DatabaseError):
    """The Engine could not execute the statement."""

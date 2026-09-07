"""Errors raised through the public Database interface."""


class DatabaseError(Exception):
    """Base of every error the Database package raises."""


class ConfigurationError(DatabaseError):
    """The layer's own configuration, or a secret it names, is missing or invalid."""


class UnknownInstance(DatabaseError):
    """The selected Instance was never declared. It is never answered with the default."""


class ConnectionUnavailable(DatabaseError):
    """The selected Instance could not be reached. No other Instance is used instead."""


class InvalidOperation(DatabaseError):
    """The requested operation is not valid for the given Model or arguments."""


class InvalidData(DatabaseError):
    """The data does not satisfy the Model's own declarations.

    ``fields`` names each field the shared Model validation refused.
    """

    def __init__(self, message: str, fields: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.fields = fields


class NotFound(DatabaseError):
    """No record matches the given identifier."""


class ConstraintViolation(DatabaseError):
    """The change would break a rule this layer guarantees over stored data."""


class UnsupportedRequirement(DatabaseError):
    """A required rule cannot be represented or enforced on the selected Engine."""

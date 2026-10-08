"""Errors: the base error and every failure kind of Database."""


class DatabaseError(Exception):
    """The base of every Database failure."""


class ConfigurationError(DatabaseError):
    """The configuration or the selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """An input or a Field reference is invalid."""


class DeclarationMismatchError(DatabaseError):
    """An existing Table differs from the Declaration of its Entity."""


class ConnectionFailureError(DatabaseError):
    """The connection to an Instance could not be opened."""


class ExecutionError(DatabaseError):
    """A request failed while it ran."""


class SetupError(DatabaseError):
    """A Setup Operation did not complete."""

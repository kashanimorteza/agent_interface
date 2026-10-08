"""Errors (Core): the base error and every failure kind."""


class DatabaseError(Exception):
    """The base of every Database error."""


class ConfigurationError(DatabaseError):
    """Invalid configuration or Instance."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """Invalid input or Field."""


class DeclarationMismatchError(DatabaseError):
    """An existing Table differs from the Declaration of its Entity."""


class ConnectionFailureError(DatabaseError):
    """The connection to an Instance failed."""


class ExecutionError(DatabaseError):
    """An Engine failed to execute a request."""


class SetupError(DatabaseError):
    """A Setup Operation did not complete."""

"""The Database error kinds: one base error and one distinct error for each failure kind."""


class DatabaseError(Exception):
    """The base of every Database error."""


class ConfigurationError(DatabaseError):
    """The configuration or the selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """A request holds invalid input or an invalid Field."""


class DeclarationMismatchError(DatabaseError):
    """An existing Table differs from its Entity's Declaration."""


class ConnectionFailureError(DatabaseError):
    """The connection to the Instance could not be established."""


class ExecutionError(DatabaseError):
    """A command or operation failed while running."""


class SetupError(DatabaseError):
    """A Setup Operation did not complete."""

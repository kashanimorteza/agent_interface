"""The base error and every error kind of the Database contract."""


class DatabaseError(Exception):
    """Every Database failure."""


class ConfigurationError(DatabaseError):
    """Invalid configuration or Instance."""


class InactiveInstanceError(DatabaseError):
    """Inactive Instance selected."""


class InvalidInputError(DatabaseError):
    """Invalid input or Field."""


class DeclarationMismatchError(DatabaseError):
    """Declaration incompatibility."""


class ConnectionFailureError(DatabaseError):
    """Connection failure."""


class ExecutionError(DatabaseError):
    """Execution failure."""


class SetupError(DatabaseError):
    """Incomplete Setup execution."""

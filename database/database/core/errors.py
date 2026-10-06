"""The failure kinds of the Database. None of them carries a connection value."""


class DatabaseError(Exception):
    """The base of every Database failure."""


class ConfigurationError(DatabaseError):
    """The configuration or a selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """An input, Entity, or Field is invalid."""


class DeclarationMismatchError(DatabaseError):
    """Storage and an Entity's Declaration are incompatible."""


class ConnectionFailureError(DatabaseError):
    """The Instance could not be reached."""


class ExecutionError(DatabaseError):
    """A request could not be executed."""


class LifecycleError(DatabaseError):
    """A Lifecycle Command left an incomplete state."""

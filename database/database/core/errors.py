class DatabaseError(Exception):
    """Base of every failure the Database publishes."""


class ConfigurationError(DatabaseError):
    """The configuration or the selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """An input or a Field reference is invalid."""


class DeclarationMismatchError(DatabaseError):
    """An existing Table differs from the Declaration of its Entity."""


class ConnectionFailureError(DatabaseError):
    """The storage of an Instance could not be reached."""


class ExecutionError(DatabaseError):
    """A request reached storage and failed there."""


class LifecycleError(DatabaseError):
    """A Setup Operation did not complete and left an incomplete state."""

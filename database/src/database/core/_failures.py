"""Public failure meanings.

Each meaning is its own class, so a consumer can tell them apart by class or by the
``meaning`` attribute. Each class also derives from the built-in error a consumer
would expect for that kind of problem. No failure carries a credential or a
caller-supplied value.
"""

from collections.abc import Callable
from functools import wraps
from typing import ClassVar


class DatabaseError(Exception):
    """Base of every Database failure."""

    meaning: ClassVar[str] = "database_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ConfigurationFailure(DatabaseError, ValueError):
    """The configuration, or the Instance a request selects, is invalid."""

    meaning = "invalid_configuration"


class InstanceInactiveFailure(DatabaseError, LookupError):
    """The selected Instance exists but is not active."""

    meaning = "inactive_instance"


class InvalidInputFailure(DatabaseError, ValueError):
    """A request, Field, or record is invalid."""

    meaning = "invalid_input"


class DeclarationFailure(DatabaseError, TypeError):
    """The stored structure and a public Declaration are incompatible."""

    meaning = "declaration_incompatibility"


class ConnectionFailure(DatabaseError, ConnectionError):
    """The selected Instance could not be reached."""

    meaning = "connection_failure"


class ExecutionFailure(DatabaseError, RuntimeError):
    """The selected Instance failed to execute a request."""

    meaning = "execution_failure"


class LifecycleFailure(DatabaseError, RuntimeError):
    """A Lifecycle Command could not complete."""

    meaning = "incomplete_lifecycle"


def sanitized[**P, R](function: Callable[P, R]) -> Callable[P, R]:
    """Detach a raised failure from the driver error that caused it.

    The driver's own error carries the statement and its bound values, which may hold
    a credential. A failure leaves Database without that chained context.
    """

    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return function(*args, **kwargs)
        except DatabaseError as error:
            error.__context__ = None
            error.__cause__ = None
            error.__suppress_context__ = True
            raise

    return wrapper

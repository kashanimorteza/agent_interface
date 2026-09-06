"""Error types shared by the Backend layers.

Data Access translates Database errors into these, Logic raises them for domain conditions, and API
maps them to HTTP responses. No layer above Data Access depends on Database exception types.
"""


class BackendError(Exception):
    """Base class of every error raised by the Backend layers."""


class NotFoundError(BackendError):
    """The requested record does not exist."""


class ConflictError(BackendError):
    """A storage constraint (uniqueness or a RESTRICT reference) rejected the change."""


class InvalidFieldError(BackendError):
    """An unknown field, a field that may not be written, or an invalid value was supplied."""


class UnknownModelError(BackendError):
    """The given Model key is not a shared Model."""


class UnsupportedActionError(BackendError):
    """The requested action is not supported for the Model."""

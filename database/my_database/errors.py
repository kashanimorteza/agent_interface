"""Errors raised through the public Database interface."""


class DatabaseError(Exception):
    """Base of every error the Database package raises."""


class ConfigurationError(DatabaseError):
    """The runtime configuration or a required secret is missing or invalid."""


class UnknownInstance(DatabaseError):
    """The selected Instance key is not defined."""


class InvalidOperation(DatabaseError):
    """The requested operation is not valid for the given Model or arguments."""


class NotFound(DatabaseError):
    """No record matches the given identifier."""


class ConstraintViolation(DatabaseError):
    """The operation would violate a mapped storage constraint."""

"""Public exceptions raised by the Database package."""

from __future__ import annotations


class DatabaseConfigurationError(Exception):
    """A required runtime storage configuration or secret is missing or invalid."""


class UnknownInstanceError(Exception):
    """An explicit Instance selection does not name a configured Instance."""


class UnsupportedCredentialModeError(Exception):
    """A credential-classified field declares a storage mode Database does not support."""


class SchemaDriftError(Exception):
    """The running storage structure does not match the recorded Migration history."""


class ActivationNotSupportedError(Exception):
    """An activation (enable/disable) was requested on a Domain Definition with no active-state field."""


class ControlledCommandRejectedError(Exception):
    """A controlled command attempted a structural change, privilege change, or Migration operation."""

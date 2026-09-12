"""Backend-owned logical outcomes that depend on operation or
referenced-entity context, distinct from Database's persistence outcomes.
"""

from __future__ import annotations


class BackendLogicError(Exception):
    """Base class for an application-context rule Logic itself enforces."""


class MissingPlatformRequiredFieldError(BackendLogicError):
    """An Instance is missing a connection field its selected Trading
    Platform requires.
    """

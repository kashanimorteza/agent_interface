"""What can go wrong, named where all three responsibilities can see it.

The route to stored data must be able to refuse something in terms the
behaviour above understands, without that behaviour learning the vocabulary of
the layer beneath. So the names live here, below all three and belonging to
none, and each responsibility raises the one that fits.

Nothing here knows about transport. Turning one of these into a response is the
external boundary's work, and it is the only part of this layer that should
know what a status code is.
"""

from __future__ import annotations


class BackendFault(Exception):
    """Anything this layer refuses or cannot do."""


class Misconfigured(BackendFault):
    """What this layer was given does not let it start."""


class NotFound(BackendFault):
    """The record an operation was to act on does not exist."""


class Invalid(BackendFault):
    """The state an operation would produce is not one the rules allow."""


class Conflict(BackendFault):
    """The operation cannot stand beside what is already stored."""


class Unsupported(BackendFault):
    """The operation is not one this kind of data offers."""


__all__ = [
    "BackendFault",
    "Conflict",
    "Invalid",
    "Misconfigured",
    "NotFound",
    "Unsupported",
]

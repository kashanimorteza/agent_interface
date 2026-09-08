"""How a credential field must be held at rest.

The Model states that a field is a credential and how it must be stored. It
does not store anything itself; the layer that persists the field reads the
declaration and applies it.
"""

from __future__ import annotations

from enum import Enum


class CredentialStorage(str, Enum):
    """The treatment a credential requires wherever it comes to rest."""

    HASH = "hash"
    ENCRYPTED = "encrypted"

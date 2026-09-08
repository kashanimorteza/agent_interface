"""The vocabulary the three responsibilities inside this package agree on.

Failures and results have to be named somewhere all three can see, and that
place cannot be one of them: the storage responsibility must be able to raise
something a consumer will recognise without the boundary above it reaching
downward for the name. So the vocabulary lives here, beneath all three and
belonging to none, and the published boundary is what re-exports it.

Nothing here does anything. It declares what things are called.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class DatabaseError(Exception):
    """Anything this layer refuses or cannot do."""


class ConfigurationError(DatabaseError):
    """The settings this layer owns do not hold together."""


class MissingSecret(DatabaseError):
    """A secret this layer requires was not supplied."""


class OperationError(DatabaseError):
    """An operation was asked for something it cannot do."""


class CredentialError(DatabaseError):
    """A credential could not be treated as its declaration requires."""


class CommandRefused(DatabaseError):
    """A command was refused before it ran."""


class TransactionCancelled(DatabaseError):
    """A group of related changes was called off, and none of them stand."""


@dataclass(frozen=True, slots=True)
class CommandResult:
    """What a command did, carrying nothing it used to do it."""

    rows: tuple[Mapping[str, Any], ...] = ()
    changed: int = 0

    def __len__(self) -> int:
        return len(self.rows)


@dataclass(frozen=True, slots=True)
class InstanceDescription:
    """One stored identity, described without anything that connects."""

    key: str
    name: str
    purpose: str
    engine: str


__all__ = [
    "CommandRefused",
    "CommandResult",
    "ConfigurationError",
    "CredentialError",
    "DatabaseError",
    "InstanceDescription",
    "MissingSecret",
    "OperationError",
    "TransactionCancelled",
]

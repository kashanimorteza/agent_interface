"""The only place in this layer that talks to stored data.

Everything above asks for data operations in terms of the shared definitions and
gets logical data back. What is on the other side — how records are held, what
holds a group of changes together, which engine any of it runs on — stops here.

This translates, and it does nothing else. It decides no behaviour, chooses no
grouping, and reads nothing about what the application is for.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Mapping

from my_database import (
    DISABLE,
    ENABLE,
    ConfigurationError,
    Database,
    OperationError,
)
from my_model import Entity, PartialView

from ..configuration import Configuration, load
from ..faults import Conflict, Invalid, Misconfigured, Unsupported

ENABLED = ENABLE
DISABLED = DISABLE


def _translated(error: Exception) -> Exception:
    """The same refusal, said in this layer's words.

    What the layer beneath calls things is its own business; the behaviour above
    should never have to learn it in order to catch a refusal.
    """

    text = str(error)
    if isinstance(error, OperationError):
        return Unsupported(text)
    lowered = text.lower()
    if "unique" in lowered or "foreign key" in lowered or "constraint" in lowered:
        return Conflict(text)
    return Invalid(text)


class Operations:
    """The data operations this layer can ask for, on one open unit of work."""

    def __init__(self, unit: Any) -> None:
        self._unit = unit

    def create(self, definition: type[Entity], values: Mapping[str, Any]) -> PartialView:
        try:
            return self._unit.create(definition, values)
        except Exception as error:
            raise _translated(error) from error

    def get(self, definition: type[Entity], criteria: Mapping[str, Any]) -> PartialView | None:
        try:
            return self._unit.read(definition, criteria)
        except Exception as error:
            raise _translated(error) from error

    def list(
        self,
        definition: type[Entity],
        criteria: Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> list[PartialView]:
        try:
            return self._unit.list(
                definition, criteria, limit=limit, offset=offset, order_by=order_by
            )
        except Exception as error:
            raise _translated(error) from error

    def update(
        self, definition: type[Entity], criteria: Mapping[str, Any], changes: Any
    ) -> int:
        try:
            return self._unit.update(definition, criteria, changes)
        except Exception as error:
            raise _translated(error) from error

    def delete(self, definition: type[Entity], criteria: Mapping[str, Any]) -> int:
        try:
            return self._unit.delete(definition, criteria)
        except Exception as error:
            raise _translated(error) from error

    def set_status(
        self, definition: type[Entity], criteria: Mapping[str, Any], *, enabled: bool
    ) -> int:
        try:
            return self._unit.set_status(
                definition, criteria, ENABLED if enabled else DISABLED
            )
        except Exception as error:
            raise _translated(error) from error

    def credential_matches(
        self,
        definition: type[Entity],
        criteria: Mapping[str, Any],
        field: str,
        candidate: str,
    ) -> bool:
        try:
            return self._unit.credential_matches(definition, criteria, field, candidate)
        except Exception as error:
            raise _translated(error) from error


class DataAccess:
    """This layer's single route to stored data."""

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._configuration = configuration or load()
        try:
            self._store = Database()
        except ConfigurationError as error:
            raise Misconfigured(f"stored data cannot be reached: {error}") from error
        self._identity = self._resolve_identity()

    def _resolve_identity(self) -> str | None:
        """Which stored identity to act on, taken from the declared binding.

        The composition says which one; this layer only checks that it is one
        the layer beneath actually publishes, and says so plainly when it is
        not, rather than quietly working somewhere else.
        """

        bound = self._configuration.bindings.stored_identity
        if bound is None:
            return None
        available = {identity.key for identity in self._store.instances}
        if bound not in available:
            raise Misconfigured(
                f"the composition binds this layer to the stored identity {bound!r}, "
                f"which is not one the layer beneath publishes; it publishes "
                f"{sorted(available)}"
            )
        return bound

    @property
    def identity(self) -> str:
        """The stored identity operations act on."""

        return self._identity or self._store.instances.default.key

    def available_identities(self) -> tuple[str, ...]:
        return tuple(identity.key for identity in self._store.instances)

    @contextmanager
    def unit(self) -> Iterator[Operations]:
        """One unit of work whose operations hold together or not at all.

        What belongs in a unit is decided above; how it is held together is
        owned below. This connects the two and passes on neither.
        """

        with self._store.transaction(self._identity) as opened:
            yield Operations(opened)

    def operations(self) -> Iterator[Operations]:
        """A single operation, atomic on its own."""

        return self.unit()

    def close(self) -> None:
        self._store.close()


__all__ = ["DataAccess", "Operations"]

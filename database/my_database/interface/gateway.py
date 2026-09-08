"""The one boundary consumers reach stored data through.

Everything a consumer can do is here: choose which stored identity to act on,
work with any definition through the same operations, group related changes so
they hold or fail together, and — for the little that cannot be said that way —
run a controlled command under the same protections.

What a consumer never gets is anything underneath: no connection, no mapping, no
engine, no recorded history. Those exist so this boundary can keep its promises.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Mapping

from my_model import PartialView

from ..contract import (
    CommandRefused,
    CommandResult,
    ConfigurationError,
    OperationError,
    TransactionCancelled,
)
from ..data_logic.access import DataAccess, Unit
from ..data_logic.operations import DISABLE, ENABLE
from ..data_logic.seeding import SeedOutcome
from .registry import InstanceIdentity, InstanceRegistry


class Transaction:
    """A group of related changes on one stored identity.

    Nothing inside takes effect on its own. The group either commits as a whole
    when it succeeds, or leaves the stored data exactly as it found it.
    """

    def __init__(self, unit: Unit, instance: InstanceIdentity) -> None:
        self._operations = unit.operations
        self._instance = instance
        self._engine = unit.engine

    @property
    def instance(self) -> InstanceIdentity:
        """Which stored identity this group is acting on."""

        return self._instance

    def create(self, definition: Any, values: Mapping[str, Any] | None = None) -> PartialView:
        return self._operations.create(definition, values)

    def read(self, definition: Any, criteria: Mapping[str, Any]) -> PartialView | None:
        return self._operations.read(definition, criteria)

    def list(self, definition: Any, criteria: Mapping[str, Any] | None = None, **limits: Any):
        return self._operations.list(definition, criteria, **limits)

    def update(self, definition: Any, criteria: Mapping[str, Any], changes: Any) -> int:
        return self._operations.update(definition, criteria, changes)

    def delete(self, definition: Any, criteria: Mapping[str, Any]) -> int:
        return self._operations.delete(definition, criteria)

    def set_status(self, definition: Any, criteria: Mapping[str, Any], action: str) -> int:
        return self._operations.set_status(definition, criteria, action)

    def credential_matches(
        self, definition: Any, criteria: Mapping[str, Any], field: str, candidate: str
    ) -> bool:
        return self._operations.credential_matches(definition, criteria, field, candidate)

    def execute(
        self,
        statement: str,
        parameters: Mapping[str, Any] | None = None,
        *,
        engine_specific: str | None = None,
    ) -> CommandResult:
        return self._operations.execute(
            statement,
            parameters,
            engine=self._engine,
            engine_specific=engine_specific,
        )

    def seed(self) -> SeedOutcome:
        """Store the declared starting records inside this group."""

        return self._operations.seed()

    def cancel(self) -> None:
        """Call the group off; nothing it did will stand."""

        raise TransactionCancelled("this group of changes was called off")


class Database:
    """The published gateway to stored data."""

    def __init__(self, configuration: object | None = None) -> None:
        self._access = DataAccess(configuration)
        self._registry = InstanceRegistry(
            self._access.described_instances(), self._access.default_instance()
        )

    # <!---------------------------- stored identities -->

    @property
    def instances(self) -> InstanceRegistry:
        """The stored identities a consumer may select from."""

        return self._registry

    # <!---------------------------- grouping related changes -->

    @contextmanager
    def transaction(self, instance: str | InstanceIdentity | None = None) -> Iterator[Transaction]:
        """Group related changes on one stored identity."""

        key = instance.key if isinstance(instance, InstanceIdentity) else instance
        with self._access.unit(key) as unit:
            yield Transaction(unit, self._registry.get(unit.instance.key))

    # <!---------------------------- operations -->

    def create(
        self,
        definition: Any,
        values: Mapping[str, Any] | None = None,
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> PartialView:
        """Store one record of a definition."""

        with self.transaction(instance) as unit:
            return unit.create(definition, values)

    def read(
        self,
        definition: Any,
        criteria: Mapping[str, Any],
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> PartialView | None:
        """One stored record of a definition, or nothing."""

        with self.transaction(instance) as unit:
            return unit.read(definition, criteria)

    def list(
        self,
        definition: Any,
        criteria: Mapping[str, Any] | None = None,
        *,
        instance: str | InstanceIdentity | None = None,
        **limits: Any,
    ) -> list[PartialView]:
        """Every stored record of a definition that matches."""

        with self.transaction(instance) as unit:
            return unit.list(definition, criteria, **limits)

    def update(
        self,
        definition: Any,
        criteria: Mapping[str, Any],
        changes: Any,
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> int:
        """Change the stated fields of the records that match."""

        with self.transaction(instance) as unit:
            return unit.update(definition, criteria, changes)

    def delete(
        self,
        definition: Any,
        criteria: Mapping[str, Any],
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> int:
        """Remove the records that match."""

        with self.transaction(instance) as unit:
            return unit.delete(definition, criteria)

    def set_status(
        self,
        definition: Any,
        criteria: Mapping[str, Any],
        action: str,
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> int:
        """Enable or disable the records that match."""

        with self.transaction(instance) as unit:
            return unit.set_status(definition, criteria, action)

    def credential_matches(
        self,
        definition: Any,
        criteria: Mapping[str, Any],
        field: str,
        candidate: str,
        *,
        instance: str | InstanceIdentity | None = None,
    ) -> bool:
        """Whether a supplied value is the one behind a stored credential.

        This is how a credential is used without ever being handed back.
        """

        with self.transaction(instance) as unit:
            return unit.credential_matches(definition, criteria, field, candidate)

    def execute(
        self,
        statement: str,
        parameters: Mapping[str, Any] | None = None,
        *,
        engine_specific: str | None = None,
        instance: str | InstanceIdentity | None = None,
    ) -> CommandResult:
        """Run a controlled command the operations above cannot express."""

        with self.transaction(instance) as unit:
            return unit.execute(statement, parameters, engine_specific=engine_specific)

    # <!---------------------------- declared starting records -->

    def seed(self, *, instance: str | InstanceIdentity | None = None) -> SeedOutcome:
        """Store the records the definitions declare, safely more than once."""

        with self.transaction(instance) as unit:
            return unit.seed()

    # <!---------------------------- lifetime -->

    def close(self) -> None:
        """Let go of everything this gateway holds open."""

        self._access.release()

    def __enter__(self) -> Database:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


__all__ = [
    "DISABLE",
    "ENABLE",
    "CommandRefused",
    "CommandResult",
    "ConfigurationError",
    "Database",
    "OperationError",
    "Transaction",
    "TransactionCancelled",
]

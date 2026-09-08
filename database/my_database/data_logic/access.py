"""What the published boundary is given to work with.

The boundary above needs three things: which stored identities exist, a unit of
work against one of them, and the pipeline to run inside it. It gets all three
from here, and never reaches the storage responsibility itself — that is this
layer's neighbour, not the boundary's.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from ..contract import InstanceDescription, TransactionCancelled
from ..storage_adapter import Configuration, Connections
from .operations import Operations


@dataclass(frozen=True, slots=True)
class Unit:
    """One open unit of work: the pipeline, and what it is acting on."""

    operations: Operations
    instance: InstanceDescription
    engine: str


class DataAccess:
    """The way in, for the boundary above."""

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._connections = Connections(configuration)

    # <!---------------------------- stored identities -->

    def described_instances(self) -> tuple[InstanceDescription, ...]:
        """Every stored identity, described without anything that connects."""

        return tuple(
            InstanceDescription(
                key=instance.key,
                name=instance.name,
                purpose=instance.purpose,
                engine=instance.engine,
            )
            for instance in self._connections.configuration.instances.values()
        )

    def default_instance(self) -> str:
        """Which identity is used when a caller names none."""

        return self._connections.configuration.default_instance

    # <!---------------------------- units of work -->

    @contextmanager
    def unit(self, instance: str | None = None) -> Iterator[Unit]:
        """A unit of work whose changes hold together or not at all."""

        reached = self._connections.for_instance(instance)
        described = InstanceDescription(
            key=reached.instance.key,
            name=reached.instance.name,
            purpose=reached.instance.purpose,
            engine=reached.instance.engine,
        )

        with reached.engine.connect() as connection:
            transaction = connection.begin()
            try:
                yield Unit(
                    operations=Operations(connection),
                    instance=described,
                    engine=reached.profile.key,
                )
            except TransactionCancelled:
                transaction.rollback()
                return
            except BaseException:
                transaction.rollback()
                raise
            transaction.commit()

    def release(self) -> None:
        """Let go of everything held open."""

        self._connections.release()


__all__ = ["DataAccess", "Unit"]

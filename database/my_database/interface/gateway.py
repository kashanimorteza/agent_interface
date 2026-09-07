"""The Database gateway: every consumer operation in one place."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from my_model import Model

from ..adapter.connection import StorageAdapter
from ..config import DatabaseSettings, resolve_settings
from ..logic.credentials import CredentialTransformer
from ..logic.mapping import StorageMapping
from ..logic.operations import Pipeline
from ..logic.seed import Seeder, SeedReport
from .registry import InstanceRegistry
from .transaction import COMMITTED, ROLLED_BACK, Transaction, TransactionCancelled


class Database:
    """The generic data-access interface over every persistent Model.

    Construct it with no arguments to use the layer's own configuration.
    Every operation accepts an optional ``instance``, given as a key or as an
    identity from the registry; when none is given the declared default is
    used, and an undeclared one is refused.
    """

    def __init__(self, settings: DatabaseSettings | None = None, *, config_path: Path | None = None) -> None:
        self._settings = settings or resolve_settings(config_path)
        self._adapter = StorageAdapter(self._settings)
        default_engine = self._settings.instances[self._settings.default_instance].engine
        self._mapping = StorageMapping(engine=default_engine)
        credentials = CredentialTransformer(
            self._settings.secret(self._settings.encryption_key_secret),
            self._settings.encryption_key_secret,
        )
        self._pipeline = Pipeline(self._mapping, self._adapter, credentials)
        self._seeder = Seeder(self._mapping, credentials)
        self.instances = InstanceRegistry(self._adapter.instances)

    # -- Model operations ----------------------------------------------------

    def create(self, model: type[Model] | Model, data: Mapping[str, Any] | None = None, *,
               instance: Any = None) -> Model:
        """Store a new record from a Model instance, or from a Model and its data."""
        return self._pipeline.create(model, data, instance)

    def read(self, model: type[Model] | Model, key: Any, *, instance: Any = None) -> Model:
        """The record with the given identifier."""
        return self._pipeline.read(model, key, instance)

    def list(self, model: type[Model] | Model, criteria: Mapping[str, Any] | None = None, *,
             instance: Any = None) -> list[Model]:
        """Every record matching the equality criteria, in identifier order."""
        return self._pipeline.list(model, criteria, instance)

    def update(self, model: type[Model] | Model, key: Any, changes: Mapping[str, Any], *,
               instance: Any = None) -> Model:
        """Change only the supplied fields of the record; returns the result."""
        return self._pipeline.update(model, key, changes, instance)

    def delete(self, model: type[Model] | Model, key: Any, *, instance: Any = None) -> None:
        """Remove the record with the given identifier."""
        self._pipeline.delete(model, key, instance)

    def status(self, model: type[Model] | Model, key: Any, action: str, *,
               instance: Any = None) -> Model:
        """Apply ``enable`` or ``disable`` to a Model that declares a status field."""
        return self._pipeline.status(model, key, action, instance)

    def execute(self, statement: str, parameters: Mapping[str, Any] | None = None, *,
                engine: str | None = None, instance: Any = None) -> list[dict[str, Any]]:
        """Run one parameterized data command inside the Database boundary.

        Name ``engine`` when the command is written for one Engine; it is
        refused when the selected Instance uses another, and it carries no
        promise of portability. A command that would change the storage
        structure is refused: that belongs to the migration history.
        """
        return self._pipeline.execute(statement, parameters, engine, instance)

    # -- transaction boundary ------------------------------------------------

    @contextmanager
    def transaction(self, *, instance: Any = None) -> Iterator[Transaction]:
        """Group related operations on one Instance.

        The group's changes are committed together when the block completes,
        and undone together when it raises or when ``cancel`` is called.
        """
        key = self._adapter.instances.resolve_key(instance)
        with self._adapter.open(key) as connection:
            unit = connection.begin()
            transaction = Transaction(self._pipeline, connection, key)
            try:
                yield transaction
            except TransactionCancelled:
                unit.rollback()
                transaction.outcome = ROLLED_BACK
            except BaseException:
                unit.rollback()
                transaction.outcome = ROLLED_BACK
                raise
            else:
                unit.commit()
                transaction.outcome = COMMITTED

    # -- credentials ---------------------------------------------------------

    def verify_credential(self, model: type[Model] | Model, key: Any, field: str, given: str, *,
                          instance: Any = None) -> bool:
        """Whether ``given`` matches the stored credential, in any at-rest mode."""
        return self._pipeline.verify_credential(model, key, field, given, instance)

    def recover_credential(self, model: type[Model] | Model, key: Any, field: str, *,
                           instance: Any = None) -> str:
        """The original value of a credential stored in a recoverable mode."""
        return self._pipeline.recover_credential(model, key, field, instance)

    # -- initial data --------------------------------------------------------

    def seed(self, *, instance: Any = None) -> SeedReport:
        """Apply every Model's declared initial data as one unit; repeatable."""
        with self.transaction(instance=instance) as unit:
            return self._seeder.seed(unit._connection)

    # -- lifecycle -----------------------------------------------------------

    def close(self) -> None:
        self._adapter.dispose()

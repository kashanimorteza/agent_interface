"""The Database gateway: every consumer operation in one place."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from my_model import Model

from ..adapter.connection import StorageAdapter
from ..logic.credentials import CredentialTransformer
from ..logic.mapping import StorageMapping
from ..logic.operations import Pipeline
from ..logic.seed import Seeder, SeedReport
from ..runtime import DatabaseSettings, resolve_settings
from .registry import InstanceRegistry


class Database:
    """The generic data-access interface over every persistent Model.

    Construct it with no arguments to resolve settings from the centralized
    runtime configuration, or pass a resolved ``DatabaseSettings``. Every
    operation accepts an optional ``instance`` key; when none is given the
    default Instance is used.
    """

    def __init__(self, settings: DatabaseSettings | None = None, *, project_root: Path | None = None) -> None:
        self._settings = settings or resolve_settings(project_root)
        self._adapter = StorageAdapter(self._settings)
        self._mapping = StorageMapping()
        credentials = CredentialTransformer(
            self._settings.secret(self._settings.encryption_key_secret),
            self._settings.encryption_key_secret,
        )
        self._pipeline = Pipeline(self._mapping, self._adapter, credentials)
        self._seeder = Seeder(self._mapping, self._adapter, credentials)
        self.instances = InstanceRegistry(self._adapter.instances)

    # -- Model operations ----------------------------------------------------

    def create(self, value: Model, *, instance: str | None = None) -> Model:
        """Store a new record from a Model instance; returns it with its identifier."""
        return self._pipeline.create(value, instance)

    def read(self, model: type[Model] | Model, key: Any, *, instance: str | None = None) -> Model:
        """The record with the given identifier."""
        return self._pipeline.read(model, key, instance)

    def list(self, model: type[Model] | Model, criteria: Mapping[str, Any] | None = None, *,
             instance: str | None = None) -> list[Model]:
        """Every record matching the equality criteria, in identifier order."""
        return self._pipeline.list(model, criteria, instance)

    def update(self, model: type[Model] | Model, key: Any, changes: Mapping[str, Any], *,
               instance: str | None = None) -> Model:
        """Change only the supplied fields of the record; returns the result."""
        return self._pipeline.update(model, key, changes, instance)

    def delete(self, model: type[Model] | Model, key: Any, *, instance: str | None = None) -> None:
        """Remove the record with the given identifier."""
        self._pipeline.delete(model, key, instance)

    def status(self, model: type[Model] | Model, key: Any, action: str, *,
               instance: str | None = None) -> Model:
        """Apply ``enable`` or ``disable`` to a Model that declares a status field."""
        return self._pipeline.status(model, key, action, instance)

    def execute(self, statement: str, parameters: Mapping[str, Any] | None = None, *,
                instance: str | None = None) -> list[dict[str, Any]]:
        """Run one parameterized command inside the Database boundary."""
        return self._pipeline.execute(statement, parameters, instance)

    # -- credentials ---------------------------------------------------------

    def verify_credential(self, model: type[Model] | Model, key: Any, field: str, given: str, *,
                          instance: str | None = None) -> bool:
        """Whether ``given`` matches the stored credential, in any at-rest mode."""
        return self._pipeline.verify_credential(model, key, field, given, instance)

    def recover_credential(self, model: type[Model] | Model, key: Any, field: str, *,
                           instance: str | None = None) -> str:
        """The original value of a credential stored in a recoverable mode."""
        return self._pipeline.recover_credential(model, key, field, instance)

    # -- initial data --------------------------------------------------------

    def seed(self, *, instance: str | None = None) -> SeedReport:
        """Apply every Model's declared initial data; repeatable."""
        return self._seeder.seed(instance)

    # -- lifecycle -----------------------------------------------------------

    def close(self) -> None:
        self._adapter.dispose()

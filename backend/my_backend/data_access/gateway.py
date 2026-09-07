"""Translation of Logic's data operations into calls on the Database gateway.

Every persistence call of the Backend passes through here. The layer holds no
application Behaviour: it selects the bound Instance, forwards each operation
to the public Database interface, returns the shared Model instances it gets
back, and translates persistence errors into logical outcomes.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from my_database import ConstraintViolation, Database, InvalidOperation, NotFound
from my_model import Model

from ..outcomes import ConflictingRecord, InvalidData, RecordNotFound
from ..runtime import BackendSettings, ConfigurationError


class DataAccess:
    def __init__(self, settings: BackendSettings, database: Database | None = None) -> None:
        self._database = database or Database(project_root=settings.project_root)
        self._instance = settings.database_instance
        if self._instance is not None and self._instance not in self._database.instances:
            raise ConfigurationError(f"bound Database Instance {self._instance!r} is not defined")

    @property
    def instance(self) -> str:
        """The Instance every operation uses."""
        return self._instance or self._database.instances.default.key

    def create(self, value: Model) -> Model:
        return self._call(type(value), lambda: self._database.create(value, instance=self._instance))

    def get(self, model: type[Model], key: Any) -> Model:
        return self._call(model, lambda: self._database.read(model, key, instance=self._instance), key)

    def list(self, model: type[Model], criteria: Mapping[str, Any] | None = None) -> list[Model]:
        return self._call(model, lambda: self._database.list(model, criteria, instance=self._instance))

    def update(self, model: type[Model], key: Any, changes: Mapping[str, Any]) -> Model:
        return self._call(model, lambda: self._database.update(model, key, changes, instance=self._instance), key)

    def delete(self, model: type[Model], key: Any) -> None:
        self._call(model, lambda: self._database.delete(model, key, instance=self._instance), key)

    def close(self) -> None:
        self._database.close()

    @staticmethod
    def _call(model: type[Model], operation, key: Any = None):
        try:
            return operation()
        except NotFound as exc:
            raise RecordNotFound(model.__name__, key) from exc
        except ConstraintViolation as exc:
            raise ConflictingRecord(model.__name__) from exc
        except InvalidOperation as exc:
            raise InvalidData(model.__name__, [{"loc": [], "msg": str(exc)}]) from exc

"""Data: resolves the requested Instance and Engine, and routes each Operation to it."""

from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Type, TypeVar

import yaml
from sqlmodel import SQLModel

from my_database.database_engine import sqlite as sqlite_engine

T = TypeVar("T", bound=SQLModel)

_COMPONENT_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _COMPONENT_ROOT / "database.yaml"

_ENGINES = {
    "sqlite": sqlite_engine,
}


def _load_config() -> Dict[str, Any]:
    with open(_CONFIG_PATH, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _resolve(instance_key: Optional[str] = None):
    config = _load_config()
    key = instance_key or config["settings"]["default_instance"]
    instance = dict(config["instances"][key])
    if instance.get("path") and not Path(instance["path"]).is_absolute():
        instance["path"] = str(_COMPONENT_ROOT / instance["path"])
    engine_impl = _ENGINES[instance["engine"]]
    return engine_impl, instance


class Data:
    """Provides one Action for each published Database Operation."""

    @staticmethod
    def add(entity: T) -> T:
        engine_impl, instance = _resolve()
        return engine_impl.add(instance, entity)

    @staticmethod
    def edit(entity_class: Type[T], record_id: Any) -> Optional[T]:
        engine_impl, instance = _resolve()
        return engine_impl.get_by_id(instance, entity_class, record_id)

    @staticmethod
    def update(entity: T) -> T:
        engine_impl, instance = _resolve()
        return engine_impl.update(instance, entity)

    @staticmethod
    def list(
        entity_class: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> Sequence[T]:
        engine_impl, instance = _resolve()
        return engine_impl.list_records(instance, entity_class, filters, order_by)

    @staticmethod
    def delete(entity_class: Type[T], record_id: Any) -> Dict[str, bool]:
        engine_impl, instance = _resolve()
        return engine_impl.delete(instance, entity_class, record_id)

    @staticmethod
    def enable(entity_class: Type[T], record_id: Any) -> Optional[T]:
        engine_impl, instance = _resolve()
        return engine_impl.set_active(instance, entity_class, record_id, True)

    @staticmethod
    def disable(entity_class: Type[T], record_id: Any) -> Optional[T]:
        engine_impl, instance = _resolve()
        return engine_impl.set_active(instance, entity_class, record_id, False)

    @staticmethod
    def get_by_id(entity_class: Type[T], record_id: Any) -> Optional[T]:
        engine_impl, instance = _resolve()
        return engine_impl.get_by_id(instance, entity_class, record_id)

    @staticmethod
    def count(entity_class: Type[SQLModel], filters: Optional[Dict[str, Any]] = None) -> int:
        engine_impl, instance = _resolve()
        return engine_impl.count(instance, entity_class, filters)

    @staticmethod
    def sum(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        engine_impl, instance = _resolve()
        return engine_impl.aggregate(instance, entity_class, "sum", field, filters)

    @staticmethod
    def min(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        engine_impl, instance = _resolve()
        return engine_impl.aggregate(instance, entity_class, "min", field, filters)

    @staticmethod
    def max(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        engine_impl, instance = _resolve()
        return engine_impl.aggregate(instance, entity_class, "max", field, filters)

    @staticmethod
    def truncate(entity_class: Type[SQLModel]) -> None:
        engine_impl, instance = _resolve()
        engine_impl.truncate(instance, entity_class)

    @staticmethod
    def execute_command(command: str, parameters: Optional[Dict[str, Any]] = None):
        engine_impl, instance = _resolve()
        return engine_impl.execute_command(instance, command, parameters)

    @staticmethod
    def create_all(metadata) -> None:
        engine_impl, instance = _resolve()
        engine_impl.create_all(instance, metadata)

"""Resolve a Model key to its mapping and validate caller-supplied field names."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from ta_database.data_logic.errors import InvalidField, UnknownModel
from ta_database.storage_adapter.models import MODEL_REGISTRY


def resolve_model(model_key: str) -> type:
    try:
        return MODEL_REGISTRY[model_key]
    except (KeyError, TypeError):
        raise UnknownModel(f"unknown model {model_key!r}; expected one of {', '.join(MODEL_REGISTRY)}") from None


def column_names(mapped_class: type) -> list[str]:
    return [c.name for c in mapped_class.__table__.columns]


def primary_key_name(mapped_class: type) -> str:
    return next(c.name for c in mapped_class.__table__.columns if c.primary_key)


def validate_fields(mapped_class: type, data: Mapping[str, Any] | Iterable[str], allow_primary_key: bool = False) -> None:
    columns = set(column_names(mapped_class))
    pk = primary_key_name(mapped_class)
    for key in data:
        if key not in columns:
            raise InvalidField(f"{mapped_class.__tablename__} has no field {key!r}")
        if key == pk and not allow_primary_key:
            raise InvalidField(f"field {key!r} is the primary key and cannot be supplied")

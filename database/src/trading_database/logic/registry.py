"""Model registry — resolves a Model key to its table, columns, primary key, credential modes, and status capability."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from trading_database.errors import UnknownModelError
from trading_database.storage.base import Base
import trading_database.storage.tables  # noqa: F401 — registers every mapped table

# Resolved at-rest modes of credential fields (.interface/config/database.yaml credential_storage); never inferred from names.
CREDENTIAL_MODES: Mapping[str, Mapping[str, str]] = MappingProxyType(
    {
        "user": MappingProxyType({"password": "hash", "api_key": "hash"}),
        "account": MappingProxyType({"password": "encrypted"}),
    }
)

MODEL_KEYS: tuple[str, ...] = (
    "user",
    "currency",
    "trading_platform",
    "broker",
    "account",
    "asset",
    "trailing_group",
    "trailing_rule",
    "partial_group",
    "partial_rule",
    "action_group",
    "action",
    "position",
)


@dataclass(frozen=True)
class ModelInfo:
    key: str
    table_name: str
    mapped_class: type
    primary_key: str
    columns: tuple[str, ...]
    credential_fields: Mapping[str, str]
    has_status: bool


def build_registry() -> dict[str, ModelInfo]:
    """One ModelInfo per mapped class, in model.yaml order."""
    by_key: dict[str, ModelInfo] = {}
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        table = mapper.local_table
        key = cls.__model_key__
        pk = tuple(c.name for c in table.primary_key.columns)
        by_key[key] = ModelInfo(
            key=key,
            table_name=table.name,
            mapped_class=cls,
            primary_key=pk[0],
            columns=tuple(c.name for c in table.columns),
            credential_fields=CREDENTIAL_MODES.get(key, MappingProxyType({})),
            has_status="status" in table.columns,
        )
    missing = [k for k in MODEL_KEYS if k not in by_key]
    if missing:  # pragma: no cover - guards against an incomplete mapping
        raise RuntimeError(f"mapped tables missing for Models: {missing}")
    return {k: by_key[k] for k in MODEL_KEYS}


_REGISTRY = build_registry()
_BY_TABLE = {info.table_name: info for info in _REGISTRY.values()}


def get_model(key: str) -> ModelInfo:
    try:
        return _REGISTRY[key]
    except KeyError:
        raise UnknownModelError(f"unknown Model {key!r}; known Models: {', '.join(MODEL_KEYS)}") from None


def get_model_by_table(table_name: str) -> ModelInfo:
    try:
        return _BY_TABLE[table_name]
    except KeyError:
        raise UnknownModelError(f"no Model is stored in table {table_name!r}") from None

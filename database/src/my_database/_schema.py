"""The generic Data Logic and Mapping layer: derives physical tables from Models.

One mechanism maps every persistent Model to a table by reading that
Model's own declared fields (type, required-ness, uniqueness intent,
credential nature) and its resolved relationship targets — no per-Model
mapping code. This is what lets a new Model join the schema without a new
implementation here.
"""

from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal
from types import UnionType
from typing import Union, get_args, get_origin

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

from ._relationships import PERSISTENT_MODELS, RELATIONSHIP_TARGETS

metadata = MetaData()

_PY_TO_SA = {
    int: Integer,
    str: String,
    bool: Boolean,
    float: Float,
    Decimal: lambda: Numeric(18, 6),
    datetime: DateTime,
}


def _sa_type(annotation):
    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        annotation = args[0]
    factory = _PY_TO_SA[annotation]
    return factory() if callable(factory) and not isinstance(factory, type) else factory


def table_name(model_cls: type) -> str:
    """Derives a plural_snake_case table name from the Model's class name."""
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", model_cls.__name__).lower()
    if snake.endswith("y") and snake[-2] not in "aeiou":
        return snake[:-1] + "ies"
    return snake + "s"


_TABLES: dict[type, Table] = {}


def build_all_tables() -> dict[type, Table]:
    """Builds (once) the physical table for every persistent Model, in dependency order."""
    if _TABLES:
        return _TABLES
    for model_cls in PERSISTENT_MODELS:
        _TABLES[model_cls] = _build_table(model_cls)
    return _TABLES


def _build_table(model_cls: type) -> Table:
    relationship_targets = RELATIONSHIP_TARGETS.get(model_cls, {})
    columns: list[Column] = []
    for name, info in model_cls.model_fields.items():
        is_pk = name == "id"
        nullable = True if is_pk else info.is_required() is False and _allows_none(info.annotation)
        extra = info.json_schema_extra if isinstance(info.json_schema_extra, dict) else {}
        unique = bool(extra.get("unique")) or is_pk

        fk_target = relationship_targets.get(name)
        if fk_target is not None:
            target_table = table_name(fk_target)
            columns.append(
                Column(name, Integer, ForeignKey(f"{target_table}.id"), nullable=nullable, unique=unique)
            )
            continue

        columns.append(
            Column(
                name,
                _sa_type(info.annotation),
                primary_key=is_pk,
                autoincrement=is_pk,
                nullable=False if is_pk else nullable,
                unique=unique and not is_pk,
            )
        )

    constraints = []
    for i, group in enumerate(getattr(model_cls, "unique_together", ())):
        constraints.append(UniqueConstraint(*group, name=f"uq_{table_name(model_cls)}_{i}"))

    return Table(table_name(model_cls), metadata, *columns, *constraints)


def _allows_none(annotation) -> bool:
    origin = get_origin(annotation)
    return origin in (Union, UnionType) and type(None) in get_args(annotation)

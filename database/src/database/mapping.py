"""Storage Mapping: derives one physical table per persistent Model from its published metadata.

One shared pipeline builds every table; no Model gets a hand-written mapping.
"""

from __future__ import annotations

import datetime as dt
import decimal
import re
from typing import Any, Union, get_args, get_origin

from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model.foundation import DomainModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

ALL_MODELS: tuple[type[DomainModel], ...] = (
    User,
    TradingPlatform,
    Instance,
    Currency,
    Broker,
    Asset,
    AccountGroup,
    Account,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)

metadata = MetaData()

_tables: dict[type[DomainModel], Table] = {}


def _snake_case(name: str) -> str:
    step = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", step).lower()


def _pluralize(singular: str) -> str:
    if singular.endswith("y") and singular[-2] not in "aeiou":
        return singular[:-1] + "ies"
    return singular + "s"


def table_name_for(model_cls: type[DomainModel]) -> str:
    """The plural snake_case table name derived from a Domain Definition's class name."""
    return _pluralize(_snake_case(model_cls.__name__))


def _base_annotation(annotation: object) -> object:
    if get_origin(annotation) is Union:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def _column_type(annotation: object) -> object:
    base = _base_annotation(annotation)
    if base is int:
        return Integer()
    if base is str:
        return String()
    if base is bool:
        return Boolean()
    if base is float:
        return Numeric()
    if base is decimal.Decimal:
        return Numeric()
    if base is dt.datetime:
        return DateTime(timezone=True)
    raise TypeError(f"Unsupported field type for storage mapping: {annotation!r}")


def table_for(model_cls: type[DomainModel]) -> Table | None:
    """The physical Table for a persistent Model, built from its published metadata.

    Returns None for a Model declared non-persistent; that Model produces no
    physical structure.
    """
    if model_cls in _tables:
        return _tables[model_cls]

    persistence = model_cls.persistence_metadata()
    if not persistence["persistent"]:
        return None

    columns: list[Column] = []
    for field_name, field_meta in persistence["fields"].items():
        column_args: list[Any] = [
            field_name,
            _column_type(model_cls.model_fields[field_name].annotation),
        ]
        if field_meta["foreign_key"]:
            ref_singular, ref_field = field_meta["foreign_key"].split(".")
            column_args.append(ForeignKey(f"{_pluralize(ref_singular)}.{ref_field}"))
        columns.append(
            Column(
                *column_args,
                primary_key=field_meta["primary_key"],
                autoincrement=field_meta["auto_increment"]
                if field_meta["primary_key"]
                else False,
                nullable=field_meta["nullable"],
                unique=field_meta["unique"],
                index=field_meta["index"],
            )
        )

    table_name = table_name_for(model_cls)
    constraints = [
        UniqueConstraint(*unique_set, name=f"uq_{table_name}_{'_'.join(unique_set)}")
        for unique_set in persistence["unique_sets"]
    ]

    table = Table(table_name, metadata, *columns, *constraints)
    _tables[model_cls] = table
    return table


def build_all_tables() -> MetaData:
    """Populate the shared MetaData with every persistent Model's physical table."""
    for model_cls in ALL_MODELS:
        table_for(model_cls)
    return metadata

"""Data Logic and Mapping: generic storage mapping derived from Model.

Builds one shared SQLAlchemy ``MetaData`` by reading every persistent Model's
published ``persistence_contract()`` — never a hand-copied duplicate of
Model's field, relationship, or constraint meaning.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

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
from model.foundation import DomainModel, FieldMeta, PersistenceContract, persistence_contract
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

PERSISTENT_MODELS: tuple[type[DomainModel], ...] = (
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

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


def snake_case(name: str) -> str:
    return _CAMEL_BOUNDARY.sub("_", name).lower()


def pluralize(word: str) -> str:
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def table_name_for(cls: type[DomainModel]) -> str:
    return pluralize(snake_case(cls.__name__))


_TABLE_NAME_BY_CLASS_NAME = {cls.__name__: table_name_for(cls) for cls in PERSISTENT_MODELS}
_CLASS_BY_NAME = {cls.__name__: cls for cls in PERSISTENT_MODELS}


def _sql_type(python_type: Any) -> Any:
    origin = python_type
    # Unwrap Optional[...] (typing.Union[X, None]) to the inner type.
    args = getattr(python_type, "__args__", None)
    if args:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            origin = non_none[0]

    if origin is int:
        return Integer()
    if origin is str:
        return String()
    if origin is bool:
        return Boolean()
    if origin is Decimal:
        return Numeric(asdecimal=True)
    if origin is float:
        return Float()
    name = getattr(origin, "__name__", str(origin))
    if name in ("datetime", "AwareDatetime", "NaiveDatetime"):
        return DateTime(timezone=True)
    raise TypeError(f"No SQL type mapping for Python type {python_type!r}")


@dataclass(frozen=True, slots=True)
class MappedTable:
    model: type[DomainModel]
    table: Table
    contract: PersistenceContract


def build_metadata() -> tuple[MetaData, dict[type[DomainModel], MappedTable]]:
    metadata = MetaData()
    mapped: dict[type[DomainModel], MappedTable] = {}

    for cls in PERSISTENT_MODELS:
        contract = persistence_contract(cls)
        if not contract.persistent:
            continue

        columns: list[Column[Any]] = []
        type_hints = cls.model_fields
        for field in contract.fields:
            meta: FieldMeta = field.meta
            annotation = type_hints[field.name].annotation
            col_type = _sql_type(annotation)

            fk_arg = None
            if meta.foreign_key is not None:
                target_table = _TABLE_NAME_BY_CLASS_NAME[meta.foreign_key.target]
                fk_arg = ForeignKey(f"{target_table}.{meta.foreign_key.field}")

            args: list[Any] = [field.name, col_type]
            if fk_arg is not None:
                args.append(fk_arg)

            columns.append(
                Column(
                    *args,
                    primary_key=meta.primary_key,
                    autoincrement=meta.auto_increment if meta.primary_key else "auto",
                    nullable=meta.nullable,
                    unique=meta.unique or None,
                    index=meta.index or None,
                    default=meta.default,
                )
            )

        constraints = [
            UniqueConstraint(*names, name=f"uq_{table_name_for(cls)}_{'_'.join(names)}")
            for names in contract.unique_sets
        ]

        table = Table(table_name_for(cls), metadata, *columns, *constraints)
        mapped[cls] = MappedTable(model=cls, table=table, contract=contract)

    return metadata, mapped


METADATA, MAPPED_TABLES = build_metadata()


def table_for(cls: type[DomainModel]) -> Table:
    return MAPPED_TABLES[cls].table


def contract_for(cls: type[DomainModel]) -> PersistenceContract:
    return MAPPED_TABLES[cls].contract

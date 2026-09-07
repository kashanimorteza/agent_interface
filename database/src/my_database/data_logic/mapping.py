"""Persistence mapping of the shared Models.

Each table is derived from the installed Model class — its fields, their order,
logical types, sizes, and optionality — combined with the persistence facts that
Database owns for that Model: table name, uniqueness, composite uniqueness,
relationships, and credential at-rest modes. Every table records the Model it
implements; nothing here restates a Model definition.
"""

from __future__ import annotations

import datetime
import decimal
import types
import typing
from dataclasses import dataclass, field

import my_model
from annotated_types import MaxLen
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKeyConstraint,
    Index,
    Integer,
    MetaData,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.types import TypeDecorator

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s",
}
RELATIONSHIP_ON_DELETE = "RESTRICT"
RELATIONSHIP_ON_UPDATE = "RESTRICT"


class DecimalType(TypeDecorator):
    """A decimal stored under the Engine's NUMERIC affinity and returned as
    ``decimal.Decimal`` without the driver's float-conversion warnings."""

    impl = Numeric
    cache_ok = True

    def load_dialect_impl(self, dialect):  # noqa: ANN001
        return dialect.type_descriptor(Numeric(asdecimal=False))

    def process_bind_param(self, value, dialect):  # noqa: ANN001
        return None if value is None else str(value)

    def process_result_value(self, value, dialect):  # noqa: ANN001
        return None if value is None else decimal.Decimal(str(value))


@dataclass(frozen=True)
class Persistence:
    """The persistence facts Database owns for one Model."""

    model: type[my_model.User]
    table: str
    unique: tuple[str, ...] = ()
    composite_unique: tuple[tuple[str, ...], ...] = ()
    relationships: dict[str, type] = field(default_factory=dict)
    credentials: dict[str, str] = field(default_factory=dict)


PERSISTENCE: tuple[Persistence, ...] = (
    Persistence(my_model.User, "users", unique=("name",), credentials={"password": "hash", "api_key": "hash"}),
    Persistence(my_model.Currency, "currencies", unique=("name", "code")),
    Persistence(my_model.TradingPlatform, "trading_platforms", unique=("name",)),
    Persistence(
        my_model.Broker,
        "brokers",
        composite_unique=(("user_id", "name"),),
        relationships={"user_id": my_model.User, "trading_platform_id": my_model.TradingPlatform},
    ),
    Persistence(my_model.AccountGroup, "account_groups", unique=("name",)),
    Persistence(
        my_model.Account,
        "accounts",
        unique=("name",),
        relationships={
            "group_id": my_model.AccountGroup,
            "broker_id": my_model.Broker,
            "base_currency_id": my_model.Currency,
        },
        credentials={"password": "encrypted"},
    ),
    Persistence(my_model.Asset, "assets", unique=("name", "symbol")),
    Persistence(my_model.TrailingGroup, "trailing_groups", unique=("name",)),
    Persistence(
        my_model.TrailingRule, "trailing_rules", unique=("name",), relationships={"trailing_group_id": my_model.TrailingGroup}
    ),
    Persistence(my_model.PartialGroup, "partial_groups", unique=("name",)),
    Persistence(
        my_model.PartialRule, "partial_rules", unique=("name",), relationships={"partial_group_id": my_model.PartialGroup}
    ),
    Persistence(my_model.ActionGroup, "action_groups", unique=("name",)),
    Persistence(
        my_model.Action,
        "actions",
        unique=("name",),
        relationships={
            "action_group_id": my_model.ActionGroup,
            "asset_id": my_model.Asset,
            "account_id": my_model.Account,
            "partial_group_id": my_model.PartialGroup,
            "trailing_group_id": my_model.TrailingGroup,
        },
    ),
    Persistence(
        my_model.Position,
        "positions",
        unique=("name",),
        relationships={
            "trading_platform_id": my_model.TradingPlatform,
            "broker_id": my_model.Broker,
            "account_id": my_model.Account,
            "trailing_group_id": my_model.TrailingGroup,
            "partial_group_id": my_model.PartialGroup,
            "action_group_id": my_model.ActionGroup,
            "action_id": my_model.Action,
        },
    ),
)

PRIMARY_KEY = "id"
STATUS_FIELD = "status"
_SCALAR_TYPES = {
    int: Integer,
    str: String,
    bool: Boolean,
    decimal.Decimal: DecimalType,
    float: Float,
    datetime.datetime: DateTime,
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
_by_model: dict[type, "Mapped"] = {}
_by_table: dict[str, "Mapped"] = {}


@dataclass(frozen=True)
class Mapped:
    """A Model together with its resolved table."""

    persistence: Persistence
    table: Table

    @property
    def model(self) -> type:
        return self.persistence.model

    @property
    def fields(self) -> tuple[str, ...]:
        return tuple(self.model.model_fields)

    @property
    def credentials(self) -> dict[str, str]:
        return self.persistence.credentials

    @property
    def has_status(self) -> bool:
        return STATUS_FIELD in self.model.model_fields


def _unwrap(annotation) -> tuple[type, bool]:  # noqa: ANN001
    """The scalar type of a field annotation and whether it admits None."""
    origin = typing.get_origin(annotation)
    if origin is types.UnionType or origin is typing.Union:
        members = [a for a in typing.get_args(annotation) if a is not type(None)]
        nullable = len(members) != len(typing.get_args(annotation))
        if len(members) == 1:
            return members[0], nullable
        raise TypeError(f"unsupported field annotation {annotation!r}")
    return annotation, False


def _column_type(name: str, info) -> object:  # noqa: ANN001
    scalar, _ = _unwrap(info.annotation)
    if scalar not in _SCALAR_TYPES:
        raise TypeError(f"field {name!r} has unsupported logical type {scalar!r}")
    column_type = _SCALAR_TYPES[scalar]
    if column_type is String:
        sizes = [m.max_length for m in info.metadata if isinstance(m, MaxLen)]
        return String(sizes[0]) if sizes else String()
    return column_type()


def _build(persistence: Persistence) -> Table:
    model = persistence.model
    columns = []
    for name, info in model.model_fields.items():
        _, admits_none = _unwrap(info.annotation)
        nullable = admits_none and name != PRIMARY_KEY and name not in persistence.credentials
        columns.append(Column(name, _column_type(name, info), nullable=nullable))
    constraints = [PrimaryKeyConstraint(PRIMARY_KEY)]
    constraints += [UniqueConstraint(name) for name in persistence.unique]
    constraints += [UniqueConstraint(*combo) for combo in persistence.composite_unique]
    for field_name, target in persistence.relationships.items():
        target_table = _by_model[target].table.name
        constraints.append(
            ForeignKeyConstraint(
                [field_name],
                [f"{target_table}.{PRIMARY_KEY}"],
                ondelete=RELATIONSHIP_ON_DELETE,
                onupdate=RELATIONSHIP_ON_UPDATE,
            )
        )
    indexes = [Index(None, field_name) for field_name in persistence.relationships]
    return Table(persistence.table, metadata, *columns, *constraints, *indexes, comment=f"Model: {model.__name__}")


for _persistence in PERSISTENCE:
    _mapped = Mapped(_persistence, _build(_persistence))
    _by_model[_persistence.model] = _mapped
    _by_table[_persistence.table] = _mapped

TABLES: tuple[Mapped, ...] = tuple(_by_model.values())


def mapped(model: type) -> Mapped:
    """The mapping of a Model class; raises ``LookupError`` for anything else."""
    try:
        return _by_model[model]
    except (KeyError, TypeError):
        raise LookupError(f"{model!r} is not a persistent Model exported by my_model") from None

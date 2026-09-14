"""Traceable storage mapping from Model's published Domain Definitions to SQLAlchemy Tables
(Database Principle 10). Column types, nullability, and Field names are derived directly from
each Domain Definition's own published `model_fields` — never redeclared independently — so a
mapping cannot silently drift from the Model it maps (Database Principle 3). Only what a
Domain Definition's own fields cannot express — relationship foreign keys and Target-declared
cross-record uniqueness constraints (Database Principle 10 & 11) — is supplied here as mapping
metadata.
"""

from __future__ import annotations

import dataclasses
import datetime
import decimal
import types
import typing

import pydantic
import sqlalchemy as sa

import model as model_pkg

METADATA = sa.MetaData()


def _unwrap_annotation(annotation: object) -> tuple[object, bool]:
    """Return `(base_type, nullable)` for a Field annotation, unwrapping `Annotated[...]`
    (Model's `ExactDecimal`/`UTCDateTime`) and `X | None` (Model Preferences: `nullable_fields`)."""
    origin = typing.get_origin(annotation)
    if origin is typing.Annotated:
        base, nullable = _unwrap_annotation(typing.get_args(annotation)[0])
        return base, nullable
    if origin is types.UnionType or origin is typing.Union:
        args = typing.get_args(annotation)
        non_none = [a for a in args if a is not type(None)]
        nullable = type(None) in args
        if len(non_none) == 1:
            base, inner_nullable = _unwrap_annotation(non_none[0])
            return base, nullable or inner_nullable
        return annotation, nullable
    return annotation, False


_SA_TYPE_BY_PY_TYPE: dict[object, sa.types.TypeEngine] = {
    int: sa.Integer(),
    str: sa.String(),
    bool: sa.Boolean(),
    float: sa.Float(),
    decimal.Decimal: sa.Numeric(precision=18, scale=8),
    datetime.datetime: sa.DateTime(timezone=True),
}


@dataclasses.dataclass(frozen=True)
class ForeignKeySpec:
    field: str
    references_table: str
    references_column: str = "id"


@dataclasses.dataclass(frozen=True)
class ModelMapping:
    """Mapping metadata for one Domain Definition — everything a traceable storage mapping
    needs that the Domain Definition's own Fields cannot express (Database Principle 11)."""

    model_cls: type[pydantic.BaseModel]
    table_name: str
    foreign_keys: tuple[ForeignKeySpec, ...] = ()
    unique_together: tuple[tuple[str, ...], ...] = ()


def build_table(mapping: ModelMapping) -> sa.Table:
    """Build the SQLAlchemy Table for one Domain Definition, deriving every column from the
    Domain Definition's own published Fields (Database Principle 10)."""
    hints = typing.get_type_hints(mapping.model_cls, include_extras=True)
    fk_by_field = {fk.field: fk for fk in mapping.foreign_keys}
    columns: list[sa.Column] = []
    for name in mapping.model_cls.model_fields:
        base_type, nullable = _unwrap_annotation(hints[name])
        if base_type not in _SA_TYPE_BY_PY_TYPE:
            raise TypeError(
                f"{mapping.table_name}.{name}: no storage mapping registered for Python type "
                f"{base_type!r}"
            )
        sa_type = _SA_TYPE_BY_PY_TYPE[base_type]
        args: list[object] = [name, sa_type]
        fk = fk_by_field.get(name)
        if fk is not None:
            args.append(
                sa.ForeignKey(
                    f"{fk.references_table}.{fk.references_column}",
                    onupdate="RESTRICT",
                    ondelete="RESTRICT",
                )
            )
        columns.append(
            sa.Column(
                *args,
                primary_key=(name == "id"),
                nullable=nullable,
                index=fk is not None,
            )
        )
    constraints = [
        sa.UniqueConstraint(*combo, name=f"uq_{mapping.table_name}_{'_'.join(combo)}")
        for combo in mapping.unique_together
    ]
    return sa.Table(mapping.table_name, METADATA, *columns, *constraints)


MAPPINGS: dict[type[pydantic.BaseModel], ModelMapping] = {}


def _register(mapping: ModelMapping) -> ModelMapping:
    MAPPINGS[mapping.model_cls] = mapping
    return mapping


_register(ModelMapping(model_pkg.User, "users", unique_together=(("name",),)))

_register(ModelMapping(model_pkg.TradingPlatform, "trading_platforms"))

_register(
    ModelMapping(
        model_pkg.Broker,
        "brokers",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Instance,
        "instances",
        foreign_keys=(
            ForeignKeySpec("user_id", "users"),
            ForeignKeySpec("trading_platform_id", "trading_platforms"),
        ),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Currency,
        "currencies",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "code"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Asset,
        "assets",
        foreign_keys=(ForeignKeySpec("broker_id", "brokers"),),
        unique_together=(("broker_id", "symbol"),),
    )
)

_register(
    ModelMapping(
        model_pkg.AccountGroup,
        "account_groups",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Account,
        "accounts",
        foreign_keys=(
            ForeignKeySpec("group_id", "account_groups"),
            ForeignKeySpec("broker_id", "brokers"),
            ForeignKeySpec("instance_id", "instances"),
            ForeignKeySpec("base_currency_id", "currencies"),
        ),
        unique_together=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
    )
)

_register(
    ModelMapping(
        model_pkg.TrailingGroup,
        "trailing_groups",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.TrailingRule,
        "trailing_rules",
        foreign_keys=(ForeignKeySpec("trailing_group_id", "trailing_groups"),),
        unique_together=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
    )
)

_register(
    ModelMapping(
        model_pkg.PartialGroup,
        "partial_groups",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.PartialRule,
        "partial_rules",
        foreign_keys=(ForeignKeySpec("partial_group_id", "partial_groups"),),
        unique_together=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )
)

_register(
    ModelMapping(
        model_pkg.ActionGroup,
        "action_groups",
        foreign_keys=(ForeignKeySpec("user_id", "users"),),
        unique_together=(("user_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Action,
        "actions",
        foreign_keys=(
            ForeignKeySpec("action_group_id", "action_groups"),
            ForeignKeySpec("asset_id", "assets"),
            ForeignKeySpec("account_id", "accounts"),
            ForeignKeySpec("partial_group_id", "partial_groups"),
            ForeignKeySpec("trailing_group_id", "trailing_groups"),
        ),
        unique_together=(("action_group_id", "name"),),
    )
)

_register(
    ModelMapping(
        model_pkg.Position,
        "positions",
        foreign_keys=(
            ForeignKeySpec("user_id", "users"),
            ForeignKeySpec("trading_platform_id", "trading_platforms"),
            ForeignKeySpec("broker_id", "brokers"),
            ForeignKeySpec("account_id", "accounts"),
            ForeignKeySpec("trailing_group_id", "trailing_groups"),
            ForeignKeySpec("partial_group_id", "partial_groups"),
            ForeignKeySpec("action_group_id", "action_groups"),
            ForeignKeySpec("action_id", "actions"),
        ),
        unique_together=(("name",),),
    )
)

TABLES: dict[type[pydantic.BaseModel], sa.Table] = {
    model_cls: build_table(mapping) for model_cls, mapping in MAPPINGS.items()
}

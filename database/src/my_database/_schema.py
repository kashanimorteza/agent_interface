from __future__ import annotations

import types
import typing
from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from my_model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    DomainModel,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)

TABLE_NAMES: dict[type[DomainModel], str] = {
    User: "users",
    TradingPlatform: "trading_platforms",
    Instance: "instances",
    Currency: "currencies",
    Broker: "brokers",
    Asset: "assets",
    AccountGroup: "account_groups",
    Account: "accounts",
    TrailingGroup: "trailing_groups",
    TrailingRule: "trailing_rules",
    PartialGroup: "partial_groups",
    PartialRule: "partial_rules",
    ActionGroup: "action_groups",
    Action: "actions",
    Position: "positions",
}

MODEL_BY_NAME: dict[str, type[DomainModel]] = {cls.__name__: cls for cls in TABLE_NAMES}

_TYPE_MAP: dict[type, type[sa.types.TypeEngine]] = {
    int: sa.Integer,
    str: sa.String,
    bool: sa.Boolean,
    float: sa.Float,
    Decimal: sa.Numeric,
    datetime: sa.DateTime,
}


def _unwrap_optional(annotation: object) -> tuple[object, bool]:
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        return args[0], type(None) in typing.get_args(annotation)
    return annotation, False


def _sa_type(annotation: object) -> sa.types.TypeEngine:
    base, _ = _unwrap_optional(annotation)
    return _TYPE_MAP[base]()


def _build_table(metadata: sa.MetaData, model_cls: type[DomainModel]) -> sa.Table:
    table_name = TABLE_NAMES[model_cls]
    fk_field_targets = {
        rel.field: rel.target for rel in model_cls.relationships.values() if rel.field
    }
    columns: list[sa.Column] = []

    for field_name, field_info in model_cls.model_fields.items():
        if field_name == "id":
            columns.append(sa.Column("id", sa.Integer, primary_key=True, autoincrement=True))
            continue

        _, is_optional = _unwrap_optional(field_info.annotation)
        column_args: list = [field_name]

        if field_name in fk_field_targets:
            target_table = TABLE_NAMES[MODEL_BY_NAME[fk_field_targets[field_name]]]
            column_args.append(
                sa.ForeignKey(f"{target_table}.id", onupdate="RESTRICT", ondelete="RESTRICT")
            )
            column_type = sa.Integer()
        else:
            column_type = _sa_type(field_info.annotation)
        column_args.insert(1, column_type)

        kwargs: dict = {"nullable": is_optional}
        if field_name in fk_field_targets:
            kwargs["index"] = True
        if field_name in model_cls.unique_fields:
            kwargs["unique"] = True
        if field_info.default is not None and not field_info.is_required():
            kwargs["default"] = field_info.default

        columns.append(sa.Column(*column_args, **kwargs))

    constraints = []
    for combo in model_cls.unique_together:
        constraints.append(sa.UniqueConstraint(*combo, name=f"uq_{table_name}_{'_'.join(combo)}"))

    return sa.Table(table_name, metadata, *columns, *constraints)


metadata = sa.MetaData()
TABLES: dict[type[DomainModel], sa.Table] = {
    model_cls: _build_table(metadata, model_cls) for model_cls in TABLE_NAMES
}

"""Derive the stored structure of Entities from their published declarations."""

import re
from collections.abc import Callable, Sequence
from decimal import Decimal
from typing import Any

import sqlalchemy as sa
from model import interface
from sqlalchemy.types import TypeEngine
from sqlmodel import UTCDateTime

DecimalFactory = Callable[[int | None, int | None], TypeEngine[Any]]

UNSUPPORTED_CONSTRAINTS = ("minimum", "maximum", "pattern", "allowed_values")


def entity_classes() -> tuple[Any, ...]:
    """Return the Entity classes published through Model Interface in Target order.

    Returns:
        (tuple): The published Entity classes.
    """
    return tuple(getattr(interface, name) for name in interface.__all__)


def table_name(logical_name: str) -> str:
    """Return the stored structure name of an Entity from its logical name.

    Args:
        logical_name (str): Exact Target name of the Entity.

    Returns:
        (str): Lowercase name with words joined by underscores.
    """
    return re.sub(r"[^0-9a-z]+", "_", logical_name.lower()).strip("_")


def build_metadata(
    entities: Sequence[Any],
    decimal: DecimalFactory,
    table_kwargs: dict[str, Any] | None = None,
) -> sa.MetaData:
    """Build the stored structure of Entities from their public declarations.

    Args:
        entities (Sequence[Any]): Entity classes or objects exposing a declaration.
        decimal (DecimalFactory): Engine's stored type for decimal Fields.
        table_kwargs (dict[str, Any], optional): Engine-specific table options.

    Returns:
        (sa.MetaData): One table per Entity with its Fields, constraints, and links.
    """
    declarations = [entity.declaration for entity in entities]
    names = {d.name: table_name(d.name) for d in declarations}
    metadata = sa.MetaData()
    for declaration in declarations:
        _table(metadata, declaration, names, decimal, table_kwargs or {})
    return metadata


def _table(
    metadata: sa.MetaData,
    declaration: Any,
    names: dict[str, str],
    decimal: DecimalFactory,
    table_kwargs: dict[str, Any],
) -> sa.Table:
    name = names[declaration.name]
    columns = [_column(declaration, f, decimal) for f in declaration.fields]
    uniques = [
        sa.UniqueConstraint(*u.fields, name=f"uq_{name}_{'_'.join(u.fields)}")
        for u in declaration.unique_constraints
    ]
    links = [
        sa.ForeignKeyConstraint(
            [r.local_field],
            [f"{names[r.target_entity]}.{r.target_field}"],
            name=f"fk_{name}_{r.local_field}",
        )
        for r in declaration.relations
    ]
    indexes = [
        sa.Index(f"ix_{name}_{'_'.join(i.fields)}", *i.fields)
        for i in declaration.indexes
    ]
    return sa.Table(
        name, metadata, *columns, *uniques, *links, *indexes, **table_kwargs
    )


def _column(declaration: Any, field: Any, decimal: DecimalFactory) -> sa.Column[Any]:
    for constraint in UNSUPPORTED_CONSTRAINTS:
        if getattr(field.constraints, constraint) is not None:
            raise ValueError(
                f"{declaration.name}.{field.name}: {constraint} constraint cannot be realized in storage"
            )
    generated = (
        field.value_generation is not None
        and field.value_generation.value == "auto_increment"
    )
    return sa.Column(
        field.name,
        _type(declaration, field, decimal),
        primary_key=field.name == declaration.primary_key,
        nullable=field.nullable,
        autoincrement=generated,
        server_default=_default(declaration, field),
    )


def _type(declaration: Any, field: Any, decimal: DecimalFactory) -> TypeEngine[Any]:
    constraints = field.constraints
    match field.type.value:
        case "string":
            return sa.String(constraints.length)
        case "integer":
            return sa.Integer()
        case "boolean":
            return sa.Boolean()
        case "float":
            return sa.Float()
        case "decimal":
            return decimal(constraints.precision, constraints.scale)
        case "datetime":
            return UTCDateTime()
    raise ValueError(f"{declaration.name}.{field.name}: unknown Type {field.type}")


def _default(declaration: Any, field: Any) -> Any:
    if not field.has_default or field.default is None:
        return None
    value = field.default
    if isinstance(value, bool):
        return sa.true() if value else sa.false()
    if isinstance(value, int | float | Decimal):
        return sa.text(str(value))
    if isinstance(value, str):
        return sa.text("'" + value.replace("'", "''") + "'")
    raise ValueError(
        f"{declaration.name}.{field.name}: Default Value cannot be realized in storage"
    )

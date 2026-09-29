"""Create missing stored structure and migrate existing structure without losing records."""

from typing import Any

import sqlalchemy as sa
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from alembic.operations import Operations


def migrate(connection: sa.Connection, metadata: sa.MetaData, *, batch: bool) -> None:
    """Bring the stored structure to the declared structure by adding what is missing.

    Args:
        connection (sa.Connection): Connection inside the transaction that changes structure.
        metadata (sa.MetaData): Declared structure.
        batch (bool): Whether the Engine needs batch mode to add constraints to a table.
    """
    metadata.create_all(connection)
    context = MigrationContext.configure(
        connection, opts={"compare_type": False, "compare_server_default": False}
    )
    operations = Operations(context)
    for diff in _flatten(compare_metadata(context, metadata)):
        _apply(operations, diff, batch)


def _flatten(diffs: list[Any]) -> list[tuple[Any, ...]]:
    flat: list[tuple[Any, ...]] = []
    for diff in diffs:
        flat.extend(_flatten(diff) if isinstance(diff, list) else [diff])
    return flat


def _apply(operations: Operations, diff: tuple[Any, ...], batch: bool) -> None:
    match diff[0]:
        case "add_column":
            operations.add_column(diff[2], diff[3])
        case "add_index":
            index = diff[1]
            operations.create_index(
                index.name,
                index.table.name,
                [column.name for column in index.columns],
                unique=index.unique,
            )
        case "add_constraint":
            _add_constraint(operations, diff[1], batch)
        case "add_fk":
            _add_constraint(operations, diff[1], batch)
        case "modify_nullable":
            raise ValueError(
                f"{diff[2]}.{diff[3]}: stored nullability differs from the declaration and is not migrated"
            )


def _add_constraint(
    operations: Operations,
    constraint: sa.UniqueConstraint | sa.ForeignKeyConstraint,
    batch: bool,
) -> None:
    table = constraint.parent
    assert isinstance(table, sa.Table)
    name = str(constraint.name)
    columns = [column.name for column in constraint.columns]
    with operations.batch_alter_table(
        table.name, recreate="always" if batch else "never"
    ) as alteration:
        if isinstance(constraint, sa.ForeignKeyConstraint):
            alteration.create_foreign_key(
                name,
                constraint.referred_table.name,
                columns,
                [element.column.name for element in constraint.elements],
            )
        else:
            alteration.create_unique_constraint(name, columns)

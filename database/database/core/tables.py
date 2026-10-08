"""The Create Tables Setup Operation: the Tables of the Model Entity Collection, built from their Declarations."""

from typing import Any

from model.interface import entities

from database.core.configuration import database_instance
from database.core.data import engine_for
from database.core.errors import DeclarationMismatchError, ExecutionError, SetupError
from database.core.values import SetupResult

_FAMILIES = {
    "string": {"VARCHAR", "TEXT"},
    "integer": {"INTEGER"},
    "float": {"FLOAT", "REAL"},
    "decimal": {"VARCHAR", "TEXT"},
    "boolean": {"BOOLEAN"},
    "datetime": {"DATETIME"},
    "date": {"DATE"},
    "time": {"TIME"},
    "uuid": {"CHAR", "UUID", "VARCHAR"},
}


def _differences(entity: type, found: dict[str, Any]) -> list[str]:
    """Name what differs between an existing Table and the Declaration of its Entity."""
    declaration = entity.declaration  # ty: ignore[unresolved-attribute]
    different = []
    columns = found["columns"]
    if [column["name"] for column in columns] != [
        field.name for field in declaration.fields
    ]:
        different.append("columns")
    else:
        for column, field in zip(columns, declaration.fields, strict=True):
            size = field.constraints.size
            if (
                column["type"] not in _FAMILIES[field.type.value]
                or column["nullable"] != field.nullable
                or (size is not None and column["length"] != size)
            ):
                different.append("columns")
                break
    if found["primary_key"] != [declaration.primary_key]:
        different.append("primary key")
    tables = {item.declaration.name: item.__tablename__ for item in entities}
    expected_keys = sorted(
        (relation.local_field, tables[relation.target_entity], relation.target_field)
        for relation in declaration.relations
    )
    if found["foreign_keys"] != expected_keys:
        different.append("foreign keys")
    if found["unique"] != sorted(
        tuple(entry) for entry in declaration.unique_constraints
    ):
        different.append("uniqueness")
    if found["indexes"] != sorted(tuple(entry) for entry in declaration.indexes):
        different.append("indexes")
    return different


def create_tables(selection: Any = None) -> SetupResult:
    """Create the missing Tables of the Entity Collection; stop on any difference with an existing Table."""
    instance, engine = engine_for(selection)
    existing = engine.existing_tables()
    matching = 0
    for entity in entities:
        name = entity.__tablename__
        if name in existing:
            different = _differences(entity, engine.describe_table(name))
            if different:
                raise DeclarationMismatchError(
                    f"The Table {name} differs from the Declaration of its Entity ({', '.join(different)})."
                )
            matching += 1
    try:
        created = engine.create_tables(tuple(entities))
    except ExecutionError as error:
        raise SetupError(f"Creating the Tables did not complete: {error}") from None
    return SetupResult(
        "create_tables",
        database_instance(instance.key),
        True,
        len(entities),
        f"Created {len(created)} Tables; {matching} already matched their Entities.",
    )

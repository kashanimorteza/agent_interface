"""Core Tables: coordinates CreateTables from the Model Entity Collection."""

from typing import Any

from model.interface import entities

from database.core import data
from database.interface import DeclarationMismatchError, LifecycleResult


def _expected(connection: data.Connection, entity: type[Any]) -> dict[str, Any]:
    """Derive the structure an Entity's Declaration requires, in the Engine's own storage terms."""
    declaration = entity.declaration
    fields = data.fields_of(entity)

    def named(columns: tuple[str, ...]) -> frozenset[str]:
        return frozenset(data.physical_name(entity, column) for column in columns)

    relations = set()
    for relation in declaration.relations:
        target = next(
            item for item in entities if item.declaration.name == relation.target_entity
        )
        relations.add(
            (
                (data.physical_name(entity, relation.local_field),),
                target.__name__,
                (data.physical_name(target, relation.target_field),),
            )
        )
    types = data.route(connection, "storage_types", entity)
    return {
        "fields": {
            name: (types[name], declared.nullable) for name, declared in fields.items()
        },
        "primary_key": (data.physical_name(entity, declaration.primary_key),),
        "relations": frozenset(relations),
        "unique_constraints": frozenset(
            named(item) for item in declaration.unique_constraints
        ),
        "indexes": frozenset(named(item) for item in declaration.indexes),
    }


def _differences(expected: dict[str, Any], stored: dict[str, Any]) -> list[str]:
    problems = []
    for name in sorted(set(expected["fields"]) - set(stored["fields"])):
        problems.append(f"Field {name} is missing")
    for name in sorted(set(stored["fields"]) - set(expected["fields"])):
        problems.append(f"Field {name} is not declared")
    for name in sorted(set(expected["fields"]) & set(stored["fields"])):
        if expected["fields"][name] != stored["fields"][name]:
            problems.append(f"Field {name} has another type or nullability")
    for member, wording in (
        ("primary_key", "the primary key differs"),
        ("relations", "the relations differ"),
        ("unique_constraints", "the uniqueness constraints differ"),
        ("indexes", "the indexes differ"),
    ):
        if expected[member] != stored[member]:
            problems.append(wording)
    return problems


def create_tables(instance: Any) -> LifecycleResult:
    """Create the Table of every Model Entity on the selected Instance, stopping before any change when an existing Table differs."""
    connection = data.connection_for(instance)
    differing = []
    for entity in entities:
        stored = data.route(connection, "describe_table", entity)
        if stored is None:
            continue
        problems = _differences(_expected(connection, entity), stored)
        if problems:
            differing.append(f"{entity.__name__} ({'; '.join(problems)})")
    if differing:
        raise DeclarationMismatchError(
            f"CreateTables on Instance {connection.name!r} stopped and changed nothing: "
            "existing Tables differ from their Entity: " + ", ".join(differing) + "."
        )
    data.route(connection, "create_tables", tuple(entities))
    return LifecycleResult(
        command="create_tables",
        instance=data.instance_member(connection.key),
        success=True,
        affected=len(entities),
        message=f"{len(entities)} Table(s) are ready.",
    )

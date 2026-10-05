from typing import Any, cast

from model.interface import entities

from database.core.data import (
    DeclarationMismatchError,
    ExecutionError,
    LifecycleError,
    LifecycleResult,
    report_failure,
    run,
    select_instance,
)


def _differences(entity: Any, described: dict[str, Any], unit: Any) -> list[str]:
    declaration = entity.declaration
    expected_columns = [(item.name, unit.declared_family(item.type), item.nullable) for item in declaration.fields]
    targets = {other.declaration.name: other.__table__.name for other in cast(tuple[Any, ...], entities)}
    expected = {
        "columns": expected_columns,
        "primary_key": [declaration.primary_key],
        "unique": {tuple(item) for item in declaration.unique_constraints},
        "foreign_keys": {
            (item.local_field, targets[item.target_entity], item.target_field) for item in declaration.relations
        },
        "indexes": {tuple(item) for item in declaration.indexes},
    }
    return [aspect for aspect, wanted in expected.items() if described[aspect] != wanted]


def create_tables(instance: object = None) -> LifecycleResult:
    return report_failure("create_tables", instance, lambda: _create_tables(instance))


def _create_tables(instance: object) -> LifecycleResult:
    member = select_instance(instance).member
    models = list(cast(tuple[Any, ...], entities))
    tables = [entity.__table__ for entity in models]

    def work(unit: Any, cx: Any) -> list[str]:
        existing = unit.describe_tables(cx, [table.name for table in tables])
        problems = [
            f"{entity.declaration.name} (differs in {', '.join(differences)})"
            for entity in models
            if entity.__table__.name in existing
            if (differences := _differences(entity, existing[entity.__table__.name], unit))
        ]
        if problems:
            raise DeclarationMismatchError(
                f"An existing Table differs from its Entity Declaration: {'; '.join(problems)}"
            )
        return unit.create_tables(cx, tables)

    names = [table.name for table in tables]
    before = run(instance, lambda unit, cx: set(unit.describe_tables(cx, names)))
    try:
        created = run(instance, work)
    except ExecutionError as error:
        after = run(instance, lambda unit, cx: set(unit.describe_tables(cx, names)))
        if after - before:
            raise LifecycleError(
                f"CreateTables stopped part way and left an incomplete schema: {len(after - before)} Tables were created. {error}"
            ) from None
        raise
    message = f"Created {len(created)} of {len(tables)} Tables; {len(tables) - len(created)} already matched"
    return LifecycleResult("create_tables", member, True, len(created), message)

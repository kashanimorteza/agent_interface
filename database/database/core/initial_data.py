import json
from typing import Any, cast

from model.interface import entities

from database.core import tables
from database.core.data import (
    SETTINGS,
    ExecutionError,
    InvalidInputError,
    LifecycleResult,
    entity_values,
    materialize,
    report_failure,
    run,
    select_instance,
)


def _records() -> list[tuple[Any, tuple[str, ...], str]]:
    models = cast(tuple[Any, ...], entities)
    built = []
    for group in SETTINGS.initial_data:
        entity = next((model for model in models if model.declaration.name == group["entity"]), None)
        if entity is None:
            raise InvalidInputError(f"Initial Data names an Entity that Model does not publish: {group['entity']}")
        for position, record in enumerate(group["records"], start=1):
            try:
                built.append(
                    (entity.from_json(json.dumps(record)), tuple(record), f"{group['entity']} record {position}")
                )
            except ValueError:
                raise InvalidInputError(
                    f"Initial Data record {position} of {group['entity']} does not satisfy its Entity contract"
                ) from None
    return built


def insert_initial_data(instance: object = None) -> LifecycleResult:
    return report_failure("insert_initial_data", instance, lambda: _insert_initial_data(instance))


def _insert_initial_data(instance: object) -> LifecycleResult:
    member = select_instance(instance).member
    records = _records()

    def work(unit: Any, cx: Any) -> tuple[int, int]:
        inserted = skipped = 0
        for record, supplied, label in records:
            model = type(record)
            values = entity_values(record)
            present = None
            for key in model.declaration.unique_constraints:
                if all(name in supplied for name in key):
                    present = unit.find(cx, model, {name: values[name] for name in key})
                    if present is not None:
                        break
            if present is None:
                materialize(model, unit.add(cx, model, values))
                inserted += 1
                continue
            differing = [name for name in supplied if present[name] != values[name]]
            if differing:
                raise ExecutionError(
                    f"Initial Data conflicts with an existing record: {label} differs in {', '.join(differing)}"
                )
            skipped += 1
        return inserted, skipped

    inserted, skipped = run(instance, work)
    message = f"Inserted {inserted} of {len(records)} Initial Data records; {skipped} already present"
    return LifecycleResult("insert_initial_data", member, True, inserted, message)


def prepare(instance: object = None) -> LifecycleResult:
    return report_failure("prepare", instance, lambda: _prepare(instance))


def _prepare(instance: object) -> LifecycleResult:
    created = tables.create_tables(instance)
    seeded = insert_initial_data(instance)
    return LifecycleResult(
        "prepare",
        created.instance,
        True,
        (created.affected or 0) + (seeded.affected or 0),
        f"{created.message}. {seeded.message}",
    )

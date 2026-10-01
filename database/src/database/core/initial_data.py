"""Core Initial Data: coordinates InsertInitialData from the shared collection."""

import json
from typing import Any

from database.core import data, tables
from database.interface import (
    ConfigurationError,
    DatabaseError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    LifecycleError,
    LifecycleResult,
)


def _collected() -> list[Any]:
    """Build every collected record through its Entity's own reconstruction, in collection order."""
    built = []
    for entity, records in data.configuration().initial_data:
        for index, record in enumerate(records, start=1):
            try:
                built.append(
                    entity.from_json(json.dumps(dict(record), allow_nan=False))
                )
            except TypeError, ValueError:
                raise ConfigurationError(
                    f"Initial Data record {index} of {entity.__name__} is not accepted by its Entity."
                ) from None
    return built


def _lookups(entity: Any) -> list[list[Filter]]:
    """Return the Filter sets that find a stored record with the same identity as the collected one.

    A record is identified by each Uniqueness Constraint whose Fields it fills; an Entity that declares
    none is identified by all of its Fields that storage does not generate.
    """
    kind = type(entity)
    fields = data.fields_of(kind)
    if kind.declaration.unique_constraints:
        groups = [
            [data.physical_name(kind, column) for column in constraint]
            for constraint in kind.declaration.unique_constraints
        ]
    else:
        groups = [
            [
                name
                for name, declared in fields.items()
                if declared.value_generation is None
            ]
        ]
    lookups = []
    for names in groups:
        values = [getattr(entity, name) for name in names]
        if (
            all(value is not None for value in values)
            or not kind.declaration.unique_constraints
        ):
            lookups.append(
                [
                    Filter(getattr(kind, name), FilterOperator.IS_NULL)
                    if value is None
                    else Filter(getattr(kind, name), FilterOperator.EQUALS, value)
                    for name, value in zip(names, values, strict=True)
                ]
            )
    return lookups


def _present(connection: data.Connection, entity: Any) -> bool:
    """Whether an identical record is stored; a stored record with the same identity but other values is a conflict."""
    kind = type(entity)
    fields = data.fields_of(kind)
    found = False
    for lookup in _lookups(entity):
        query = data.Query(tuple(lookup), FilterCombination.AND, (), -1)
        for row in data.route(connection, "list_records", kind, query):
            identical = all(
                getattr(entity, name) == row[name]
                for name, declared in fields.items()
                if declared.value_generation is None
            )
            if not identical:
                raise LifecycleError(
                    f"InsertInitialData on Instance {connection.name!r} stopped and inserted nothing: "
                    f"a stored {kind.__name__} record conflicts with the Initial Data."
                )
            found = True
    return found


def insert_initial_data(instance: Any) -> LifecycleResult:
    """Insert every missing Initial Data record on the selected Instance, skipping identical ones and failing on a conflict."""
    records = _collected()
    connection = data.connection_for(instance)
    missing = [record for record in records if not _present(connection, record)]
    if missing:
        try:
            data.route(connection, "insert_many", missing)
        except ExecutionError as error:
            raise LifecycleError(
                f"InsertInitialData on Instance {connection.name!r} stopped and inserted nothing: {error}"
            ) from None
    return LifecycleResult(
        command="insert_initial_data",
        instance=data.instance_member(connection.key),
        success=True,
        affected=len(records),
        message=(
            f"{len(missing)} Initial Data record(s) were inserted and "
            f"{len(records) - len(missing)} already present were skipped."
        ),
    )


def prepare(instance: Any) -> LifecycleResult:
    """Run CreateTables and then InsertInitialData on the selected Instance; stop when CreateTables fails."""
    where = f"Prepare on Instance {data.connection_for(instance).name!r}"
    try:
        created = tables.create_tables(instance)
    except DatabaseError as error:
        raise type(error)(f"{where} stopped: {error}") from None
    try:
        inserted = insert_initial_data(instance)
    except DatabaseError as error:
        raise LifecycleError(
            f"{where} is incomplete: the Tables exist but Initial Data was not inserted. {error}"
        ) from None
    return LifecycleResult(
        command="prepare",
        instance=created.instance,
        success=True,
        affected=(created.affected or 0) + (inserted.affected or 0),
        message=f"{created.message} {inserted.message}",
    )

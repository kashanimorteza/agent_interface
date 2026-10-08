"""The shared routing of every public request: validate, resolve, forward to the Engine unit, materialize, normalize."""

import importlib
from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy.orm.attributes import set_committed_value

from database.core import query
from database.core.configuration import (
    CONFIGURATION,
    InstanceConfiguration,
    connection_for,
    database_instance,
    resolve_instance,
)
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    ExecutionError,
    InvalidInputError,
)
from database.core.values import CommandResult

_engines: dict[str, Any] = {}


def engine_for(selection: Any) -> tuple[InstanceConfiguration, Any]:
    """Resolve the selected Instance and return it with the Engine unit that serves it."""
    instance = resolve_instance(selection)
    if instance.key not in _engines:
        try:
            unit = importlib.import_module(f"database.engine.{instance.engine}")
        except ModuleNotFoundError:
            raise ConfigurationError(
                "The Engine of the selected Instance has no unit."
            ) from None
        _engines[instance.key] = unit.Engine(connection_for(instance))
    return instance, _engines[instance.key]


def _generated(entity: type) -> tuple[str, ...]:
    return tuple(
        field.name
        for field in entity.declaration.fields  # ty: ignore[unresolved-attribute]
        if field.value_generation is not None
        and field.value_generation.value == "auto_increment"
    )


def materialize(entity: type, row: Mapping[str, Any]) -> Any:
    """Build an Entity from a stored row through the Entity's own construction, keeping the stored identity."""
    pending = _generated(entity)
    try:
        values = {
            field.name: row[field.name]
            for field in entity.declaration.fields  # ty: ignore[unresolved-attribute]
            if field.name not in pending
        }
        built = entity(**values)
        for name in pending:
            set_committed_value(built, name, row[name])
    except KeyError, ValueError, TypeError:
        raise DeclarationMismatchError(
            "A stored row does not satisfy the contract of its Entity."
        ) from None
    return built


def _values(item: Any, mutable_only: bool) -> dict[str, Any]:
    return {
        field.name: getattr(item, field.name)
        for field in type(item).declaration.fields
        if field.value_generation is None and not (mutable_only and field.immutable)
    }


def _optional(row: Mapping[str, Any] | None, entity: type) -> Any:
    return None if row is None else materialize(entity, row)


class Data:
    """Routes every Entity Operation and Command Operation."""

    def add(self, entity: Any, instance: Any = None) -> Any:
        item = query.check_entity_instance(entity)
        if any(getattr(item, name) is not None for name in _generated(type(item))):
            raise InvalidInputError(
                "An Entity to add is new: its generated Fields are still pending."
            )
        _, engine = engine_for(instance)
        return materialize(
            type(item), engine.add(type(item), _values(item, mutable_only=False))
        )

    def update(self, entity: Any, instance: Any = None) -> Any:
        item = query.check_entity_instance(entity)
        key = query.check_id(item.id)
        _, engine = engine_for(instance)
        return _optional(
            engine.update(type(item), key, _values(item, mutable_only=True)), type(item)
        )

    def list(
        self,
        entity: Any,
        filters: Any = None,
        combination: Any = None,
        orders: Any = None,
        limit: Any = None,
        instance: Any = None,
    ) -> Sequence[Any]:
        cls = query.check_entity_class(entity)
        settings = CONFIGURATION.settings
        checked = query.check_filters(cls, filters)
        joined = query.check_combination(combination, settings.filter_combination)
        ordered = query.check_orders(
            cls, orders, settings.default_order_field, settings.default_order_direction
        )
        bound = query.check_limit(limit, settings.default_limit)
        _, engine = engine_for(instance)
        return [
            materialize(cls, row)
            for row in engine.list(cls, checked, joined, ordered, bound)
        ]

    def get_by_id(self, entity: Any, id: Any, instance: Any = None) -> Any:
        cls = query.check_entity_class(entity)
        key = query.check_id(id)
        _, engine = engine_for(instance)
        return _optional(engine.get(cls, key), cls)

    def delete(self, entity: Any, id: Any, instance: Any = None) -> Any:
        cls = query.check_entity_class(entity)
        key = query.check_id(id)
        _, engine = engine_for(instance)
        return _optional(engine.delete(cls, key), cls)

    def _set_active(self, entity: Any, id: Any, active: bool, instance: Any) -> Any:
        cls = query.check_entity_class(entity)
        key = query.check_id(id)
        _, engine = engine_for(instance)
        return _optional(engine.set_active(cls, key, active), cls)

    def enable(self, entity: Any, id: Any, instance: Any = None) -> Any:
        return self._set_active(entity, id, True, instance)

    def disable(self, entity: Any, id: Any, instance: Any = None) -> Any:
        return self._set_active(entity, id, False, instance)

    def count(
        self,
        entity: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> int:
        cls = query.check_entity_class(entity)
        checked = query.check_filters(cls, filters)
        joined = query.check_combination(
            combination, CONFIGURATION.settings.filter_combination
        )
        _, engine = engine_for(instance)
        return engine.count(cls, checked, joined)

    def _aggregate(
        self,
        operation: str,
        entity: Any,
        field: Any,
        filters: Any,
        combination: Any,
        instance: Any,
    ) -> Any:
        cls = query.check_entity_class(entity)
        name, field_type = query.check_aggregate_field(cls, field, operation)
        checked = query.check_filters(cls, filters)
        joined = query.check_combination(
            combination, CONFIGURATION.settings.filter_combination
        )
        _, engine = engine_for(instance)
        if operation == "sum":
            return engine.total(cls, name, field_type, checked, joined)
        return engine.extreme(
            cls, name, field_type, operation == "max", checked, joined
        )

    def sum(
        self,
        entity: Any,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        return self._aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        return self._aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        return self._aggregate("max", entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: Any = None) -> int:
        cls = query.check_entity_class(entity)
        _, engine = engine_for(instance)
        return engine.truncate(cls)

    def execute_command(
        self, command: Any, parameters: Any = None, instance: Any = None
    ) -> CommandResult:
        if not isinstance(command, str) or not command.strip():
            raise InvalidInputError(
                "A command is a non-empty text in the Engine's query language."
            )
        if parameters is not None and (
            isinstance(parameters, str | bytes)
            or not isinstance(parameters, Mapping | Sequence)
        ):
            raise InvalidInputError("Command parameters are a mapping or a sequence.")
        selected, engine = engine_for(instance)
        member = database_instance(selected.key)
        try:
            bound = (
                dict(parameters)
                if isinstance(parameters, Mapping)
                else parameters and tuple(parameters)
            )
            raw = engine.execute(command, bound or None)
        except ExecutionError as error:
            return CommandResult(None, None, None, False, str(error), member)
        rows = None if raw["rows"] is None else tuple(raw["rows"])
        affected = (
            raw["affected"]
            if raw["affected"] is not None and raw["affected"] >= 0
            else None
        )
        columns = None if raw["columns"] is None else tuple(raw["columns"])
        return CommandResult(
            rows, affected, columns, True, "The command completed.", member
        )

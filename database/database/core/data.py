"""Core Data: shared validation, default resolution, Instance selection, routing, and normalization.

Core holds no driver call and no Instance-specific storage behaviour; every Engine unit receives the
same checked request and returns raw results.
"""

import importlib
from collections.abc import Mapping, Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from model.interface import entities as _model_entities
from pydantic import ValidationError
from sqlalchemy.orm.attributes import InstrumentedAttribute, set_committed_value

from database.core.configuration import (
    Configuration,
    InstanceConfig,
    connection_for,
    load_configuration,
)
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.query import Condition, Sorting
from database.core.values import (
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
)

_TEXT_OPERATORS = {
    FilterOperator.CONTAINS,
    FilterOperator.STARTS_WITH,
    FilterOperator.ENDS_WITH,
}
_RANGE_OPERATORS = {
    FilterOperator.GREATER_THAN,
    FilterOperator.GREATER_OR_EQUAL,
    FilterOperator.LESS_THAN,
    FilterOperator.LESS_OR_EQUAL,
}
_NULL_OPERATORS = {FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL}
_COMPARABLE = {"integer", "float", "decimal", "string", "datetime", "date", "time"}
_AUTO_INCREMENT = "auto_increment"


def normalize_value(type_name: str, value: Any, where: str) -> Any:
    """Return a value in the form of a declared Type, or refuse a value that is not compatible."""
    ok: bool
    match type_name:
        case "string":
            ok = isinstance(value, str)
        case "integer":
            ok = isinstance(value, int) and not isinstance(value, bool)
        case "float":
            ok = isinstance(value, int | float) and not isinstance(value, bool)
            value = float(value) if ok else value
        case "decimal":
            ok = isinstance(value, Decimal | int) and not isinstance(value, bool)
            value = Decimal(value) if ok else value
        case "boolean":
            ok = isinstance(value, bool)
        case "datetime":
            ok = isinstance(value, datetime) and value.tzinfo is not None
        case "date":
            ok = isinstance(value, date) and not isinstance(value, datetime)
        case "time":
            ok = isinstance(value, time)
        case "uuid":
            ok = isinstance(value, UUID)
        case _:
            ok = False
    if not ok:
        raise InvalidInputError(f"{where}: the value is not compatible with a {type_name} Field")
    return value


class Data:
    """Core Data: one per Database; it reads the configuration when first needed."""

    def __init__(self) -> None:
        self._configuration: Configuration | None = None
        self._engines: dict[str, Any] = {}

    # ------------------------------------------------------------ configuration and Instance
    @property
    def configuration(self) -> Configuration:
        if self._configuration is None:
            self._configuration = load_configuration()
        return self._configuration

    def instance(self, selected: DatabaseInstance | None) -> InstanceConfig:
        """Resolve the selected DatabaseInstance, or the default, before any storage is touched."""
        configuration = self.configuration
        if selected is None:
            return configuration.instances[configuration.settings.default_instance]
        if not isinstance(selected, DatabaseInstance):
            raise ConfigurationError("The Instance must be a DatabaseInstance member")
        for instance in configuration.instances.values():
            if instance.member == selected.name:
                if not instance.active:
                    raise InactiveInstanceError(f"The Instance {instance.key} is not active")
                return instance
        raise ConfigurationError("The selected Instance is not configured")

    # ------------------------------------------------------------ Entity and Field inputs
    @staticmethod
    def entity_class(entity: Any, *, instance: bool) -> Any:
        """Check that an Entity argument is an Entity of Model: an instance, or a class."""
        is_class = isinstance(entity, type)
        entity_cls = entity if is_class else type(entity)
        if entity_cls not in _model_entities:
            raise InvalidInputError("The Entity must be an Entity imported from Model")
        if instance and is_class:
            raise InvalidInputError(
                f"{entity_cls.declaration.name} needs an Entity instance, not the class"
            )
        if not instance and not is_class:
            raise InvalidInputError(
                f"{entity_cls.declaration.name} needs the Entity class, not an instance"
            )
        return entity_cls

    @staticmethod
    def field(entity_cls: Any, reference: Any) -> Any:
        """Check a Field reference of the Entity and return its Declaration."""
        if not isinstance(reference, InstrumentedAttribute) or reference.class_ is not entity_cls:
            raise InvalidInputError(
                f"A Field must be a Field reference of {entity_cls.declaration.name}, "
                "not a name or a Field of another Entity"
            )
        for declared in entity_cls.declaration.fields:
            if declared.name == reference.key:
                return declared
        raise InvalidInputError(f"{reference.key} is not a Field of {entity_cls.declaration.name}")

    def conditions(
        self, entity_cls: Any, filters: Sequence[Filter] | None
    ) -> tuple[Condition, ...]:
        """Check every Filter against the Entity before any Instance is accessed."""
        if filters is None:
            return ()
        if isinstance(filters, str | Filter) or not isinstance(filters, Sequence):
            raise InvalidInputError("Filters must be a list of Filter values")
        checked = []
        for item in filters:
            if not isinstance(item, Filter):
                raise InvalidInputError("Every filter must be a Filter value")
            declared = self.field(entity_cls, item.field)
            type_name = declared.type.value
            where = f"{entity_cls.declaration.name}.{declared.name}"
            operator = item.operator
            if operator in _TEXT_OPERATORS and type_name != "string":
                raise InvalidInputError(f"{where}: {operator.name} needs a textual Field")
            if operator in _RANGE_OPERATORS and type_name not in _COMPARABLE:
                raise InvalidInputError(f"{where}: {operator.name} needs a comparable Field")
            if operator in _NULL_OPERATORS:
                value = None
            elif operator is FilterOperator.IN:
                if not item.value:
                    raise InvalidInputError(f"{where}: IN needs at least one value")
                value = tuple(normalize_value(type_name, each, where) for each in item.value)
            else:
                value = normalize_value(type_name, item.value, where)
            checked.append(Condition(declared.name, type_name, operator, value))
        return tuple(checked)

    def sortings(self, entity_cls: Any, orders: Sequence[Order]) -> tuple[Sorting, ...]:
        checked = []
        for item in orders:
            if not isinstance(item, Order):
                raise InvalidInputError("Every order must be an Order value")
            declared = self.field(entity_cls, item.field)
            descending = item.direction.name == "DESCENDING"
            checked.append(Sorting(declared.name, declared.type.value, descending))
        return tuple(checked)

    # ------------------------------------------------------------ query defaults
    def combination(self, combination: FilterCombination | None) -> FilterCombination:
        if combination is None:
            return self.configuration.settings.query.filter_combination
        if not isinstance(combination, FilterCombination):
            raise InvalidInputError("The combination must be a FilterCombination member")
        return combination

    def query(
        self,
        entity_cls: Any,
        combination: FilterCombination | None,
        orders: Sequence[Order] | None,
        limit: int | None,
    ) -> tuple[FilterCombination, tuple[Sorting, ...], int | None]:
        """Resolve an omitted combination, Order set, and limit from the configuration."""
        query = self.configuration.settings.query
        if orders is None:
            default = query.default_order
            declared = {f.name: f for f in entity_cls.declaration.fields}.get(default.field)
            if declared is None:
                raise ConfigurationError("The default order names a Field the Entity does not have")
            sortings = (
                Sorting(declared.name, declared.type.value, default.direction.name == "DESCENDING"),
            )
        else:
            if isinstance(orders, str | Order) or not isinstance(orders, Sequence):
                raise InvalidInputError("Orders must be a list of Order values")
            sortings = self.sortings(entity_cls, orders)
        if limit is None:
            limit = query.default_limit
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise InvalidInputError("The limit must be a whole number")
        return self.combination(combination), sortings, (limit if limit > 0 else None)

    # ------------------------------------------------------------ rows to Entities
    @staticmethod
    def materialize(entity_cls: Any, row: Mapping[str, Any]) -> Any:
        """Build an Entity from a stored row through the Entity's own construction.

        The Entity refuses a supplied value for a field storage generates, so that identity is
        applied afterwards, the way storage itself assigns it. A row that does not satisfy the
        Entity contract is an error and is never repaired.
        """
        declaration = entity_cls.declaration
        missing = [f.name for f in declaration.fields if f.name not in row]
        if missing:
            raise DeclarationMismatchError(
                f"A stored {declaration.name} row lacks: {', '.join(missing)}"
            )
        generated = [
            f
            for f in declaration.fields
            if f.value_generation is not None and f.value_generation.value == _AUTO_INCREMENT
        ]
        names = {f.name for f in generated}
        values = {f.name: row[f.name] for f in declaration.fields if f.name not in names}
        try:
            entity = entity_cls(**values)
        except ValidationError as error:
            fields = sorted(
                {str(item["loc"][0]) for item in error.errors(include_input=False) if item["loc"]}
            )
            raise DeclarationMismatchError(
                f"A stored {declaration.name} row breaks the Entity contract in: "
                f"{', '.join(fields)}"
            ) from None
        except ValueError, TypeError:
            raise DeclarationMismatchError(
                f"A stored {declaration.name} row breaks the Entity contract"
            ) from None
        for field in generated:
            identity = row[field.name]
            if isinstance(identity, bool) or not isinstance(identity, int):
                raise DeclarationMismatchError(
                    f"A stored {declaration.name} row has an invalid {field.name}"
                )
            set_committed_value(entity, field.name, identity)
        return entity

    # ------------------------------------------------------------ routing
    def engine(self, instance: InstanceConfig) -> Any:
        """Return the Engine unit of the Instance's Engine, one per Instance connection."""
        cached = self._engines.get(instance.key)
        if cached is None:
            try:
                unit = importlib.import_module(f"database.engine.{instance.engine}")
            except ModuleNotFoundError:
                raise ConfigurationError(
                    f"No Engine unit exists for the Engine of Instance {instance.key}"
                ) from None
            cached = unit.Engine(connection_for(self.configuration, instance.key))
            self._engines[instance.key] = cached
        return cached

    def _route(self, instance: DatabaseInstance | None) -> Any:
        return self.engine(self.instance(instance))

    @staticmethod
    def _identity_name(entity_cls: Any) -> str:
        return entity_cls.declaration.primary_key

    def _identity(self, entity_cls: Any, identity: Any) -> Any:
        declared = {f.name: f for f in entity_cls.declaration.fields}[
            self._identity_name(entity_cls)
        ]
        return normalize_value(declared.type.value, identity, f"{entity_cls.declaration.name}.id")

    def _rows(self, entity_cls: Any, rows: Sequence[Mapping[str, Any]]) -> list[Any]:
        return [self.materialize(entity_cls, row) for row in rows]

    def _one(self, entity_cls: Any, row: Mapping[str, Any] | None) -> Any:
        """A missing record is null, never an error."""
        return None if row is None else self.materialize(entity_cls, row)

    @staticmethod
    def _generated(entity_cls: Any) -> set[str]:
        return {
            f.name
            for f in entity_cls.declaration.fields
            if f.value_generation is not None and f.value_generation.value == _AUTO_INCREMENT
        }

    def add(self, entity: Any, instance: DatabaseInstance | None) -> Any:
        entity_cls = self.entity_class(entity, instance=True)
        generated = self._generated(entity_cls)
        if any(getattr(entity, name) is not None for name in generated):
            raise InvalidInputError(
                f"Add needs a new {entity_cls.declaration.name}; it is already stored"
            )
        engine = self._route(instance)
        values = {
            f.name: getattr(entity, f.name)
            for f in entity_cls.declaration.fields
            if f.name not in generated
        }
        return self._one(entity_cls, engine.add(entity_cls, values))

    def update(self, entity: Any, instance: DatabaseInstance | None) -> Any:
        entity_cls = self.entity_class(entity, instance=True)
        identity = getattr(entity, self._identity_name(entity_cls))
        if identity is None:
            raise InvalidInputError(
                f"Update needs a stored {entity_cls.declaration.name}; it has no id yet"
            )
        engine = self._route(instance)
        values = {
            f.name: getattr(entity, f.name)
            for f in entity_cls.declaration.fields
            if not f.immutable and f.name not in self._generated(entity_cls)
        }
        return self._one(entity_cls, engine.update(entity_cls, identity, values))

    def read(
        self,
        entity: Any,
        filters: Sequence[Filter] | None,
        combination: FilterCombination | None,
        orders: Sequence[Order] | None,
        limit: int | None,
        instance: DatabaseInstance | None,
    ) -> list[Any]:
        entity_cls = self.entity_class(entity, instance=False)
        conditions = self.conditions(entity_cls, filters)
        resolved, sortings, resolved_limit = self.query(entity_cls, combination, orders, limit)
        engine = self._route(instance)
        return self._rows(
            entity_cls, engine.list(entity_cls, conditions, resolved, sortings, resolved_limit)
        )

    def get_by_id(self, entity: Any, identity: Any, instance: DatabaseInstance | None) -> Any:
        entity_cls = self.entity_class(entity, instance=False)
        identity = self._identity(entity_cls, identity)
        return self._one(entity_cls, self._route(instance).get_by_id(entity_cls, identity))

    def delete(self, entity: Any, identity: Any, instance: DatabaseInstance | None) -> Any:
        entity_cls = self.entity_class(entity, instance=False)
        identity = self._identity(entity_cls, identity)
        return self._one(entity_cls, self._route(instance).delete(entity_cls, identity))

    def set_active(
        self, entity: Any, identity: Any, active: bool, instance: DatabaseInstance | None
    ) -> Any:
        entity_cls = self.entity_class(entity, instance=False)
        identity = self._identity(entity_cls, identity)
        return self._one(entity_cls, self._route(instance).set_active(entity_cls, identity, active))

    def count(
        self,
        entity: Any,
        filters: Sequence[Filter] | None,
        combination: FilterCombination | None,
        instance: DatabaseInstance | None,
    ) -> int:
        entity_cls = self.entity_class(entity, instance=False)
        conditions = self.conditions(entity_cls, filters)
        resolved = self.combination(combination)
        return self._route(instance).count(entity_cls, conditions, resolved)

    def aggregate(
        self,
        kind: str,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None,
        combination: FilterCombination | None,
        instance: DatabaseInstance | None,
    ) -> Any:
        entity_cls = self.entity_class(entity, instance=False)
        declared = self.field(entity_cls, field)
        type_name = declared.type.value
        allowed = {"integer", "float", "decimal"} if kind == "sum" else _COMPARABLE
        if type_name not in allowed:
            what = "numeric" if kind == "sum" else "comparable"
            raise InvalidInputError(f"{kind} needs a {what} Field; {declared.name} is not")
        conditions = self.conditions(entity_cls, filters)
        resolved = self.combination(combination)
        engine = self._route(instance)
        return engine.aggregate(entity_cls, kind, declared.name, type_name, conditions, resolved)

    def truncate(self, entity: Any, instance: DatabaseInstance | None) -> int:
        entity_cls = self.entity_class(entity, instance=False)
        return self._route(instance).truncate(entity_cls)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None,
        instance: DatabaseInstance | None,
    ) -> CommandResult:
        if not isinstance(command, str) or not command.strip():
            raise InvalidInputError("A command must be non-empty text")
        if parameters is not None and (
            isinstance(parameters, str | bytes) or not isinstance(parameters, Mapping | Sequence)
        ):
            raise InvalidInputError("Command parameters must be a mapping or a sequence")
        selected = self.instance(instance)
        raw = self.engine(selected).execute_command(command, parameters)
        return CommandResult(
            rows=raw["rows"],
            affected=raw["affected"],
            columns=raw["columns"],
            success=True,
            message=raw["message"],
            instance=DatabaseInstance[selected.member],
        )

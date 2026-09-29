"""Shared form of every Database Operation: validation, routing, and result handling."""

from collections.abc import Mapping, Sequence
from importlib import import_module
from typing import Any

from database.core import initial_data, statements, structure, tables
from database.core.config import Configuration, load_configuration
from database.core.vocabulary import (
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    Order,
)


class Data:
    """Resolve the requested Instance, forward each Operation, and return its result."""

    def __init__(self, configuration: Configuration | None = None) -> None:
        self.configuration = configuration or load_configuration()
        self.entities = structure.entity_classes()
        self._implementations: dict[DatabaseInstance, Any] = {}

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a complete Entity instance and return it with generated values."""
        entity_class = self._entity_instance(entity)
        row = self._implementation(instance).add(
            entity_class, statements.values_of(entity)
        )
        return entity_class(**row)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace every mutable Field of the record with the Entity's identity."""
        entity_class = self._entity_instance(entity)
        values = statements.values_of(entity)
        if values.get(entity_class.declaration.primary_key) is None:
            raise ValueError("Update requires an Entity instance that has an id")
        row = self._implementation(instance).update(entity_class, values)
        return None if row is None else entity_class(**row)

    def list(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return matching Entity instances in the requested order."""
        entity_class = self._entity_class(entity)
        defaults = self.configuration.query_defaults
        chosen_filters, chosen_combination = self._selection(
            entity_class, filters, combination
        )
        chosen_orders = list(orders) if orders else [defaults.order]
        for order in chosen_orders:
            self._check_order(entity_class, order)
        rows = self._implementation(instance).select(
            entity_class,
            chosen_filters,
            chosen_combination,
            chosen_orders,
            defaults.limit if limit is None else self._limit(limit),
        )
        return [entity_class(**row) for row in rows]

    def delete(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> bool:
        """Delete a record and report whether one existed."""
        entity_class = self._entity_class(entity)
        identity = self._identity(record_id)
        return self._implementation(instance).delete(entity_class, identity)

    def enable(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Set a record active and return it, or None when no record has the id."""
        return self._set_active(entity, record_id, True, instance)

    def disable(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Set a record inactive and return it, or None when no record has the id."""
        return self._set_active(entity, record_id, False, instance)

    def get_by_id(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Return the record with the id as an Entity instance, or None."""
        entity_class = self._entity_class(entity)
        identity = self._identity(record_id)
        row = self._implementation(instance).get(entity_class, identity)
        return None if row is None else entity_class(**row)

    def count(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        entity_class = self._entity_class(entity)
        chosen_filters, chosen_combination = self._selection(
            entity_class, filters, combination
        )
        return self._implementation(instance).count(
            entity_class, chosen_filters, chosen_combination
        )

    def sum(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field over matching records, ignoring null."""
        return self._aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest non-null value of a Field over matching records."""
        return self._aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest non-null value of a Field over matching records."""
        return self._aggregate("max", entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of an Entity and return how many were removed."""
        entity_class = self._entity_class(entity)
        return self._implementation(instance).truncate(entity_class)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Execute a SQL command with named bound parameters."""
        if not isinstance(command, str):
            raise TypeError("command must be a SQL command string")
        if parameters is not None and not isinstance(parameters, Mapping):
            raise TypeError("parameters must map each parameter name to its value")
        return self._implementation(instance).execute(command, parameters or {})

    def create_tables(self, instance: DatabaseInstance | None = None) -> None:
        """Create or migrate every stored structure on the Instance."""
        tables.create_tables(self._implementation(instance), self.entities)

    def insert_initial_data(self, instance: DatabaseInstance | None = None) -> int:
        """Insert the declared Initial Data the Instance does not hold and return the count."""
        return initial_data.insert_initial_data(
            self._implementation(instance), self.entities
        )

    def _aggregate(
        self,
        function: str,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None,
        combination: FilterCombination | None,
        instance: DatabaseInstance | None,
    ) -> Any:
        entity_class = self._entity_class(entity)
        declared = self._field(entity_class, field)
        chosen_filters, chosen_combination = self._selection(
            entity_class, filters, combination
        )
        return self._implementation(instance).aggregate(
            entity_class, function, declared, chosen_filters, chosen_combination
        )

    def _set_active(
        self,
        entity: Any,
        record_id: int,
        active: bool,
        instance: DatabaseInstance | None,
    ) -> Any:
        entity_class = self._entity_class(entity)
        identity = self._identity(record_id)
        row = self._implementation(instance).set_active(entity_class, identity, active)
        return None if row is None else entity_class(**row)

    def _implementation(self, instance: DatabaseInstance | None) -> Any:
        if instance is None:
            instance = self.configuration.default
        elif not isinstance(instance, DatabaseInstance):
            raise TypeError("instance must be a DatabaseInstance member")
        if instance not in self._implementations:
            settings = self.configuration.instances[instance.value]
            module = import_module(f"database.engine.{instance.value}")
            self._implementations[instance] = module.create(
                settings, self.configuration.engines[settings.engine], self.entities
            )
        return self._implementations[instance]

    def _entity_class(self, entity: Any) -> Any:
        if not isinstance(entity, type) or entity not in self.entities:
            raise TypeError("an Entity class published by Model is required")
        return entity

    def _entity_instance(self, entity: Any) -> Any:
        if type(entity) not in self.entities:
            raise TypeError("an Entity instance published by Model is required")
        return type(entity)

    def _field(self, entity_class: Any, name: Any) -> Any:
        if not isinstance(name, str):
            raise TypeError("a Field name must be a string")
        for field in entity_class.declaration.fields:
            if field.name == name:
                return field
        raise ValueError(f"{entity_class.declaration.name} declares no Field {name}")

    def _selection(
        self,
        entity_class: Any,
        filters: Sequence[Filter] | None,
        combination: FilterCombination | None,
    ) -> tuple[list[Filter], FilterCombination]:
        chosen = list(filters or [])
        for filter_ in chosen:
            if not isinstance(filter_, Filter):
                raise TypeError("filters must be Filter objects")
            self._field(entity_class, filter_.field)
        if combination is None:
            combination = self.configuration.query_defaults.combination
        elif not isinstance(combination, FilterCombination):
            raise TypeError("combination must be a FilterCombination member")
        return chosen, combination

    def _check_order(self, entity_class: Any, order: Order) -> None:
        if not isinstance(order, Order):
            raise TypeError("orders must be Order objects")
        self._field(entity_class, order.field)

    @staticmethod
    def _identity(record_id: Any) -> int:
        if isinstance(record_id, bool) or not isinstance(record_id, int):
            raise TypeError("a record id must be an integer")
        return record_id

    @staticmethod
    def _limit(limit: Any) -> int:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        return limit

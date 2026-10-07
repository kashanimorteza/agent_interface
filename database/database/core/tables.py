import math
from datetime import date, datetime, time
from decimal import Decimal
from functools import cache
from types import ModuleType
from typing import Any
from uuid import UUID

from sqlalchemy.orm.attributes import InstrumentedAttribute

from database.core.configuration import Connection
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    ExecutionError,
    InvalidInputError,
    LifecycleError,
)

_DECLARATION_MEMBERS = (
    "name",
    "fields",
    "primary_key",
    "relations",
    "unique_constraints",
    "indexes",
)
_FIELD_MEMBERS = ("name", "type", "nullable", "immutable", "value_generation")


@cache
def entity_collection() -> tuple[type[Any], ...]:
    """The Model's Entity Collection, the only source of Entities."""
    try:
        from model.interface import entities as published
    except ImportError as error:
        raise ConfigurationError("The Model Interface cannot be loaded.") from error
    entities: Any = published
    if not isinstance(entities, tuple) or not entities:
        raise ConfigurationError("The Model Interface publishes no Entity Collection.")
    for entity in entities:
        declaration = getattr(entity, "declaration", None)
        if declaration is None or not all(hasattr(declaration, m) for m in _DECLARATION_MEMBERS):
            raise DeclarationMismatchError(f"The Declaration of {entity.__name__} is incomplete.")
        for field in declaration.fields:
            if not all(hasattr(field, member) for member in _FIELD_MEMBERS):
                raise DeclarationMismatchError(
                    f"A Field Declaration of {entity.__name__} is incomplete."
                )
        if not hasattr(entity, "__table__"):
            raise DeclarationMismatchError(f"{entity.__name__} has no table form.")
    return entities


def entity_named(identity: str) -> type[Any] | None:
    """The Entity of the Collection whose public identity is the given name."""
    for entity in entity_collection():
        if entity.__name__ == identity:
            return entity
    return None


_NUMERIC_TYPES = ("integer", "float", "decimal")


def check_entity_class(entity: Any) -> type[Any]:
    """An Entity of the Model passed as itself; a name or any other string is refused."""
    if isinstance(entity, type) and entity in entity_collection():
        return entity
    raise InvalidInputError("The Entity must be an Entity class of the Model, never a name.")


def check_entity_instance(entity: Any) -> type[Any]:
    """An instance of an Entity of the Model; returns its Entity class."""
    if type(entity) in entity_collection():
        return type(entity)
    raise InvalidInputError("The Entity must be an Entity instance of the Model.")


def normalize_value(entity: type[Any], field: Any, value: Any) -> Any:
    """Return the value in the form its declared Type requires, or refuse it."""
    kind = field.type.value
    valid = False
    if kind == "string":
        valid = isinstance(value, str)
    elif kind == "integer":
        valid = isinstance(value, int) and not isinstance(value, bool)
    elif kind == "float":
        valid = isinstance(value, int | float) and not isinstance(value, bool)
        if valid:
            value = float(value)
            valid = math.isfinite(value)
    elif kind == "decimal":
        if isinstance(value, int) and not isinstance(value, bool):
            value = Decimal(value)
        valid = isinstance(value, Decimal) and value.is_finite()
    elif kind == "boolean":
        valid = isinstance(value, bool)
    elif kind == "datetime":
        valid = isinstance(value, datetime) and value.tzinfo is not None
    elif kind == "date":
        valid = isinstance(value, date) and not isinstance(value, datetime)
    elif kind == "time":
        valid = isinstance(value, time)
    elif kind == "uuid":
        valid = isinstance(value, UUID)
    if not valid:
        raise InvalidInputError(
            f"The value for {entity.declaration.name}.{field.name} is not a valid {kind}."
        )
    return value


def check_id(entity: type[Any], value: Any) -> Any:
    """An id acceptable for the identity Field of the Entity."""
    declaration = entity.declaration
    identity = next(field for field in declaration.fields if field.name == declaration.primary_key)
    return normalize_value(entity, identity, value)


def field_declaration(entity: type[Any], reference: Any) -> Any:
    """The Declaration of the Field a Field reference points to; a name is refused."""
    if not isinstance(reference, InstrumentedAttribute) or reference.class_ is not entity:
        raise InvalidInputError(
            f"The Field must be a Field reference of {entity.declaration.name}, never a name."
        )
    for field in entity.declaration.fields:
        if field.name == reference.key:
            return field
    raise InvalidInputError(f"The Field is not a Field of {entity.declaration.name}.")


def check_aggregate_field(entity: type[Any], reference: Any, *, numeric: bool) -> Any:
    """A Field reference usable in an aggregate: numeric for a sum, comparable otherwise."""
    field = field_declaration(entity, reference)
    kind = field.type.value
    if (numeric and kind not in _NUMERIC_TYPES) or (not numeric and kind == "boolean"):
        raise InvalidInputError(
            f"{entity.declaration.name}.{field.name} cannot be used in this aggregate."
        )
    return field


def create_tables(unit: ModuleType, connection: Connection) -> int:
    """Create the Tables of exactly the Model Entities; return how many were created.

    A difference between an existing Table and its Declaration stops everything before any
    Table is created; it is reported, never resolved.
    """
    entities = entity_collection()
    report = unit.differences(connection, entities)
    if report:
        listed = "; ".join(f"{name}: {', '.join(found)}" for name, found in report.items())
        raise DeclarationMismatchError(
            f"An existing Table differs from its Entity and nothing was created. {listed}."
        )
    try:
        return unit.create_tables(connection, entities)
    except ExecutionError as error:
        if getattr(unit, "ATOMIC_DDL", False):
            raise
        raise LifecycleError(
            f"Table creation did not complete and may have left an incomplete state: {error}"
        ) from None

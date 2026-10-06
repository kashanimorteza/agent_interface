"""Parameter forms: how non-simple Parameters travel and are built before a Handler runs."""

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from logic.interface import Entity
from pydantic import PlainSerializer, PlainValidator
from pydantic.json_schema import WithJsonSchema

InvalidInputError = Entity.Error.InvalidInputError


def refusal(error: ValueError) -> InvalidInputError:
    """An Invalid Input error naming fields and reasons, never repeating a submitted value."""
    details = getattr(error, "errors", None)
    if callable(details):
        items = details(include_input=False, include_url=False, include_context=False)
        return InvalidInputError(
            "; ".join(f"{'.'.join(map(str, i['loc'])) or 'value'}: {i['msg']}" for i in items)
        )
    return InvalidInputError(str(error))


def entity_schema(entity_class: Any) -> dict[str, Any]:
    kinds = {
        "integer": {"type": "integer"},
        "float": {"type": "number"},
        "boolean": {"type": "boolean"},
        "datetime": {"type": "string", "format": "date-time"},
    }
    properties, required = {}, []
    for field in entity_class.declaration.fields:
        schema = kinds.get(field.type.value, {"type": "string"})
        properties[field.name] = (
            {"anyOf": [schema, {"type": "null"}]}
            if field.nullable or field.name == "id"
            else schema
        )
        if not field.has_default and not field.nullable and field.name != "id":
            required.append(field.name)
    return {
        "type": "object",
        "title": entity_class.__name__,
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def entity_object(entity_class: Any) -> tuple[Any, ...]:
    """An Entity instance travels as a JSON object of its Fields, built from the bound class."""

    def build(value: Any) -> Any:
        if not isinstance(value, dict):
            raise InvalidInputError("The Entity must be a JSON object")
        values = dict(value)
        identity = values.pop("id", None)
        if identity is not None and (isinstance(identity, bool) or not isinstance(identity, int)):
            raise InvalidInputError("id: must be an integer")
        try:
            entity = entity_class.from_json(json.dumps({**values, "id": None}))
        except ValueError as error:
            raise refusal(error) from None
        return entity.model_copy(update={"id": identity}) if identity is not None else entity

    return (PlainValidator(build), WithJsonSchema(entity_schema(entity_class)))


def field_names(entity_class: Any) -> list[str]:
    return [field.name for field in entity_class.declaration.fields]


def resolve_field(entity_class: Any, name: Any) -> Any:
    if not isinstance(name, str) or name not in field_names(entity_class):
        raise InvalidInputError("field: unknown field name")
    return getattr(entity_class, name)


def field_reference(entity_class: Any) -> tuple[Any, ...]:
    """A reference to a field of the bound class travels as the field's name."""
    return (
        PlainValidator(lambda name: resolve_field(entity_class, name)),
        WithJsonSchema({"type": "string", "enum": field_names(entity_class)}),
    )


def field_value(entity_class: Any, name: str, value: Any) -> Any:
    """A Filter value takes the Field's Type: decimals as text, datetimes as ISO 8601 text."""
    kind = {field.name: field.type.value for field in entity_class.declaration.fields}[name]
    if kind == "decimal":
        if isinstance(value, bool) or not isinstance(value, str | int):
            raise InvalidInputError(f"{name}: a decimal value must be text or an integer")
        try:
            return Decimal(str(value))
        except InvalidOperation:
            raise InvalidInputError(f"{name}: not a decimal value") from None
    if kind == "datetime":
        try:
            return datetime.fromisoformat(value) if isinstance(value, str) else value
        except ValueError:
            raise InvalidInputError(f"{name}: not an ISO 8601 datetime") from None
    return value


def member(enumeration: Any, name: Any, label: str) -> Any:
    if not isinstance(name, str) or name not in enumeration.__members__:
        raise InvalidInputError(f"{label}: unknown member")
    return enumeration[name]


def _object(value: Any, keys: set[str], required: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not required <= set(value) <= keys:
        raise InvalidInputError(f"{label}: must be an object of {', '.join(sorted(keys))}")
    return value


def filters(entity_class: Any) -> tuple[Any, ...]:
    """Every Filter travels as {field, operator, value}, built from the published Filter."""
    parameter = Entity.Parameter
    nulls = {parameter.FilterOperator.IS_NULL, parameter.FilterOperator.IS_NOT_NULL}

    def build(values: Any) -> Any:
        if values is None:
            return None
        if not isinstance(values, list):
            raise InvalidInputError("filters: must be a list of filter objects")
        built = []
        for item in values:
            item = _object(item, {"field", "operator", "value"}, {"field", "operator"}, "filter")
            field = resolve_field(entity_class, item["field"])
            operator = member(parameter.FilterOperator, item["operator"], "filter operator")
            if operator in nulls:
                if "value" in item:
                    raise InvalidInputError("filter: a null test takes no value")
                built.append(parameter.Filter(field, operator))
                continue
            if "value" not in item:
                raise InvalidInputError("filter: value is required")
            value = item["value"]
            if operator == parameter.FilterOperator.IN:
                if not isinstance(value, list):
                    raise InvalidInputError("filter: IN takes a list of values")
                value = [field_value(entity_class, item["field"], v) for v in value]
            else:
                value = field_value(entity_class, item["field"], value)
            built.append(parameter.Filter(field, operator, value))
        return built

    names = field_names(entity_class)
    operators = list(Entity.Parameter.FilterOperator.__members__)
    item = {
        "type": "object",
        "properties": {
            "field": {"type": "string", "enum": names},
            "operator": {"type": "string", "enum": operators},
            "value": {},
        },
        "required": ["field", "operator"],
        "additionalProperties": False,
    }
    return (
        PlainValidator(build),
        WithJsonSchema({"anyOf": [{"type": "array", "items": item}, {"type": "null"}]}),
    )


def orders(entity_class: Any) -> tuple[Any, ...]:
    """Every Order travels as {field, direction}, built from the published Order."""
    parameter = Entity.Parameter

    def build(values: Any) -> Any:
        if values is None:
            return None
        if not isinstance(values, list):
            raise InvalidInputError("orders: must be a list of order objects")
        built = []
        for item in values:
            item = _object(item, {"field", "direction"}, {"field"}, "order")
            field = resolve_field(entity_class, item["field"])
            if "direction" in item:
                direction = member(parameter.OrderDirection, item["direction"], "order direction")
                built.append(parameter.Order(field, direction))
            else:
                built.append(parameter.Order(field))
        return built

    item = {
        "type": "object",
        "properties": {
            "field": {"type": "string", "enum": field_names(entity_class)},
            "direction": {"type": "string", "enum": list(parameter.OrderDirection.__members__)},
        },
        "required": ["field"],
        "additionalProperties": False,
    }
    return (
        PlainValidator(build),
        WithJsonSchema({"anyOf": [{"type": "array", "items": item}, {"type": "null"}]}),
    )


def enumeration(enumeration_class: Any, label: str) -> tuple[Any, ...]:
    """A member of a published enumeration travels as its name."""

    def build(value: Any) -> Any:
        return None if value is None else member(enumeration_class, value, label)

    names = list(enumeration_class.__members__)
    schema = {"anyOf": [{"type": "string", "enum": names}, {"type": "null"}]}
    return (PlainValidator(build), WithJsonSchema(schema))


def database_instance() -> tuple[Any, ...]:
    """A Database Instance travels as its name."""
    return enumeration(Entity.Parameter.DatabaseInstance, "instance")


def filter_combination() -> tuple[Any, ...]:
    """A Filter combination travels as its member name."""
    return enumeration(Entity.Parameter.FilterCombination, "combination")


def exact_json(value: Any) -> Any:
    """A result as JSON: an Entity as its JSON Object, decimals as exact text, datetimes as ISO."""
    if hasattr(value, "to_json"):
        return json.loads(value.to_json())
    if isinstance(value, list | tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


RESULT = PlainSerializer(exact_json, when_used="json")

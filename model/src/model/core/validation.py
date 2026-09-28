"""Validation of Field values and of Entity construction input against a Declaration."""

import re
import uuid
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any

from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)


def check_value(field: FieldDeclaration, value: Any) -> str | None:
    """Return the rule a value violates for a Field, or None when it is acceptable.

    Args:
        field (FieldDeclaration): Field the value is meant for.
        value (Any): Candidate value.

    Returns:
        (str | None): Description of the first violated rule.
    """
    if value is None:
        return None if field.nullable else "must not be null"
    if not _has_type(field.type, value):
        return f"must be of type {field.type}"
    rules = field.constraints
    if isinstance(value, str):
        if rules.length is not None and len(value) > rules.length:
            return f"must not exceed {rules.length} characters"
        if rules.pattern is not None and re.fullmatch(rules.pattern, value) is None:
            return "must match the declared pattern"
    if isinstance(value, int | float | Decimal) and not isinstance(value, bool):
        if rules.minimum is not None and value < rules.minimum:
            return f"must not be below {rules.minimum}"
        if rules.maximum is not None and value > rules.maximum:
            return f"must not exceed {rules.maximum}"
    if isinstance(value, Decimal):
        exponent = int(value.as_tuple().exponent)
        scale = max(-exponent, 0)
        precision = max(len(value.as_tuple().digits), scale) + max(exponent, 0)
        if rules.scale is not None and scale > rules.scale:
            return f"must not have more than {rules.scale} fractional digits"
        if rules.precision is not None and precision > rules.precision:
            return f"must not have more than {rules.precision} significant digits"
    if rules.allowed_values is not None and value not in rules.allowed_values:
        return "must be one of the allowed values"
    return None


def _has_type(field_type: FieldType, value: Any) -> bool:
    match field_type:
        case FieldType.STRING:
            return isinstance(value, str)
        case FieldType.INTEGER:
            return isinstance(value, int) and not isinstance(value, bool)
        case FieldType.BOOLEAN:
            return isinstance(value, bool)
        case FieldType.FLOAT:
            return isinstance(value, float)
        case FieldType.DECIMAL:
            return isinstance(value, Decimal) and value.is_finite()
        case FieldType.DATETIME:
            return isinstance(value, datetime) and value.utcoffset() is not None
    return False


_REQUIRED = object()


def _omitted_value(field: FieldDeclaration) -> Any:
    if field.has_default:
        return field.default
    if field.value_generation == ValueGeneration.GENERATED_IDENTIFIER:
        return str(uuid.uuid4())
    if field.value_generation == ValueGeneration.AUTO_INCREMENT or field.nullable:
        return None
    return _REQUIRED


def validate_defaults(declaration: Declaration) -> None:
    """Reject a Declaration whose Default Values violate their own Field.

    Args:
        declaration (Declaration): Declaration to check.
    """
    errors = [
        f"{declaration.name}.{f.name}: default {problem}"
        for f in declaration.fields
        if f.has_default and (problem := check_value(f, f.default))
    ]
    if errors:
        raise ValueError("\n".join(errors))


def resolve_values(declaration: Declaration, data: dict[str, Any]) -> dict[str, Any]:
    """Validate construction input and return the value of every declared Field.

    Args:
        declaration (Declaration): Declaration of the Entity being constructed.
        data (dict[str, Any]): Supplied Field values.

    Returns:
        (dict[str, Any]): Value of each declared Field in Declaration order.
    """
    known = {f.name for f in declaration.fields}
    errors = [
        f"{declaration.name}: unknown Field {key}" for key in data if key not in known
    ]
    values: dict[str, Any] = {}
    for f in declaration.fields:
        if f.name not in data:
            value = _omitted_value(f)
            if value is _REQUIRED:
                errors.append(f"{declaration.name}.{f.name}: is required")
            else:
                values[f.name] = value
            continue
        value = data[f.name]
        pending = value is None and f.value_generation == ValueGeneration.AUTO_INCREMENT
        if not pending and (problem := check_value(f, value)):
            errors.append(f"{declaration.name}.{f.name}: {problem}")
        values[f.name] = value
    if errors:
        raise ValueError("\n".join(errors))
    return values


def check_assignment(
    declaration: Declaration, current: Mapping[str, Any], name: str, value: Any
) -> None:
    """Reject an assignment that breaks a Field contract.

    Args:
        declaration (Declaration): Declaration of the Entity being changed.
        current (Mapping[str, Any]): Values the Entity currently holds.
        name (str): Field being assigned.
        value (Any): Value being assigned.
    """
    field = next((f for f in declaration.fields if f.name == name), None)
    if field is None:
        return
    held = current.get(name)
    if value != held and (
        (field.immutable and name in current)
        or (name == declaration.primary_key and held is not None)
    ):
        raise ValueError(f"{declaration.name}.{name}: is immutable")
    pending = value is None and field.value_generation == ValueGeneration.AUTO_INCREMENT
    if not pending and (problem := check_value(field, value)):
        raise ValueError(f"{declaration.name}.{name}: {problem}")

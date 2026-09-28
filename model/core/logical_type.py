from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BeforeValidator, ConfigDict, Field, TypeAdapter
from pydantic_core import PydanticCustomError


class LogicalType(StrEnum):
    """Portable category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"


def _require_float(value: Any) -> Any:
    if not isinstance(value, float):
        raise PydanticCustomError("float_required", "a float value is required")
    return value


Float = Annotated[float, BeforeValidator(_require_float), Field(allow_inf_nan=False)]
"""Finite float that accepts no other numeric Type."""

PYTHON_TYPES: dict[LogicalType, Any] = {
    LogicalType.INTEGER: int,
    LogicalType.STRING: str,
    LogicalType.BOOLEAN: bool,
    LogicalType.FLOAT: Float,
    LogicalType.DECIMAL: Decimal,
    LogicalType.DATETIME: datetime,
}

_ADAPTERS: dict[LogicalType, TypeAdapter[Any]] = {
    logical_type: TypeAdapter(
        python_type, config=ConfigDict(strict=True, hide_input_in_errors=True)
    )
    for logical_type, python_type in PYTHON_TYPES.items()
}


def validate_value(logical_type: LogicalType, value: Any) -> Any:
    """Return the value unchanged when it belongs to the logical Type, otherwise raise.

    Args:
        logical_type (LogicalType): Category the value must belong to.
        value (Any): Value to check; no conversion between categories is applied.

    Returns:
        (Any): The same value.
    """
    return _ADAPTERS[logical_type].validate_python(value)

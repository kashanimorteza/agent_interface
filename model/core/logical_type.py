from enum import StrEnum
from typing import Annotated, Any

from pydantic import BeforeValidator, Field


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
        # pydantic reports only a ValueError as a validation error
        raise ValueError("a float value is required")  # noqa: TRY004
    return value


Float = Annotated[float, BeforeValidator(_require_float), Field(allow_inf_nan=False)]
"""Finite float that accepts no other numeric Type."""

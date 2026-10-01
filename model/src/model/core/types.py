"""The one realization of every Type a Target may declare."""

from collections.abc import Mapping
from datetime import date, time
from decimal import Decimal
from types import MappingProxyType
from typing import Any
from uuid import UUID

from pydantic import AwareDatetime

_PYTHON_TYPES: Mapping[str, Any] = MappingProxyType(
    {
        "string": str,
        "integer": int,
        "float": float,
        "decimal": Decimal,
        "boolean": bool,
        "datetime": AwareDatetime,
        "date": date,
        "time": time,
        "uuid": UUID,
    }
)


def python_type(type_name: str) -> Any:
    """Return the realization of a declared Type, stopping when it is not recognized."""
    try:
        return _PYTHON_TYPES[type_name]
    except KeyError:
        raise ValueError(
            f"Unknown Type {type_name!r}; generation stops instead of guessing."
        ) from None

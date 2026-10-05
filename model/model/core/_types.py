from collections.abc import Mapping
from datetime import date, time
from decimal import Decimal
from types import MappingProxyType
from typing import Any
from uuid import UUID

from pydantic import AwareDatetime

REALIZATIONS: Mapping[str, Any] = MappingProxyType(
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


def realize(type_name: str) -> Any:
    try:
        return REALIZATIONS[type_name]
    except KeyError:
        raise ValueError(f"Unknown Type '{type_name}'; supported Types: {', '.join(REALIZATIONS)}") from None

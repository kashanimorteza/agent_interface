"""Private annotation aliases that realize Field Types beyond the plain built-ins."""

from decimal import Decimal
from typing import Annotated, Any

from pydantic import AwareDatetime, BeforeValidator, Field
from pydantic_core import PydanticCustomError


def _only_float(value: Any) -> Any:
    """Refuse anything but a float instead of converting it."""
    if not isinstance(value, float):
        raise PydanticCustomError("float_type", "Input should be a float.")
    return value


Float = Annotated[float, BeforeValidator(_only_float), Field(allow_inf_nan=False)]
DecimalValue = Annotated[Decimal, Field(allow_inf_nan=False)]
Timestamp = AwareDatetime

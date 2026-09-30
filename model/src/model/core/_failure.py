"""Private helper that reports a contract failure without exposing any value."""

from typing import LiteralString, cast

from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError


def reject(
    entity: str, field: str | None, code: LiteralString, message: LiteralString
) -> ValidationError:
    """Build a validation failure that names the Entity and Field, never a value."""
    detail = InitErrorDetails(
        type=PydanticCustomError(code, message),
        loc=(field,) if field else (),
        input=None,
    )
    return ValidationError.from_exception_data(entity, [detail], hide_input=True)


def withhold_inputs(error: ValidationError) -> ValidationError:
    """Rebuild a failure keeping its type, location, and message but no input."""
    details = [
        InitErrorDetails(
            type=PydanticCustomError(
                cast(LiteralString, line["type"]), cast(LiteralString, line["msg"])
            ),
            loc=line["loc"],
            input=None,
        )
        for line in error.errors(
            include_url=False, include_context=False, include_input=False
        )
    ]
    return ValidationError.from_exception_data(error.title, details, hide_input=True)

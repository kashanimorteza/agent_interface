"""Validation failures that never carry a supplied value."""

from collections.abc import Callable
from typing import Any

from pydantic import ValidationError


def without_inputs(error: ValidationError) -> ValidationError:
    """Rebuild a validation failure so that no supplied value survives in it."""
    lines: list[Any] = []
    for item in error.errors():
        line: dict[str, Any] = {"type": item["type"], "loc": item["loc"], "input": None}
        if "ctx" in item:
            line["ctx"] = item["ctx"]
        lines.append(line)
    return ValidationError.from_exception_data(error.title, lines, hide_input=True)


def strictly[T](check: Callable[[], T]) -> T:
    """Run a validation and raise its failure without any supplied value."""
    failure: ValidationError | None = None
    try:
        return check()
    except ValidationError as error:
        failure = without_inputs(error)
    raise failure

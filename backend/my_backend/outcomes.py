"""Logical outcomes reported by Logic and Data Access.

They carry no transport detail and no persistence detail, so that API can map
each to a response and Logic stays independent of both.
"""

from __future__ import annotations

from typing import Any


class LogicalOutcome(Exception):
    """Base of every non-success outcome."""


class RecordNotFound(LogicalOutcome):
    def __init__(self, model_name: str, key: Any) -> None:
        super().__init__(f"{model_name} {key!r} does not exist")
        self.model_name = model_name
        self.key = key


class ConflictingRecord(LogicalOutcome):
    def __init__(self, model_name: str) -> None:
        super().__init__(f"{model_name} conflicts with an existing record on a unique field")
        self.model_name = model_name


class InvalidData(LogicalOutcome):
    """The data violates the shared Model. ``errors`` names each failing field."""

    def __init__(self, model_name: str, errors: list[dict[str, Any]]) -> None:
        fields = ", ".join(".".join(str(p) for p in e.get("loc", ())) or "?" for e in errors)
        super().__init__(f"{model_name} is invalid: {fields}")
        self.model_name = model_name
        self.errors = errors


class NoLogicUnit(LogicalOutcome):
    def __init__(self, model_name: str) -> None:
        super().__init__(f"no Logic unit is defined for {model_name}")
        self.model_name = model_name

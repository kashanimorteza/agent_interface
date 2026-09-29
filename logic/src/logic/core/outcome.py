"""Application Outcomes: the transport-independent, storage-independent answer to a request."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class OutcomeKind(StrEnum):
    """The situations an Application Outcome distinguishes."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    INVALID = "invalid"
    CONFLICT = "conflict"
    BROKEN_REFERENCE = "broken_reference"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class Outcome[T]:
    """The result of one Operation: a success with its value, or an expected failure.

    Attributes:
        kind: Situation this Outcome reports.
        value: Result of a success; None for a failure.
        reason: Safe explanation of a failure; None for a success.
    """

    kind: OutcomeKind
    value: T | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        """Keep a success free of a reason and a failure free of a value."""
        if self.kind is OutcomeKind.SUCCESS:
            if self.reason is not None:
                raise ValueError("a success carries no reason")
        elif self.value is not None or not self.reason:
            raise ValueError("a failure carries a reason and no value")

    @property
    def succeeded(self) -> bool:
        """Report whether the Operation succeeded."""
        return self.kind is OutcomeKind.SUCCESS

    @classmethod
    def success(cls, value: T | None = None) -> Outcome[T]:
        """Build a success carrying a value."""
        return cls(OutcomeKind.SUCCESS, value)

    @classmethod
    def failure(cls, kind: OutcomeKind, reason: str) -> Outcome[Any]:
        """Build an expected failure with a safe reason."""
        return cls(kind, None, reason)

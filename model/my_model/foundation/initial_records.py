"""The records an entity must contain when the project begins.

A declared record carries the values the project states for it. Where the
project requires a value to be generated, the record carries the requirement
instead, so nothing here is a stand-in for a credential.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .generation import awaits_generation


@dataclass(frozen=True, slots=True)
class InitialRecord:
    """One record the project requires to exist from the start."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def generated_fields(self) -> tuple[str, ...]:
        """The fields whose value is to be produced rather than declared."""

        return tuple(
            name for name, value in self.values.items() if awaits_generation(value)
        )

    def declared_values(self) -> dict[str, Any]:
        """The values actually stated, leaving out those awaiting generation."""

        return {
            name: value
            for name, value in self.values.items()
            if not awaits_generation(value)
        }

    def __repr__(self) -> str:
        shown = ", ".join(f"{name}={value!r}" for name, value in self.values.items())
        return f"InitialRecord({shown})"

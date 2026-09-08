"""Values the project requires to be generated rather than written down.

A declared record may need a value that must not exist in the declaration: a
password or an API key. The declaration carries the requirement, and whichever
layer stores the record produces the value.
"""

from __future__ import annotations

from typing import Any, Final


class Generated:
    """A stated requirement to generate a value, carrying no value itself."""

    __slots__ = ("method",)

    def __init__(self, method: str = "secure_random") -> None:
        self.method = method

    def __repr__(self) -> str:
        return f"Generated({self.method!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Generated) and other.method == self.method

    def __hash__(self) -> int:
        return hash(("Generated", self.method))


GENERATE_SECURELY: Final[Generated] = Generated("secure_random")


def awaits_generation(value: Any) -> bool:
    """Whether a value is a pending generation requirement rather than a value."""

    return isinstance(value, Generated)

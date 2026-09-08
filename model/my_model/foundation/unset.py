"""The distinction between a property nobody stated and one stated as empty.

A field property that was never stated may be completed from a default. A
property stated as ``False`` or ``None`` is a decision and survives completion
untouched, so the two cases need separate representations.
"""

from __future__ import annotations

from typing import Any, Final


class _Unset:
    """The single value meaning "nothing was stated here"."""

    _instance: _Unset | None = None

    def __new__(cls) -> _Unset:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "UNSET"

    def __copy__(self) -> _Unset:
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> _Unset:
        return self

    def __reduce__(self) -> str:
        return "UNSET"


UNSET: Final[_Unset] = _Unset()


def is_stated(value: Any) -> bool:
    """Whether a property carries a stated value, empty ones included."""

    return value is not UNSET

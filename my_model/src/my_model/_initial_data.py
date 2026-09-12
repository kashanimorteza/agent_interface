"""Support for declaring required initial records without inserting them.

Model declares which initial records must exist and their required domain
values; it never performs their insertion (that belongs to Database). A
field whose value the Target defines as "generate securely" has no literal
value to declare, so it is marked with ``GENERATE_SECURELY`` instead of a
fabricated placeholder.
"""

from __future__ import annotations


class _GenerateSecurely:
    """Sentinel marking a field whose initial value is generated at
    insertion time rather than declared literally."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "GENERATE_SECURELY"


GENERATE_SECURELY = _GenerateSecurely()

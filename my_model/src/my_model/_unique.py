"""Pure, deterministic uniqueness-comparison support.

Model owns only the *rule* — which field combination must be unique — and a
side-effect-free way to compare two already-available records against that
rule. Model does not query or hold persisted state: proving uniqueness across
all persisted records is a Database concern (Model Standard, Validation
Ownership). Each model that declares a uniqueness rule exposes it through the
``UNIQUE_TOGETHER`` class attribute so the rule stays traceable to the Model
even though another component enforces it.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any


def shares_unique_key(a: Any, b: Any, fields: Sequence[str]) -> bool:
    """Return whether two records collide on every field of one uniqueness key.

    Deterministic and free of I/O: it reads only the attributes already
    present on the two supplied records.
    """
    return all(getattr(a, field) == getattr(b, field) for field in fields)


def find_colliding_record(
    candidate: Any, existing: Iterable[Any], fields: Sequence[str]
) -> Any | None:
    """Return the first record in ``existing`` that collides with ``candidate``.

    ``existing`` is supplied by the caller (Database resolves it from
    persisted state); this function performs no lookup of its own.
    """
    for record in existing:
        if shares_unique_key(candidate, record, fields):
            return record
    return None

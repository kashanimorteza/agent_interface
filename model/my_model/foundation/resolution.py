"""Completing the properties an entity leaves unstated.

An exact-name default is tried first, then a name-shape default. Both only fill
properties nobody stated, and neither one introduces a field: a name that
appears among the defaults but not in the entity stays out of it.
"""

from __future__ import annotations

from fnmatch import fnmatchcase
from typing import Any

from .defaults import COMMON_FIELD_DEFAULTS, FIELD_PATTERN_DEFAULTS
from .field_spec import FieldSpec


def normalize(field_name: str) -> str:
    """The form a field name is matched in."""

    return field_name.strip().lower()


def applicable_defaults(field_name: str) -> dict[str, Any]:
    """The default properties that apply to ``field_name``, most specific first."""

    name = normalize(field_name)
    resolved: dict[str, Any] = dict(COMMON_FIELD_DEFAULTS.get(name, {}))
    for pattern, defaults in FIELD_PATTERN_DEFAULTS:
        if fnmatchcase(name, pattern):
            for property_name, value in defaults.items():
                resolved.setdefault(property_name, value)
    return resolved


def complete_field(field_name: str, spec: FieldSpec) -> FieldSpec:
    """``spec`` with every property it leaves unstated taken from the defaults."""

    return spec.completed_with(applicable_defaults(field_name))


def complete_fields(fields: dict[str, FieldSpec]) -> dict[str, FieldSpec]:
    """Every declared field of an entity, completed and in declaration order."""

    return {name: complete_field(name, spec) for name, spec in fields.items()}

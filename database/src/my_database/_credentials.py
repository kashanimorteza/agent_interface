"""Resolves, for every credential field, its at-rest persistence transformation.

Preference order: an explicit project-stated storage mode, then a field-name
default, then the selected project-wide default. Explicit modes below are
the storage rules the project's own Target definition states for these
specific fields; everything else falls through to the generic defaults.
"""

from __future__ import annotations

import my_model as m

from . import _secrets

EXPLICIT_MODES: dict[tuple[type, str], str] = {
    (m.User, "password"): "hash",
    (m.User, "api_key"): "hash",
    (m.Instance, "password"): "encrypted",
    (m.Instance, "api_key"): "encrypted",
    (m.Account, "password"): "encrypted",
}

FIELD_NAME_DEFAULTS: dict[str, str] = {
    "password": "hash",
    "api_key": "hash",
}

SELECTED_DEFAULT = "plaintext"

_TRANSFORM = {
    "hash": _secrets.hash_value,
    "encrypted": _secrets.encrypt_value,
    "plaintext": _secrets.plaintext_value,
}


def resolve_mode(model_cls: type, field_name: str) -> str:
    return (
        EXPLICIT_MODES.get((model_cls, field_name))
        or FIELD_NAME_DEFAULTS.get(field_name)
        or SELECTED_DEFAULT
    )


def transform(model_cls: type, field_name: str, value: str) -> str:
    mode = resolve_mode(model_cls, field_name)
    return _TRANSFORM[mode](value)

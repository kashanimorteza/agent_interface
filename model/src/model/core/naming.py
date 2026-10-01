"""Deterministic physical names derived from exact logical names."""

import keyword
import re

from sqlmodel import SQLModel

_RESERVED_FIELD_NAMES = frozenset(dir(SQLModel)) | {
    "declaration",
    "to_json",
    "from_json",
}
_RESERVED_ENTITY_NAMES = frozenset({"Declaration", "Entity", "Foundation", "SQLModel"})
_ALLOWED = re.compile(r"[0-9A-Za-z]+(?:[ _][0-9A-Za-z]+)*")
_WORD = re.compile(r"[0-9A-Za-z]+")
_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _physical(logical: str, physical: str, kind: str) -> str:
    if not _ALLOWED.fullmatch(logical):
        raise ValueError(f"{kind} name {logical!r} has no deterministic physical name.")
    if (
        not physical.isidentifier()
        or physical.startswith("_")
        or keyword.iskeyword(physical)
    ):
        raise ValueError(f"{kind} name {logical!r} has no valid physical name.")
    return physical


def entity_name(logical: str) -> str:
    """Return the physical Entity name: the logical words joined in PascalCase."""
    joined = "".join(word[0].upper() + word[1:] for word in _WORD.findall(logical))
    physical = _physical(logical, joined, "Entity")
    if physical in _RESERVED_ENTITY_NAMES:
        raise ValueError(f"Entity name {logical!r} collides with a reserved name.")
    return physical


def field_name(logical: str) -> str:
    """Return the physical Field name: the logical words joined in snake_case."""
    words = _WORD.findall(_CAMEL_BOUNDARY.sub("_", logical))
    physical = _physical(logical, "_".join(words).lower(), "Field")
    if physical in _RESERVED_FIELD_NAMES:
        raise ValueError(
            f"Field name {logical!r} collides with a reserved member name."
        )
    return physical

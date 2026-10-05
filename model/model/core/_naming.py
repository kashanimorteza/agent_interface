import keyword
import re

from sqlmodel import SQLModel

_ENTITY_NAME = re.compile(r"[A-Za-z][A-Za-z0-9]*( [A-Za-z0-9]+)*")
_FIELD_NAME = re.compile(r"[a-z][a-z0-9]*(_[a-z0-9]+)*")
_WORD_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")

RESERVED_NAMES = frozenset(keyword.kwlist) | frozenset(dir(SQLModel)) | {"declaration", "to_json", "from_json"}


def entity_class_name(logical_name: str) -> str:
    if not _ENTITY_NAME.fullmatch(logical_name):
        raise ValueError(f"Entity name '{logical_name}' cannot be normalized to a class name")
    name = "".join(word[0].upper() + word[1:] for word in logical_name.split(" "))
    if name in RESERVED_NAMES:
        raise ValueError(f"Entity name '{logical_name}' collides with a reserved word")
    return name


def field_attribute_name(logical_name: str) -> str:
    name = _WORD_BOUNDARY.sub("_", logical_name.replace(" ", "_")).lower()
    if not _FIELD_NAME.fullmatch(name):
        raise ValueError(f"Field name '{logical_name}' cannot be normalized to an attribute name")
    if name in RESERVED_NAMES:
        raise ValueError(f"Field name '{logical_name}' collides with a reserved word")
    return name

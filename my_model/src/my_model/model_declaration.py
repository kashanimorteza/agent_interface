"""Technology-independent records of what an Entity's data means.

A declaration only describes; it carries no runtime behaviour.
"""

from dataclasses import dataclass
from typing import Any, Literal

FieldType = Literal["integer", "string", "boolean", "float", "decimal", "datetime"]
ValueGeneration = Literal[
    "auto_increment", "generated_identifier", "generated_timestamp"
]


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The meaning of one Field of an Entity."""

    name: str
    type: FieldType
    nullable: bool
    purpose: str = ""
    has_default: bool = False
    default: Any = None
    sensitive: bool = False
    immutable: bool = False
    length: int | None = None
    value_generation: ValueGeneration | None = None
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ReferenceDeclaration:
    """A Reference from one Field to the identity of another Entity."""

    field: str
    entity: str
    target_field: str = "id"


@dataclass(frozen=True, slots=True)
class IndexDeclaration:
    """An access intention over one Field or a combination of Fields."""

    fields: tuple[str, ...]
    unique: bool = False


@dataclass(frozen=True, slots=True)
class Model_Declaration:
    """The complete data meaning of one Entity."""

    entity: str
    purpose: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: tuple[str, ...] = ("id",)
    references: tuple[ReferenceDeclaration, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[IndexDeclaration, ...] = ()

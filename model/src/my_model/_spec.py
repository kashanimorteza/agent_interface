"""Immutable descriptions of the resolved logical definition of a Model.

These structures carry what a Model means — its fields and their properties, its
relationships, its domain rules, and its initial records — so consumers can read
one Model's definition without redefining it. They describe the domain only; how a
Model is stored, exposed, or presented belongs to the Database, Backend, and
Frontend layers.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


class LogicalType(StrEnum):
    """The logical type of a field, independent of any language or storage engine."""

    integer = "integer"
    string = "string"
    boolean = "boolean"
    decimal = "decimal"
    float = "float"
    datetime = "datetime"


class _Unset:
    """The absence of a declared value, distinct from None and from False."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"

    def __bool__(self) -> bool:
        return False


UNSET = _Unset()
"""Marks a field property that the Model definition does not declare."""


@dataclass(frozen=True, slots=True)
class GenerateValue:
    """An initial-data value that is produced securely when the data is seeded.

    The Model package never produces the value; fulfilling the instruction belongs
    to the layer that seeds the data.
    """

    instruction: str = "Generate securely"


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldSpec:
    """The resolved logical definition of one field of a Model."""

    name: str | None = None
    type: LogicalType
    nullable: bool
    size: int | None = None
    default: Any = UNSET
    auto_increment: bool = False
    primary_key: bool = False
    unique: bool = False
    credential: bool = False
    purpose: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class RelationshipSpec:
    """A conceptual connection from one Model to another."""

    name: str
    type: str
    target: str
    field: str | None = None
    role: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class RuleSpec:
    """A domain rule constraining the valid state of a Model."""

    rule: str
    kind: str
    field: str | None = None
    fields: tuple[str, ...] | None = None
    storage: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ModelSpec:
    """The complete resolved logical definition of one Model."""

    key: str
    purpose: str
    fields: tuple[FieldSpec, ...]
    relationships: tuple[RelationshipSpec, ...] = ()
    rules: tuple[RuleSpec, ...] = ()
    initial_data: tuple[Mapping[str, Any], ...] = ()

    def field(self, name: str) -> FieldSpec:
        """Return the definition of one field by name."""
        for spec in self.fields:
            if spec.name == name:
                return spec
        raise KeyError(name)

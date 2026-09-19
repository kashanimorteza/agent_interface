"""The Declaration Vocabulary.

One standard, technology-independent set of terms in which every Domain Definition states its Fields,
its relationships, and itself. The terms and their meanings are fixed by the Model Declaration Schema; this
module only realizes them for Pydantic. Field and relationship terms travel as metadata inside the
``Annotated`` type of the Field they describe, so the same Domain Definition that application code uses
carries its own declaration and no second artifact exists beside it.

Nothing here is storage-specific: there is no table, column, index, foreign key, or migration term.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from types import UnionType
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict


class Persistence(StrEnum):
    """Whether a Domain Definition is stored by Database. Declared explicitly, never inferred."""

    PERSISTENT = "persistent"
    NON_PERSISTENT = "non-persistent"


class AtRestTreatment(StrEnum):
    """The at-rest treatment the Target requires for a credential Field."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class Cardinality(StrEnum):
    """The multiplicity of an association, from the declaring definition's side."""

    ONE = "one"
    MANY = "many"


@dataclass(frozen=True, kw_only=True)
class Identity:
    """Marks a Field as part of what identifies one record. Several marked Fields form an ordered set."""


@dataclass(frozen=True, kw_only=True)
class Generated:
    """Marks a Field whose value the domain does not supply because something else produces it.

    A generated Field is absent until it is produced and is never null afterwards, so its declared
    optionality stays ``False`` even though an unproduced value is representable.
    """


@dataclass(frozen=True, kw_only=True)
class Unique:
    """Marks a Field whose value does not repeat across the records of a Domain Definition."""


@dataclass(frozen=True, kw_only=True)
class Activation:
    """Marks the Field that says whether a record is active."""


@dataclass(frozen=True, kw_only=True)
class Credential:
    """Classifies a Field as a credential and states the at-rest treatment the Target requires."""

    treatment: AtRestTreatment


@dataclass(frozen=True, kw_only=True)
class Reference:
    """The association a Field carries to another Domain Definition.

    The referenced Domain Definition is carried as the definition itself, never as a name in text, so a
    reference that does not resolve fails where it is written.
    """

    definition: type[BaseModel]
    field: str
    cardinality: Cardinality
    optional: bool

    def __post_init__(self) -> None:
        if not (
            isinstance(self.definition, type)
            and hasattr(self.definition, "declaration")
        ):
            raise TypeError(f"{self.definition!r} is not a Domain Definition")
        if self.field not in self.definition.model_fields:
            raise ValueError(
                f"{self.definition.__name__} has no Field named {self.field!r}"
            )
        if not isinstance(self.cardinality, Cardinality):
            raise TypeError("a relationship states its cardinality as a Cardinality")


class Precision(BaseModel):
    """The total digits and scale of an exact numeric value."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    digits: int | None
    scale: int | None


class FieldDeclaration(BaseModel):
    """What a Domain Definition declares about one of its Fields, as a consumer reads it back."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    type: str
    length: int | None
    precision: Precision | None
    optional: bool
    has_default: bool
    default: Any
    identity: bool
    generated: bool
    unique: bool
    credential: AtRestTreatment | None
    activation: bool


class RelationshipDeclaration(BaseModel):
    """What a Domain Definition declares about an association to another Domain Definition."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    field: str
    definition: type[BaseModel]
    referenced_field: str
    cardinality: Cardinality
    optional: bool


class DefinitionDeclaration(BaseModel):
    """What a Domain Definition declares about itself, as a consumer reads it back."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    persistence: Persistence
    fields: tuple[FieldDeclaration, ...]
    identity: tuple[str, ...]
    unique_sets: tuple[tuple[str, ...], ...]
    relationships: tuple[RelationshipDeclaration, ...]


_LOGICAL_TYPES: dict[Any, str] = {
    bool: "boolean",
    int: "integer",
    float: "float",
    Decimal: "decimal",
    str: "string",
    datetime: "datetime",
}


def logical_type(annotation: Any) -> tuple[str, bool]:
    """Return a Field annotation's logical type name and whether the annotation admits no value."""
    admits_none = False
    if get_origin(annotation) in (Union, UnionType):
        members = get_args(annotation)
        remaining = [member for member in members if member is not type(None)]
        admits_none = len(remaining) != len(members)
        if len(remaining) != 1:
            raise TypeError(f"a Field holds one logical type, not {annotation!r}")
        annotation = remaining[0]
    try:
        return _LOGICAL_TYPES[annotation], admits_none
    except KeyError, TypeError:
        raise TypeError(
            f"{annotation!r} has no logical type in the Declaration Vocabulary"
        ) from None

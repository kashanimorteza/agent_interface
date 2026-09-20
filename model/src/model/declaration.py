"""The Declaration Vocabulary: the one technology-independent language every Domain Definition
states itself in, and the readable form of what a definition has stated.

A Field states its logical type, length, precision and default through its ordinary annotation;
identity, generated, unique, credential and activation are stated with the markers below.
Nothing here names a table, index, column type or any other storage structure.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from types import NoneType, UnionType
from typing import Annotated, Any, Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AtRest(StrEnum):
    """The at-rest treatment the Target requires for a credential: stated here, never applied."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class Persistence(StrEnum):
    """Whether a Domain Definition is stored. It is always stated, never inferred."""

    PERSISTENT = "persistent"
    NON_PERSISTENT = "non-persistent"


class Cardinality(StrEnum):
    """The multiplicity of an association, from the side of the definition that declares it."""

    ONE = "one"
    MANY = "many"


@dataclass(frozen=True)
class Identity:
    """Marks the Field that identifies one record of a Domain Definition."""


@dataclass(frozen=True)
class Generated:
    """Marks a Field whose value the domain does not supply because something else produces it.

    Such a Field has no value until it is produced. That absence is what `generated` means, not
    optionality: the Field's `optional` term stays as the Target states it.
    """


@dataclass(frozen=True)
class Unique:
    """Marks a Field whose value does not repeat across the records of a Domain Definition."""


@dataclass(frozen=True)
class Activation:
    """Marks the Field that says whether a record is active."""


@dataclass(frozen=True)
class Credential:
    """Classifies a Field as a credential and states the at-rest treatment the Target requires."""

    at_rest: AtRest


@dataclass(frozen=True)
class Precision:
    """Total digits and scale of an exact numeric value, where the Target states them."""

    digits: int | None
    scale: int | None


@dataclass(frozen=True)
class FieldDeclaration:
    """What a Domain Definition has stated about one Field."""

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
    credential: AtRest | None
    activation: bool


_LOGICAL_TYPES: dict[type, str] = {
    int: "integer",
    str: "string",
    Decimal: "decimal",
    bool: "boolean",
    datetime: "datetime",
    float: "float",
}


def _split_optional(annotation: Any) -> tuple[Any, bool]:
    if get_origin(annotation) in (Union, UnionType):
        members = get_args(annotation)
        present = [member for member in members if member is not NoneType]
        if len(present) != 1:
            raise TypeError(f"a Field holds one logical type, found {annotation!r}")
        return _unwrap(present[0]), len(present) != len(members)
    return annotation, False


def _unwrap(annotation: Any) -> Any:
    return get_args(annotation)[0] if get_origin(annotation) is Annotated else annotation


def _constraint(info: FieldInfo, name: str) -> int | None:
    for item in info.metadata:
        value = getattr(item, name, None)
        if isinstance(value, int):
            return value
    return None


def declare_field(name: str, info: FieldInfo) -> FieldDeclaration:
    """Read what a Domain Definition has stated about the Field `name`."""
    held, allows_none = _split_optional(info.annotation)
    if held not in _LOGICAL_TYPES:
        raise TypeError(f"Field {name!r} has no logical type for {held!r}")

    generated = any(isinstance(item, Generated) for item in info.metadata)
    credentials = [item for item in info.metadata if isinstance(item, Credential)]
    digits = _constraint(info, "max_digits")
    scale = _constraint(info, "decimal_places")
    has_default = not info.is_required() and not generated

    return FieldDeclaration(
        name=name,
        type=_LOGICAL_TYPES[held],
        length=_constraint(info, "max_length"),
        precision=Precision(digits, scale) if digits is not None or scale is not None else None,
        optional=allows_none and not generated,
        has_default=has_default,
        default=info.default if has_default else None,
        identity=any(isinstance(item, Identity) for item in info.metadata),
        generated=generated,
        unique=any(isinstance(item, Unique) for item in info.metadata),
        credential=credentials[0].at_rest if credentials else None,
        activation=any(isinstance(item, Activation) for item in info.metadata),
    )


@dataclass(frozen=True)
class Relationship:
    """An association from one Domain Definition to another.

    `reference` is the referenced definition itself, never its name, and `field` is the Field of
    it that is referred to. `via` is the Field of the declaring definition that holds the
    reference value. Cardinality and optionality have no default: the Target states both.
    """

    name: str
    via: str
    reference: type[BaseModel]
    field: str
    cardinality: Cardinality
    optional: bool

    def __post_init__(self) -> None:
        # The checks below are runtime guards for callers the type checker cannot see: a
        # relationship must fail where it is written, however it was written.
        if not (
            isinstance(self.reference, type)  # pyright: ignore[reportUnnecessaryIsInstance]
            and issubclass(self.reference, BaseModel)  # pyright: ignore[reportUnnecessaryIsInstance]
        ):
            raise TypeError(
                f"relationship {self.name!r} must carry the referenced Domain Definition itself"
            )
        if self.field not in self.reference.model_fields:
            raise TypeError(
                f"relationship {self.name!r} refers to {self.field!r}, which "
                f"{self.reference.__name__} does not declare"
            )
        if not isinstance(self.cardinality, Cardinality):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"relationship {self.name!r} must state its cardinality")


@dataclass(frozen=True)
class Declaration:
    """Everything a Domain Definition has stated about itself, readable by any Component."""

    name: str
    persistence: Persistence
    fields: tuple[FieldDeclaration, ...]
    relationships: tuple[Relationship, ...]
    unique_sets: tuple[tuple[str, ...], ...]

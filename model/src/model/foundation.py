"""Model Foundation: the mechanisms every Domain Definition shares.

It supplies mechanism only and never a Field or a Domain Relationship. Every Domain
Definition declares its own complete set of Fields and relationships.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import NoneType
from typing import Annotated, Any, ClassVar, Literal, Self, Union, get_args, get_origin

from pydantic import (
    AwareDatetime,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
)
from pydantic.fields import FieldInfo

# ---------------------------------------------------------------- Declaration Vocabulary

Persistence = Literal["persistent", "non-persistent"]
Cardinality = Literal["one-to-one", "many-to-one", "one-to-many", "many-to-many"]
AtRest = Literal["hash", "encrypted"]

_PERSISTENCE: tuple[str, ...] = get_args(Persistence)
_CARDINALITY: tuple[str, ...] = get_args(Cardinality)
_AT_REST: tuple[str, ...] = get_args(AtRest)


@dataclass(frozen=True, slots=True)
class Identity:
    """Marks the Field that identifies one record of a Domain Definition."""


@dataclass(frozen=True, slots=True)
class Generated:
    """Marks a Field whose value the domain does not supply because something else produces it."""


@dataclass(frozen=True, slots=True)
class Unique:
    """Marks a Field whose value does not repeat across the records of a Domain Definition."""


@dataclass(frozen=True, slots=True)
class Credential:
    """Classifies a Field as a credential and states the at-rest treatment the Target requires."""

    at_rest: AtRest

    def __post_init__(self) -> None:
        if self.at_rest not in _AT_REST:
            raise TypeError(f"unknown at-rest treatment {self.at_rest!r}")


@dataclass(frozen=True, slots=True)
class Relationship:
    """Association from one Domain Definition to another.

    ``reference`` is the referenced Domain Definition itself, never its name. ``field`` is the
    Field of the declaring definition that carries the reference value, and ``reference_field``
    is the Field of the referenced definition it refers to. Cardinality and optionality have no
    default: the Target states them.
    """

    field: str
    reference: type[ModelFoundation]
    reference_field: str
    cardinality: Cardinality
    optional: bool


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """What a Domain Definition declares about one of its Fields."""

    name: str
    type: str
    optional: bool
    has_default: bool
    default: Any
    length: int | None
    precision: tuple[int | None, int | None] | None
    identity: bool
    generated: bool
    unique: bool
    credential: AtRest | None


@dataclass(frozen=True, slots=True)
class DefinitionDeclaration:
    """What a Domain Definition declares about itself."""

    name: str
    persistence: Persistence
    fields: tuple[FieldDeclaration, ...]
    relationships: tuple[Relationship, ...]
    unique_sets: tuple[tuple[str, ...], ...]


# The logical type each supported realization type stands for. A type outside this table is a
# declaration error at the moment it is written.
_LOGICAL_TYPES: dict[Any, str] = {
    int: "integer",
    str: "string",
    bool: "boolean",
    Decimal: "decimal",
    float: "float",
    datetime: "datetime",
    AwareDatetime: "datetime",
}


def _walk(annotation: Any) -> tuple[Any, bool, list[Any]]:
    """Return the base type, whether the annotation allows no value, and all nested metadata."""
    origin = get_origin(annotation)
    if origin is Annotated:
        base, *metadata = get_args(annotation)
        inner, optional, nested = _walk(base)
        return inner, optional, [*nested, *metadata]
    if origin is Union:
        members = get_args(annotation)
        present = [member for member in members if member is not NoneType]
        if len(present) != 1:
            raise TypeError(f"a Field holds one logical type, not a union of {members!r}")
        inner, optional, nested = _walk(present[0])
        return inner, optional or len(present) != len(members), nested
    return annotation, False, []


def _declare_field(name: str, info: FieldInfo) -> FieldDeclaration:
    base, allows_none, nested = _walk(info.annotation)
    metadata = [*info.metadata, *nested]
    logical = _LOGICAL_TYPES.get(base)
    if logical is None:
        raise TypeError(f"Field {name!r} has type {base!r}, which has no logical type")
    generated = any(isinstance(item, Generated) for item in metadata)
    has_default = not info.is_required() and not generated
    digits = next((item.max_digits for item in metadata if getattr(item, "max_digits", None) is not None), None)
    scale = next((item.decimal_places for item in metadata if getattr(item, "decimal_places", None) is not None), None)
    credential: AtRest | None = None
    for item in metadata:
        if isinstance(item, Credential):
            credential = item.at_rest
            break
    return FieldDeclaration(
        name=name,
        type=logical,
        optional=allows_none and not generated,
        has_default=has_default,
        default=info.get_default(call_default_factory=True) if has_default else None,
        length=next((item.max_length for item in metadata if getattr(item, "max_length", None) is not None), None),
        precision=None if digits is None and scale is None else (digits, scale),
        identity=any(isinstance(item, Identity) for item in metadata),
        generated=generated,
        unique=any(isinstance(item, Unique) for item in metadata),
        credential=credential,
    )


# ---------------------------------------------------------------- Shared Field types
# Types used by more than one Domain Definition live here. Numbers, text, and flags are strict so
# that coercion cannot hide invalid domain data; an exact decimal never accepts an approximation.


def _exact_input(value: Any) -> Any:
    if isinstance(value, (float, bool)):
        raise ValueError("an exact decimal does not accept an approximate or boolean value")
    return value


def _instant_input(value: Any) -> Any:
    if not isinstance(value, (datetime, str)):
        raise ValueError("an instant is given as a datetime or its text form")
    return value


Integer = Annotated[int, Field(strict=True)]
Text = Annotated[str, Field(strict=True)]
Flag = Annotated[bool, Field(strict=True)]
Approximate = Annotated[float, Field(strict=True)]
ExactDecimal = Annotated[Decimal, BeforeValidator(_exact_input)]
# Absolute instants are timezone-aware.
Instant = Annotated[AwareDatetime, BeforeValidator(_instant_input)]
# A generated identity is absent until whatever produces it supplies it; that absence is not
# domain optionality, so the declaration states the Field as not optional.
GeneratedId = Annotated[int | None, Identity(), Generated(), Field(strict=True)]
# A credential is kept exactly as given, so the configured whitespace stripping does not apply.
Secret = Annotated[str, StringConstraints(strip_whitespace=False, strict=True)]
HashedCredential = Annotated[Secret, Credential("hash")]
EncryptedCredential = Annotated[Secret, Credential("encrypted")]


# ---------------------------------------------------------------- Model Foundation


class ModelFoundation(BaseModel):
    """Base of every Domain Definition. Declares no Field and no relationship."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        str_strip_whitespace=True,
    )

    persistence: ClassVar[Persistence]
    relationships: ClassVar[tuple[Relationship, ...]] = ()
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        cls._check_declaration()

    @classmethod
    def _check_declaration(cls) -> None:
        if getattr(cls, "persistence", None) not in _PERSISTENCE:
            raise TypeError(f"{cls.__name__} must declare persistence as one of {_PERSISTENCE}")
        for relationship in cls.relationships:
            reference = relationship.reference
            # The typed signature already promises a definition; this rejects an untyped caller that passes a name instead.
            if not (isinstance(reference, type) and issubclass(reference, ModelFoundation)):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"{cls.__name__}: relationship {relationship.field!r} must carry the referenced Domain Definition itself")
            if relationship.field not in cls.model_fields:
                raise TypeError(f"{cls.__name__}: relationship Field {relationship.field!r} is not declared")
            if relationship.reference_field not in reference.model_fields:
                raise TypeError(f"{cls.__name__}: {reference.__name__} declares no Field {relationship.reference_field!r}")
            if relationship.cardinality not in _CARDINALITY:
                raise TypeError(f"{cls.__name__}: unknown cardinality {relationship.cardinality!r}")
            if not isinstance(relationship.optional, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"{cls.__name__}: relationship {relationship.field!r} must state optionality")
        for unique_set in cls.unique_sets:
            if not unique_set or any(name not in cls.model_fields for name in unique_set):
                raise TypeError(f"{cls.__name__}: unique set {unique_set!r} names an undeclared Field")
        cls.declaration()

    def serialize(self) -> dict[str, Any]:
        """The Plain Representation of this instance: simple named values of its own Fields.

        Every value is expressible in JSON without a custom encoder. A relationship appears only
        as its declared reference value, and no Field is withheld.
        """
        return self.model_dump(mode="json")

    @classmethod
    def deserialize(cls, data: Mapping[str, Any]) -> Self:
        """Build an instance from a Plain Representation, applying the Intrinsic Rules.

        Raises ``pydantic.ValidationError`` (a ``ValueError``) naming every offending Field when
        the data misses a required Field, holds a wrongly typed value, carries an unknown Field,
        or violates a declared constraint.
        """
        return cls.model_validate(data)

    @classmethod
    def declaration(cls) -> DefinitionDeclaration:
        """The Declaration Vocabulary statement of this Domain Definition."""
        return DefinitionDeclaration(
            name=cls.__name__,
            persistence=cls.persistence,
            fields=tuple(_declare_field(name, info) for name, info in cls.model_fields.items()),
            relationships=cls.relationships,
            unique_sets=cls.unique_sets,
        )

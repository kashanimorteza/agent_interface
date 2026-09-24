"""Model Foundation: the mechanisms every Domain Definition shares.

The foundation owns no Field and no relationship. Each Domain Definition declares its own
complete, Target-derived set and receives validation, conversion, and declaration
mechanisms from here.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from types import NoneType, UnionType
from typing import Annotated, Any, ClassVar, Literal, Self, Union, get_args, get_origin

from annotated_types import MaxLen
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationInfo,
)
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

__all__ = [
    "Constraint",
    "Declaration",
    "Declare",
    "ExactDecimal",
    "FieldDeclaration",
    "FiniteFloat",
    "ModelFoundation",
    "Relationship",
    "Rule",
    "Sensitivity",
    "UtcDatetime",
]

_PLAIN_CONTEXT = "plain_representation"
"""Validation-context key set only while a Plain Representation is being converted in."""


def _converting_in(info: ValidationInfo) -> bool:
    return bool(info.context and info.context.get(_PLAIN_CONTEXT))


def _decimal_from_plain(value: Any, info: ValidationInfo) -> Any:
    """Accept the plain string form of a decimal, and only while converting in."""
    if isinstance(value, str) and _converting_in(info):
        if value != value.strip() or "_" in value:
            raise ValueError("not a plain decimal value")
        try:
            return Decimal(value)
        except InvalidOperation as error:
            raise ValueError("not a plain decimal value") from error
    return value


def _datetime_from_plain(value: Any, info: ValidationInfo) -> Any:
    """Accept the plain ISO 8601 string form of a date-time, and only while converting in."""
    if isinstance(value, str) and _converting_in(info):
        try:
            return datetime.fromisoformat(value)
        except ValueError as error:
            raise ValueError("not a plain ISO 8601 date-time") from error
    return value


def _require_finite_decimal(value: Decimal) -> Decimal:
    if not value.is_finite():
        raise ValueError("a non-finite decimal is not a valid value")
    return value


def _require_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("a date-time must carry timezone information")
    return value.astimezone(UTC)


ExactDecimal = Annotated[
    Decimal,
    BeforeValidator(_decimal_from_plain),
    AfterValidator(_require_finite_decimal),
]
"""An exact decimal value; NaN and infinities are rejected."""

FiniteFloat = Annotated[float, Field(allow_inf_nan=False)]
"""An approximate number; NaN and infinities are rejected."""

UtcDatetime = Annotated[
    datetime, BeforeValidator(_datetime_from_plain), AfterValidator(_require_aware_utc)
]
"""A timezone-aware absolute instant, held in UTC."""


# --------------------------------------------------------------------------- Declaration Vocabulary
# The terms and their meanings are fixed by the Model Declaration Schema. These records carry
# that vocabulary in Python; they add no term and invent no default.

LogicalType = Literal["integer", "string", "boolean", "decimal", "float", "datetime"]
Kind = Literal["entity", "value-object"]
Persistence = Literal["persistent", "non-persistent"]
Aggregation = Literal["none", "shared", "composite"]

_CARDINALITY = re.compile(r"^(?:0|[1-9]\d*)(?:\.\.(?:0|[1-9]\d*|\*))?$")


@dataclass(frozen=True, slots=True, kw_only=True)
class Sensitivity:
    """A Target-declared sensitivity or credential classification and its at-rest treatment."""

    classification: str
    at_rest: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Constraint:
    """A declared constraint with a stable identity, unique within its Domain Definition."""

    id: str
    description: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Rule:
    """A declared Intrinsic Rule with a stable identity, unique within its Domain Definition."""

    id: str
    description: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Declare:
    """The Target-derived meaning of one Field that Python typing cannot carry.

    Placed in the Field's ``Annotated`` metadata. Nullability, whether the Field is required,
    and its default are read from the Field itself, so they cannot drift from the declaration.
    """

    description: str
    logical_type: LogicalType
    identity: bool | None = None
    generated: bool | None = None
    unique: bool | None = None
    length: int | None = None
    precision: int | None = None
    constraints: tuple[Constraint, ...] = ()
    sensitivity: Sensitivity | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldDeclaration:
    """One Field of a Domain Definition in the Declaration Vocabulary."""

    name: str
    description: str
    logical_type: LogicalType
    cardinality: str
    nullable: bool
    required: bool
    has_default: bool
    default: Any = None
    identity: bool | None = None
    generated: bool | None = None
    unique: bool | None = None
    length: int | None = None
    precision: int | None = None
    constraints: tuple[Constraint, ...] = ()
    sensitivity: Sensitivity | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Relationship:
    """A Domain Relationship. It carries the referenced Domain Definition itself."""

    name: str
    description: str
    definition: type[ModelFoundation]
    cardinality: str
    optional: bool
    aggregation: Aggregation | None = None
    inverse: str | None = None
    ordered: bool | None = None
    distinct: bool | None = None

    def __post_init__(self) -> None:
        if not (
            isinstance(self.definition, type)
            and issubclass(self.definition, ModelFoundation)
        ):
            raise TypeError(
                f"relationship {self.name!r} must carry a Domain Definition, not a name"
            )
        if not hasattr(self.definition, "declaration"):
            raise TypeError(
                f"relationship {self.name!r} refers to a definition without a declaration"
            )
        if not _CARDINALITY.match(self.cardinality):
            raise ValueError(
                f"relationship {self.name!r} has invalid cardinality {self.cardinality!r}"
            )
        if self.inverse is not None and self.inverse not in {
            r.name for r in self.definition.declaration.relationships
        }:
            raise ValueError(
                f"relationship {self.name!r} names an inverse the referenced definition lacks"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class Declaration:
    """A Domain Definition in the Declaration Vocabulary."""

    id: str
    name: str
    description: str
    kind: Kind
    persistent: Persistence
    fields: tuple[FieldDeclaration, ...]
    relationships: tuple[Relationship, ...] = ()
    intrinsic_rules: tuple[Rule, ...] = ()
    composite_constraints: tuple[Constraint, ...] = ()


def _nullable(annotation: Any) -> bool:
    if annotation is None or annotation is NoneType:
        return True
    if get_origin(annotation) in (Union, UnionType):
        return any(_nullable(arg) for arg in get_args(annotation))
    return False


def _field_declaration(name: str, info: FieldInfo) -> FieldDeclaration:
    declared = [m for m in info.metadata if isinstance(m, Declare)]
    if len(declared) != 1:
        raise TypeError(
            f"Field {name!r} must carry exactly one Declare(...) in its Annotated metadata"
        )
    meaning = declared[0]
    if meaning.length is not None and not any(
        isinstance(m, MaxLen) and m.max_length == meaning.length for m in info.metadata
    ):
        raise TypeError(
            f"Field {name!r} declares length {meaning.length} without enforcing it"
        )
    if info.default_factory is not None:
        raise TypeError(
            f"Field {name!r} uses a default factory; the Target declares plain defaults"
        )
    has_default = info.default is not PydanticUndefined
    return FieldDeclaration(
        name=name,
        description=meaning.description,
        logical_type=meaning.logical_type,
        cardinality="1",
        nullable=_nullable(info.annotation),
        required=info.is_required(),
        has_default=has_default,
        default=info.default if has_default else None,
        identity=meaning.identity,
        generated=meaning.generated,
        unique=meaning.unique,
        length=meaning.length,
        precision=meaning.precision,
        constraints=meaning.constraints,
        sensitivity=meaning.sensitivity,
    )


def _unique(kind: str, ids: Sequence[str]) -> None:
    if len(set(ids)) != len(ids):
        raise ValueError(
            f"{kind} identifiers must be unique within a Domain Definition"
        )


class ModelFoundation(BaseModel):
    """Common base of every Domain Definition."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_assignment=True,
        validate_default=True,
        str_strip_whitespace=True,
    )

    declaration: ClassVar[Declaration]
    """This Domain Definition in the Declaration Vocabulary."""

    def __init_subclass__(
        cls,
        *,
        description: str | None = None,
        persistent: Persistence | None = None,
        kind: Kind = "entity",
        relationships: Sequence[Relationship] = (),
        intrinsic_rules: Sequence[Rule] = (),
        composite_constraints: Sequence[Constraint] = (),
        **kwargs: Any,
    ) -> None:
        """Accept the declaration keywords; ``__pydantic_init_subclass__`` acts on them."""
        super().__init_subclass__(**kwargs)

    @classmethod
    def __pydantic_init_subclass__(
        cls,
        *,
        description: str | None = None,
        persistent: Persistence | None = None,
        kind: Kind = "entity",
        relationships: Sequence[Relationship] = (),
        intrinsic_rules: Sequence[Rule] = (),
        composite_constraints: Sequence[Constraint] = (),
        **kwargs: Any,
    ) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if description is None or persistent is None:
            raise TypeError(
                f"{cls.__name__} must declare its description and whether it is persistent"
            )
        fields = tuple(
            _field_declaration(name, info) for name, info in cls.model_fields.items()
        )
        _unique("Field", [f.name for f in fields])
        _unique("Relationship", [r.name for r in relationships])
        _unique(
            "Constraint",
            [c.id for c in composite_constraints]
            + [c.id for f in fields for c in f.constraints],
        )
        _unique("Rule", [r.id for r in intrinsic_rules])
        cls.declaration = Declaration(
            id=cls.__name__,
            name=cls.__name__,
            description=description,
            kind=kind,
            persistent=persistent,
            fields=fields,
            relationships=tuple(relationships),
            intrinsic_rules=tuple(intrinsic_rules),
            composite_constraints=tuple(composite_constraints),
        )

    def serialize(self) -> dict[str, Any]:
        """Return the Plain Representation: named values expressible in JSON.

        Accepts nothing. Returns every Field by name; a relationship appears only as its
        declared reference value. Deterministic, data-only, no external I/O.
        """
        return self.model_dump(mode="json")

    @classmethod
    def deserialize(cls, data: Mapping[str, Any]) -> Self:
        """Build a validated instance from a Plain Representation.

        Applies the same validation as construction. Fails with ``ValidationError`` when the
        value is not a mapping, a Field is missing, unknown, or of a form the definition does
        not permit, or an Intrinsic Rule is not satisfied.
        """
        return cls.model_validate(data, strict=True, context={_PLAIN_CONTEXT: True})

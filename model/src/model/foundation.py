"""The Model Foundation: the one common foundation every Domain Definition builds on.

It supplies shared validation behaviour and the value types more than one Domain Definition
needs. It declares no Field and no relationship, so a definition states its complete
Target-derived set for itself.
"""

from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any, ClassVar, Self

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    Persistence,
    Relationship,
    declare_field,
)


def _reject_float(value: object) -> object:
    if isinstance(value, float):
        raise ValueError("an exact decimal must not be supplied as a floating point number")
    return value


def _to_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("an absolute instant must carry timezone information")
    return value.astimezone(UTC)


# Strictness is on by default so that coercion cannot hide invalid domain data. These two
# value types opt out only where a Plain Representation must be parsed back into the value:
# text is accepted for a decimal or an instant, and floating point is refused for a decimal.
ExactDecimal = Annotated[
    Decimal,
    Field(strict=False, allow_inf_nan=False),
    BeforeValidator(_reject_float),
]
Instant = Annotated[datetime, Field(strict=False), AfterValidator(_to_utc)]


class ModelFoundation(BaseModel):
    """Shared validation behaviour for every Domain Definition.

    Choices where the Target is silent: names a definition does not declare are refused rather
    than ignored; surrounding whitespace is removed from text; assignment to an existing instance
    is validated like construction; definitions are entities, so they are not frozen; and
    validation is strict, so a value of the wrong type is refused rather than converted.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        str_strip_whitespace=True,
        strict=True,
    )

    persistence: ClassVar[Persistence]
    relationships: ClassVar[tuple[Relationship, ...]] = ()
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """Refuse an incomplete declaration where the definition is written."""
        super().__pydantic_init_subclass__(**kwargs)
        if not isinstance(getattr(cls, "persistence", None), Persistence):
            raise TypeError(f"{cls.__name__} must state whether it is persistent or non-persistent")
        for relationship in cls.relationships:
            if relationship.via not in cls.model_fields:
                raise TypeError(
                    f"{cls.__name__}.{relationship.name} names {relationship.via!r}, "
                    "which the definition does not declare"
                )
        for unique_set in cls.unique_sets:
            unknown = [name for name in unique_set if name not in cls.model_fields]
            if unknown:
                raise TypeError(f"{cls.__name__} unique set names undeclared Fields {unknown}")
        if sum(d.activation for d in cls.field_declarations()) > 1:
            raise TypeError(f"{cls.__name__} declares more than one activation Field")

    @classmethod
    def declaration(cls) -> Declaration:
        """Return everything this definition has stated about itself."""
        return Declaration(
            name=cls.__name__,
            persistence=cls.persistence,
            fields=cls.field_declarations(),
            relationships=cls.relationships,
            unique_sets=cls.unique_sets,
        )

    @classmethod
    def field_declarations(cls) -> tuple[FieldDeclaration, ...]:
        """Return what this definition has stated about each of its Fields, in declaration order."""
        return tuple(declare_field(name, info) for name, info in cls.model_fields.items())

    def serialize(self) -> dict[str, Any]:
        """Return the Plain Representation: every Field as a simple, JSON-compatible value.

        A relationship appears only as its reference value, and no Field is withheld.
        """
        return self.model_dump(mode="json")

    @classmethod
    def deserialize(cls, data: Mapping[str, Any]) -> Self:
        """Return a validated instance from a Plain Representation.

        The same Intrinsic Rules apply as on construction; a violation raises a validation error.
        """
        return cls.model_validate(data)

"""The Model Foundation.

The one technology-independent foundation every Domain Definition receives shared mechanisms from:
validation behaviour, the Serialization pair that converts a definition to and from its Plain
Representation, and reading of the definition's declaration. It owns no domain Field and no relationship;
each Domain Definition declares its complete Target-derived set itself.

Everything here depends only on the data of the definition it acts on, is deterministic, and performs
no external I/O.

Recorded modelling choices
--------------------------
* Validation is strict by default, so a value of the wrong kind is never silently coerced into a valid
  one. Exact decimals and instants are exempt because their Plain Representation is text.
* Text values are trimmed of surrounding whitespace when validated, so " admin " and "admin" are the same
  value; this applies to every text Field, credentials included.
* A generated Field is absent until something else produces it; it is declared non-optional because the
  domain never allows it to be null once produced.
* A nullable Field without a Target-declared default may be omitted, in which case it holds no value; that
  absence is not reported as a declared default.
"""

from collections.abc import Mapping
from decimal import Decimal
from typing import Annotated, Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from model.vocabulary import (
    Activation,
    Credential,
    DefinitionDeclaration,
    FieldDeclaration,
    Generated,
    Identity,
    Persistence,
    Precision,
    Reference,
    RelationshipDeclaration,
    Unique,
    logical_type,
)

ExactDecimal = Annotated[Decimal, Field(strict=False)]
"""An exact decimal value; its Plain Representation is text, so it is exempt from strict validation."""

GeneratedIdentity = Annotated[int | None, Identity(), Generated()]
"""The identity of a record, produced by whatever stores it rather than supplied by the domain."""

ActiveFlag = Annotated[bool, Activation()]
"""The Field that says whether a record is active."""


def _metadata_value(info: FieldInfo, attribute: str) -> Any:
    for item in info.metadata:
        value = getattr(item, attribute, None)
        if value is not None:
            return value
    return None


def _declare_field(name: str, info: FieldInfo) -> FieldDeclaration:
    type_name, admits_none = logical_type(info.annotation)
    terms = info.metadata
    generated = any(isinstance(term, Generated) for term in terms)
    credentials = [term for term in terms if isinstance(term, Credential)]
    digits = _metadata_value(info, "max_digits")
    scale = _metadata_value(info, "decimal_places")
    has_default = info.default is not PydanticUndefined and not (
        info.default is None and admits_none
    )
    return FieldDeclaration(
        name=name,
        type=type_name,
        length=_metadata_value(info, "max_length"),
        precision=Precision(digits=digits, scale=scale)
        if digits is not None or scale is not None
        else None,
        optional=admits_none and not generated,
        has_default=has_default,
        default=info.default if has_default else None,
        identity=any(isinstance(term, Identity) for term in terms),
        generated=generated,
        unique=any(isinstance(term, Unique) for term in terms),
        credential=credentials[0].treatment if credentials else None,
        activation=any(isinstance(term, Activation) for term in terms),
    )


class ModelFoundation(BaseModel):
    """Base of every Domain Definition.

    A concrete definition declares ``persistence`` explicitly and, where the Target states one, its
    composite ``unique_sets``. Both are checked when the definition is written, so a broken declaration
    fails where it is declared.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        str_strip_whitespace=True,
        strict=True,
    )

    persistence: ClassVar[Persistence]
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "persistence" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must declare persistence as persistent or non-persistent"
            )
        if not isinstance(cls.__dict__["persistence"], Persistence):
            raise TypeError(f"{cls.__name__} persistence must be a Persistence value")
        for unique_set in cls.unique_sets:
            unknown = [name for name in unique_set if name not in cls.model_fields]
            if unknown:
                raise ValueError(
                    f"{cls.__name__} unique set names unknown Fields {unknown}"
                )
        declared = cls.declaration()
        if sum(field.activation for field in declared.fields) > 1:
            raise ValueError(f"{cls.__name__} declares more than one activation Field")
        for relationship in declared.relationships:
            field = next(f for f in declared.fields if f.name == relationship.field)
            if field.optional != relationship.optional:
                raise ValueError(
                    f"{cls.__name__}.{relationship.field} relationship optionality contradicts its Field"
                )

    def serialize(self) -> dict[str, Any]:
        """Convert this definition to its Plain Representation.

        Accepts nothing. Returns a dictionary of simple named values, one per Field, that any
        consumer can encode as JSON without a custom encoder: exact decimals and instants appear as
        text, and a relationship appears only as its reference value. No Field is withheld.
        Outcome: always succeeds for a valid instance.
        """
        return self.model_dump(mode="json")

    @classmethod
    def deserialize(cls, data: Mapping[str, Any]) -> Self:
        """Build a validated definition from a Plain Representation.

        Accepts a mapping of Field names to values. Returns a new instance of the definition.
        Outcomes: succeeds when every Intrinsic Rule holds; otherwise raises a ``ValidationError``
        whose errors name each offending Field. An unknown key, a missing required Field, a null in a
        Field that is not optional, and a value of the wrong kind are all rejected.
        """
        return cls.model_validate(data)

    @classmethod
    def declaration(cls) -> DefinitionDeclaration:
        """Read what this definition declares about itself.

        Accepts nothing. Returns a ``DefinitionDeclaration``: the definition's name, persistence,
        every Field's declared terms, its identity, its composite unique sets, and its relationships,
        each carrying the referenced definition itself. Outcome: always succeeds.
        """
        fields = tuple(
            _declare_field(name, info) for name, info in cls.model_fields.items()
        )
        relationships = tuple(
            RelationshipDeclaration(
                field=name,
                definition=term.definition,
                referenced_field=term.field,
                cardinality=term.cardinality,
                optional=term.optional,
            )
            for name, info in cls.model_fields.items()
            for term in info.metadata
            if isinstance(term, Reference)
        )
        return DefinitionDeclaration(
            name=cls.__name__,
            persistence=cls.persistence,
            fields=fields,
            identity=tuple(f.name for f in fields if f.identity),
            unique_sets=cls.unique_sets,
            relationships=relationships,
        )

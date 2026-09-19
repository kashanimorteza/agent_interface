"""Model Foundation: the mechanisms every Domain Definition shares.

The Foundation supplies validation, the Declaration Vocabulary, and the Serialization pair.
It never contributes a Field or a relationship to a Domain Definition.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from types import NoneType
from typing import Annotated, Any, ClassVar, Literal, Self, get_args

from pydantic import BaseModel, ConfigDict, StringConstraints, ValidationError
from pydantic_core import (
    InitErrorDetails,
    PydanticCustomError,
    PydanticUndefined,
    to_jsonable_python,
)

type LogicalType = Literal[
    "integer", "float", "string", "decimal", "boolean", "datetime"
]
type CredentialTreatment = Literal["hash", "encrypted"]
type Cardinality = Literal["many-to-one"]


@dataclass(frozen=True, slots=True)
class Reference:
    """A Domain Relationship: the referenced Domain Definition and its field."""

    definition: str
    field: str = "id"
    cardinality: Cardinality = "many-to-one"


@dataclass(frozen=True, slots=True)
class Declare:
    """The Declaration Vocabulary for one Field, carried in its annotation."""

    logical_type: LogicalType
    length: int | None = None
    precision: tuple[int, int] | None = None
    primary_key: bool = False
    generated: bool = False
    unique: bool = False
    credential: CredentialTreatment | None = None
    references: Reference | None = None


# Credentials are values, not text to tidy: whitespace is never stripped from them.
CredentialText = Annotated[str, StringConstraints(strip_whitespace=False)]


# A generated identity is absent until persistence generates it; its declaration is never nullable.
GeneratedId = Annotated[
    int | None, Declare("integer", primary_key=True, generated=True)
]


class RelationshipDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    definition: str
    field: str
    cardinality: Cardinality
    optional: bool


class FieldDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    logical_type: LogicalType
    length: int | None
    precision: tuple[int, int] | None
    nullable: bool
    has_default: bool
    default: Any
    primary_key: bool
    generated: bool
    unique: bool
    credential_treatment: CredentialTreatment | None
    relationship: RelationshipDeclaration | None


class DefinitionDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    persistent: bool
    fields: dict[str, FieldDeclaration]
    unique_sets: tuple[tuple[str, ...], ...]


class DomainDefinition(BaseModel):
    """Base of every Domain Definition; provides validation, declaration, and Serialization.

    Every Domain Definition offers four Operations.

    Construct — ``Definition(**fields)``
        Accepts the definition's Fields as keyword arguments. Returns a validated instance.
        Outcomes: an instance, or ``ValidationError`` when a Field is missing, unknown,
        of the wrong type, or breaks a declared property.
    Declaration — ``Definition.declaration()``
        Accepts nothing. Returns a ``DefinitionDeclaration``. Always succeeds.
    Serialize — ``instance.serialize()``
        Accepts nothing. Returns a ``dict`` of JSON-compatible named values. Always succeeds.
    Deserialize — ``Definition.deserialize(data)``
        Accepts a ``dict`` in the shape ``serialize`` returns. Returns a validated instance.
        Outcomes: an instance, or ``ValidationError`` when the data does not satisfy the definition.
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_assignment=True,
        validate_default=True,
        str_strip_whitespace=True,
    )

    persistent: ClassVar[bool]
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "persistent" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must declare `persistent` as True or False"
            )
        for name, field in cls.model_fields.items():
            if not any(isinstance(item, Declare) for item in field.metadata):
                raise TypeError(
                    f"{cls.__name__}.{name} has no Declaration Vocabulary entry"
                )
        for unique_set in cls.unique_sets:
            unknown = [name for name in unique_set if name not in cls.model_fields]
            if unknown:
                raise TypeError(
                    f"{cls.__name__} unique set names unknown fields: {unknown}"
                )

    @classmethod
    def declaration(cls) -> DefinitionDeclaration:
        """Publish this definition's Declaration Vocabulary.

        Accepts nothing. Returns a ``DefinitionDeclaration``. Always succeeds.
        """
        fields: dict[str, FieldDeclaration] = {}
        for name, field in cls.model_fields.items():
            declare = next(item for item in field.metadata if isinstance(item, Declare))
            allows_none = NoneType in get_args(field.annotation)
            nullable = allows_none and not declare.generated
            # A nullable Field left out resolves to null: that is this realization's omission rule,
            # not a default the Target declared, so it is never published as one.
            has_default = (
                not declare.generated
                and field.default is not PydanticUndefined
                and not (allows_none and field.default is None)
            )
            relationship = None
            if declare.references is not None:
                relationship = RelationshipDeclaration(
                    definition=declare.references.definition,
                    field=declare.references.field,
                    cardinality=declare.references.cardinality,
                    optional=nullable,
                )
            fields[name] = FieldDeclaration(
                logical_type=declare.logical_type,
                length=declare.length,
                precision=declare.precision,
                nullable=nullable,
                has_default=has_default,
                default=to_jsonable_python(field.default) if has_default else None,
                primary_key=declare.primary_key,
                generated=declare.generated,
                unique=declare.unique,
                credential_treatment=declare.credential,
                relationship=relationship,
            )
        return DefinitionDeclaration(
            name=cls.__name__,
            persistent=cls.persistent,
            fields=fields,
            unique_sets=cls.unique_sets,
        )

    def serialize(self) -> dict[str, Any]:
        """Return the Plain Representation: JSON-compatible named values, never encoded text.

        Accepts nothing. Returns a ``dict`` with every Field of the instance. Always succeeds.
        """
        return self.model_dump(mode="json")

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Self:
        """Build an instance from a Plain Representation, failing when an Intrinsic Rule is not met.

        Accepts a ``dict`` in the shape ``serialize`` returns: decimals as strings and datetimes
        as ISO 8601 strings. Returns a validated instance. Accepts and rejects exactly what
        construction does.

        Raises ``ValidationError`` when the data breaks any rule construction enforces,
        including a value of the wrong type or data that is not JSON-compatible.
        """
        try:
            text = json.dumps(data)
        except TypeError, ValueError:
            raise ValidationError.from_exception_data(
                cls.__name__,
                [
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "plain_representation",
                            "Input is not a JSON-compatible Plain Representation",
                        ),
                        loc=(),
                        input=data,
                    )
                ],
            ) from None
        errors: list[InitErrorDetails] = []
        if isinstance(data, dict):
            for name, logical_type in cls._string_form_fields().items():
                value = data.get(name)
                if value is None:
                    continue
                if not isinstance(value, str):
                    errors.append(
                        InitErrorDetails(type="string_type", loc=(name,), input=value)
                    )
                elif logical_type == "datetime" and not _is_iso_datetime(value):
                    errors.append(
                        InitErrorDetails(
                            type=PydanticCustomError(
                                "iso_datetime",
                                "Input should be an ISO 8601 datetime string",
                            ),
                            loc=(name,),
                            input=value,
                        )
                    )
        if errors:
            raise ValidationError.from_exception_data(cls.__name__, errors)
        # Validating the JSON form keeps decimals and datetimes as strings while every
        # type rule stays as strict as construction.
        return cls.model_validate_json(text, strict=True)

    @classmethod
    def _string_form_fields(cls) -> dict[str, str]:
        """Fields whose Plain Representation is a string: decimals and datetimes."""
        found: dict[str, str] = {}
        for name, field in cls.model_fields.items():
            for item in field.metadata:
                if isinstance(item, Declare) and item.logical_type in (
                    "decimal",
                    "datetime",
                ):
                    found[name] = item.logical_type
        return found


def _is_iso_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


__all__ = [
    "Cardinality",
    "CredentialText",
    "CredentialTreatment",
    "Declare",
    "DefinitionDeclaration",
    "DomainDefinition",
    "FieldDeclaration",
    "GeneratedId",
    "LogicalType",
    "Reference",
    "RelationshipDeclaration",
    "ValidationError",
]

"""Record the technology-independent meaning of Entities.

Declaration holds meaning and metadata only. It has no storage, transport, or workflow behaviour.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

NO_DEFAULT: Final = object()
"""Marks a Field that declares no Default Value, so that a default of `None`, `False`, or `0` stays distinguishable."""


class FieldType(StrEnum):
    """Technology-independent category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Value category of a sensitive Field. Declaration records it and never handles the value."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class Generation(StrEnum):
    """Way a Field value is supplied automatically when an Entity is created."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """Meaning and Field Rules of one Field.

    Attributes:
        name (str): Domain name of the Field.
        type (FieldType): Logical Type of the Field.
        nullable (bool): Whether the Field may hold no value.
        default (Any): Fixed Default Value, or `NO_DEFAULT` when none is declared.
        generation (Generation | None): Value Generation, mutually exclusive with a Default Value.
        sensitivity (Sensitivity | None): Optional sensitivity marker.
        immutable (bool): Whether the value may not change after creation.
        length (int | None): Maximum length of a string value.
        precision (int | None): Total number of significant digits of a decimal value.
        scale (int | None): Number of digits after the decimal point of a decimal value.
        minimum (int | float | None): Lowest permitted numeric value.
        maximum (int | float | None): Highest permitted numeric value.
        pattern (str | None): Pattern a string value must match.
        allowed_values (tuple[Any, ...] | None): Complete set of permitted values.
    """

    name: str
    type: FieldType
    nullable: bool = False
    default: Any = NO_DEFAULT
    generation: Generation | None = None
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    length: int | None = None
    precision: int | None = None
    scale: int | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None
    pattern: str | None = None
    allowed_values: tuple[Any, ...] | None = None

    def __post_init__(self) -> None:
        if self.has_default and self.generation is not None:
            raise ValueError(
                f"Field '{self.name}' cannot declare both a Default Value and Value Generation"
            )

    @property
    def has_default(self) -> bool:
        """Report whether a Default Value is declared."""
        return self.default is not NO_DEFAULT


@dataclass(frozen=True, slots=True)
class Reference:
    """Field-level reference that holds another Entity's `id`.

    Attributes:
        field (str): Field of the referring Entity that holds the value.
        entity (str): Name of the referenced Entity.
        target_field (str): Referenced Field, always `id`.
    """

    field: str
    entity: str
    target_field: str = "id"

    def __post_init__(self) -> None:
        if self.target_field != "id":
            raise ValueError(
                f"Reference '{self.field}' must identify the 'id' of '{self.entity}'"
            )


def _require_fields(kind: str, fields: tuple[str, ...]) -> None:
    if not fields or len(set(fields)) != len(fields):
        raise ValueError(f"{kind} must cover one or more distinct Fields, got {fields}")


@dataclass(frozen=True, slots=True)
class Unique:
    """Uniqueness Constraint over one Field or a declared combination of Fields.

    Attributes:
        fields (tuple[str, ...]): Names of the covered Fields.
    """

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_fields("Uniqueness Constraint", self.fields)


@dataclass(frozen=True, slots=True)
class Index:
    """Access intention over one Field or a declared combination of Fields.

    Attributes:
        fields (tuple[str, ...]): Names of the covered Fields.
    """

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_fields("Index", self.fields)


@dataclass(frozen=True, slots=True)
class Declaration:
    """Complete technology-independent meaning of one Entity.

    Attributes:
        entity (str): Domain name of the Entity.
        fields (tuple[FieldDeclaration, ...]): Every Field, including the `id` Identity.
        references (tuple[Reference, ...]): Every connection to another Entity.
        uniques (tuple[Unique, ...]): Every Uniqueness Constraint.
        indexes (tuple[Index, ...]): Every Index intention.
    """

    entity: str
    fields: tuple[FieldDeclaration, ...]
    references: tuple[Reference, ...] = ()
    uniques: tuple[Unique, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        names = [f.name for f in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(
                f"Entity '{self.entity}' declares a Field name more than once"
            )
        if "id" not in names or self.identity.nullable:
            raise ValueError(
                f"Entity '{self.entity}' must declare a non-nullable 'id' Identity"
            )
        covered = [r.field for r in self.references] + [
            n for c in (*self.uniques, *self.indexes) for n in c.fields
        ]
        if unknown := set(covered) - set(names):
            raise ValueError(
                f"Entity '{self.entity}' refers to undeclared Fields {sorted(unknown)}"
            )

    @property
    def primary_key(self) -> str:
        """Name of the Primary Key Field, always `id`."""
        return "id"

    @property
    def identity(self) -> FieldDeclaration:
        """Declaration of the `id` Identity Field."""
        return self.field(self.primary_key)

    def field(self, name: str) -> FieldDeclaration:
        """Return the declaration of one Field.

        Args:
            name (str): Name of the Field.

        Returns:
            (FieldDeclaration): The declared Field.
        """
        return next(f for f in self.fields if f.name == name)

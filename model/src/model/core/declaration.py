"""Public logical contract: what an Entity and each of its Fields mean."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType


class FieldType(StrEnum):
    """Logical value category of a Field."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Recognized Sensitivity Marker; records value meaning and causes no protection."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class ValueGeneration(StrEnum):
    """Declared way a Field value is supplied automatically by its owner."""

    AUTO_INCREMENT = "auto_increment"


@dataclass(frozen=True)
class Relation:
    """Entity Metadata connecting one local Field to a target Entity and Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True)
class FieldDeclaration:
    """Complete public record of one Field.

    Attributes:
        name: Logical Field name.
        description: Purpose of the Field, if the Target states one.
        type: Logical value category.
        nullable: Whether null is a valid value.
        has_default: Whether a Default Value is declared; distinct from a null default.
        default: The Default Value when has_default is true.
        sensitivity: Recognized Sensitivity Marker, if any.
        immutable: Whether the value cannot change once assigned.
        constraints: Applicable value constraints, read-only.
        value_generation: Declared automatic value supply, if any.
    """

    name: str
    description: str | None
    type: FieldType
    nullable: bool
    has_default: bool = False
    default: object = None
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: Mapping[str, int] = field(default_factory=lambda: MappingProxyType({}))
    value_generation: ValueGeneration | None = None


@dataclass(frozen=True)
class Declaration:
    """Complete public record of one Entity.

    Attributes:
        name: Logical Entity name.
        description: Purpose of the Entity.
        fields: Fields in Target order.
        primary_key: Name of the identity Field.
        relations: Relations to other Entities.
        unique_constraints: Ordered Field names that must be unique together.
        indexes: Ordered Field names with an access intention.
    """

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

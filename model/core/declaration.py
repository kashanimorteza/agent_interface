from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .logical_type import LogicalType


class Sensitivity(StrEnum):
    """Value category marker carried by a Field Declaration."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class ValueGeneration(StrEnum):
    """Declared way a Field value is supplied automatically at Entity creation."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


@dataclass(frozen=True)
class FieldDeclaration:
    """Canonical record of one Field.

    Attributes:
        name (str): Exact Target Field name.
        type (LogicalType): Logical Type of the value.
        nullable (bool): Whether the Field may hold null.
        has_default (bool): Whether a Default Value is declared; an explicit null default is present.
        default (Any): Declared Default Value, meaningful only when has_default is true.
        immutable (bool): Whether the value cannot change once assigned.
        description (str | None): Domain meaning of the Field.
        sensitivity (Sensitivity | None): Declared sensitivity marker.
        length (int | None): Maximum number of characters of a string value.
        minimum (Any): Smallest permitted value of an ordered Type.
        maximum (Any): Largest permitted value of an ordered Type.
        pattern (str | None): Pattern a string value must match.
        precision (int | None): Total digits of a decimal value.
        scale (int | None): Fractional digits of a decimal value.
        allowed_values (tuple[Any, ...] | None): Complete set of permitted values.
        value_generation (ValueGeneration | None): Declared automatic value supply.
    """

    name: str
    type: LogicalType
    nullable: bool
    has_default: bool
    default: Any
    immutable: bool
    description: str | None = None
    sensitivity: Sensitivity | None = None
    length: int | None = None
    minimum: Any = None
    maximum: Any = None
    pattern: str | None = None
    precision: int | None = None
    scale: int | None = None
    allowed_values: tuple[Any, ...] | None = None
    value_generation: ValueGeneration | None = None


@dataclass(frozen=True)
class Relation:
    """Connection from one local Field to a Field of another Entity, recorded by name only.

    Attributes:
        local_field (str): Field of the declaring Entity.
        target_entity (str): Exact Target name of the related Entity.
        target_field (str): Field of the related Entity.
    """

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True)
class Declaration:
    """Canonical record of one Entity's meaning and Entity Metadata.

    Attributes:
        name (str): Exact Target Entity name.
        description (str): Domain meaning of the Entity.
        fields (tuple[FieldDeclaration, ...]): Field Declarations in Target order.
        primary_key (str): Name of the identity Field.
        relations (tuple[Relation, ...]): Declared Relations.
        unique_constraints (tuple[tuple[str, ...], ...]): Ordered Field names of each Uniqueness Constraint.
        indexes (tuple[tuple[str, ...], ...]): Ordered Field names of each Index.
    """

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...]
    unique_constraints: tuple[tuple[str, ...], ...]
    indexes: tuple[tuple[str, ...], ...]

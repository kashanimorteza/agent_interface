"""Technology-independent meaning of Model Entities.

Declaration records what an Entity means: its Fields, Types, Field Rules, Primary Key,
Uniqueness Constraints, References, Index intentions, and Value Generation. It holds
structured data only and provides no runtime behaviour.
"""

from dataclasses import dataclass, field
from enum import StrEnum


class _NoDefault:
    """Marker type for a Field whose Target declares no default."""

    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT = _NoDefault()


class LogicalType(StrEnum):
    """Technology-independent category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    FLOAT = "float"
    DATETIME = "datetime"


class ValueGeneration(StrEnum):
    """Declared way to supply a Field value automatically."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"
    GENERATED_TIMESTAMP = "generated_timestamp"


@dataclass(frozen=True)
class FieldDeclaration:
    """One named value of an Entity with its Field Rules.

    Attributes:
        name (str): Field name.
        type (LogicalType): Logical Type of the Field.
        nullable (bool): Whether the Field may hold no value.
        default (object): Declared default (including false and None), or `NO_DEFAULT` when the Target declares none.
        sensitive (bool): Whether the Field carries data whose handling is decided outside Model.
        immutable (bool): Whether the Field value may never change after creation.
        length (int | None): Declared maximum length, when declared.
        constraints (dict[str, object]): Any other declared restriction, keyed by its kind.
        generation (ValueGeneration | None): Declared Value Generation, when declared.
    """

    name: str
    type: LogicalType
    nullable: bool = False
    default: object = NO_DEFAULT
    sensitive: bool = False
    immutable: bool = False
    length: int | None = None
    constraints: dict[str, object] = field(default_factory=dict)
    generation: ValueGeneration | None = None


@dataclass(frozen=True)
class ReferenceDeclaration:
    """Field-level expression of a Relationship to another Entity.

    Attributes:
        field (str): Name of the referencing Field.
        entity (str): Name of the referenced Entity.
        target_field (str): Name of the referenced identity Field.
    """

    field: str
    entity: str
    target_field: str = "id"


@dataclass(frozen=True)
class ModelDeclaration:
    """Complete technology-independent meaning of one Entity.

    Attributes:
        entity (str): Entity name.
        fields (tuple[FieldDeclaration, ...]): Every Field of the Entity.
        primary_key (tuple[str, ...]): Field names that form the Identity.
        references (tuple[ReferenceDeclaration, ...]): Every declared Reference.
        unique_constraints (tuple[tuple[str, ...], ...]): Field combinations that must hold no duplicate.
        indexes (tuple[tuple[str, ...], ...]): Field combinations with a declared access intention.
    """

    entity: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: tuple[str, ...]
    references: tuple[ReferenceDeclaration, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

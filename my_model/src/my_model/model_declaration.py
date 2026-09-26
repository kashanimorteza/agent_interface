"""Technology-independent meaning of Model Entities.

Declaration records what an Entity means: its Fields and Types, Field Rules, Primary Key,
Relationships, Uniqueness Constraints, Index intentions, and Value Generation. It provides no
runtime behaviour; every record is immutable data.
"""

from dataclasses import dataclass
from enum import StrEnum


class LogicalType(StrEnum):
    """Technology-independent category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    FLOAT = "float"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Sensitivity classification of a Field."""

    NONE = "none"
    CREDENTIAL = "credential"


class AtRest(StrEnum):
    """Storage treatment the Target requires for a sensitive Field at rest."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class ValueGeneration(StrEnum):
    """Declared way to supply a Field value automatically."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"
    GENERATED_TIMESTAMP = "generated_timestamp"


class RelationshipKind(StrEnum):
    """Domain meaning of a Relationship from one Entity to another."""

    BELONGS_TO = "belongs_to"
    USES = "uses"


@dataclass(frozen=True)
class FieldDeclaration:
    """Meaning and Field Rules of one Field.

    Attributes:
        name: Field name.
        type: Logical Type of the Field's values.
        nullable: Whether the Field may be absent.
        has_default: Whether the Target declares a default; distinguishes a declared None.
        default: Declared default value when has_default is set.
        size: Declared size of a string Field.
        sensitivity: Sensitivity classification.
        at_rest: Storage treatment the Target requires for a sensitive Field.
        immutable: Whether the Field may not change after creation.
        generation: Declared Value Generation.
        purpose: Domain meaning of the Field.
    """

    name: str
    type: LogicalType
    nullable: bool = False
    has_default: bool = False
    default: object = None
    size: int | None = None
    sensitivity: Sensitivity = Sensitivity.NONE
    at_rest: AtRest | None = None
    immutable: bool = False
    generation: ValueGeneration | None = None
    purpose: str = ""


@dataclass(frozen=True)
class Reference:
    """Relationship expressed at Field level.

    Attributes:
        field: Field that holds the reference.
        entity: Name of the referenced Entity.
        identity: Field of the referenced Entity that the reference identifies.
        kind: Domain meaning of the Relationship.
    """

    field: str
    entity: str
    identity: str
    kind: RelationshipKind


@dataclass(frozen=True)
class UniquenessConstraint:
    """Condition that a Field, or a combination of Fields, has no duplicate value.

    Attributes:
        fields: Names of the Fields covered.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True)
class Index:
    """Declared access intention for a Field or a combination of Fields.

    Attributes:
        fields: Names of the Fields covered.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True)
class ModelDeclaration:
    """Complete technology-independent meaning of one Entity.

    Attributes:
        entity: Entity name.
        purpose: Domain meaning of the Entity.
        fields: Every Field of the Entity.
        primary_key: Names of the Fields that form the Identity.
        references: Every Relationship to another Entity.
        unique_constraints: Every Uniqueness Constraint.
        indexes: Every Index intention.
    """

    entity: str
    purpose: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: tuple[str, ...] = ("id",)
    references: tuple[Reference, ...] = ()
    unique_constraints: tuple[UniquenessConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

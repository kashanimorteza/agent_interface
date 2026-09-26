"""Technology-independent records of Entity meaning. Data only, no runtime behaviour."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class FieldType(StrEnum):
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
    """Protection a credential Field must receive when stored, as declared by the Target."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class GenerationKind(StrEnum):
    """Declared way a Field value is supplied automatically."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"
    GENERATED_TIMESTAMP = "generated_timestamp"


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """One named value of an Entity with its logical Type and Field Rules.

    Attributes:
        name (str): Field name.
        type (FieldType): Logical Type of the value.
        purpose (str): Domain meaning of the Field.
        nullable (bool): Whether the value may be absent.
        required (bool): Whether a value must be supplied because the Field has neither a default nor Value Generation.
        default (bool | int | float | str | Decimal | None): Declared default; None when none is declared or the default is null.
        max_length (int | None): Declared maximum length of a string value.
        sensitivity (Sensitivity): Sensitivity classification.
        at_rest (AtRest | None): Protection the Target requires for a credential Field at rest; realized outside Model.
        immutable (bool): Whether the value may never change after it is first set.
    """

    name: str
    type: FieldType
    purpose: str
    nullable: bool = False
    required: bool = True
    default: bool | int | float | str | Decimal | None = None
    max_length: int | None = None
    sensitivity: Sensitivity = Sensitivity.NONE
    at_rest: AtRest | None = None
    immutable: bool = False


@dataclass(frozen=True, slots=True)
class Reference:
    """Field-level expression of a Relationship to another Entity.

    Attributes:
        field (str): Field holding the reference.
        entity (str): Name of the referenced Entity.
        identity (str): Field of the referenced Entity that the value identifies.
    """

    field: str
    entity: str
    identity: str = "id"


@dataclass(frozen=True, slots=True)
class Generation:
    """Value Generation declared for one Field.

    Attributes:
        field (str): Field whose value is generated.
        kind (GenerationKind): Declared way the value is supplied.
    """

    field: str
    kind: GenerationKind


@dataclass(frozen=True, slots=True)
class Declaration:
    """Complete technology-independent meaning of one Entity.

    Attributes:
        entity (str): Entity name.
        purpose (str): Domain meaning of the Entity.
        fields (tuple[FieldDeclaration, ...]): Every Field in declaration order.
        primary_key (tuple[str, ...]): Fields that form the Identity.
        unique (tuple[tuple[str, ...], ...]): Every Uniqueness Constraint, each over one Field or a combination of Fields.
        references (tuple[Reference, ...]): Every Relationship to another Entity.
        indexes (tuple[tuple[str, ...], ...]): Declared Index intentions, each over one Field or a combination of Fields.
        generation (tuple[Generation, ...]): Declared Value Generation.
        rules (tuple[str, ...]): Target-declared rules that depend on other Entities and cannot be evaluated from this Entity alone.
    """

    entity: str
    purpose: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: tuple[str, ...] = ("id",)
    unique: tuple[tuple[str, ...], ...] = ()
    references: tuple[Reference, ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()
    generation: tuple[Generation, ...] = ()
    rules: tuple[str, ...] = ()

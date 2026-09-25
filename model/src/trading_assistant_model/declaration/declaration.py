"""Technology-independent vocabulary that records an Entity's data meaning.

Everything here is plain data. Declaration holds meaning and provides no runtime
behaviour: validation and conversion belong to Foundation, and physical storage
choices belong to Database.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import Any


class Omitted(Enum):
    """Marker for a property the definition does not state.

    An omitted property is distinct from an explicit ``None`` or ``False``.
    """

    OMITTED = "omitted"


OMITTED = Omitted.OMITTED


class FieldType(StrEnum):
    """Logical Type of a Field, independent of any language or database."""

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


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """Meaning of one Field of a Domain Entity.

    Every property except ``name`` and ``type`` is ``OMITTED`` unless stated.

    Attributes:
        name: Field name.
        type: Logical Type.
        nullable: Whether the Field may hold null.
        default: Value used when the Field is omitted; an explicit ``None`` is a null default.
        sensitive: Whether the value is a credential that must never be exposed.
        immutable: Whether the value cannot change after construction.
        length: Maximum length of a string value.
        restrictions: Any further declared restriction (range, pattern, precision, scale,
            allowed values, or comparable), keyed by the restriction's name.
        generation: Declared automatic supply of the value.
    """

    name: str
    type: FieldType
    nullable: bool | Omitted = OMITTED
    default: Any = OMITTED
    sensitive: bool | Omitted = OMITTED
    immutable: bool | Omitted = OMITTED
    length: int | Omitted = OMITTED
    restrictions: Mapping[str, Any] = field(default_factory=dict)
    generation: ValueGeneration | Omitted = OMITTED


@dataclass(frozen=True, slots=True)
class UniqueConstraint:
    """Uniqueness over one Field or a combination of Fields.

    Attributes:
        fields: Names of the Fields whose combined value must not repeat.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Reference:
    """Relationship from this Entity to another, expressed at Field level.

    Attributes:
        fields: Names of this Entity's Fields that hold the reference.
        entity: Name of the target Entity.
        identity: Names of the target Entity's Fields that the reference identifies.
    """

    fields: tuple[str, ...]
    entity: str
    identity: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Index:
    """Access intention over one Field or a combination of Fields.

    Attributes:
        fields: Names of the Fields covered by the intention.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Declaration:
    """Complete technology-independent meaning of one Domain Entity.

    Attributes:
        entity: Name of the Domain Entity.
        fields: Meaning of every Field, in declared order.
        primary_key: Names of the Fields that form the Identity.
        unique_constraints: Declared Uniqueness Constraints.
        references: Declared Relationships to other Entities.
        indexes: Declared Index intentions.
    """

    entity: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: tuple[str, ...]
    unique_constraints: tuple[UniqueConstraint, ...] = ()
    references: tuple[Reference, ...] = ()
    indexes: tuple[Index, ...] = ()

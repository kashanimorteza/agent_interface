"""Canonical logical records that describe Entity meaning and Entity Metadata."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import Any


class FieldType(StrEnum):
    """Target-defined categories of values a Field may hold."""

    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Value categories a Field may be marked with."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class ValueGeneration(StrEnum):
    """Ways a Field value is supplied automatically when an Entity is created."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


@dataclass(frozen=True, slots=True)
class Constraints:
    """Value constraints of a Field; an absent constraint is None.

    Attributes:
        length: Maximum number of characters of a string value.
        minimum: Smallest permitted numeric value.
        maximum: Largest permitted numeric value.
        pattern: Regular expression a string value must match completely.
        precision: Maximum number of significant digits of a decimal value.
        scale: Maximum number of fractional digits of a decimal value.
        allowed_values: The only values the Field may hold.
    """

    length: int | None = None
    minimum: int | float | Decimal | None = None
    maximum: int | float | Decimal | None = None
    pattern: str | None = None
    precision: int | None = None
    scale: int | None = None
    allowed_values: tuple[Any, ...] | None = None


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """Canonical logical record of one Field.

    Attributes:
        name: Exact Target name of the Field.
        type: Target-declared Type.
        nullable: Whether the Field may hold null.
        description: Optional description of the Field.
        has_default: Whether a Default Value is declared, including an explicit null.
        default: The Default Value; meaningful only when has_default is true.
        sensitivity: Optional sensitivity marker.
        immutable: Whether the Field cannot change once it holds a value.
        constraints: Value constraints of the Field.
        value_generation: Optional automatic value generation.
    """

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    has_default: bool = False
    default: Any = None
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: Constraints = field(default_factory=Constraints)
    value_generation: ValueGeneration | None = None


@dataclass(frozen=True, slots=True)
class Relation:
    """Entity Metadata connecting one local Field to a target Field by name.

    Attributes:
        local_field: Name of the Field in the declaring Entity.
        target_entity: Name of the related Entity.
        target_field: Name of the Field in the related Entity.
    """

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True)
class UniqueConstraint:
    """Entity Metadata requiring a Field combination to have no duplicate value.

    Attributes:
        fields: Ordered names of the participating Fields.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Index:
    """Entity Metadata declaring an access intention for a Field combination.

    Attributes:
        fields: Ordered names of the participating Fields.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Declaration:
    """Canonical logical record of one Entity.

    Attributes:
        name: Exact Target name of the Entity.
        description: Description of the Entity.
        fields: Field Declarations in Target order.
        primary_key: Name of the Field that identifies an Entity.
        relations: Relations of the Entity.
        unique_constraints: Uniqueness Constraints of the Entity.
        indexes: Indexes of the Entity.
    """

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniqueConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        """Reject a Declaration whose vocabulary or structure is invalid."""
        errors: list[str] = []
        names = [f.name for f in self.fields]
        for name in dict.fromkeys(n for n in names if names.count(n) > 1):
            errors.append(f"{self.name}.{name}: Field name is declared more than once")
        for f in self.fields:
            errors.extend(_field_errors(self.name, f))
        errors.extend(self._contract_errors(names))
        errors.extend(self._metadata_errors(names))
        if errors:
            raise ValueError("\n".join(errors))

    def _contract_errors(self, names: list[str]) -> list[str]:
        errors: list[str] = []
        by_name = {f.name: f for f in self.fields}
        if "id" not in by_name:
            errors.append(f"{self.name}: the id Field is not declared")
        if self.primary_key != "id":
            errors.append(f"{self.name}: the Primary Key must name the id Field")
        active = by_name.get("is_active")
        if active is None or active.type != FieldType.BOOLEAN or active.nullable:
            errors.append(
                f"{self.name}.is_active: a non-nullable boolean Field is required"
            )
        return errors

    def _metadata_errors(self, names: list[str]) -> list[str]:
        errors: list[str] = []
        groups = [
            ("Uniqueness Constraint", [c.fields for c in self.unique_constraints]),
            ("Index", [i.fields for i in self.indexes]),
        ]
        for label, declared in groups:
            for position, fields in enumerate(declared):
                errors.extend(
                    f"{self.name}: {label} names unknown Field {n}"
                    for n in fields
                    if n not in names
                )
                if len(set(fields)) != len(fields):
                    errors.append(f"{self.name}: {label} repeats a Field")
                if declared.index(fields) != position:
                    errors.append(f"{self.name}: {label} is declared more than once")
        errors.extend(
            f"{self.name}: Relation names unknown Field {r.local_field}"
            for r in self.relations
            if r.local_field not in names
        )
        if len(set(self.relations)) != len(self.relations):
            errors.append(f"{self.name}: a Relation is declared more than once")
        return errors


def _field_errors(entity: str, f: FieldDeclaration) -> list[str]:
    errors: list[str] = []
    for label, enum, value in (
        ("Type", FieldType, f.type),
        ("sensitivity marker", Sensitivity, f.sensitivity),
        ("Value Generation", ValueGeneration, f.value_generation),
    ):
        if value is not None and value not in tuple(enum):
            errors.append(f"{entity}.{f.name}: unknown {label}")
    if f.has_default and f.value_generation is not None:
        errors.append(
            f"{entity}.{f.name}: a Field cannot have both a Default Value and Value Generation"
        )
    if not f.has_default and f.default is not None:
        errors.append(
            f"{entity}.{f.name}: a default is given but no Default Value is declared"
        )
    if f.has_default and f.default is None and not f.nullable:
        errors.append(
            f"{entity}.{f.name}: an explicit null Default Value requires a nullable Field"
        )
    if (
        f.value_generation == ValueGeneration.AUTO_INCREMENT
        and f.type != FieldType.INTEGER
    ):
        errors.append(f"{entity}.{f.name}: Auto Increment requires an integer Field")
    if (
        f.value_generation == ValueGeneration.GENERATED_IDENTIFIER
        and f.type != FieldType.STRING
    ):
        errors.append(
            f"{entity}.{f.name}: a generated identifier requires a string Field"
        )
    return errors

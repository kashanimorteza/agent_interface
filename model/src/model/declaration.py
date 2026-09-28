"""Declaration layer: records the technology-independent meaning and metadata of every Entity."""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic_core import PydanticUndefined
from sqlalchemy import Index, UniqueConstraint
from sqlmodel import Field, SQLModel

_INFO_KEY = "declaration"


class Type(StrEnum):
    """Technology-independent category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Value category marker; Model records it and never inspects or transforms the value."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class Generation(StrEnum):
    """Way a Field value is supplied automatically when an Entity is created."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


@dataclass(frozen=True)
class Reference:
    """Field-level Reference to another Entity's identity."""

    entity: str
    target: str = "id"


@dataclass(frozen=True)
class FieldDeclaration:
    """Complete declared meaning of one Field."""

    name: str
    type: Type
    nullable: bool
    has_default: bool
    default: Any
    sensitivity: Sensitivity | None
    immutable: bool
    length: int | None
    minimum: Any
    maximum: Any
    pattern: str | None
    precision: int | None
    scale: int | None
    allowed: tuple[Any, ...] | None
    generation: Generation | None
    reference: Reference | None
    description: str | None


@dataclass(frozen=True)
class EntityDeclaration:
    """Complete declared meaning of one Entity."""

    name: str
    primary_key: str
    fields: tuple[FieldDeclaration, ...]
    uniques: tuple[tuple[str, ...], ...]
    indexes: tuple[tuple[str, ...], ...]

    @property
    def references(self) -> tuple[tuple[str, Reference], ...]:
        """Every Field that holds a Reference, paired with that Reference."""
        return tuple((f.name, f.reference) for f in self.fields if f.reference)


_TYPES: tuple[tuple[type, Type], ...] = (
    (bool, Type.BOOLEAN),
    (int, Type.INTEGER),
    (float, Type.FLOAT),
    (Decimal, Type.DECIMAL),
    (datetime, Type.DATETIME),
    (str, Type.STRING),
)


def _type_of(annotation: Any) -> Type:
    """Map a Field annotation, ignoring `None`, to its logical Type."""
    kinds = [
        a for a in getattr(annotation, "__args__", (annotation,)) if a is not type(None)
    ]
    return next(logical for python, logical in _TYPES if kinds[0] is python)


class Declaration:
    """Declare Field and Entity metadata, and read the declaration of a published Entity."""

    @staticmethod
    def field(
        *,
        nullable: bool = False,
        default: Any = PydanticUndefined,
        sensitivity: Sensitivity | None = None,
        immutable: bool = False,
        length: int | None = None,
        minimum: Any = None,
        maximum: Any = None,
        pattern: str | None = None,
        precision: int | None = None,
        scale: int | None = None,
        allowed: tuple[Any, ...] | None = None,
        generation: Generation | None = None,
        reference: type[SQLModel] | None = None,
        unique: bool = False,
        index: bool = False,
        primary_key: bool = False,
        description: str | None = None,
    ) -> Any:
        """Declare one Field.

        Args:
            nullable (bool): Whether the Field may hold no value.
            default (Any): Fixed Default Value applied when the Field is omitted.
            sensitivity (Sensitivity, optional): Sensitivity marker.
            immutable (bool): Whether the Field may not change after creation.
            length (int, optional): Maximum length.
            minimum (Any, optional): Smallest allowed value.
            maximum (Any, optional): Largest allowed value.
            pattern (str, optional): Pattern the value must match.
            precision (int, optional): Total number of digits of a decimal.
            scale (int, optional): Number of fractional digits of a decimal.
            allowed (tuple, optional): The only values the Field may hold.
            generation (Generation, optional): Value Generation.
            reference (type, optional): Entity whose identity the Field holds.
            unique (bool): Whether the Field alone must have no duplicate value.
            index (bool): Whether an Index is intended on the Field.
            primary_key (bool): Whether the Field is the Primary Key.
            description (str, optional): Purpose of the Field.

        Returns:
            (Any): The Field definition to assign to the Entity attribute.

        Raises:
            ValueError: If both a Default Value and Value Generation are declared.
        """
        has_default = default is not PydanticUndefined
        if has_default and generation:
            raise ValueError(
                "A Field never declares both a Default Value and Value Generation."
            )
        declared = {
            "nullable": nullable,
            "has_default": has_default,
            "default": default if has_default else None,
            "sensitivity": sensitivity,
            "immutable": immutable,
            "length": length,
            "minimum": minimum,
            "maximum": maximum,
            "pattern": pattern,
            "precision": precision,
            "scale": scale,
            "allowed": allowed,
            "generation": generation,
            "reference": reference.__name__ if reference else None,
            "description": description,
        }
        value: dict[str, Any] = {}
        if has_default:
            value["default"] = default
        elif generation is Generation.GENERATED_IDENTIFIER:
            value["default_factory"] = lambda: str(uuid.uuid4())
        elif nullable or generation is Generation.AUTO_INCREMENT:
            value["default"] = None
        return Field(
            **value,
            primary_key=primary_key,
            nullable=nullable,
            unique=unique,
            index=index,
            foreign_key=f"{reference.__tablename__}.id" if reference else None,
            max_length=length,
            ge=minimum,
            le=maximum,
            regex=pattern,
            max_digits=precision,
            decimal_places=scale,
            description=description,
            sa_column_kwargs={"info": {_INFO_KEY: declared}},
        )

    @staticmethod
    def identity(generation: Generation = Generation.AUTO_INCREMENT) -> Any:
        """Declare the `id` Identity, which is also the Primary Key.

        Args:
            generation (Generation): Value Generation that supplies the identity.

        Returns:
            (Any): The Field definition to assign to `id`.
        """
        return Declaration.field(primary_key=True, generation=generation)

    @staticmethod
    def composite(
        entity: str,
        *,
        unique: tuple[tuple[str, ...], ...] = (),
        index: tuple[tuple[str, ...], ...] = (),
    ) -> tuple[UniqueConstraint | Index, ...]:
        """Declare Uniqueness Constraints and Indexes over combinations of Fields.

        Args:
            entity (str): Name of the Entity that owns them.
            unique (tuple): Field combinations that must have no duplicate value.
            index (tuple): Field combinations with an Index intention.

        Returns:
            (tuple): The value to assign to the Entity's table arguments.
        """
        return (
            *(
                UniqueConstraint(*f, name=f"uq_{entity.lower()}_{'_'.join(f)}")
                for f in unique
            ),
            *(Index(f"ix_{entity.lower()}_{'_'.join(f)}", *f) for f in index),
        )

    @staticmethod
    def of(entity: type[SQLModel]) -> EntityDeclaration:
        """Read the complete declaration of an Entity.

        Args:
            entity (type): Published Entity class.

        Returns:
            (EntityDeclaration): The Entity's declared meaning.
        """
        table = entity.__table__  # type: ignore[attr-defined]
        fields = []
        for name, info in entity.model_fields.items():
            declared = dict(table.c[name].info[_INFO_KEY])
            fields.append(
                FieldDeclaration(
                    name=name,
                    type=_type_of(info.annotation),
                    **{
                        **declared,
                        "reference": Reference(declared["reference"])
                        if declared["reference"]
                        else None,
                    },
                )
            )
        position = {name: i for i, name in enumerate(entity.model_fields)}

        def ordered(columns: Any) -> tuple[tuple[str, ...], ...]:
            found = {tuple(c.name for c in group) for group in columns}
            return tuple(
                sorted(found, key=lambda g: (len(g), [position[n] for n in g]))
            )

        return EntityDeclaration(
            name=entity.__name__,
            primary_key=next(iter(table.primary_key.columns)).name,
            fields=tuple(fields),
            uniques=ordered(
                u.columns for u in table.constraints if isinstance(u, UniqueConstraint)
            ),
            indexes=ordered(i.columns for i in table.indexes),
        )

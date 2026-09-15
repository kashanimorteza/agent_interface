"""Model Foundation: shared mechanisms for every concrete Domain Definition.

The Foundation provides validation, serialization, and metadata-publishing
mechanisms common to every Domain Definition. It never declares a Field or a
Domain Relationship itself; each concrete Domain Definition declares its own
complete set of Fields and relationships.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict


class Credential(StrEnum):
    """The required at-rest treatment for a credential field."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class ForeignKey(BaseModel):
    """Technology-independent reference from one Domain Definition field to another."""

    model_config = ConfigDict(frozen=True)

    target: str
    field: str = "id"
    cardinality: str = "many_to_one"


class DomainModel(BaseModel):
    """Common foundation shared by every concrete Domain Definition.

    Publishes storage-relevant meaning (identity, uniqueness, nullability,
    defaults, foreign keys, cardinality, and credential treatment) as
    technology-independent metadata for Database consumption, without owning
    persistence itself.
    """

    model_config = ConfigDict(
        strict=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    __persistent__: ClassVar[bool] = True
    __primary_key__: ClassVar[tuple[str, ...]] = ("id",)
    __auto_increment__: ClassVar[tuple[str, ...]] = ("id",)
    __unique__: ClassVar[tuple[str, ...]] = ()
    __unique_sets__: ClassVar[tuple[tuple[str, ...], ...]] = ()
    __foreign_keys__: ClassVar[dict[str, ForeignKey]] = {}
    __credentials__: ClassVar[dict[str, Credential]] = {}

    @classmethod
    def persistence_metadata(cls) -> dict[str, Any]:
        """Publish this Domain Definition's technology-independent persistence meaning.

        Conceptual only: identity, uniqueness, nullability, defaults, foreign
        keys, cardinality, and credential treatment. Physical mapping,
        migration, and enforcement remain owned by Database.
        """

        fields: dict[str, Any] = {}
        for name, field_info in cls.model_fields.items():
            fields[name] = {
                "nullable": _is_nullable(field_info.annotation),
                "required": field_info.is_required(),
                "default": None if field_info.is_required() else field_info.get_default(),
            }

        return {
            "persistent": cls.__persistent__,
            "primary_key": cls.__primary_key__,
            "auto_increment": cls.__auto_increment__,
            "unique": cls.__unique__,
            "unique_sets": cls.__unique_sets__,
            "foreign_keys": {name: fk.model_dump() for name, fk in cls.__foreign_keys__.items()},
            "credentials": {
                name: credential.value for name, credential in cls.__credentials__.items()
            },
            "fields": fields,
        }


def _is_nullable(annotation: Any) -> bool:
    return annotation is not None and type(None) in getattr(annotation, "__args__", ())

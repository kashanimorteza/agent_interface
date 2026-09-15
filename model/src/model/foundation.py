"""Shared Model Foundation.

Gives every concrete Domain Definition common validation, serialization, and
metadata-publishing mechanisms, without owning or injecting any Field or
Domain Relationship of its own.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic_core import PydanticUndefined


def field_meta(
    *,
    nullable: bool = False,
    primary_key: bool = False,
    auto_increment: bool = False,
    unique: bool = False,
    index: bool = False,
    foreign_key: str | None = None,
    cardinality: str | None = None,
    credential: str | None = None,
) -> dict[str, Any]:
    """Build the technology-independent persistence metadata attached to one Field.

    ``foreign_key`` names the referenced Domain Definition and field, such as
    ``"user.id"``. ``credential`` names the declared at-rest treatment, such as
    ``"hash"`` or ``"encrypted"``, for a Field classified as a credential.
    """
    return {
        "persistence": {
            "nullable": nullable,
            "primary_key": primary_key,
            "auto_increment": auto_increment,
            "unique": unique,
            "index": index,
            "foreign_key": foreign_key,
            "cardinality": cardinality,
            "credential": credential,
        }
    }


class DomainModel(BaseModel):
    """Shared Model Foundation realized on top of the Model Foundation mechanism.

    Every concrete Domain Definition declares its own complete set of Fields
    and relationships; this Foundation contributes none. It exists so that
    every Domain Definition gains consistent validation, serialization, and
    metadata-publication behavior.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )

    __persistent__: ClassVar[bool] = True
    __unique_sets__: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def persistence_metadata(cls) -> dict[str, Any]:
        """Publish this Domain Definition's technology-independent storage-relevant metadata.

        Includes whether it is persistent, and per-field primary-key, generated
        identity, uniqueness, index, foreign-key, cardinality, nullability,
        default, and credential-classification metadata, together with any
        composite uniqueness sets declared at the Domain Definition level.
        """
        fields: dict[str, Any] = {}
        for name, info in cls.model_fields.items():
            extra = (
                info.json_schema_extra
                if isinstance(info.json_schema_extra, dict)
                else {}
            )
            raw_persistence = extra.get("persistence", {})
            persistence: dict[str, Any] = (
                raw_persistence if isinstance(raw_persistence, dict) else {}
            )
            default = None if info.default is PydanticUndefined else info.default
            fields[name] = {
                "nullable": persistence.get("nullable", False),
                "default": default,
                "primary_key": persistence.get("primary_key", False),
                "auto_increment": persistence.get("auto_increment", False),
                "unique": persistence.get("unique", False),
                "index": persistence.get("index", False),
                "foreign_key": persistence.get("foreign_key"),
                "cardinality": persistence.get("cardinality"),
                "credential": persistence.get("credential"),
            }
        return {
            "persistent": cls.__persistent__,
            "fields": fields,
            "unique_sets": [list(item) for item in cls.__unique_sets__],
        }

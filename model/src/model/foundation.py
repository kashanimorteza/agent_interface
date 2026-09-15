"""The shared, technology-independent Model Foundation.

Every concrete Domain Definition in this package draws on this module for
common validation, serialization, and metadata-publishing mechanisms. The
Foundation declares no domain Field or Domain Relationship of its own; each
Domain Definition declares its own complete set of Fields and relationships.
"""

from __future__ import annotations

import typing
from enum import StrEnum
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo


class CredentialTreatment(StrEnum):
    """The declared at-rest treatment required for a credential Field."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


def persistence_field(
    *,
    default: Any = ...,
    primary_key: bool = False,
    auto_increment: bool = False,
    unique: bool = False,
    index: bool = False,
    foreign_key: str | None = None,
    cardinality: str | None = None,
    credential: CredentialTreatment | None = None,
    description: str | None = None,
    **kwargs: Any,
) -> Any:
    """Declare one Domain Definition Field together with the storage-relevant and credential meaning Model publishes for it.

    This is a Model Foundation mechanism, not a Field: calling it never adds a
    Field to the Foundation itself, only to the concrete Domain Definition
    that calls it for one of its own attributes.
    """
    extra: dict[str, Any] = {
        "primary_key": primary_key,
        "auto_increment": auto_increment,
        "unique": unique,
        "index": index,
    }
    if foreign_key is not None:
        extra["foreign_key"] = foreign_key
        extra["cardinality"] = cardinality or "one"
    if credential is not None:
        extra["credential"] = credential.value
    return Field(
        default=default, json_schema_extra=extra, description=description, **kwargs
    )


def _is_nullable(info: FieldInfo) -> bool:
    return type(None) in typing.get_args(info.annotation)


def _default_value(info: FieldInfo) -> Any:
    return None if info.is_required() else info.default


class ModelBase(BaseModel):
    """Shared foundation used by every concrete Domain Definition.

    Provides strict, deterministic validation, standard serialization
    through Pydantic's own mechanisms, and a metadata-publishing method that
    exposes the technology-independent, storage-relevant meaning Database
    consumes. It owns no Field or Domain Relationship.
    """

    model_config = ConfigDict(
        strict=True,
        validate_assignment=True,
        from_attributes=True,
        extra="forbid",
    )

    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def persistence_contract(cls) -> dict[str, Any]:
        """Publish this Domain Definition's technology-independent, storage-relevant metadata.

        Includes per-Field primary-key, auto-increment, uniqueness,
        nullability, default, index, foreign-key, and cardinality meaning,
        plus composite uniqueness sets and the persistent/non-persistent
        declaration. Publishes meaning only; it maps, migrates, and enforces
        nothing.
        """
        fields: dict[str, Any] = {}
        for name, info in cls.model_fields.items():
            extra = (
                info.json_schema_extra
                if isinstance(info.json_schema_extra, dict)
                else {}
            )
            fields[name] = {
                "nullable": _is_nullable(info),
                "default": _default_value(info),
                **extra,
            }
        return {
            "persistent": cls.persistent,
            "unique_sets": [list(field_set) for field_set in cls.unique_sets],
            "fields": fields,
        }

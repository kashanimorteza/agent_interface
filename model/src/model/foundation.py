"""The shared foundation every Domain Definition builds on: validation, serialization, and metadata publishing, with no Field or relationship of its own."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field


class ForeignKeyDeclaration(BaseModel):
    """Identifies a referenced Domain Definition and field, with cardinality and optionality, in a vocabulary that names no Engine or ORM."""

    model_config = ConfigDict(frozen=True)

    references: str
    field: str
    cardinality: str
    optional: bool


class CredentialDeclaration(BaseModel):
    """The Target-declared credential classification and required at-rest treatment for one Field."""

    model_config = ConfigDict(frozen=True)

    classification: str
    treatment: str


def domain_field(
    *,
    type: str,
    nullable: bool,
    default: Any = ...,
    primary_key: bool = False,
    auto_increment: bool = False,
    unique: bool = False,
    length: int | None = None,
    precision: tuple[int, int] | None = None,
    index: bool = False,
    foreign_key: ForeignKeyDeclaration | None = None,
    credential: CredentialDeclaration | None = None,
    description: str | None = None,
) -> Any:  # Any, like Pydantic's own Field(), so it fits any annotated field type.
    """Build a Field carrying the one standard, technology-independent declaration vocabulary."""
    declaration: dict[str, Any] = {
        "type": type,
        "nullable": nullable,
        "primary_key": primary_key,
        "auto_increment": auto_increment,
        "unique": unique,
        "index": index,
    }
    if length is not None:
        declaration["length"] = length
    if precision is not None:
        declaration["precision"] = {"total_digits": precision[0], "scale": precision[1]}
    if foreign_key is not None:
        declaration["foreign_key"] = foreign_key.model_dump()
    if credential is not None:
        declaration["credential"] = credential.model_dump()
    if description is not None:
        declaration["description"] = description

    field_kwargs: dict[str, Any] = {"json_schema_extra": {"declaration": declaration}}
    if default is not ...:
        field_kwargs["default"] = default
    elif auto_increment:
        field_kwargs["default"] = (
            None  # Absent until persistence generates it (Target-declared, not invented).
        )
    elif nullable:
        field_kwargs["default"] = (
            None  # May already hold no value; "omittable" realizes "nullable", nothing new.
        )

    return Field(**field_kwargs)


class DomainModel(BaseModel):
    """Base class every concrete Domain Definition subclasses for shared validation, serialization, and metadata publishing."""

    model_config = ConfigDict(strict=True, validate_assignment=True, extra="forbid")

    persistent: ClassVar[bool]
    unique_sets: ClassVar[list[list[str]]] = []

    @classmethod
    def declaration(cls) -> dict[str, Any]:
        """Publish this Domain Definition's complete technology-independent vocabulary."""
        fields: dict[str, Any] = {}
        for name, info in cls.model_fields.items():
            extra = info.json_schema_extra
            fields[name] = (
                extra["declaration"]
                if isinstance(extra, dict) and "declaration" in extra
                else {}
            )
        return {
            "persistent": cls.persistent,
            "unique_sets": [list(s) for s in cls.unique_sets],
            "fields": fields,
        }

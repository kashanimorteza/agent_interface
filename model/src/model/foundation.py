"""Shared Model Foundation.

Gives every concrete Domain Definition realization common validation,
serialization, and metadata-publishing mechanisms without owning, injecting,
or requiring any Field or Domain Relationship of its own.
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict

CredentialTreatment = Literal["hash", "encrypted"]


class FieldContract(BaseModel):
    """Storage-relevant metadata published for one field of a Domain Definition."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    primary_key: bool = False
    auto_increment: bool = False
    unique: bool = False
    nullable: bool = False
    default: Any = None
    index: bool = False
    credential: CredentialTreatment | None = None


class RelationshipContract(BaseModel):
    """Storage-relevant metadata published for one relationship of a Domain Definition."""

    model_config = ConfigDict(frozen=True)

    field: str
    references: str
    referenced_field: str = "id"
    cardinality: Literal["one", "many"] = "one"
    optional: bool = False


class PersistenceContract(BaseModel):
    """Technology-independent storage-relevant metadata published for Database consumption.

    Publishes meaning only; Database owns physical mapping, migration, and
    enforcement.
    """

    model_config = ConfigDict(frozen=True)

    persistent: bool
    fields: dict[str, FieldContract]
    relationships: tuple[RelationshipContract, ...] = ()
    unique_sets: tuple[tuple[str, ...], ...] = ()


class DomainModel(BaseModel):
    """Shared foundation for every concrete Domain Definition realization."""

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    PERSISTENCE_CONTRACT: ClassVar[PersistenceContract]

    @classmethod
    def persistence_contract(cls) -> PersistenceContract:
        """Return this Domain Definition's published storage-relevant metadata."""
        return cls.PERSISTENCE_CONTRACT

    @classmethod
    def is_persistent(cls) -> bool:
        """Whether Database must store this Domain Definition."""
        return cls.PERSISTENCE_CONTRACT.persistent

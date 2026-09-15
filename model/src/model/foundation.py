"""Shared, technology-independent Model Foundation.

Provides deterministic validation, serialization, and persistence-metadata
-publishing mechanisms common to every Domain Definition, without owning,
injecting, or requiring any Field or Domain Relationship of its own.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict

CredentialTreatment = Literal["hash", "encrypted"]
Cardinality = Literal["one-to-one", "one-to-many", "many-to-one", "many-to-many"]


@dataclass(frozen=True, slots=True)
class ForeignKey:
    """Identifies a referenced Domain Definition and field, with no Engine or ORM detail."""

    target: str
    field: str
    cardinality: Cardinality = "many-to-one"


@dataclass(frozen=True, slots=True)
class FieldMeta:
    """Technology-independent, per-field persistence-relevant metadata.

    Publishes storage-relevant meaning only; Database owns physical mapping,
    migration, and enforcement.
    """

    primary_key: bool = False
    auto_increment: bool = False
    unique: bool = False
    nullable: bool = True
    default: Any = None
    index: bool = False
    foreign_key: ForeignKey | None = None
    credential: CredentialTreatment | None = None


class PersistenceMeta:
    """Per-Domain-Definition persistence-relevant metadata published for Database consumption.

    A Domain Definition declares this as a nested class named ``Meta``.
    """

    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()


class DomainModel(BaseModel):
    """Shared Model Foundation.

    Every concrete Domain Definition inherits DomainModel to receive
    deterministic validation and serialization mechanisms. DomainModel
    declares no Field and no Domain Relationship of its own.
    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")


@dataclass(frozen=True, slots=True)
class PublishedField:
    """One field's published persistence metadata."""

    name: str
    meta: FieldMeta


@dataclass(frozen=True, slots=True)
class PersistenceContract:
    """The complete, technology-independent persistence contract of one Domain Definition."""

    persistent: bool
    unique_sets: tuple[tuple[str, ...], ...]
    fields: tuple[PublishedField, ...]


def persistence_contract(model: type[DomainModel]) -> PersistenceContract:
    """Extract a Domain Definition's published persistence contract.

    Reads only ``FieldMeta`` annotations and the model's ``Meta`` class;
    never inspects an ORM, an Engine, or any stored data.
    """
    meta_cls = getattr(model, "Meta", PersistenceMeta)
    fields: list[PublishedField] = []
    for name, info in model.model_fields.items():
        field_meta = next((m for m in info.metadata if isinstance(m, FieldMeta)), None)
        if field_meta is None:
            field_meta = FieldMeta(nullable=not info.is_required())
        fields.append(PublishedField(name=name, meta=field_meta))
    return PersistenceContract(
        persistent=getattr(meta_cls, "persistent", True),
        unique_sets=tuple(getattr(meta_cls, "unique_sets", ())),
        fields=tuple(fields),
    )

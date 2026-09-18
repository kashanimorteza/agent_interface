"""Model Foundation.

The technology-independent common foundation every concrete Domain
Definition in this package receives its shared validation, serialization,
and declaration-vocabulary metadata-publishing mechanisms through. The
Foundation declares no Field or Domain Relationship of its own; every
concrete Domain Definition declares its own complete set of Fields and
relationships from the Target.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict


class DomainModel(BaseModel):
    """Shared mechanisms for every concrete Domain Definition.

    Subclasses declare their own Fields, each carrying its declaration
    vocabulary (type, length, precision, nullability, default, identity,
    uniqueness, and relationships) as ``json_schema_extra`` on the Field
    itself, so the vocabulary is carried by the same definition application
    code uses rather than a second schema artifact.
    """

    model_config = ConfigDict(
        strict=True,
        validate_assignment=True,
        extra="forbid",
    )

    # Class-level declarations every concrete Domain Definition states for
    # itself: whether it is persistent, and its composite uniqueness sets.
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def declaration_vocabulary(cls) -> dict[str, Any]:
        """Publish this Domain Definition's technology-independent vocabulary.

        Reads the vocabulary carried by this Domain Definition's own Field
        declarations and class-level identity statements; there is no
        second schema artifact. Each consumer, Database among them, maps
        this vocabulary to its own technology.
        """
        fields: dict[str, Any] = {}
        for field_name, field_info in cls.model_fields.items():
            extra = field_info.json_schema_extra
            fields[field_name] = dict(extra) if isinstance(extra, dict) else {}
        return {
            "fields": fields,
            "unique_sets": [list(group) for group in cls.unique_sets],
            "persistent": cls.persistent,
        }

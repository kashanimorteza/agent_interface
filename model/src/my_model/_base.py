"""Shared declaration surface for every domain Model in the package."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field


class DomainModel(BaseModel):
    """Base class every domain Model derives from.

    Provides the common construction behaviour (reject unknown fields,
    validate on assignment) and the class-level declaration of composite
    uniqueness intent that a Model states but does not itself enforce
    across stored records.
    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    unique_together: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def credential_fields(cls) -> tuple[str, ...]:
        """Names of fields declared as carrying a credential value."""
        names = []
        for name, info in cls.model_fields.items():
            extra = info.json_schema_extra
            if isinstance(extra, dict) and extra.get("credential"):
                names.append(name)
        return tuple(names)


def credential_field(**kwargs: Any) -> Any:
    """A Field declared as carrying a credential value."""
    extra = dict(kwargs.pop("json_schema_extra", None) or {})
    extra["credential"] = True
    return Field(json_schema_extra=extra, **kwargs)

"""Shared foundation every domain Model in this package extends.

The project base class is named `BaseModel`, not `Model`: Model Preferences
forbid using the Component name `Model` as this implementation base-class
name, to keep the domain concept "Model" distinct from this one concrete
implementation detail.
"""

from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Strict base configuration shared by every domain Model."""

    model_config = ConfigDict(extra="forbid")


class _GenerateSecurely:
    """Marks a credential value that must be generated securely before persistence.

    Used only in initial-data declarations, never as a Model field value, so that
    a required credential is never satisfied with a fake placeholder.
    """

    def __repr__(self) -> str:
        return "GENERATE_SECURELY"


GENERATE_SECURELY: Any = _GenerateSecurely()


def credential_field(*, storage: str, description: str, default: Any = ...) -> Any:
    """Declare a field as a sensitive credential and its required storage-at-rest meaning.

    Model does not perform the storage itself; the responsible technical component
    reads this declaration and applies the actual hashing or encryption.
    """

    return Field(
        default=default,
        description=description,
        json_schema_extra={"credential": True, "storage_at_rest": storage},
    )

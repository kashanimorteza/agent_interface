"""Shared foundation every domain Model in this package inherits from."""

from typing import Any, Literal

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Project base class for every concrete domain Model.

    Rejects unknown fields by default, consistent with a closed domain object.
    """

    model_config = ConfigDict(extra="forbid")


def credential_field(
    *,
    storage_at_rest: Literal["hash", "encrypted"],
    default: Any = ...,
    description: str | None = None,
    **kwargs: Any,
) -> Any:
    """Declare a field that carries a credential.

    Model does not decide how a credential is hashed, encrypted, or otherwise
    protected at rest; it only declares that the field is sensitive and which
    storage strategy the domain requires, so a responsible technical
    component (Database) can apply it. Consumers introspect this metadata
    through the field's ``json_schema_extra``.
    """

    extra = {"credential": True, "storage_at_rest": storage_at_rest}
    return Field(default=default, description=description, json_schema_extra=extra, **kwargs)

from enum import StrEnum
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field


class CredentialStorage(StrEnum):
    HASH = "hash"
    ENCRYPTED = "encrypted"


class ModelBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
    )

    unique_together: ClassVar[tuple[tuple[str, ...], ...]] = ()


def credential_field(*, storage: CredentialStorage, **kwargs: Any) -> Any:
    return Field(json_schema_extra={"credential_storage": storage.value}, **kwargs)

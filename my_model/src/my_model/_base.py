"""Shared base representation every concrete domain Model inherits from."""

from __future__ import annotations

from pydantic import BaseModel as _PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(_PydanticBaseModel):
    """Project base class for every concrete domain Model.

    Rejects unknown fields by default (closed domain objects) and normalizes
    attribute-style construction across the package.
    """

    model_config = ConfigDict(extra="forbid", strict=False, validate_assignment=True)

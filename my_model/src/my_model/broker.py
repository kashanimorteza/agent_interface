"""The Broker domain entity: a broker supported by the system."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class Broker(BaseModel):
    """A broker supported by the system.

    Identifies the user who owns its configuration without coupling the
    Broker definition to one Trading Platform.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"name": "FxPro", "user_id": 1},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(
        description="Identifies the user who owns the broker configuration."
    )
    status: bool = Field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = Field(default=None, description="Describes the broker.")

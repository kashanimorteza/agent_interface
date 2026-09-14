"""The Instance Domain Definition (Target: Model > Instance)."""

from __future__ import annotations

from typing import ClassVar

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Instance(ModelFoundation):
    """A user-owned connection instance through which the system accesses a supported Trading
    Platform."""

    CREDENTIAL_STORAGE: ClassVar[dict[str, str]] = {
        "password": "encrypted",
        "api_key": "encrypted",
    }

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns this instance."
    )
    name: str = pydantic.Field(description="The instance's display name.")
    trading_platform_id: int = pydantic.Field(
        description="Identifies the trading platform used by this instance."
    )
    ip: str | None = pydantic.Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = pydantic.Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = pydantic.Field(
        default=None,
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = pydantic.Field(
        default=None,
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    is_active: bool = is_active_field("Indicates whether the instance is active.")
    description: str | None = description_field("Describes the instance.")

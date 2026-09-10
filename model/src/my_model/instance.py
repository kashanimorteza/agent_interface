from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Instance(DomainModel):
    user_id: int = Field(..., description="Identifies the user who owns this instance.")
    name: str = Field(..., description="The instance's display name.")
    trading_platform_id: int = Field(
        ..., description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = Field(
        default=None,
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = Field(
        default=None,
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    status: bool = Field(default=True, description="Indicates whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("user_id", "name")]
    credential_fields: ClassVar[frozenset[str]] = frozenset({"password", "api_key"})
    credential_storage: ClassVar[dict[str, str]] = {"password": "encrypted", "api_key": "encrypted"}
    relationships: ClassVar[dict[str, Relationship]] = {
        "user": Relationship(target="User", cardinality="one", field="user_id"),
        "trading_platform": Relationship(
            target="TradingPlatform", cardinality="one", field="trading_platform_id"
        ),
    }
    domain_rules: ClassVar[list[str]] = [
        "The Trading Platform selected through trading_platform_id defines which connection "
        "fields are required; every field it requires must be present before the Instance can be used.",
    ]


INSTANCE_INITIAL_DATA: list[dict] = [
    {
        "name": "MetaTrader",
        "user_id": 1,
        "trading_platform_id": 1,
        "ip": "127.0.0.1",
        "username": "test",
        "password": "<generate securely>",
        "api_key": "<generate securely>",
    },
]

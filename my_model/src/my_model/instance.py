"""The Instance domain entity."""

from __future__ import annotations

from typing import ClassVar

from pydantic import Field, model_validator

from ._base import GENERATE_SECURELY, BaseModel


class Instance(BaseModel):
    """A user-owned connection instance through which the system accesses a
    supported Trading Platform.
    """

    credential_fields = frozenset({"password", "api_key"})
    initial_data = (
        {
            "name": "MetaTrader",
            "user_id": 1,
            "trading_platform_id": 1,
            "ip": "127.0.0.1",
            "username": "test",
            "password": GENERATE_SECURELY,
            "api_key": GENERATE_SECURELY,
        },
    )

    #: Connection fields a given Trading Platform identity requires before an
    #: Instance that uses it is considered usable. Empty until the component that
    #: owns each Trading Platform's specific requirements declares them; Instance
    #: only enforces what has actually been declared here from its own data.
    platform_required_fields: ClassVar[dict[int, frozenset[str]]] = {}

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns this instance.")
    name: str = Field(min_length=1, description="The instance's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None, description="Technical network address used to reach the platform."
    )
    username: str | None = Field(default=None, description="Technical username for the connection.")
    password: str | None = Field(default=None, description="Technical password for the connection.")
    api_key: str | None = Field(
        default=None, description="Technical API credential for the connection."
    )
    status: bool = Field(default=True, description="Whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")

    @model_validator(mode="after")
    def _connection_fields_required_by_platform(self) -> Instance:
        required = self.platform_required_fields.get(self.trading_platform_id, frozenset())
        missing = sorted(field for field in required if getattr(self, field, None) is None)
        if missing:
            fields = ", ".join(missing)
            platform = self.trading_platform_id
            raise ValueError(f"trading platform {platform} requires connection field(s): {fields}")
        return self

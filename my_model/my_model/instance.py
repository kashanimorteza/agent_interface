"""The Instance domain entity: a user-owned Trading Platform connection."""

from pydantic import Field

from my_model._base import BaseModel, credential_field


class Instance(BaseModel):
    """A user-owned connection instance through which the system accesses a
    supported Trading Platform.

    Which of this Instance's technical connection fields a particular Trading
    Platform actually requires is resolved from the referenced Trading
    Platform rather than from this record alone, so that resolved requirement
    is not enforced by this single-record Model.
    """

    id: int = Field(description="The instance's logical identity.")
    user_id: int = Field(description="Identifies the user who owns this instance.")
    name: str = Field(description="The instance's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None,
        description="The technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="The technical username used to establish the Instance connection when required.",
    )
    password: str | None = credential_field(
        storage_at_rest="encrypted",
        default=None,
        description="The technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = credential_field(
        storage_at_rest="encrypted",
        default=None,
        description="The technical API credential used to establish the Instance connection when required.",
    )
    status: bool = Field(default=True, description="Whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")


# password and api_key are generated securely by Database when required by
# the referenced Trading Platform; they are absent here for that reason.
INITIAL_DATA: list[dict[str, object]] = [
    {
        "name": "MetaTrader",
        "user_id": 1,
        "trading_platform_id": 1,
        "ip": "127.0.0.1",
        "username": "test",
    },
]

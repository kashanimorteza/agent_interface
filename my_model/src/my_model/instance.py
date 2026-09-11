from pydantic import Field

from ._base import BaseModel


class Instance(BaseModel):
    """A user-owned connection instance through which the system accesses a supported Trading Platform."""

    id: int | None = Field(
        default=None, description="Generated once the Instance is persisted."
    )
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
    password: str | None = Field(
        default=None,
        description="The technical password used to establish the Instance connection when required.",
        json_schema_extra={"credential": True},
    )
    api_key: str | None = Field(
        default=None,
        description="The technical API credential used to establish the Instance connection when required.",
        json_schema_extra={"credential": True},
    )
    status: bool = Field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = Field(default=None, description="Describes the instance.")

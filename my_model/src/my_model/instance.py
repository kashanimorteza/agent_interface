"""The Instance domain Model: a user-owned connection to a supported Trading Platform."""

from pydantic import Field

from ._base import GENERATE_SECURELY, BaseModel, credential_field


class Instance(BaseModel):
    """A user-owned connection instance through which the system accesses a Trading Platform.

    Which connection fields are required is defined by the referenced Trading
    Platform; that cross-Model requirement is a domain rule traceable to this
    Model, enforced where the referenced platform's requirements are known.
    The combination-uniqueness of `user_id` and `name` is likewise traceable
    here and enforced by Database.
    """

    id: int | None = Field(default=None, description="The instance's generated identity.")
    user_id: int = Field(description="Identifies the user who owns this instance.")
    name: str = Field(description="The instance's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = credential_field(
        storage="encrypted",
        description="Defines the technical password used to establish the Instance connection when required.",
        default=None,
    )
    api_key: str | None = credential_field(
        storage="encrypted",
        description="Defines the technical API credential used to establish the Instance connection when required.",
        default=None,
    )
    status: bool = Field(default=True, description="Indicates whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")


INITIAL_DATA: list[dict[str, object]] = [
    {
        "name": "MetaTrader",
        "user_id": 1,
        "trading_platform_id": 1,
        "ip": "127.0.0.1",
        "username": "test",
        "password": GENERATE_SECURELY,
        "api_key": GENERATE_SECURELY,
    },
]

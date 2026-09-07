"""The Broker Model."""

from pydantic import Field

from ._base import Model


class Broker(Model):
    """Defines a broker that the system can work with through its selected trading platform. Multiple
    brokers can be added so the system is not limited to a specific broker and can operate with any
    configured broker.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(description="Identifies the user who owns the broker configuration.")
    trading_platform_id: int = Field(description="Identifies the trading platform used by the broker.")
    status: bool = Field(default=True, description="Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")

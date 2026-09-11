from pydantic import Field

from ._base import BaseModel


class Broker(BaseModel):
    """A broker supported by the system, owned by a user and independent of any one Trading Platform."""

    id: int | None = Field(
        default=None, description="Generated once the Broker is persisted."
    )
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(
        description="Identifies the user who owns the broker configuration."
    )
    status: bool = Field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = Field(default=None, description="Describes the broker.")

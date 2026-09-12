"""The Broker domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class Broker(BaseModel):
    """A broker supported by the system, owned by a user, independent of any
    one Trading Platform.
    """

    id: int = Field(description="The broker's logical identity.")
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(description="Identifies the user who owns the broker configuration.")
    status: bool = Field(default=True, description="Whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")


INITIAL_DATA: list[dict[str, object]] = [
    {"name": "FxPro", "user_id": 1},
]

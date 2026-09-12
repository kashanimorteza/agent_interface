"""The Broker domain Model: a broker supported by the system."""

from pydantic import Field

from ._base import BaseModel


class Broker(BaseModel):
    """A broker supported by the system.

    Identifies the user who owns its configuration without coupling the Broker
    definition to one Trading Platform. The combination-uniqueness of `user_id`
    and `name` is a domain rule traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The broker's generated identity.")
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(description="Identifies the user who owns the broker configuration.")
    status: bool = Field(default=True, description="Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")


INITIAL_DATA: list[dict[str, object]] = [
    {"name": "FxPro", "user_id": 1},
]

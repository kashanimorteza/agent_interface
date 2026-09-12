"""The Action Group domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class ActionGroup(BaseModel):
    """An independent grouping for trading actions based on their risk
    profile, such as high risk, normal risk, or low risk.
    """

    id: int = Field(description="The action group's logical identity.")
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    status: bool = Field(default=True, description="Whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]

"""The Action Group domain Model: an independent grouping for trading Actions by risk profile."""

from pydantic import Field

from ._base import BaseModel


class ActionGroup(BaseModel):
    """An independent grouping for trading actions based on their risk profile.

    Such as high risk, normal risk, or low risk. Actions are assigned to these
    groups so trades can be organized and selected by their intended risk
    level. The combination-uniqueness of `user_id` and `name` is a domain rule
    traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The action group's generated identity.")
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = Field(default=None, description="Describes the action group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]

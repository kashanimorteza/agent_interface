from pydantic import Field

from ._base import BaseModel


class ActionGroup(BaseModel):
    """An independent grouping for trading actions based on their risk profile."""

    id: int | None = Field(
        default=None, description="Generated once the Action Group is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the action group."
    )

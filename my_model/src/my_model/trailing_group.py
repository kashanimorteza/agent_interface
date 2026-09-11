from pydantic import Field

from ._base import BaseModel


class TrailingGroup(BaseModel):
    """An independent group organizing the rules that manage Stop Loss and Take Profit during a trade."""

    id: int | None = Field(
        default=None, description="Generated once the Trailing Group is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing group."
    )

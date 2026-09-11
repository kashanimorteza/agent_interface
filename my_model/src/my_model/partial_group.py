from pydantic import Field

from ._base import BaseModel


class PartialGroup(BaseModel):
    """An independent group of rules for managing portions of an open trade."""

    id: int | None = Field(
        default=None, description="Generated once the Partial Group is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial group."
    )

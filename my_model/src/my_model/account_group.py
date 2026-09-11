from pydantic import Field

from ._base import BaseModel


class AccountGroup(BaseModel):
    """An independent group for organizing trading accounts owned by one user."""

    id: int | None = Field(
        default=None, description="Generated once the Account Group is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(description="The account group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the account group."
    )

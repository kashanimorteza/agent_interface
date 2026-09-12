"""The Account Group domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class AccountGroup(BaseModel):
    """An independent group for organizing trading accounts owned by one user."""

    id: int = Field(description="The account group's logical identity.")
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(description="The account group's display name.")
    status: bool = Field(default=True, description="Whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]

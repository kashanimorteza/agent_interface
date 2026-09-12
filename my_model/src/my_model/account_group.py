"""The Account Group domain Model: an independent group organizing trading accounts."""

from pydantic import Field

from ._base import BaseModel


class AccountGroup(BaseModel):
    """An independent group for organizing trading accounts owned by one user.

    The combination-uniqueness of `user_id` and `name` is a domain rule
    traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The account group's generated identity.")
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(description="The account group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = Field(default=None, description="Describes the account group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]

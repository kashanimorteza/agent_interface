"""The AccountGroup Model."""

from pydantic import Field

from ._base import Model


class AccountGroup(Model):
    """Defines an independent group for organizing trading accounts."""

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The account group's display name. Unique.")
    status: bool = Field(default=True, description="Indicates whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")

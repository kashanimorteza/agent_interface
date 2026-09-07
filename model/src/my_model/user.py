"""The User Model."""

from pydantic import Field

from ._base import Model


class User(Model):
    """Defines an independent user of the system and enables multi-user operation. Each user can have a
    separate set of settings, allowing new users to be added with configurations that remain
    distinct from those of existing users.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The user's display name. Unique.")
    username: str = Field(description="The username used to identify the user.")
    password: str | None = Field(
        default=None,
        description="The password credential used by the user. Credential: accepted on write, never returned.",
    )
    api_key: str | None = Field(
        default=None,
        description="The API key assigned to the user. Credential: accepted on write, never returned.",
    )
    status: bool = Field(default=True, description="Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")

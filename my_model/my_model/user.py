"""The User domain entity: an independent user of the system."""

from pydantic import Field

from my_model._base import BaseModel, credential_field


class User(BaseModel):
    """An independent user of the system, enabling multi-user operation.

    Each user can have a separate set of settings, allowing new users to be
    added with configurations that remain distinct from existing users.
    """

    id: int = Field(description="The user's logical identity.")
    name: str = Field(description="The user's display name.")
    username: str = Field(description="The username used to identify the user.")
    password: str = credential_field(
        storage_at_rest="hash",
        description="The password credential used by the user.",
    )
    api_key: str = credential_field(
        storage_at_rest="hash",
        description="The API key assigned to the user.",
    )
    status: bool = Field(default=True, description="Whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")


# Domain values known before generation and persistence. Fields absent here
# (id, password, api_key) are system-generated: id is assigned on persistence
# and the two credential fields are generated securely by Database, which
# recognizes them from this Model's own credential declaration.
INITIAL_DATA: list[dict[str, object]] = [
    {"name": "Admin", "username": "admin"},
]

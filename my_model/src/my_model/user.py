from pydantic import Field

from ._base import BaseModel


class User(BaseModel):
    """An independent user of the system enabling multi-user operation."""

    id: int | None = Field(
        default=None, description="Generated once the User is persisted."
    )
    name: str = Field(description="The user's display name.")
    username: str = Field(description="The username used to identify the user.")
    password: str = Field(
        description="The password credential used by the user.",
        json_schema_extra={"credential": True},
    )
    api_key: str = Field(
        description="The API key assigned to the user.",
        json_schema_extra={"credential": True},
    )
    status: bool = Field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = Field(default=None, description="Describes the user.")

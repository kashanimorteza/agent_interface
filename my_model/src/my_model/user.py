"""The User domain Model: an independent user of the system enabling multi-user operation."""

from pydantic import Field

from ._base import GENERATE_SECURELY, BaseModel, credential_field


class User(BaseModel):
    """An independent user of the system.

    Each user can have a separate set of settings, allowing new users to be added
    with configurations that remain distinct from those of existing users.

    The uniqueness of `name` is a domain rule traceable to this Model; enforcing
    it across stored records belongs to Database.
    """

    id: int | None = Field(default=None, description="The user's generated identity.")
    name: str = Field(description="The user's display name.")
    username: str = Field(description="The username used to identify the user.")
    password: str = credential_field(
        storage="hash", description="The password credential used by the user."
    )
    api_key: str = credential_field(
        storage="hash", description="The API key assigned to the user."
    )
    status: bool = Field(default=True, description="Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")


INITIAL_DATA: list[dict[str, object]] = [
    {
        "name": "Admin",
        "username": "admin",
        "password": GENERATE_SECURELY,
        "api_key": GENERATE_SECURELY,
    },
]

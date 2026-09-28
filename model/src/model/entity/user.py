"""User Entity."""

from model.declaration import Declaration, Sensitivity
from model.foundation import Foundation


class User(Foundation, table=True):
    """Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(unique=True, description="The user's display name.")
    username: str = Declaration.field(
        unique=True, description="The username used to identify the user."
    )
    password: str = Declaration.field(
        sensitivity=Sensitivity.PASSWORD,
        description="The password credential used by the user.",
    )
    api_key: str = Declaration.field(
        sensitivity=Sensitivity.SENSITIVE,
        description="The API key assigned to the user.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the user."
    )

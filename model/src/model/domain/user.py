"""The User Domain Definition: an independent user of the system, enabling multi-user operation."""

from model.foundation import DomainModel, domain_field


class User(DomainModel):
    """A user of the system with a distinct, independently owned set of settings."""

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the user.",
    )
    name: str = domain_field(unique=True, description="The user's display name.")
    username: str = domain_field(
        unique=True, description="The username used to identify the user."
    )
    password: str = domain_field(
        credential="hash", description="The password credential used by the user."
    )
    api_key: str = domain_field(
        credential="hash", description="The API key assigned to the user."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the user."
    )

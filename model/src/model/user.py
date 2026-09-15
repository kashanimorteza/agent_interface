"""The User Domain Definition."""

from __future__ import annotations

from model.foundation import CredentialTreatment, ModelBase, persistence_field


class User(ModelBase):
    """An independent user of the system, enabling multi-user operation.

    Each user can have a separate set of settings, allowing new users to be
    added with configurations that remain distinct from those of existing
    users.
    """

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the user.",
    )
    name: str = persistence_field(unique=True, description="The user's display name.")
    username: str = persistence_field(
        unique=True, description="The username used to identify the user."
    )
    password: str = persistence_field(
        credential=CredentialTreatment.HASH,
        description="The password credential used by the user.",
    )
    api_key: str = persistence_field(
        credential=CredentialTreatment.HASH,
        description="The API key assigned to the user.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the user."
    )

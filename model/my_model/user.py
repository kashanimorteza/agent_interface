"""User: an independent user of the system."""

from __future__ import annotations

from .base import CredentialStorage, Generate, Model, field


class User(Model):
    """Defines an independent user of the system and enables multi-user
    operation. Each user can have a separate set of settings, allowing new
    users to be added with configurations that remain distinct from those of
    existing users."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The user's display name.")
    username: str = field("string", purpose="The username used to identify the user.")
    password: str = field("string", credential=True, purpose="The password credential used by the user.")
    api_key: str = field("string", credential=True, purpose="The API key assigned to the user.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the user is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the user.")

    rules = (
        CredentialStorage(field="password", mode="hash"),
        CredentialStorage(field="api_key", mode="hash"),
    )

    initial_data = (
        {"name": "Admin", "username": "admin", "password": Generate, "api_key": Generate},
    )

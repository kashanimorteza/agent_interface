"""The User Domain Definition: an independent user of the system enabling multi-user operation."""

from __future__ import annotations

from model.foundation import CredentialDeclaration, DomainModel, domain_field


class User(DomainModel):
    persistent = True

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The user's display name.",
    )
    username: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The username used to identify the user.",
    )
    password: str = domain_field(
        type="string",
        nullable=False,
        credential=CredentialDeclaration(classification="credential", treatment="hash"),
        description="The password credential used by the user.",
    )
    api_key: str = domain_field(
        type="string",
        nullable=False,
        credential=CredentialDeclaration(classification="credential", treatment="hash"),
        description="The API key assigned to the user.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the user is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the user."
    )

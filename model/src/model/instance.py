"""The Instance Domain Definition: a user-owned connection instance through which the system accesses a supported Trading Platform."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import (
    CredentialDeclaration,
    DomainModel,
    ForeignKeyDeclaration,
    domain_field,
)


class Instance(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["user_id", "name"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    user_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="User", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the user who owns this instance.",
    )
    trading_platform_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="TradingPlatform",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the trading platform used by this instance.",
    )
    name: str = domain_field(
        type="string", nullable=False, description="The instance's display name."
    )
    ip: str | None = domain_field(
        type="string",
        nullable=True,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = domain_field(
        type="string",
        nullable=True,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = domain_field(
        type="string",
        nullable=True,
        credential=CredentialDeclaration(
            classification="credential", treatment="encrypted"
        ),
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = domain_field(
        type="string",
        nullable=True,
        credential=CredentialDeclaration(
            classification="credential", treatment="encrypted"
        ),
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the instance is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the instance."
    )

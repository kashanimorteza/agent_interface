"""The Instance Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class Instance(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns this instance.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="trading_platform_id",
                description="Identifies the trading platform used by this instance.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The instance's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="ip",
                description="Identifies the technical network address used to reach the Trading Platform when required.",
                type="string",
                nullable=True,
            ),
            FieldDeclaration(
                name="username",
                description="Defines the technical username used to establish the Instance connection when required.",
                type="string",
                nullable=True,
            ),
            FieldDeclaration(
                name="password",
                description="Defines the technical password used to establish the Instance connection when required.",
                type="string",
                nullable=True,
            ),
            FieldDeclaration(
                name="api_key",
                description="Defines the technical API credential used to establish the Instance connection when required.",
                type="string",
                nullable=True,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the instance is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the instance.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("user_id", "User", "id"),
            Relation("trading_platform_id", "Trading Platform", "id"),
        ),
        unique_constraints=(
            ("user_id", "name"),
        ),
    )

    id: int | None = None
    user_id: int
    trading_platform_id: int
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

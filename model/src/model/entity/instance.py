from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Instance",
    description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
    fields=(
        identity(),
        FieldDeclaration(
            name="user_id",
            description="Identifies the user who owns this instance.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="trading_platform_id",
            description="Identifies the trading platform used by this instance.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="name",
            description="The instance's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="ip",
            description="Identifies the technical network address used to reach the Trading Platform when required.",
            type=FieldType.STRING,
            nullable=True,
        ),
        FieldDeclaration(
            name="username",
            description="Defines the technical username used to establish the Instance connection when required.",
            type=FieldType.STRING,
            nullable=True,
        ),
        FieldDeclaration(
            name="password",
            description="Defines the technical password used to establish the Instance connection when required.",
            type=FieldType.STRING,
            nullable=True,
        ),
        FieldDeclaration(
            name="api_key",
            description="Defines the technical API credential used to establish the Instance connection when required.",
            type=FieldType.STRING,
            nullable=True,
        ),
        activity("Indicates whether the instance is active."),
        FieldDeclaration(
            name="description",
            description="Describes the instance.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        RelationDeclaration("user_id", "User", "id"),
        RelationDeclaration("trading_platform_id", "Trading Platform", "id"),
    ),
    unique_constraints=(
        UniqueConstraintDeclaration(
            (
                "user_id",
                "name",
            )
        ),
    ),
)


class Instance(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    trading_platform_id: int = column(_DECLARATION, "trading_platform_id")
    name: str = column(_DECLARATION, "name")
    ip: str | None = column(_DECLARATION, "ip")
    username: str | None = column(_DECLARATION, "username")
    password: str | None = column(_DECLARATION, "password")
    api_key: str | None = column(_DECLARATION, "api_key")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")

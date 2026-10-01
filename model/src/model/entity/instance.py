"""The Instance Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Instance",
    description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
            sensitivity="password",
        ),
        FieldDeclaration(
            name="api_key",
            description="Defines the technical API credential used to establish the Instance connection when required.",
            type="string",
            nullable=True,
            sensitivity="sensitive",
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
        Relation(local_field="user_id", target_entity="User", target_field="id"),
        Relation(
            local_field="trading_platform_id",
            target_entity="Trading Platform",
            target_field="id",
        ),
    ),
    unique_constraints=(("user_id", "name"),),
    indexes=(),
)


class Instance(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    user_id: int = Field(
        description="Identifies the user who owns this instance.",
        **column_options(_DECLARATION, "user_id"),
    )
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance.",
        **column_options(_DECLARATION, "trading_platform_id"),
    )
    name: str = Field(
        description="The instance's display name.",
        **column_options(_DECLARATION, "name"),
    )
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
        **column_options(_DECLARATION, "ip"),
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
        **column_options(_DECLARATION, "username"),
    )
    password: str | None = Field(
        default=None,
        description="Defines the technical password used to establish the Instance connection when required.",
        **column_options(_DECLARATION, "password"),
    )
    api_key: str | None = Field(
        default=None,
        description="Defines the technical API credential used to establish the Instance connection when required.",
        **column_options(_DECLARATION, "api_key"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the instance is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the instance.",
        **column_options(_DECLARATION, "description"),
    )

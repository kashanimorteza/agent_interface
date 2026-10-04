"""The Instance Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Instance(Entity, table=True):
    """The Instance Entity."""

    __tablename__ = "Instance"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            identity_declaration(),
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
            activity_declaration("Indicates whether the instance is active."),
            FieldDeclaration(
                name="description",
                description="Describes the instance.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="user_id", target_entity="User", target_field="id"
            ),
            RelationDeclaration(
                local_field="trading_platform_id",
                target_entity="Trading Platform",
                target_field="id",
            ),
        ),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = identity_field()
    user_id: int = Field(
        foreign_key="User.id", description="Identifies the user who owns this instance."
    )
    trading_platform_id: int = Field(
        foreign_key="TradingPlatform.id",
        description="Identifies the trading platform used by this instance.",
    )
    name: str = Field(description="The instance's display name.")
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = Field(
        default=None,
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = Field(
        default=None,
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    is_active: bool = activity_field("Indicates whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")

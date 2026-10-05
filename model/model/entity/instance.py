from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Instance(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Instance",
        "Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns this instance.", "integer", False),
            FieldDeclaration(
                "trading_platform_id", "Identifies the trading platform used by this instance.", "integer", False
            ),
            FieldDeclaration("name", "The instance's display name.", "string", False),
            FieldDeclaration(
                "ip",
                "Identifies the technical network address used to reach the Trading Platform when required.",
                "string",
                True,
            ),
            FieldDeclaration(
                "username",
                "Defines the technical username used to establish the Instance connection when required.",
                "string",
                True,
            ),
            FieldDeclaration(
                "password",
                "Defines the technical password used to establish the Instance connection when required.",
                "string",
                True,
            ),
            FieldDeclaration(
                "api_key",
                "Defines the technical API credential used to establish the Instance connection when required.",
                "string",
                True,
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the instance is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the instance.", "string", True),
        ),
        "id",
        relations=(
            Relation("user_id", "User", "id"),
            Relation("trading_platform_id", "Trading Platform", "id"),
        ),
        unique_constraints=(
            (
                "user_id",
                "name",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns this instance.")
    trading_platform_id: int = Field(
        foreign_key="TradingPlatform.id", description="Identifies the trading platform used by this instance."
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
    is_active: bool = Field(default=True, description="Indicates whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")

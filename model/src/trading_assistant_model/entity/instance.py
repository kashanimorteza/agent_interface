from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class Instance(Foundation, table=True):
    """Defines a user-owned connection instance through which the system accesses a
    supported Trading Platform.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Instance",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("user_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("trading_platform_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("ip", FieldType.STRING, nullable=True),
            FieldDeclaration("username", FieldType.STRING, nullable=True),
            FieldDeclaration(
                "password", FieldType.STRING, nullable=True, sensitive=True
            ),
            FieldDeclaration(
                "api_key", FieldType.STRING, nullable=True, sensitive=True
            ),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("user_id", "name")),),
        references=(
            Reference(("user_id",), "User", ("id",)),
            Reference(("trading_platform_id",), "TradingPlatform", ("id",)),
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the instance, assigned automatically.",
    )
    user_id: int = Field(description="Identifies the user who owns this instance.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance."
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
    is_active: bool = Field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = Field(default=None, description="Describes the instance.")

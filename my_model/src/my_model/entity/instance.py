"""Instance Domain Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Instance(ModelFoundation, table=True):
    """Defines a user-owned connection instance through which the system accesses a supported Trading Platform."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Instance",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", LogicalType.INTEGER),
            FieldDeclaration("trading_platform_id", LogicalType.INTEGER),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("ip", LogicalType.STRING, nullable=True),
            FieldDeclaration("username", LogicalType.STRING, nullable=True),
            FieldDeclaration(
                "password", LogicalType.STRING, nullable=True, sensitive=True
            ),
            FieldDeclaration(
                "api_key", LogicalType.STRING, nullable=True, sensitive=True
            ),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(
            ReferenceDeclaration("user_id", "User"),
            ReferenceDeclaration("trading_platform_id", "Trading Platform"),
        ),
        unique_constraints=(("user_id", "name"),),
    )

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    trading_platform_id: int = Field(foreign_key="tradingplatform.id")
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

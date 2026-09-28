"""Entity: Instance."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    Sensitivity,
    Unique,
    ValueGeneration,
)
from model.foundation import Foundation


class Instance(Foundation, table=True):
    """Instance Entity."""

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

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    declaration: ClassVar[Declaration] = Declaration(
        entity="Instance",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", FieldType.INTEGER),
            FieldDeclaration("trading_platform_id", FieldType.INTEGER),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("ip", FieldType.STRING, nullable=True),
            FieldDeclaration("username", FieldType.STRING, nullable=True),
            FieldDeclaration(
                "password",
                FieldType.STRING,
                nullable=True,
                sensitivity=Sensitivity.PASSWORD,
            ),
            FieldDeclaration(
                "api_key",
                FieldType.STRING,
                nullable=True,
                sensitivity=Sensitivity.SENSITIVE,
            ),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(
            Reference("user_id", "User"),
            Reference("trading_platform_id", "TradingPlatform"),
        ),
        uniques=(
            Unique(
                (
                    "user_id",
                    "name",
                )
            ),
        ),
    )

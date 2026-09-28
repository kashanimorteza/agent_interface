"""Broker Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Reference,
    Unique,
)
from model.foundation import Foundation


class Broker(Foundation, table=True):
    """Supported broker owned by a user, independent of any one Trading Platform."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="Broker",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("user_id", FieldType.INTEGER),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("user_id", "User"),),
        uniques=(Unique(("user_id", "name")),),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id")
    is_active: bool = True
    description: str | None = None

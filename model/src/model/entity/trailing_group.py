"""Trailing Group Entity."""

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


class TrailingGroup(Foundation, table=True):
    """Independent group organizing the rules that manage Stop Loss and Take Profit during a trade."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="TrailingGroup",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", FieldType.INTEGER),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("user_id", "User"),),
        uniques=(Unique(("user_id", "name")),),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    is_active: bool = True
    description: str | None = None

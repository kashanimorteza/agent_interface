"""User Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Sensitivity,
    Unique,
)
from model.foundation import Foundation


class User(Foundation, table=True):
    """Independent user of the system."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="User",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("username", FieldType.STRING),
            FieldDeclaration(
                "password", FieldType.STRING, sensitivity=Sensitivity.PASSWORD
            ),
            FieldDeclaration(
                "api_key", FieldType.STRING, sensitivity=Sensitivity.SENSITIVE
            ),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        uniques=(Unique(("name",)), Unique(("username",))),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None

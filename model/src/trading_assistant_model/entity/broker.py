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


class Broker(Foundation, table=True):
    """Defines a broker supported by the system and identifies the user who owns its
    configuration without coupling the Broker definition to one Trading Platform.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Broker",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("user_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("user_id", "name")),),
        references=(Reference(("user_id",), "User", ("id",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the broker, assigned automatically.",
    )
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(
        description="Identifies the user who owns the broker configuration."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = Field(default=None, description="Describes the broker.")

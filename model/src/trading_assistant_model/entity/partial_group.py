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


class PartialGroup(Foundation, table=True):
    """Defines an independent group of rules for managing portions of an open trade. Its
    rules determine how much of the trade volume must be closed when profit or loss
    reaches specified thresholds.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="PartialGroup",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("user_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
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
        description="Unique identifier of the partial group, assigned automatically.",
    )
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    is_active: bool = Field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial group."
    )

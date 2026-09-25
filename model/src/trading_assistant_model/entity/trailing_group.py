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


class TrailingGroup(Foundation, table=True):
    """Defines an independent group for organizing the rules that manage Stop Loss and Take
    Profit during a trade. The group identifies the rule set, while each rule separately
    defines its activation condition and the changes to apply.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="TrailingGroup",
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
        description="Unique identifier of the trailing group, assigned automatically.",
    )
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    is_active: bool = Field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing group."
    )

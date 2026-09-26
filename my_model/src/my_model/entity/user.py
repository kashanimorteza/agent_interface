"""User Entity."""

from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    AtRest,
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class User(ModelFoundation, table=True):
    """Defines an independent user of the system and enables multi-user operation."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="User",
        purpose="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The user's display name"
            ),
            FieldDeclaration(
                "username",
                LogicalType.STRING,
                purpose="The username used to identify the user",
            ),
            FieldDeclaration(
                "password",
                LogicalType.STRING,
                sensitivity=Sensitivity.CREDENTIAL,
                at_rest=AtRest.HASH,
                purpose="The password credential used by the user",
            ),
            FieldDeclaration(
                "api_key",
                LogicalType.STRING,
                sensitivity=Sensitivity.CREDENTIAL,
                at_rest=AtRest.HASH,
                purpose="The API key assigned to the user",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the user is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the user",
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(("username",)),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None

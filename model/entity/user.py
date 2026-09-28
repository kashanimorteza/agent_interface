from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, ValueGeneration
from ..core.logical_type import LogicalType


class User(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The user's display name.",
            ),
            FieldDeclaration(
                name="username",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The username used to identify the user.",
            ),
            FieldDeclaration(
                name="password",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The password credential used by the user.",
            ),
            FieldDeclaration(
                name="api_key",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The API key assigned to the user.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the user is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the user.",
            ),
        ),
        primary_key="id",
        relations=(),
        unique_constraints=(
            ("name",),
            ("username",),
        ),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None

"""The Instance Entity."""

from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Instance(Entity, table=True):
    """The Instance Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns this instance.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the trading platform used by this instance.",
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The instance's display name.",
            ),
            FieldDeclaration(
                name="ip",
                type=FieldType.STRING,
                nullable=True,
                description="Identifies the technical network address used to reach the Trading Platform when required.",
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.STRING,
                nullable=True,
                description="Defines the technical username used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.STRING,
                nullable=True,
                description="Defines the technical password used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.STRING,
                nullable=True,
                description="Defines the technical API credential used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the instance is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the instance.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
            Relation(
                local_field="trading_platform_id",
                target_entity="Trading Platform",
                target_field="id",
            ),
        ),
        unique_constraints=(UniqueConstraint(fields=("user_id", "name")),),
    )

    __table_args__ = (TableUniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    trading_platform_id: int
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

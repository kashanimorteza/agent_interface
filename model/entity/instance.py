from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class Instance(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
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
                name="user_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the user who owns this instance.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the trading platform used by this instance.",
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The instance's display name.",
            ),
            FieldDeclaration(
                name="ip",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the technical network address used to reach the Trading Platform when required.",
            ),
            FieldDeclaration(
                name="username",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the technical username used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="password",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the technical password used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="api_key",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the technical API credential used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the instance is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
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
        unique_constraints=(("user_id", "name"),),
        indexes=(),
    )

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

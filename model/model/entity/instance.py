"""Instance Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Instance",
    description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns this instance.",
        ),
        FieldDeclaration(
            name="trading_platform_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the trading platform used by this instance.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The instance's display name.",
        ),
        FieldDeclaration(
            name="ip",
            type=FieldType.string,
            nullable=True,
            description="Identifies the technical network address used to reach the Trading Platform when required.",
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.string,
            nullable=True,
            description="Defines the technical username used to establish the Instance connection when required.",
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.string,
            nullable=True,
            description="Defines the technical password used to establish the Instance connection when required.",
        ),
        FieldDeclaration(
            name="api_key",
            type=FieldType.string,
            nullable=True,
            description="Defines the technical API credential used to establish the Instance connection when required.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the instance is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
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
    unique_constraints=(UniquenessConstraint(fields=("user_id", "name")),),
)


class Instance(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    trading_platform_id: int = realize_field(DECLARATION, "trading_platform_id")
    name: str = realize_field(DECLARATION, "name")
    ip: str | None = realize_field(DECLARATION, "ip")
    username: str | None = realize_field(DECLARATION, "username")
    password: str | None = realize_field(DECLARATION, "password")
    api_key: str | None = realize_field(DECLARATION, "api_key")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")

"""The Instance Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Instance(Foundation, table=True):
    __tablename__ = "Instance"
    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "user_id",
                FieldType.integer,
                False,
                description="Identifies the user who owns this instance.",
            ),
            FieldDeclaration(
                "trading_platform_id",
                FieldType.integer,
                False,
                description="Identifies the trading platform used by this instance.",
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The instance's display name.",
            ),
            FieldDeclaration(
                "ip",
                FieldType.string,
                True,
                description="Identifies the technical network address used to reach the Trading Platform when required.",
            ),
            FieldDeclaration(
                "username",
                FieldType.string,
                True,
                description="Defines the technical username used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                "password",
                FieldType.string,
                True,
                description="Defines the technical password used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                "api_key",
                FieldType.string,
                True,
                description="Defines the technical API credential used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the instance is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the instance.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation("user_id", "User", "id"),
            Relation("trading_platform_id", "Trading Platform", "id"),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    user_id: int = realize_field(declaration, "user_id")
    trading_platform_id: int = realize_field(declaration, "trading_platform_id")
    name: str = realize_field(declaration, "name")
    ip: str | None = realize_field(declaration, "ip")
    username: str | None = realize_field(declaration, "username")
    password: str | None = realize_field(declaration, "password")
    api_key: str | None = realize_field(declaration, "api_key")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")

"""The Instance Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Instance",
    description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "user_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the user who owns this instance.",
        ),
        FieldDeclaration(
            "trading_platform_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the trading platform used by this instance.",
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The instance's display name.",
        ),
        FieldDeclaration(
            "ip",
            FieldType.string,
            nullable=True,
            description="Identifies the technical network address used to reach the Trading Platform when required.",
        ),
        FieldDeclaration(
            "username",
            FieldType.string,
            nullable=True,
            description="Defines the technical username used to establish the Instance connection when required.",
        ),
        FieldDeclaration(
            "password",
            FieldType.string,
            nullable=True,
            description="Defines the technical password used to establish the Instance connection when required.",
            sensitivity=Sensitivity.password,
        ),
        FieldDeclaration(
            "api_key",
            FieldType.string,
            nullable=True,
            description="Defines the technical API credential used to establish the Instance connection when required.",
            sensitivity=Sensitivity.sensitive,
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the instance is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the instance.",
        ),
    ),
    relations=(
        Relation("user_id", "User", "id"),
        Relation("trading_platform_id", "Trading Platform", "id"),
    ),
    unique_constraints=(UniqueConstraint(("user_id", "name")),),
)


class Instance(Foundation, table=True):
    __tablename__ = "Instance"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

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

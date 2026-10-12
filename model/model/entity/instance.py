"""The Instance Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Instance(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description=(
            "Defines a user-owned connection instance through which the system accesses a "
            "supported Trading Platform."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
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
                description=(
                    "Identifies the technical network address used to reach the Trading "
                    "Platform when required."
                ),
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.STRING,
                nullable=True,
                description=(
                    "Defines the technical username used to establish the Instance connection "
                    "when required."
                ),
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.STRING,
                nullable=True,
                description=(
                    "Defines the technical password used to establish the Instance connection "
                    "when required."
                ),
                sensitivity=Sensitivity.PASSWORD,
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.STRING,
                nullable=True,
                description=(
                    "Defines the technical API credential used to establish the Instance "
                    "connection when required."
                ),
                sensitivity=Sensitivity.SENSITIVE,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the instance is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the instance.",
            ),
        ),
        relations=(
            Relation("user_id", "User", "id"),
            Relation("trading_platform_id", "Trading Platform", "id"),
        ),
        unique_constraints=(UniquenessConstraint(("user_id", "name")),),
    )

    __tablename__ = "Instance"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    user_id: int = mapped_field(declaration, "user_id")
    trading_platform_id: int = mapped_field(declaration, "trading_platform_id")
    name: str = mapped_field(declaration, "name")
    ip: str | None = mapped_field(declaration, "ip")
    username: str | None = mapped_field(declaration, "username")
    password: str | None = mapped_field(declaration, "password")
    api_key: str | None = mapped_field(declaration, "api_key")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")

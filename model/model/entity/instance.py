"""Instance Entity."""

from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Instance(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Instance",
        description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        primary_key="id",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.integer,
                nullable=False,
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
                sensitivity=Sensitivity.password,
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.string,
                nullable=True,
                description="Defines the technical API credential used to establish the Instance connection when required.",
                sensitivity=Sensitivity.sensitive,
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
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
            Relation(
                local_field="trading_platform_id",
                target_entity="Trading Platform",
                target_field="id",
            ),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __tablename__ = "Instance"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    user_id: int = storage.field(declaration, "user_id")
    trading_platform_id: int = storage.field(declaration, "trading_platform_id")
    name: str = storage.field(declaration, "name")
    ip: str | None = storage.field(declaration, "ip")
    username: str | None = storage.field(declaration, "username")
    password: str | None = storage.field(declaration, "password")
    api_key: str | None = storage.field(declaration, "api_key")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")

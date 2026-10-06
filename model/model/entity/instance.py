"""The Instance Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Instance",
    description=(
        "Defines a user-owned connection instance through which the system "
        "accesses a supported Trading Platform."
    ),
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
            description=(
                "Identifies the technical network address used to reach the Trading "
                "Platform when required."
            ),
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.string,
            nullable=True,
            description=(
                "Defines the technical username used to establish the Instance "
                "connection when required."
            ),
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.string,
            nullable=True,
            description=(
                "Defines the technical password used to establish the Instance "
                "connection when required."
            ),
        ),
        FieldDeclaration(
            name="api_key",
            type=FieldType.string,
            nullable=True,
            description=(
                "Defines the technical API credential used to establish the Instance "
                "connection when required."
            ),
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the instance is active.",
            has_default=True,
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
            local_field="trading_platform_id", target_entity="Trading Platform", target_field="id"
        ),
    ),
    unique_constraints=(UniqueConstraint(fields=("user_id", "name")),),
)


class Instance(Foundation, table=True):
    """Instance."""

    __tablename__ = "Instance"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    trading_platform_id: int = column(_DECLARATION, "trading_platform_id")
    name: str = column(_DECLARATION, "name")
    ip: str | None = column(_DECLARATION, "ip")
    username: str | None = column(_DECLARATION, "username")
    password: str | None = column(_DECLARATION, "password")
    api_key: str | None = column(_DECLARATION, "api_key")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")

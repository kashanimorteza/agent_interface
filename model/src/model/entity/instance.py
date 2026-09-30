"""The Instance Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Instance(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Instance",
        description=(
            "Defines a user-owned connection instance through "
            "which the system accesses a supported Trading "
            "Platform."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns this instance.",
            ),
            FieldDeclaration(
                "trading_platform_id",
                "integer",
                nullable=False,
                description=("Identifies the trading platform used by this instance."),
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The instance's display name.",
            ),
            FieldDeclaration(
                "ip",
                "string",
                nullable=True,
                description=(
                    "Identifies the technical network address used to "
                    "reach the Trading Platform when required."
                ),
            ),
            FieldDeclaration(
                "username",
                "string",
                nullable=True,
                description=(
                    "Defines the technical username used to establish the "
                    "Instance connection when required."
                ),
            ),
            FieldDeclaration(
                "password",
                "string",
                nullable=True,
                description=(
                    "Defines the technical password used to establish the "
                    "Instance connection when required."
                ),
                sensitivity="password",
            ),
            FieldDeclaration(
                "api_key",
                "string",
                nullable=True,
                description=(
                    "Defines the technical API credential used to "
                    "establish the Instance connection when required."
                ),
                sensitivity="sensitive",
            ),
            activity("Indicates whether the instance is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
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

    id: int | None = None
    user_id: int
    trading_platform_id: int
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

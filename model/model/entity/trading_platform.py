"""The Trading Platform Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration


class TradingPlatform(Entity, table=True):
    """The Trading Platform Entity."""

    __tablename__ = "TradingPlatform"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments()

    declaration = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="name",
                description="The platform's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="code",
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
                type="string",
                nullable=False,
            ),
            activity_declaration("Indicates whether the platform is active."),
            FieldDeclaration(
                name="description",
                description="Describes the platform.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        unique_constraints=(("name",),),
    )

    id: int | None = identity_field()
    name: str = Field(unique=True, description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`."
    )
    is_active: bool = activity_field("Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")

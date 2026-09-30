"""The Trading Platform Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration


class TradingPlatform(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Trading Platform",
        description=(
            "Defines a supported trading API standard, such as "
            "MetaTrader 5 or Binance, while keeping the system "
            "independent of any specific exchange or broker. "
            "Every trading platform implementation exposes the "
            "same application-facing trading functions through a "
            "dedicated class, while handling communication with "
            "its destination API according to that platform's own "
            "mechanism. Additional platform implementations can "
            "be added without changing the system's common "
            "trading interface."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The platform's display name.",
            ),
            FieldDeclaration(
                "code",
                "string",
                nullable=False,
                description=(
                    "Identifies the implementation class the application "
                    "must use for this trading platform, such as "
                    "`binance` or `metatrader_5`."
                ),
            ),
            activity("Indicates whether the platform is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the platform.",
            ),
        ),
        primary_key="id",
        unique_constraints=(("name",),),
    )

    id: int | None = None
    name: str
    code: str
    is_active: bool = True
    description: str | None = None

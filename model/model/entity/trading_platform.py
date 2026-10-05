from typing import ClassVar

from sqlalchemy import Identity
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration


class TradingPlatform(EntityBase, table=True):
    __table_args__ = ({"sqlite_autoincrement": True},)
    declaration: ClassVar[Declaration] = Declaration(
        "Trading Platform",
        "Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The platform's display name.", "string", False),
            FieldDeclaration(
                "code",
                "Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
                "string",
                False,
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the platform is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the platform.", "string", True),
        ),
        "id",
        unique_constraints=(("name",),),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(unique=True, description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`."
    )
    is_active: bool = Field(default=True, description="Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")

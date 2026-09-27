"""The Trading Platform Entity."""

from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
)
from my_model.model_foundation import Model_Foundation


class TradingPlatform(Model_Foundation, table=True):
    """A supported trading API standard, independent of any specific exchange or broker."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="TradingPlatform",
        purpose="A supported trading API standard, independent of any specific exchange or broker.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The platform's display name.",
            ),
            FieldDeclaration(
                name="code",
                type="string",
                nullable=False,
                purpose="Identifies the implementation class the application must use for this trading platform.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the platform is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the platform.",
            ),
        ),
        unique_constraints=(("name",),),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    code: str
    is_active: bool = True
    description: str | None = None

"""The Instance Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Instance(Model_Foundation, table=True):
    """A user-owned connection instance through which the system accesses a supported Trading Platform."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Instance",
        purpose="A user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="user_id",
                type="integer",
                nullable=False,
                purpose="Identifies the user who owns this instance.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type="integer",
                nullable=False,
                purpose="Identifies the trading platform used by this instance.",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The instance's display name.",
            ),
            FieldDeclaration(
                name="ip",
                type="string",
                nullable=True,
                purpose="The technical network address used to reach the Trading Platform when required.",
            ),
            FieldDeclaration(
                name="username",
                type="string",
                nullable=True,
                purpose="The technical username used to establish the Instance connection when required.",
            ),
            FieldDeclaration(
                name="password",
                type="string",
                nullable=True,
                purpose="The technical password used to establish the Instance connection when required.",
                sensitive=True,
            ),
            FieldDeclaration(
                name="api_key",
                type="string",
                nullable=True,
                purpose="The technical API credential used to establish the Instance connection when required.",
                sensitive=True,
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the instance is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the instance.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="user_id", entity="User"),
            ReferenceDeclaration(field="trading_platform_id", entity="TradingPlatform"),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    trading_platform_id: int = Field(foreign_key="tradingplatform.id")
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

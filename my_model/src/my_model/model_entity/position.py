"""The Position Entity."""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from sqlalchemy import DateTime
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Position(Model_Foundation, table=True):
    """The complete information for every position created by the system, whether opened or pending execution."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Position",
        purpose="The complete information for every position created by the system, whether opened or pending execution.",
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
                purpose="Identifies the user who owns the position.",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The position's display name.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type="integer",
                nullable=False,
                purpose="Identifies the trading platform used to execute the position.",
            ),
            FieldDeclaration(
                name="broker_id",
                type="integer",
                nullable=False,
                purpose="Identifies the broker through which the position is executed.",
            ),
            FieldDeclaration(
                name="account_id",
                type="integer",
                nullable=False,
                purpose="Identifies the trading account used for the position.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the Trailing Group applied to the position.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the Partial Group applied to the position.",
            ),
            FieldDeclaration(
                name="action_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the Action Group associated with the position.",
            ),
            FieldDeclaration(
                name="action_id",
                type="integer",
                nullable=False,
                purpose="Identifies the action from which the position is created.",
            ),
            FieldDeclaration(
                name="date",
                type="datetime",
                nullable=False,
                purpose="The position's date and time.",
            ),
            FieldDeclaration(
                name="volume",
                type="decimal",
                nullable=False,
                purpose="The position's trading volume.",
            ),
            FieldDeclaration(
                name="profit",
                type="decimal",
                nullable=False,
                purpose="The position's current profit or loss.",
                has_default=True,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="is_executed",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the position has been executed.",
                has_default=True,
                default=False,
            ),
            FieldDeclaration(
                name="order_type",
                type="string",
                nullable=False,
                purpose="The position's order type.",
            ),
            FieldDeclaration(
                name="base_tp",
                type="decimal",
                nullable=False,
                purpose="The position's initial Take Profit value.",
            ),
            FieldDeclaration(
                name="base_sl",
                type="decimal",
                nullable=False,
                purpose="The position's initial Stop Loss value.",
            ),
            FieldDeclaration(
                name="real_tp",
                type="decimal",
                nullable=False,
                purpose="The position's current Take Profit value.",
            ),
            FieldDeclaration(
                name="real_sl",
                type="decimal",
                nullable=False,
                purpose="The position's current Stop Loss value.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the position is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the position.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="user_id", entity="User"),
            ReferenceDeclaration(field="trading_platform_id", entity="TradingPlatform"),
            ReferenceDeclaration(field="broker_id", entity="Broker"),
            ReferenceDeclaration(field="account_id", entity="Account"),
            ReferenceDeclaration(field="trailing_group_id", entity="TrailingGroup"),
            ReferenceDeclaration(field="partial_group_id", entity="PartialGroup"),
            ReferenceDeclaration(field="action_group_id", entity="ActionGroup"),
            ReferenceDeclaration(field="action_id", entity="Action"),
        ),
        unique_constraints=(("name",),),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(unique=True)
    trading_platform_id: int = Field(foreign_key="tradingplatform.id")
    broker_id: int = Field(foreign_key="broker.id")
    account_id: int = Field(foreign_key="account.id")
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    action_group_id: int = Field(foreign_key="actiongroup.id")
    action_id: int = Field(foreign_key="action.id")
    date: datetime = Field(sa_type=DateTime(timezone=True))
    volume: Decimal
    profit: Decimal = Decimal(0)
    is_executed: bool = False
    order_type: str
    base_tp: Decimal
    base_sl: Decimal
    real_tp: Decimal
    real_sl: Decimal
    is_active: bool = True
    description: str | None = None

"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Action(Model_Foundation, table=True):
    """Defines how a position must be opened, selecting the asset and account and the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Action",
        purpose="Defines how a position must be opened, selecting the asset and account and the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings.",
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
                purpose="The action's display name.",
            ),
            FieldDeclaration(
                name="action_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the action group that contains the action.",
            ),
            FieldDeclaration(
                name="asset_id",
                type="integer",
                nullable=False,
                purpose="Identifies the asset traded by the action.",
            ),
            FieldDeclaration(
                name="account_id",
                type="integer",
                nullable=False,
                purpose="Identifies the account used to execute the action.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the Partial Group used by the action.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the Trailing Group used by the action.",
            ),
            FieldDeclaration(
                name="risk_by_reward",
                type="decimal",
                nullable=False,
                purpose="The numeric risk-to-reward value used by the action.",
            ),
            FieldDeclaration(
                name="take_profit",
                type="decimal",
                nullable=False,
                purpose="The Take Profit value used by the action.",
            ),
            FieldDeclaration(
                name="stop_loss",
                type="decimal",
                nullable=False,
                purpose="The Stop Loss value used by the action.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the action is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the action.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="action_group_id", entity="ActionGroup"),
            ReferenceDeclaration(field="asset_id", entity="Asset"),
            ReferenceDeclaration(field="account_id", entity="Account"),
            ReferenceDeclaration(field="partial_group_id", entity="PartialGroup"),
            ReferenceDeclaration(field="trailing_group_id", entity="TrailingGroup"),
        ),
        unique_constraints=(("action_group_id", "name"),),
    )
    __table_args__ = (UniqueConstraint("action_group_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str
    action_group_id: int = Field(foreign_key="actiongroup.id")
    asset_id: int = Field(foreign_key="asset.id")
    account_id: int = Field(foreign_key="account.id")
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    risk_by_reward: Decimal
    take_profit: Decimal
    stop_loss: Decimal
    is_active: bool = True
    description: str | None = None

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class Action(Foundation, table=True):
    """Defines how a position must be opened. An action selects the asset and account and
    provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group
    settings that determine the position's parameters and execution behavior.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Action",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("action_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("asset_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("account_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("partial_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("risk_by_reward", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("take_profit", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("stop_loss", FieldType.DECIMAL, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("action_group_id", "name")),),
        references=(
            Reference(("action_group_id",), "ActionGroup", ("id",)),
            Reference(("asset_id",), "Asset", ("id",)),
            Reference(("account_id",), "Account", ("id",)),
            Reference(("partial_group_id",), "PartialGroup", ("id",)),
            Reference(("trailing_group_id",), "TrailingGroup", ("id",)),
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the action, assigned automatically.",
    )
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(
        description="Identifies the action group that contains the action."
    )
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(
        description="Identifies the account used to execute the action."
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = Field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(
        description="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = Field(
        description="Defines the Stop Loss value used by the action."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the action is active."
    )
    description: str | None = Field(default=None, description="Describes the action.")

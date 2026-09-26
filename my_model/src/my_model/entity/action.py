"""Action Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Action(ModelFoundation, table=True):
    """Defines how a position must be opened."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Action",
        purpose="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The action's display name"
            ),
            FieldDeclaration(
                "action_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the action group that contains the action",
            ),
            FieldDeclaration(
                "asset_id",
                LogicalType.INTEGER,
                purpose="Identifies the asset traded by the action",
            ),
            FieldDeclaration(
                "account_id",
                LogicalType.INTEGER,
                purpose="Identifies the account used to execute the action",
            ),
            FieldDeclaration(
                "partial_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the Partial Group used by the action",
            ),
            FieldDeclaration(
                "trailing_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the Trailing Group used by the action",
            ),
            FieldDeclaration(
                "risk_by_reward",
                LogicalType.DECIMAL,
                purpose="Defines the numeric risk-to-reward value used by the action",
            ),
            FieldDeclaration(
                "take_profit",
                LogicalType.DECIMAL,
                purpose="Defines the Take Profit value used by the action",
            ),
            FieldDeclaration(
                "stop_loss",
                LogicalType.DECIMAL,
                purpose="Defines the Stop Loss value used by the action",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the action is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the action",
            ),
        ),
        references=(
            Reference(
                "action_group_id", "ActionGroup", "id", RelationshipKind.BELONGS_TO
            ),
            Reference("asset_id", "Asset", "id", RelationshipKind.USES),
            Reference("account_id", "Account", "id", RelationshipKind.USES),
            Reference("partial_group_id", "PartialGroup", "id", RelationshipKind.USES),
            Reference(
                "trailing_group_id", "TrailingGroup", "id", RelationshipKind.USES
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(
                (
                    "action_group_id",
                    "name",
                )
            ),
        ),
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

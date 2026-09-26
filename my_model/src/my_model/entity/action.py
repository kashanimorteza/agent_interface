"""Action Domain Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Action(ModelFoundation, table=True):
    """Defines how a position must be opened."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Action",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("action_group_id", LogicalType.INTEGER),
            FieldDeclaration("asset_id", LogicalType.INTEGER),
            FieldDeclaration("account_id", LogicalType.INTEGER),
            FieldDeclaration("partial_group_id", LogicalType.INTEGER),
            FieldDeclaration("trailing_group_id", LogicalType.INTEGER),
            FieldDeclaration("risk_by_reward", LogicalType.DECIMAL),
            FieldDeclaration("take_profit", LogicalType.DECIMAL),
            FieldDeclaration("stop_loss", LogicalType.DECIMAL),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(
            ReferenceDeclaration("action_group_id", "Action Group"),
            ReferenceDeclaration("asset_id", "Asset"),
            ReferenceDeclaration("account_id", "Account"),
            ReferenceDeclaration("partial_group_id", "Partial Group"),
            ReferenceDeclaration("trailing_group_id", "Trailing Group"),
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

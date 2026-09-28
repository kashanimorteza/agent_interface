"""Action Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Reference,
    Unique,
)
from model.foundation import Foundation


class Action(Foundation, table=True):
    """Description of how a position must be opened, with its asset, account, risk, and management groups."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="Action",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("action_group_id", FieldType.INTEGER),
            FieldDeclaration("asset_id", FieldType.INTEGER),
            FieldDeclaration("account_id", FieldType.INTEGER),
            FieldDeclaration("partial_group_id", FieldType.INTEGER),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER),
            FieldDeclaration("risk_by_reward", FieldType.DECIMAL),
            FieldDeclaration("take_profit", FieldType.DECIMAL),
            FieldDeclaration("stop_loss", FieldType.DECIMAL),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(
            Reference("action_group_id", "ActionGroup"),
            Reference("asset_id", "Asset"),
            Reference("account_id", "Account"),
            Reference("partial_group_id", "PartialGroup"),
            Reference("trailing_group_id", "TrailingGroup"),
        ),
        uniques=(Unique(("action_group_id", "name")),),
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

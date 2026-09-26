"""Account Domain Entity."""

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


class Account(ModelFoundation, table=True):
    """Defines a funded trading account through which the system executes trades and launches positions."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Account",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("group_id", LogicalType.INTEGER),
            FieldDeclaration("broker_id", LogicalType.INTEGER),
            FieldDeclaration("instance_id", LogicalType.INTEGER),
            FieldDeclaration("base_currency_id", LogicalType.INTEGER),
            FieldDeclaration("username", LogicalType.STRING),
            FieldDeclaration("password", LogicalType.STRING, sensitive=True),
            FieldDeclaration("leverage", LogicalType.INTEGER),
            FieldDeclaration("balance", LogicalType.DECIMAL, default=Decimal(0)),
            FieldDeclaration("account_type", LogicalType.STRING),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(
            ReferenceDeclaration("group_id", "Account Group"),
            ReferenceDeclaration("broker_id", "Broker"),
            ReferenceDeclaration("instance_id", "Instance"),
            ReferenceDeclaration("base_currency_id", "Currency"),
        ),
        unique_constraints=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
    )

    __table_args__ = (UniqueConstraint("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    group_id: int = Field(foreign_key="accountgroup.id")
    broker_id: int = Field(foreign_key="broker.id")
    instance_id: int = Field(foreign_key="instance.id")
    base_currency_id: int = Field(foreign_key="currency.id")
    username: str
    password: str
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None

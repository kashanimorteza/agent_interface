"""Entity: Account."""

from decimal import Decimal
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    Sensitivity,
    Unique,
    ValueGeneration,
)
from model.foundation import Foundation


class Account(Foundation, table=True):
    """Account Entity."""

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

    __table_args__ = (UniqueConstraint("group_id", "broker_id", "instance_id"),)

    declaration: ClassVar[Declaration] = Declaration(
        entity="Account",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("group_id", FieldType.INTEGER),
            FieldDeclaration("broker_id", FieldType.INTEGER),
            FieldDeclaration("instance_id", FieldType.INTEGER),
            FieldDeclaration("base_currency_id", FieldType.INTEGER),
            FieldDeclaration("username", FieldType.STRING),
            FieldDeclaration(
                "password", FieldType.STRING, sensitivity=Sensitivity.PASSWORD
            ),
            FieldDeclaration("leverage", FieldType.INTEGER),
            FieldDeclaration("balance", FieldType.DECIMAL, default=Decimal(0)),
            FieldDeclaration("account_type", FieldType.STRING),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(
            Reference("group_id", "AccountGroup"),
            Reference("broker_id", "Broker"),
            Reference("instance_id", "Instance"),
            Reference("base_currency_id", "Currency"),
        ),
        uniques=(
            Unique(("name",)),
            Unique(
                (
                    "group_id",
                    "broker_id",
                    "instance_id",
                )
            ),
        ),
    )

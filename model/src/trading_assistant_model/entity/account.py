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


class Account(Foundation, table=True):
    """Defines a funded trading account through which the system executes trades and
    launches positions. Each Account identifies the trading account and its
    account-level login credentials, while its selected Instance owns the separate
    technical connection to the Trading Platform.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Account",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("broker_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("instance_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("base_currency_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("username", FieldType.STRING, nullable=False),
            FieldDeclaration(
                "password", FieldType.STRING, nullable=False, sensitive=True
            ),
            FieldDeclaration("leverage", FieldType.INTEGER, nullable=False),
            FieldDeclaration(
                "balance", FieldType.DECIMAL, nullable=False, default=Decimal(0)
            ),
            FieldDeclaration("account_type", FieldType.STRING, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(
            UniqueConstraint(("name",)),
            UniqueConstraint(("group_id", "broker_id", "instance_id")),
        ),
        references=(
            Reference(("group_id",), "AccountGroup", ("id",)),
            Reference(("broker_id",), "Broker", ("id",)),
            Reference(("instance_id",), "Instance", ("id",)),
            Reference(("base_currency_id",), "Currency", ("id",)),
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the account, assigned automatically.",
    )
    name: str = Field(description="The account's display name.")
    group_id: int = Field(
        description="Identifies the account group that contains the account."
    )
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(
        description="Identifies the base currency used by the account."
    )
    username: str = Field(
        description="The username identifier used to access the trading account."
    )
    password: str = Field(
        description="The credential used to access the trading account."
    )
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = Field(
        description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = Field(default=None, description="Describes the account.")

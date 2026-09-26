"""Account Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    AtRest,
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Account(ModelFoundation, table=True):
    """Defines a funded trading account through which the system executes trades and launches positions."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Account",
        purpose="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The account's display name"
            ),
            FieldDeclaration(
                "group_id",
                LogicalType.INTEGER,
                purpose="Identifies the account group that contains the account",
            ),
            FieldDeclaration(
                "broker_id",
                LogicalType.INTEGER,
                purpose="Identifies the broker that owns the account",
            ),
            FieldDeclaration(
                "instance_id",
                LogicalType.INTEGER,
                purpose="Identifies the trading-platform instance used to connect this account",
            ),
            FieldDeclaration(
                "base_currency_id",
                LogicalType.INTEGER,
                purpose="Identifies the base currency used by the account",
            ),
            FieldDeclaration(
                "username",
                LogicalType.STRING,
                purpose="The username identifier used to access the trading account",
            ),
            FieldDeclaration(
                "password",
                LogicalType.STRING,
                sensitivity=Sensitivity.CREDENTIAL,
                at_rest=AtRest.ENCRYPTED,
                purpose="The credential used to access the trading account",
            ),
            FieldDeclaration(
                "leverage",
                LogicalType.INTEGER,
                purpose="Defines the account's leverage multiplier",
            ),
            FieldDeclaration(
                "balance",
                LogicalType.DECIMAL,
                has_default=True,
                default=Decimal(0),
                purpose="Stores the account's current balance",
            ),
            FieldDeclaration(
                "account_type",
                LogicalType.STRING,
                purpose="Identifies the account model, such as `cfd` or `spread_betting`",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the account is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the account",
            ),
        ),
        references=(
            Reference("group_id", "AccountGroup", "id", RelationshipKind.BELONGS_TO),
            Reference("broker_id", "Broker", "id", RelationshipKind.BELONGS_TO),
            Reference("instance_id", "Instance", "id", RelationshipKind.USES),
            Reference("base_currency_id", "Currency", "id", RelationshipKind.USES),
        ),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(
                (
                    "group_id",
                    "broker_id",
                    "instance_id",
                )
            ),
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

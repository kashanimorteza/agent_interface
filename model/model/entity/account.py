"""The Account Entity."""

from decimal import Decimal

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import DecimalText, table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Account(Entity, table=True):
    """The Account Entity."""

    __tablename__ = "Account"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("group_id", "broker_id", "instance_id"),
    )

    declaration = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="name",
                description="The account's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="group_id",
                description="Identifies the account group that contains the account.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="broker_id",
                description="Identifies the broker that owns the account.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="instance_id",
                description="Identifies the trading-platform instance used to connect this account.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="base_currency_id",
                description="Identifies the base currency used by the account.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="username",
                description="The username identifier used to access the trading account.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="password",
                description="The credential used to access the trading account.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="leverage",
                description="Defines the account's leverage multiplier.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="balance",
                description="Stores the account's current balance.",
                type="decimal",
                nullable=False,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="account_type",
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
                type="string",
                nullable=False,
            ),
            activity_declaration("Indicates whether the account is active."),
            FieldDeclaration(
                name="description",
                description="Describes the account.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="group_id", target_entity="Account Group", target_field="id"
            ),
            RelationDeclaration(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
            RelationDeclaration(
                local_field="instance_id", target_entity="Instance", target_field="id"
            ),
            RelationDeclaration(
                local_field="base_currency_id",
                target_entity="Currency",
                target_field="id",
            ),
        ),
        unique_constraints=(("name",), ("group_id", "broker_id", "instance_id")),
    )

    id: int | None = identity_field()
    name: str = Field(unique=True, description="The account's display name.")
    group_id: int = Field(
        foreign_key="AccountGroup.id",
        description="Identifies the account group that contains the account.",
    )
    broker_id: int = Field(
        foreign_key="Broker.id",
        description="Identifies the broker that owns the account.",
    )
    instance_id: int = Field(
        foreign_key="Instance.id",
        description="Identifies the trading-platform instance used to connect this account.",
    )
    base_currency_id: int = Field(
        foreign_key="Currency.id",
        description="Identifies the base currency used by the account.",
    )
    username: str = Field(
        description="The username identifier used to access the trading account."
    )
    password: str = Field(
        description="The credential used to access the trading account."
    )
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal(0),
        sa_type=DecimalText,
        description="Stores the account's current balance.",
    )
    account_type: str = Field(
        description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    is_active: bool = activity_field("Indicates whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")

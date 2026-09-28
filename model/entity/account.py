from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class Account(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The account's display name.",
            ),
            FieldDeclaration(
                name="group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the account group that contains the account.",
            ),
            FieldDeclaration(
                name="broker_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                name="instance_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the trading-platform instance used to connect this account.",
            ),
            FieldDeclaration(
                name="base_currency_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                name="username",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The username identifier used to access the trading account.",
            ),
            FieldDeclaration(
                name="password",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The credential used to access the trading account.",
            ),
            FieldDeclaration(
                name="leverage",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the account's leverage multiplier.",
            ),
            FieldDeclaration(
                name="balance",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=True,
                default=Decimal(0),
                immutable=False,
                description="Stores the account's current balance.",
            ),
            FieldDeclaration(
                name="account_type",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the account is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the account.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(local_field="group_id", target_entity="Account Group", target_field="id"),
            Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
            Relation(local_field="instance_id", target_entity="Instance", target_field="id"),
            Relation(local_field="base_currency_id", target_entity="Currency", target_field="id"),
        ),
        unique_constraints=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: str
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None

"""Account Domain Entity: a funded trading account."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.account_group import AccountGroup
    from my_model.model_entity.broker import Broker
    from my_model.model_entity.currency import Currency
    from my_model.model_entity.instance import Instance


class Account(Model_Declaration, Model_Foundation, table=True):
    """A funded trading account through which the system executes trades and launches positions."""

    __tablename__ = "account"
    __table_args__ = (UniqueConstraint("group_id", "broker_id", "instance_id"),)

    name: str = Field(nullable=False, unique=True)
    group_id: int = Field(foreign_key="account_group.id", nullable=False)
    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    instance_id: int = Field(foreign_key="instance.id", nullable=False)
    base_currency_id: int = Field(foreign_key="currency.id", nullable=False)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False, schema_extra={"sensitivity_marker": "password"})
    leverage: int = Field(nullable=False)
    balance: Decimal = Field(default=Decimal("0"), nullable=False)
    account_type: str = Field(nullable=False)

    account_group: "AccountGroup" = Relationship()
    broker: "Broker" = Relationship()
    instance: "Instance" = Relationship()
    base_currency: "Currency" = Relationship()

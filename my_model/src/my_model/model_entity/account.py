"""Account: a funded trading account through which the system executes trades and launches positions."""

from decimal import Decimal

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Account(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    group_id: int = Field(foreign_key="account_group.id", nullable=False)
    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    instance_id: int = Field(foreign_key="instance.id", nullable=False)
    base_currency_id: int = Field(foreign_key="currency.id", nullable=False)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False, schema_extra={"sensitivity": "password"})
    leverage: int = Field(nullable=False)
    balance: Decimal = Field(default=Decimal("0"), nullable=False)
    account_type: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)

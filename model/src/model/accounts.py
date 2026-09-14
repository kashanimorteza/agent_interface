from decimal import Decimal

from pydantic import SecretStr

from .foundation import CredentialStorage, ModelBase, credential_field


class AccountGroup(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None


class Account(ModelBase):
    unique_together = (("name",), ("group_id", "broker_id", "instance_id"))

    id: int | None = None
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: SecretStr = credential_field(storage=CredentialStorage.ENCRYPTED)
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None

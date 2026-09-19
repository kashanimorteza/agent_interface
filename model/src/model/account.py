"""Account: a funded trading account through which the system executes trades."""

from decimal import Decimal
from typing import Annotated

from .account_group import AccountGroup
from .broker import Broker
from .currency import Currency
from .foundation import EncryptedCredential, ExactDecimal, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text, Unique
from .instance import Instance


class Account(ModelFoundation):
    persistence = "persistent"
    relationships = (
        Relationship(field="group_id", reference=AccountGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="broker_id", reference=Broker, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="instance_id", reference=Instance, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="base_currency_id", reference=Currency, reference_field="id", cardinality="many-to-one", optional=False),
    )
    unique_sets = (("group_id", "broker_id", "instance_id"),)

    id: GeneratedId = None
    name: Annotated[Text, Unique()]
    group_id: Integer
    broker_id: Integer
    instance_id: Integer
    base_currency_id: Integer
    username: Text
    password: EncryptedCredential
    leverage: Integer
    balance: ExactDecimal = Decimal(0)
    account_type: Text
    is_active: Flag = True
    description: Text | None = None

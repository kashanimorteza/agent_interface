"""The Account Domain Definition.

A funded trading account through which the system executes trades and launches positions.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly. Monetary and rate values are exact decimals.
"""

from decimal import Decimal
from typing import Annotated

from model.account_group import AccountGroup
from model.broker import Broker
from model.currency import Currency
from model.declaration import (
    Activation,
    AtRest,
    Cardinality,
    Credential,
    Generated,
    Identity,
    Persistence,
    Relationship,
    Unique,
)
from model.foundation import ExactDecimal, ModelFoundation
from model.instance import Instance


class Account(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="group",
            via="group_id",
            reference=AccountGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="broker",
            via="broker_id",
            reference=Broker,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="instance",
            via="instance_id",
            reference=Instance,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="base_currency",
            via="base_currency_id",
            reference=Currency,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("group_id", "broker_id", "instance_id"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    name: Annotated[str, Unique()]
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: Annotated[str, Credential(AtRest.ENCRYPTED)]
    leverage: int
    balance: ExactDecimal = Decimal("0")
    account_type: str
    is_active: Annotated[bool, Activation()] = True
    description: str | None

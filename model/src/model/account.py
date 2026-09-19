"""Account Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* `balance` is an exact decimal value with no declared precision, because the Target states type `decimal` and no precision.
"""

from decimal import Decimal
from typing import Annotated

from model.account_group import AccountGroup
from model.broker import Broker
from model.currency import Currency
from model.foundation import (
    ActiveFlag,
    ExactDecimal,
    GeneratedIdentity,
    ModelFoundation,
)
from model.instance import Instance
from model.vocabulary import (
    AtRestTreatment,
    Cardinality,
    Credential,
    Persistence,
    Reference,
    Unique,
)


class Account(ModelFoundation):
    """A funded trading account through which the system executes trades and launches positions.

    The Target rule that the same credential must not be duplicated across an Instance and an Account
    depends on data outside the Account, so this definition does not evaluate it."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("group_id", "broker_id", "instance_id"),)

    id: GeneratedIdentity = None
    name: Annotated[str, Unique()]
    group_id: Annotated[
        int,
        Reference(
            definition=AccountGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    broker_id: Annotated[
        int,
        Reference(
            definition=Broker, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    instance_id: Annotated[
        int,
        Reference(
            definition=Instance, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    base_currency_id: Annotated[
        int,
        Reference(
            definition=Currency, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    username: str
    password: Annotated[str, Credential(treatment=AtRestTreatment.ENCRYPTED)]
    leverage: int
    balance: ExactDecimal = Decimal(0)
    account_type: str
    is_active: ActiveFlag = True
    description: str | None = None

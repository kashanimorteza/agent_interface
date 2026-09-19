from decimal import Decimal
from typing import Annotated, ClassVar

from model.foundation import (
    CredentialText,
    Declare,
    DomainDefinition,
    GeneratedId,
    Reference,
)


class Account(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("group_id", "broker_id", "instance_id"),
    )

    id: GeneratedId = None
    name: Annotated[str, Declare("string", unique=True)]
    group_id: Annotated[int, Declare("integer", references=Reference("AccountGroup"))]
    broker_id: Annotated[int, Declare("integer", references=Reference("Broker"))]
    instance_id: Annotated[int, Declare("integer", references=Reference("Instance"))]
    base_currency_id: Annotated[
        int, Declare("integer", references=Reference("Currency"))
    ]
    username: Annotated[str, Declare("string")]
    password: Annotated[CredentialText, Declare("string", credential="encrypted")]
    leverage: Annotated[int, Declare("integer")]
    balance: Annotated[Decimal, Declare("decimal")] = Decimal(0)
    account_type: Annotated[str, Declare("string")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

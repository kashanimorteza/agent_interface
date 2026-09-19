from decimal import Decimal
from typing import Annotated, ClassVar

from pydantic import AwareDatetime

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class Position(DomainDefinition):
    persistent: ClassVar[bool] = True

    id: GeneratedId = None
    user_id: Annotated[int, Declare("integer", references=Reference("User"))]
    name: Annotated[str, Declare("string", unique=True)]
    trading_platform_id: Annotated[
        int, Declare("integer", references=Reference("TradingPlatform"))
    ]
    broker_id: Annotated[int, Declare("integer", references=Reference("Broker"))]
    account_id: Annotated[int, Declare("integer", references=Reference("Account"))]
    trailing_group_id: Annotated[
        int, Declare("integer", references=Reference("TrailingGroup"))
    ]
    partial_group_id: Annotated[
        int, Declare("integer", references=Reference("PartialGroup"))
    ]
    action_group_id: Annotated[
        int, Declare("integer", references=Reference("ActionGroup"))
    ]
    action_id: Annotated[int, Declare("integer", references=Reference("Action"))]
    date: Annotated[AwareDatetime, Declare("datetime")]
    volume: Annotated[Decimal, Declare("decimal")]
    profit: Annotated[Decimal, Declare("decimal")] = Decimal(0)
    is_executed: Annotated[bool, Declare("boolean")] = False
    order_type: Annotated[str, Declare("string")]
    base_tp: Annotated[Decimal, Declare("decimal")]
    base_sl: Annotated[Decimal, Declare("decimal")]
    real_tp: Annotated[Decimal, Declare("decimal")]
    real_sl: Annotated[Decimal, Declare("decimal")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

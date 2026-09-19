from decimal import Decimal
from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class Action(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("action_group_id", "name"),)

    id: GeneratedId = None
    name: Annotated[str, Declare("string")]
    action_group_id: Annotated[
        int, Declare("integer", references=Reference("ActionGroup"))
    ]
    asset_id: Annotated[int, Declare("integer", references=Reference("Asset"))]
    account_id: Annotated[int, Declare("integer", references=Reference("Account"))]
    partial_group_id: Annotated[
        int, Declare("integer", references=Reference("PartialGroup"))
    ]
    trailing_group_id: Annotated[
        int, Declare("integer", references=Reference("TrailingGroup"))
    ]
    risk_by_reward: Annotated[Decimal, Declare("decimal")]
    take_profit: Annotated[Decimal, Declare("decimal")]
    stop_loss: Annotated[Decimal, Declare("decimal")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

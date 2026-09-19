from decimal import Decimal
from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class TrailingRule(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("trailing_group_id", "trigger_percentage"),
    )

    id: GeneratedId = None
    name: Annotated[str, Declare("string", unique=True)]
    trailing_group_id: Annotated[
        int, Declare("integer", references=Reference("TrailingGroup"))
    ]
    trigger_percentage: Annotated[Decimal, Declare("decimal")]
    take_profit_adjustment: Annotated[Decimal | None, Declare("decimal")] = None
    stop_loss_adjustment: Annotated[Decimal | None, Declare("decimal")] = None
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None
